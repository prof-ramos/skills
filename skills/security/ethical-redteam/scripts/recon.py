#!/usr/bin/env python3
"""
recon.py — Módulo de Reconhecimento (OSINT / DNS / IP Enumeration).

Realiza coleta de informações passiva e ativa sobre o alvo, incluindo
enumeração de subdomínios, consultas DNS, registros WHOIS, geolocalização
de IP e busca em fontes OSINT públicas.

Requisitos: Python 3.11+, dnspython, ipwhois, requests, rich
Uso: python scripts/recon.py --target alvo.com --mode passive --output ./saida/

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import dns.resolver
    import requests
    from ipwhois import IPWhois
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"[ERRO] Dependência ausente: {e}. Execute: pip install -r requirements.txt")
    sys.exit(1)

# Importação condicional de utils (mesmo diretório)
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    configurar_logger, exibir_disclaimer_e_validar,
    validar_alvo, salvar_json, detectar_ambiente
)

# Importação condicional de SubfinderEnum (subfinder module)
# Reuse a lógica centralizada de validação e enumeração
try:
    from subfinder import SubfinderEnum, RESTRICTED_TLDS
    SUBFINDER_AVAILABLE = True
except ImportError:
    SUBFINDER_AVAILABLE = False
    RESTRICTED_TLDS = set()

console = Console()


class ModuloReconhecimento:
    """
    Módulo de reconhecimento passivo e ativo para testes de segurança.

    Encapsula todas as técnicas de coleta de informações, garantindo
    que o disclaimer e a validação de autorização sejam exibidos antes
    de qualquer operação.
    """

    TIMEOUT_DNS = 10
    TIMEOUT_HTTP = 15
    TIPOS_DNS = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]

    def __init__(self, alvo: str, modo: str, diretorio_saida: str):
        """
        Inicializa o módulo de reconhecimento.

        Parâmetros:
            alvo: IP, domínio ou URL do alvo autorizado.
            modo: Modo de operação ('passive', 'active' ou 'full').
            diretorio_saida: Diretório para salvar os resultados.
        """
        self.alvo = alvo
        self.modo = modo
        self.diretorio_saida = diretorio_saida
        self.timestamp_inicio = datetime.now(timezone.utc).isoformat()
        self.logger, self.log_file = configurar_logger("recon")
        self.resultados: dict = {
            "alvo": alvo,
            "modo": modo,
            "timestamp_inicio": self.timestamp_inicio,
            "ambiente": detectar_ambiente(),
            "dns": {},
            "whois": {},
            "subdomains": [],
            "ips_encontrados": [],
            "osint": {},
            "metadata": {}
        }

        validacao = validar_alvo(alvo)
        if not validacao["valido"]:
            self.logger.error(f"Alvo inválido: {alvo}")
            console.print(f"[bold red]❌ Alvo inválido: {alvo}[/bold red]")
            sys.exit(1)

        self.tipo_alvo = validacao["tipo"]
        self.logger.info(f"Módulo de reconhecimento iniciado | alvo={alvo} | modo={modo}")

    def consultar_dns(self) -> dict:
        """
        Realiza consultas DNS para múltiplos tipos de registro.

        Consulta registros A, AAAA, MX, NS, TXT, SOA e CNAME
        para o domínio alvo e registra os resultados.

        Retorna:
            dict: Dicionário com registros DNS organizados por tipo.
        """
        registros = {}
        console.print("[bold cyan]→ Consultando registros DNS...[/bold cyan]")

        for tipo in self.TIPOS_DNS:
            try:
                respostas = dns.resolver.resolve(self.alvo, tipo, lifetime=self.TIMEOUT_DNS)
                registros[tipo] = [str(r) for r in respostas]
                self.logger.info(f"DNS {tipo}: {registros[tipo]}")
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                    dns.resolver.NoNameservers, dns.exception.Timeout):
                registros[tipo] = []
            except Exception as e:
                registros[tipo] = []
                self.logger.warning(f"DNS {tipo} erro: {e}")

        return registros

    def resolver_ip(self) -> list:
        """
        Resolve o domínio alvo para seus endereços IP.

        Retorna:
            list: Lista de endereços IP associados ao domínio.
        """
        ips = []
        try:
            infos = socket.getaddrinfo(self.alvo, None)
            ips = list({info[4][0] for info in infos})
            self.logger.info(f"IPs resolvidos: {ips}")
        except socket.gaierror as e:
            self.logger.warning(f"Falha ao resolver IPs: {e}")
        return ips

    def consultar_whois_ip(self, ip: str) -> dict:
        """
        Consulta informações WHOIS de um endereço IP.

        Parâmetros:
            ip: Endereço IP a ser consultado.

        Retorna:
            dict: Informações de registro, ASN e geolocalização do IP.
        """
        try:
            obj = IPWhois(ip)
            resultado = obj.lookup_rdap(depth=1)
            return {
                "asn": resultado.get("asn"),
                "asn_description": resultado.get("asn_description"),
                "country": resultado.get("asn_country_code"),
                "network_name": resultado.get("network", {}).get("name"),
                "cidr": resultado.get("network", {}).get("cidr"),
            }
        except Exception as e:
            self.logger.warning(f"WHOIS falhou para {ip}: {e}")
            return {}

    def enumerar_subdomains_passivo(self) -> list:
        """
        Enumera subdomínios usando fontes OSINT passivas (sem contato direto).

        Consulta APIs públicas como crt.sh (Certificate Transparency Logs)
        para descobrir subdomínios registrados.

        Retorna:
            list: Lista de subdomínios encontrados.
        """
        subdomains = set()
        console.print("[bold cyan]→ Enumerando subdomínios (OSINT passivo)...[/bold cyan]")

        # Fonte 1: crt.sh (Certificate Transparency)
        try:
            url = f"https://crt.sh/?q=%.{self.alvo}&output=json"
            resp = requests.get(url, timeout=self.TIMEOUT_HTTP, headers={
                "User-Agent": "EthicalRedTeamSkill/1.0 (Authorized Security Testing)"
            })
            if resp.status_code == 200:
                dados = resp.json()
                for entrada in dados:
                    nome = entrada.get("name_value", "")
                    for sub in nome.split("\n"):
                        sub = sub.strip().lower().replace("*.", "")
                        if sub.endswith(self.alvo) and sub != self.alvo:
                            subdomains.add(sub)
                self.logger.info(f"crt.sh: {len(subdomains)} subdomínios encontrados")
        except Exception as e:
            self.logger.warning(f"crt.sh falhou: {e}")

        return sorted(list(subdomains))

    def enumerar_subdomains_subfinder(self) -> list:
        """
        Enumera subdomínios usando subfinder (ProjectDiscovery).

        Reutiliza a classe SubfinderEnum do módulo subfinder.py para
        evitar duplicação de lógica, garantindo validação de TLDs
        restritos e tratamento de erros consistente.

        Requer subfinder instalado no sistema.
        Graceful degradation: retorna lista vazia se subfinder não disponível.

        Returns:
            list: Lista de subdomínios encontrados via subfinder.
        """
        console.print("[bold cyan]→ Enumerando subdomínios (subfinder)...[/bold cyan]")

        # Verificar se o módulo SubfinderEnum está disponível
        if not SUBFINDER_AVAILABLE:
            self.logger.warning("módulo subfinder.py não disponível, pulando enumeração")
            return []

        # Verificar TLDs restritos usando a lista compartilhada
        if any(self.alvo.endswith(tld) for tld in RESTRICTED_TLDS):
            self.logger.warning(f"Subfinder pulado: TLD restrito detectado em {self.alvo}")
            return []

        try:
            # Instanciar SubfinderEnum e delegar a enumeração
            # A validação de domínio e TLD é feita no __init__ de SubfinderEnum
            enum = SubfinderEnum(self.alvo, self.diretorio_saida)
            # Usar o método enumerate() diretamente (sem execute/show_output)
            subdomains = enum.enumerate(sources="all")
            self.logger.info(f"subfinder: {len(subdomains)} subdomínios encontrados")
            return subdomains

        except ValueError as e:
            # Erro de validação (TLD restrito ou domínio inválido)
            self.logger.warning(f"Subfinder pulado: {e}")
            return []
        except RuntimeError as e:
            # subfinder não instalado ou erro de execução
            self.logger.warning(f"Subfinder não disponível: {e}")
            return []
        except Exception as e:
            # Outros erros inesperados
            self.logger.warning(f"Subfinder erro: {e}")
            return []

    def coletar_headers_http(self) -> dict:
        """
        Coleta cabeçalhos HTTP do alvo para fingerprinting passivo.

        Retorna:
            dict: Cabeçalhos HTTP da resposta e código de status.
        """
        try:
            url = self.alvo if self.alvo.startswith("http") else f"https://{self.alvo}"
            resp = requests.get(url, timeout=self.TIMEOUT_HTTP, allow_redirects=True, headers={
                "User-Agent": "EthicalRedTeamSkill/1.0 (Authorized Security Testing)"
            })
            return {
                "status_code": resp.status_code,
                "url_final": resp.url,
                "headers": dict(resp.headers),
                "server": resp.headers.get("Server", "N/A"),
                "x_powered_by": resp.headers.get("X-Powered-By", "N/A"),
            }
        except Exception as e:
            self.logger.warning(f"HTTP headers falhou: {e}")
            return {}

    def executar(self) -> str:
        """
        Orquestra a execução completa do módulo de reconhecimento.

        Executa passive, active ou full conforme o modo configurado
        e salva os resultados em arquivo JSON.

        Retorna:
            str: Caminho do arquivo JSON com os resultados.
        """
        console.print(Panel(
            f"[bold green]🔍 Reconhecimento iniciado[/bold green]\n"
            f"Alvo: [cyan]{self.alvo}[/cyan] | Modo: [yellow]{self.modo}[/yellow]",
            border_style="green"
        ))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            # Passive
            if self.modo in ("passive", "full"):
                # OSINT passivo via crt.sh
                t = p.add_task("OSINT: subdomínios (crt.sh)...")
                crt_subs = self.enumerar_subdomains_passivo()
                p.remove_task(t)

                # Subfinder para descoberta adicional
                t = p.add_task("OSINT: subdomínios (subfinder)...")
                subfinder_subs = self.enumerar_subdomains_subfinder()
                p.remove_task(t)

                # Merge de resultados (remove duplicatas)
                all_subs = sorted(list(set(crt_subs + subfinder_subs)))
                self.resultados["subdomains"] = all_subs
                self.resultados["subdomains_sources"] = {
                    "crtsh": crt_subs,
                    "subfinder": subfinder_subs,
                    "total_crtsh": len(crt_subs),
                    "total_subfinder": len(subfinder_subs),
                    "total_unique": len(all_subs)
                }

            # Active
            if self.modo in ("active", "full") and self.tipo_alvo in ("dominio", "url"):
                t = p.add_task("DNS: consultando registros...")
                self.resultados["dns"] = self.consultar_dns()
                p.remove_task(t)

                t = p.add_task("Resolvendo IPs...")
                ips = self.resolver_ip()
                self.resultados["ips_encontrados"] = ips
                p.remove_task(t)

                for ip in ips[:3]:  # Limitar para M3 com 4GB RAM
                    t = p.add_task(f"WHOIS: {ip}...")
                    self.resultados["whois"][ip] = self.consultar_whois_ip(ip)
                    p.remove_task(t)

            # HTTP Fingerprinting (ambos os modos)
            if self.tipo_alvo in ("dominio", "url", "url"):
                t = p.add_task("HTTP: coletando cabeçalhos...")
                self.resultados["osint"]["http_headers"] = self.coletar_headers_http()
                p.remove_task(t)

        self.resultados["timestamp_fim"] = datetime.now(timezone.utc).isoformat()

        # Exibir resumo
        tabela = Table(title="📊 Resumo do Reconhecimento", border_style="cyan")
        tabela.add_column("Métrica", style="bold")
        tabela.add_column("Valor", style="green")
        tabela.add_row("Subdomínios encontrados", str(len(self.resultados["subdomains"])))
        tabela.add_row("IPs resolvidos", str(len(self.resultados["ips_encontrados"])))
        tabela.add_row("Registros DNS coletados", str(len(self.resultados["dns"])))
        tabela.add_row("Log de auditoria", self.log_file)
        console.print(tabela)

        caminho = salvar_json(self.resultados, f"{self.alvo.replace('.', '_')}_recon", self.diretorio_saida)
        console.print(f"[bold green]✅ Resultados salvos em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de reconhecimento."""
    parser = argparse.ArgumentParser(
        description="Módulo de Reconhecimento — Ethical Red Team Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplo: python recon.py --target example.com --mode passive --output ./saida/"
    )
    parser.add_argument("--target", required=True, help="Alvo: IP, CIDR, domínio ou URL")
    parser.add_argument(
        "--mode", choices=["passive", "active", "full"], default="passive",
        help="Modo: passive (só OSINT), active (DNS+IP), full (completo)"
    )
    parser.add_argument("--output", default="recon_output", help="Diretório de saída")
    parser.add_argument("--skip-disclaimer", action="store_true",
                        help="Pular disclaimer (apenas para ambientes CI/CD autorizados)")
    args = parser.parse_args()

    # Logger temporário para validação
    logger, _ = configurar_logger("recon_auth")

    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    modulo = ModuloReconhecimento(args.target, args.mode, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
