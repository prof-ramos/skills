#!/usr/bin/env python3
"""
subfinder.py — Enumeração de subdomínios via ProjectDiscovery subfinder.

Realiza descoberta de subdomínios usando subfinder da ProjectDiscovery,
com validações éticas para bloqueio de TLDs governamentais e
requerimento de autorização explícita.

Requisitos: subfinder instalado (go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest)
Uso: python scripts/subfinder.py --target example.com --output subfinder_output/

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Importação condicional de utils (mesmo diretório)
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    configurar_logger, exibir_disclaimer_e_validar,
    validar_alvo, salvar_json, detectar_ambiente
)

# TLDs governamentais sensíveis (bloqueio ético)
RESTRICTED_TLDS = {
    ".gov", ".mil", ".gov.br", ".jus.br", ".leg.br",
    ".mp.br", ".gc.ca", ".gov.uk", ".gob.mx", ".gob.ar",
    ".gov.au", ".gov.in", ".gov.my", ".gov.sg", ".gov.il"
}


class SubfinderEnum:
    """
    Wrapper para subfinder com validações éticas e logging.

    Encapsula a execução do subfinder garantindo que:
    - O disclaimer seja exibido antes da execução
    - TLDs governamentais sejam bloqueados
    - Os resultados sejam salvos em JSON para auditoria
    """

    TIMEOUT_SECONDS = 300  # 5 minutos máximo

    def __init__(self, alvo: str, output_dir: str):
        """
        Inicializa o enumerador de subdomínios.

        Parâmetros:
            alvo: Domínio alvo para enumeração.
            output_dir: Diretório para salvar os resultados.

        Raises:
            ValueError: Se o alvo for inválido ou contiver TLD restrito.
        """
        self.alvo = alvo
        self.output_dir = output_dir
        self.logger, self.log_file = configurar_logger("subfinder")

        # Validação ética do TLD
        if self._is_restricted_tld(alvo):
            raise ValueError(
                f"Domínio {alvo} contém TLD governamental restrito. "
                "Apenas escopos autorizados com documentação formal podem ser testados."
            )

        # Validação básica
        validacao = validar_alvo(alvo)
        if not validacao["valido"]:
            raise ValueError(f"Alvo inválido para subfinder: {alvo}")

        if validacao["tipo"] != "dominio":
            raise ValueError(
                f"Subfinder requer um domínio válido. Tipo recebido: {validacao['tipo']}"
            )

        self.logger.info(f"SubfinderEnum inicializado | alvo={alvo} | output={output_dir}")

    def _is_restricted_tld(self, dominio: str) -> bool:
        """
        Verifica se o domínio possui TLD governamental restrito.

        Parâmetros:
            dominio: Domínio a ser verificado.

        Returns:
            bool: True se o TLD for restrito, False caso contrário.
        """
        dominio_lower = dominio.lower().strip()
        return any(dominio_lower.endswith(tld) for tld in RESTRICTED_TLDS)

    def _check_subfinder_installed(self) -> bool:
        """
        Verifica se subfinder está instalado e acessível.

        Returns:
            bool: True se subfinder estiver instalado, False caso contrário.
        """
        try:
            result = subprocess.run(
                ["subfinder", "-version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip().decode("utf-8", errors="ignore")
                self.logger.info(f"subfinder detectado: {version}")
                return True
        except FileNotFoundError:
            self.logger.warning("subfinder não encontrado no PATH")
        except subprocess.TimeoutExpired:
            self.logger.warning("timeout ao verificar subfinder")
        except Exception as e:
            self.logger.warning(f"erro ao verificar subfinder: {e}")
        return False

    def enumerate(self, sources: str = "all") -> List[str]:
        """
        Executa subfinder e retorna lista de subdomínios.

        Parâmetros:
            sources: Fontes a usar (all, rapid, ou lista específica).

        Returns:
            Lista de subdomínios únicos encontrados.

        Raises:
            RuntimeError: Se subfinder não estiver instalado ou falhar.
        """
        if not self._check_subfinder_installed():
            raise RuntimeError(
                "subfinder não encontrado. Instale com: "
                "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
            )

        output_file = Path(self.output_dir) / f"{self.alvo}_subfinder_raw.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Comando subfinder com flags seguras
        cmd = [
            "subfinder",
            "-d", self.alvo,
            "-silent",           # Sem banners/output extra
            "-json",             # Saída JSON para parsing fácil
            "-o", str(output_file)
        ]

        # Opcional: especificar fontes
        if sources and sources != "all":
            cmd.extend(["-sources", sources])

        self.logger.info(f"Executando: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.TIMEOUT_SECONDS
            )

            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8", errors="ignore")
                self.logger.error(f"subfinder falhou (rc={result.returncode}): {error_msg}")
                raise RuntimeError(f"subfinder error: {error_msg}")

        except subprocess.TimeoutExpired:
            self.logger.error(f"subfinder timeout após {self.TIMEOUT_SECONDS}s")
            raise RuntimeError(f"subfinder timeout após {self.TIMEOUT_SECONDS} segundos")

        # Parse do output JSON
        subdomains = set()
        try:
            with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if "host" in data:
                            host = data["host"].strip().lower()
                            if host:
                                subdomains.add(host)
                    except json.JSONDecodeError:
                        # Se não for JSON, trata como linha simples (fallback)
                        if line and not line.startswith("{"):
                            line_clean = line.strip().lower()
                            if line_clean and line_clean != self.alvo:
                                subdomains.add(line_clean)

        except FileNotFoundError:
            self.logger.warning(f"arquivo de output não encontrado: {output_file}")
        except Exception as e:
            self.logger.warning(f"erro ao parsear output: {e}")

        # Limpar arquivo temporário
        try:
            output_file.unlink(missing_ok=True)
        except Exception:
            pass

        resultado = sorted(list(subdomains))
        self.logger.info(f"subfinder encontrou {len(resultado)} subdomínios únicos")
        return resultado

    def execute(self, sources: str = "all") -> Dict:
        """
        Executa enumeração completa e retorna dict com resultados.

        Parâmetros:
            sources: Fontes do subfinder (all, rapid, etc).

        Returns:
            Dicionário com resultados da enumeração.
        """
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        console.print(Panel(
            f"[bold green]🔍 Enumeração de Subdomínios (subfinder)[/bold green]\n"
            f"Alvo: [cyan]{self.alvo}[/cyan]",
            border_style="green"
        ))

        # Capturar timestamp antes da enumeração
        timestamp_inicio = datetime.now().isoformat()

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            t = p.add_task("Enumerando subdomínios com subfinder...")
            subdomains = self.enumerate(sources)
            p.remove_task(t)

        resultado = {
            "alvo": self.alvo,
            "ferramenta": "subfinder",
            "versao": "ProjectDiscovery subfinder v2",
            "timestamp_inicio": timestamp_inicio,
            "timestamp_fim": datetime.now().isoformat(),
            "total_encontrado": len(subdomains),
            "subdomains": subdomains,
            "fontes": sources,
            "log_file": self.log_file,
            "ambiente": detectar_ambiente(),
            "metadata": {
                "tld_restrito_verificado": self._is_restricted_tld(self.alvo),
                "timeout_segundos": self.TIMEOUT_SECONDS
            }
        }

        # Salvar JSON
        caminho = salvar_json(resultado, f"{self.alvo.replace('.', '_')}_subfinder", self.output_dir)

        # Exibir resumo
        tabela = Table(title="📊 Subdomain Enumeration (subfinder)", border_style="cyan")
        tabela.add_column("Métrica", style="bold")
        tabela.add_column("Valor", style="green")
        tabela.add_row("Alvo", self.alvo)
        tabela.add_row("Ferramenta", "subfinder (ProjectDiscovery)")
        tabela.add_row("Fontes", sources)
        tabela.add_row("Subdomínios encontrados", str(len(subdomains)))
        tabela.add_row("Log de auditoria", self.log_file)
        tabela.add_row("Output JSON", caminho)
        console.print(tabela)

        # Exibir amostra de subdomínios (primeiros 10)
        if subdomains:
            from rich.columns import Columns
            from rich.text import Text
            amostra = subdomains[:10]
            cols = Columns([Text(s, style="cyan") for s in amostra], equal=True, expand=True)
            console.print(Panel(cols, title=f"Amostra (mostrando {len(amostra)} de {len(subdomains)})"))

        console.print(f"[bold green]✅ Resultados salvos em: {caminho}[/bold green]")
        return resultado


def main():
    """Ponto de entrada principal do módulo subfinder."""
    parser = argparse.ArgumentParser(
        description="Enumeração de Subdomínios via subfinder — Ethical Red Team Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python subfinder.py --target example.com --output subfinder_output/
  python subfinder.py --target scanme.nmap.org --output results/ --sources rapid

Requisitos:
  - subfinder instalado: go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
  - Autorização escrita do proprietário do domínio
  - TOR ativo (recomendado para anonimato)

Fontes disponíveis:
  all     - Todas as fontes (padrão)
  rapid   - Apenas fontes rápidas
  Para mais fontes: subfinder -list-sources

⚠️  AVISO: O uso não autorizado desta ferramenta é ilegal.
        """
    )
    parser.add_argument("--target", required=True,
                        help="Domínio alvo (ex: example.com)")
    parser.add_argument("--output", default="subfinder_output",
                        help="Diretório de saída (padrão: subfinder_output)")
    parser.add_argument("--sources", default="all",
                        help="Fontes do subfinder (all, rapid, ou lista específica)")
    parser.add_argument("--skip-disclaimer", action="store_true",
                        help="Pular disclaimer (apenas para CI/CD autorizado)")

    args = parser.parse_args()

    # Logger temporário para validação
    logger, _ = configurar_logger("subfinder_auth")

    # Validação de autorização
    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    try:
        enum = SubfinderEnum(args.target, args.output)
        resultado = enum.execute(sources=args.sources)
        sys.exit(0)
    except ValueError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[bold yellow]⚠️  Operação cancelada pelo usuário[/bold yellow]")
        sys.exit(130)
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
