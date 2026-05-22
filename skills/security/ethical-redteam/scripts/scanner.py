#!/usr/bin/env python3
"""
scanner.py — Módulo de Scanning (Portas / Serviços / Vulnerabilidades).

Realiza varredura de portas, detecção de serviços e sistema operacional
usando nmap via python-nmap. Otimizado para Apple Silicon M3 com limite
de 4GB de RAM.

Perfis disponíveis:
    quick    — Top 100 portas, detecção rápida de SO
    standard — Top 1000 portas + banner grabbing (recomendado)
    deep     — Todas as portas + scripts NSE de vulnerabilidades

Uso: python scripts/scanner.py --target 192.168.1.1 --profile standard

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import nmap
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    print(f"[ERRO] Dependência ausente: {e}. Execute o install.sh primeiro.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    configurar_logger, exibir_disclaimer_e_validar,
    validar_alvo, salvar_json, detectar_ambiente,
    calcular_severidade_cvss
)

console = Console()


# Perfis de scan otimizados para M3 (máx. 4GB RAM)
PERFIS_SCAN = {
    "quick": {
        "descricao": "Top 100 portas, sem scripts (rápido, baixo consumo)",
        "args": "-sV -O --top-ports 100 -T3 --host-timeout 120s",
        "ram_estimada_mb": 200,
    },
    "standard": {
        "descricao": "Top 1000 portas + banner grabbing (recomendado)",
        "args": "-sV -sC --top-ports 1000 -T3 --host-timeout 300s",
        "ram_estimada_mb": 512,
    },
    "deep": {
        "descricao": "Todas as portas + scripts NSE de vulnerabilidades",
        "args": "-sV -sC -p- --script=vuln -T2 --host-timeout 600s",
        "ram_estimada_mb": 2048,
    },
}


class ModuloScanner:
    """
    Módulo de varredura de portas e serviços para testes de segurança.

    Utiliza python-nmap como interface para o nmap, com otimizações
    específicas para Apple Silicon M3 e limite de 4GB de RAM.
    """

    def __init__(self, alvo: str, perfil: str, diretorio_saida: str):
        """
        Inicializa o módulo de scanning.

        Parâmetros:
            alvo: IP, CIDR ou hostname do alvo autorizado.
            perfil: Perfil de scan ('quick', 'standard' ou 'deep').
            diretorio_saida: Diretório para salvar os resultados.
        """
        self.alvo = alvo
        self.perfil = perfil
        self.config_perfil = PERFIS_SCAN[perfil]
        self.diretorio_saida = diretorio_saida
        self.logger, self.log_file = configurar_logger("scanner")
        self.nm = nmap.PortScanner()
        self.resultados: dict = {
            "alvo": alvo,
            "perfil": perfil,
            "config_perfil": self.config_perfil,
            "timestamp_inicio": datetime.now().isoformat(),
            "ambiente": detectar_ambiente(),
            "hosts": [],
            "resumo": {},
        }

        validacao = validar_alvo(alvo)
        if not validacao["valido"]:
            console.print(f"[bold red]❌ Alvo inválido: {alvo}[/bold red]")
            sys.exit(1)

        self.logger.info(f"Scanner iniciado | alvo={alvo} | perfil={perfil}")
        self._verificar_ram()

    def _verificar_ram(self):
        """
        Verifica se há RAM suficiente para o perfil selecionado.

        Emite aviso se a RAM estimada do scan ultrapassar 3.5GB,
        prevenindo degradação de performance no M3 com 8GB.
        """
        ram_necessaria = self.config_perfil["ram_estimada_mb"]
        if ram_necessaria > 3500:
            console.print(
                f"[bold yellow]⚠️  O perfil '{self.perfil}' pode consumir ~{ram_necessaria}MB RAM. "
                f"Considere usar 'standard' para preservar 4GB no M3.[/bold yellow]"
            )
            self.logger.warning(f"Uso de RAM estimado alto: {ram_necessaria}MB")

    def executar_scan(self) -> dict:
        """
        Executa o scan nmap com os parâmetros do perfil selecionado.

        Retorna:
            dict: Resultado bruto do scan organizado por host.
        """
        console.print(Panel(
            f"[bold green]🔬 Scanner iniciado[/bold green]\n"
            f"Alvo: [cyan]{self.alvo}[/cyan] | Perfil: [yellow]{self.perfil}[/yellow]\n"
            f"{self.config_perfil['descricao']}",
            border_style="green"
        ))

        hosts_resultado = []

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            t = p.add_task(f"Executando nmap ({self.perfil})...")
            try:
                self.nm.scan(hosts=self.alvo, arguments=self.config_perfil["args"])
                p.remove_task(t)
            except nmap.PortScannerError as e:
                p.remove_task(t)
                self.logger.error(f"Erro no nmap: {e}")
                console.print(f"[bold red]❌ Erro no nmap: {e}[/bold red]")
                console.print("[yellow]Verifique se o nmap está instalado: brew install nmap[/yellow]")
                return {}

        for host in self.nm.all_hosts():
            info_host = {
                "ip": host,
                "hostname": self.nm[host].hostname(),
                "estado": self.nm[host].state(),
                "os_match": [],
                "portas": [],
            }

            # Detecção de SO
            if "osmatch" in self.nm[host]:
                info_host["os_match"] = [
                    {"nome": m["name"], "acuracia": m["accuracy"]}
                    for m in self.nm[host]["osmatch"][:3]
                ]

            # Portas e serviços
            for proto in self.nm[host].all_protocols():
                portas = sorted(self.nm[host][proto].keys())
                for porta in portas:
                    dados_porta = self.nm[host][proto][porta]
                    info_porta = {
                        "porta": porta,
                        "protocolo": proto,
                        "estado": dados_porta.get("state", "unknown"),
                        "servico": dados_porta.get("name", ""),
                        "produto": dados_porta.get("product", ""),
                        "versao": dados_porta.get("version", ""),
                        "extra": dados_porta.get("extrainfo", ""),
                        "scripts": dados_porta.get("script", {}),
                    }
                    info_host["portas"].append(info_porta)

            hosts_resultado.append(info_host)
            self.logger.info(f"Host {host}: {len(info_host['portas'])} portas encontradas")

        return hosts_resultado

    def _gerar_resumo(self, hosts: list) -> dict:
        """
        Gera um resumo estatístico dos resultados do scan.

        Parâmetros:
            hosts: Lista de hosts com informações de portas e serviços.

        Retorna:
            dict: Resumo com contadores de hosts, portas e serviços.
        """
        total_portas_abertas = sum(
            len([p for p in h["portas"] if p["estado"] == "open"])
            for h in hosts
        )
        servicos_unicos = set(
            p["servico"] for h in hosts for p in h["portas"] if p["estado"] == "open"
        )
        return {
            "total_hosts": len(hosts),
            "hosts_ativos": len([h for h in hosts if h["estado"] == "up"]),
            "total_portas_abertas": total_portas_abertas,
            "servicos_detectados": sorted(list(servicos_unicos)),
        }

    def executar(self) -> str:
        """
        Orquestra a execução completa do scan e salva os resultados.

        Retorna:
            str: Caminho do arquivo JSON com os resultados do scan.
        """
        hosts = self.executar_scan()
        self.resultados["hosts"] = hosts if hosts else []
        self.resultados["resumo"] = self._gerar_resumo(self.resultados["hosts"])
        self.resultados["timestamp_fim"] = datetime.now().isoformat()

        # Exibir tabela de resultados
        tabela = Table(title="📊 Resumo do Scan", border_style="cyan")
        tabela.add_column("Métrica", style="bold")
        tabela.add_column("Valor", style="green")
        tabela.add_row("Hosts escaneados", str(self.resultados["resumo"]["total_hosts"]))
        tabela.add_row("Hosts ativos", str(self.resultados["resumo"]["hosts_ativos"]))
        tabela.add_row("Portas abertas encontradas", str(self.resultados["resumo"]["total_portas_abertas"]))
        tabela.add_row("Serviços detectados", str(len(self.resultados["resumo"]["servicos_detectados"])))
        tabela.add_row("Log de auditoria", self.log_file)
        console.print(tabela)

        caminho = salvar_json(
            self.resultados,
            f"{self.alvo.replace('/', '_').replace('.', '_')}_scan",
            self.diretorio_saida
        )
        console.print(f"[bold green]✅ Resultados salvos em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de scanning."""
    parser = argparse.ArgumentParser(
        description="Módulo de Scanning — Ethical Red Team Skill",
    )
    parser.add_argument("--target", required=True, help="Alvo: IP, CIDR ou hostname")
    parser.add_argument(
        "--profile", choices=["quick", "standard", "deep"], default="standard",
        help="Perfil de scan (padrão: standard)"
    )
    parser.add_argument("--output", default="scan_output", help="Diretório de saída")
    parser.add_argument("--skip-disclaimer", action="store_true")
    args = parser.parse_args()

    logger, _ = configurar_logger("scanner_auth")
    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    modulo = ModuloScanner(args.target, args.profile, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
