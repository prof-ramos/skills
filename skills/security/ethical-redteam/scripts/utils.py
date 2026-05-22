#!/usr/bin/env python3
"""
utils.py — Utilitários compartilhados para a Ethical Red Team Skill.

Fornece funções de logging, validação de autorização, tratamento de erros
e helpers de saída para todos os módulos.

Autor: Ethical RedTeam Skill
Versão: 1.0.0
Compatibilidade: Python 3.11+ / macOS 13+ / Apple Silicon M3
"""

import json
import logging
import os
import platform
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text

console = Console()

# ── Configuração de Logging ────────────────────────────────────────────────────

def configurar_logger(nome_modulo: str, nivel: int = logging.DEBUG) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.

    Parâmetros:
        nome_modulo: Nome do módulo que está sendo logado.
        nivel: Nível de logging (padrão: DEBUG para auditoria completa).

    Retorna:
        logging.Logger: Logger configurado com handlers de arquivo e console.
    """
    Path("logs").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{nome_modulo}_{timestamp}.log"

    logger = logging.getLogger(nome_modulo)
    logger.setLevel(nivel)

    # Handler para arquivo (auditoria completa)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger, log_file


# ── Disclaimer e Validação de Autorização ─────────────────────────────────────

DISCLAIMER = """
╔══════════════════════════════════════════════════════════════════════════╗
║         ⚠️  ETHICAL RED TEAM SKILL — AVISO LEGAL OBRIGATÓRIO ⚠️          ║
║                                                                          ║
║  Esta ferramenta é destinada EXCLUSIVAMENTE para testes de segurança     ║
║  AUTORIZADOS em ambientes CONTROLADOS.                                   ║
║                                                                          ║
║  O uso não autorizado é ILEGAL e sujeito a processos criminais           ║
║  conforme:                                                               ║
║    • LGPD (Lei 13.709/2018)                                              ║
║    • Marco Civil da Internet (Lei 12.965/2014)                           ║
║    • Código Penal Brasileiro (Art. 154-A - invasão de dispositivos)      ║
║    • CFAA (Computer Fraud and Abuse Act) — para alvos nos EUA            ║
║                                                                          ║
║  SEMPRE obtenha autorização ESCRITA antes de iniciar qualquer teste.     ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def exibir_disclaimer_e_validar(logger: logging.Logger) -> bool:
    """
    Exibe o disclaimer legal e solicita confirmação interativa do usuário.

    Solicita confirmação para três itens obrigatórios:
    1. Autorização escrita do proprietário do sistema.
    2. Escopo de teste claramente definido.
    3. Rules of Engagement (RoE) documentado.

    Parâmetros:
        logger: Logger para registrar a validação.

    Retorna:
        bool: True se todas as confirmações forem positivas, False caso contrário.
    """
    console.print(Panel(
        Text(DISCLAIMER, style="bold red"),
        title="⚠️ AVISO LEGAL", border_style="red"
    ))

    perguntas = [
        "Você possui autorização ESCRITA do proprietário do sistema alvo?",
        "O escopo do teste está claramente definido e documentado?",
        "Existe um Rules of Engagement (RoE) formal documentado?",
    ]

    for pergunta in perguntas:
        if not Confirm.ask(f"[bold yellow]{pergunta}[/bold yellow]"):
            console.print(
                "[bold red]❌ Operação cancelada. Obtenha autorização adequada antes de prosseguir.[/bold red]"
            )
            logger.warning("AUTORIZAÇÃO NEGADA: Usuário não confirmou requisitos legais.")
            return False

    logger.info("AUTORIZAÇÃO CONFIRMADA: Usuário confirmou todos os requisitos legais.")
    return True


# ── Validação de Alvos ─────────────────────────────────────────────────────────

def validar_alvo(alvo: str) -> dict:
    """
    Valida e classifica o tipo de alvo fornecido.

    Detecta se o alvo é um endereço IP, range CIDR, domínio ou URL
    e retorna metadados para uso nos módulos.

    Parâmetros:
        alvo: String com IP, CIDR, domínio ou URL do alvo.

    Retorna:
        dict: Dicionário com keys 'tipo', 'valor', 'valido'.

    Exemplo:
        >>> validar_alvo("192.168.1.1")
        {'tipo': 'ip', 'valor': '192.168.1.1', 'valido': True}
    """
    alvo = alvo.strip()

    # IP simples
    padrao_ip = r"^(\d{1,3}\.){3}\d{1,3}$"
    # CIDR
    padrao_cidr = r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"
    # Domínio
    padrao_dominio = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    # URL
    padrao_url = r"^https?://"

    if re.match(padrao_cidr, alvo):
        return {"tipo": "cidr", "valor": alvo, "valido": True}
    elif re.match(padrao_ip, alvo):
        partes = [int(p) for p in alvo.split(".")]
        valido = all(0 <= p <= 255 for p in partes)
        return {"tipo": "ip", "valor": alvo, "valido": valido}
    elif re.match(padrao_url, alvo):
        return {"tipo": "url", "valor": alvo, "valido": True}
    elif re.match(padrao_dominio, alvo):
        return {"tipo": "dominio", "valor": alvo, "valido": True}
    else:
        return {"tipo": "desconhecido", "valor": alvo, "valido": False}


# ── Detecção de Ambiente ───────────────────────────────────────────────────────

def detectar_ambiente() -> dict:
    """
    Detecta informações do ambiente de execução para compatibilidade.

    Verifica arquitetura do processador, versão do sistema operacional
    e disponibilidade de memória RAM para otimização de parâmetros.

    Retorna:
        dict: Informações do ambiente com keys 'arch', 'os', 'versao_os',
              'python', 'apple_silicon', 'ram_gb'.
    """
    arch = platform.machine()
    sistema = platform.system()
    versao = platform.version()
    python_ver = platform.python_version()

    ram_gb = 8  # padrão conservador
    if sistema == "Darwin":
        try:
            import subprocess
            resultado = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5
            )
            ram_bytes = int(resultado.stdout.strip())
            ram_gb = ram_bytes / (1024 ** 3)
        except Exception:
            pass

    return {
        "arch": arch,
        "os": sistema,
        "versao_os": versao,
        "python": python_ver,
        "apple_silicon": arch == "arm64" and sistema == "Darwin",
        "ram_gb": round(ram_gb, 1),
    }


# ── Persistência de Resultados ────────────────────────────────────────────────

def salvar_json(dados: dict, prefixo: str, diretorio: str = ".") -> str:
    """
    Salva dados em arquivo JSON com timestamp no nome.

    Parâmetros:
        dados: Dicionário com os dados a serem salvos.
        prefixo: Prefixo para o nome do arquivo.
        diretorio: Diretório de destino (padrão: diretório atual).

    Retorna:
        str: Caminho completo do arquivo salvo.
    """
    Path(diretorio).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = Path(diretorio) / f"{prefixo}_{timestamp}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    return str(caminho)


def calcular_severidade_cvss(score: float) -> str:
    """
    Converte score CVSS v3.1 numérico para classificação textual.

    Parâmetros:
        score: Score CVSS entre 0.0 e 10.0.

    Retorna:
        str: Classificação de severidade (Crítica/Alta/Média/Baixa/Informativa).
    """
    if score >= 9.0:
        return "Crítica"
    elif score >= 7.0:
        return "Alta"
    elif score >= 4.0:
        return "Média"
    elif score > 0.0:
        return "Baixa"
    else:
        return "Informativa"
