#!/usr/bin/env python3
"""
burp_mcp.py — Web Application Scanner via Burp Suite MCP (Community Edition).

Conecta ao Burp Suite MCP Server e executa análise de aplicações web usando
APENAS as funcionalidades disponíveis na versão gratuita (Community):

  Ferramentas Community disponíveis:
    - GetProxyHttpHistory      → analisa tráfego interceptado
    - GetProxyHttpHistoryRegex → filtra requisições por padrão
    - GetProxyWebsocketHistory → analisa tráfego WebSocket
    - SendHttp1Request         → envia probes ativos
    - SetProxyInterceptState   → controla intercepção
    - UrlEncode/Decode, Base64Encode/Decode, GenerateRandomString

  Ferramentas Pro ONLY (não usadas aqui):
    - GetScannerIssues         → scanner ativo (Pro)
    - GenerateCollaboratorPayload → OAST (Pro)
    - GetCollaboratorInteractions → OAST (Pro)

Pré-requisito:
    Burp Suite rodando com a extensão MCP carregada.
    Build: ./gradlew embedProxyJar
    MCP escutando em http://127.0.0.1:9876

Uso:
    # Análise passiva do histórico de proxy
    python scripts/burp_mcp.py --mode history --output scan_output/

    # Probes ativos em um alvo (requer tráfego já interceptado)
    python scripts/burp_mcp.py --mode full --target https://alvo.com --output scan_output/

    # Apenas verificar conectividade com Burp MCP
    python scripts/burp_mcp.py --check

Autor: Ethical RedTeam Skill
Versão: 1.0.0
Repositório MCP: https://github.com/portswigger/mcp-server
"""

import argparse
import json
import queue
import re
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs

try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    print(f"[ERRO] Dependência ausente: {e}. Execute: pip install -r requirements.txt")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import configurar_logger, exibir_disclaimer_e_validar, salvar_json, calcular_severidade_cvss

console = Console()

# ── Constantes ─────────────────────────────────────────────────────────────────

BURP_MCP_HOST = "127.0.0.1"
BURP_MCP_PORT = 9876
BURP_MCP_BASE = f"http://{BURP_MCP_HOST}:{BURP_MCP_PORT}"
SSE_TIMEOUT = 10       # segundos para aguardar endpoint via SSE
TOOL_TIMEOUT = 30      # segundos para aguardar resposta de uma tool
HISTORY_LIMIT = 200    # máx. de itens do proxy history para analisar

# Caminhos sensíveis para probing ativo (Community)
PROBE_PATHS = [
    "/.git/HEAD",
    "/.env",
    "/.env.local",
    "/.env.backup",
    "/admin",
    "/admin/",
    "/wp-admin/",
    "/phpinfo.php",
    "/server-status",
    "/server-info",
    "/.htaccess",
    "/backup.zip",
    "/backup.tar.gz",
    "/db.sql",
    "/config.php.bak",
    "/crossdomain.xml",
    "/sitemap.xml",
    "/robots.txt",
    "/.well-known/security.txt",
    "/api/",
    "/api/v1/",
    "/swagger.json",
    "/openapi.json",
    "/graphql",
    "/console",
    "/actuator",
    "/actuator/health",
    "/actuator/env",
    "/.DS_Store",
    "/WEB-INF/web.xml",
]

# Headers de segurança esperados e seus riscos
SECURITY_HEADERS = {
    "strict-transport-security": {
        "descricao": "HSTS ausente — conexões HTTP não são forçadas a HTTPS",
        "cvss": 5.4,
        "cwe": "CWE-319",
    },
    "x-content-type-options": {
        "descricao": "X-Content-Type-Options ausente — MIME sniffing habilitado",
        "cvss": 4.3,
        "cwe": "CWE-693",
    },
    "x-frame-options": {
        "descricao": "X-Frame-Options ausente — vulnerável a clickjacking",
        "cvss": 4.7,
        "cwe": "CWE-1021",
    },
    "content-security-policy": {
        "descricao": "Content-Security-Policy ausente — XSS sem mitigação de CSP",
        "cvss": 6.1,
        "cwe": "CWE-79",
    },
    "x-xss-protection": {
        "descricao": "X-XSS-Protection ausente (legado — use CSP)",
        "cvss": 3.1,
        "cwe": "CWE-79",
    },
    "referrer-policy": {
        "descricao": "Referrer-Policy ausente — dados sensíveis vazam via Referer",
        "cvss": 3.7,
        "cwe": "CWE-116",
    },
    "permissions-policy": {
        "descricao": "Permissions-Policy ausente — acesso a recursos do navegador irrestrito",
        "cvss": 2.6,
        "cwe": "CWE-693",
    },
}

# Padrões de dados sensíveis em URLs/parâmetros
SENSITIVE_PATTERNS = [
    (r"[?&](password|passwd|pwd|secret|token|api_key|apikey|auth|access_token)=",
     "Dado sensível exposto na URL", 7.5, "CWE-598"),
    (r"[?&](session|sessid|phpsessid|jsessionid)=",
     "Session ID exposto na URL", 6.5, "CWE-598"),
    (r"Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+",
     "JWT token em requisição", 4.3, "CWE-522"),
    (r"Authorization:\s*Basic\s+[A-Za-z0-9+/=]+",
     "HTTP Basic Auth detectado", 5.3, "CWE-522"),
]

# Cookies com atributos de segurança ausentes
COOKIE_CHECKS = {
    "httponly": ("Cookie sem HttpOnly — acessível via JavaScript (XSS)", 5.3, "CWE-1004"),
    "secure": ("Cookie sem Secure — transmitido em HTTP não criptografado", 5.3, "CWE-614"),
    "samesite": ("Cookie sem SameSite — vulnerável a CSRF", 4.3, "CWE-352"),
}


# ── Cliente MCP SSE ─────────────────────────────────────────────────────────────

class BurpMCPClient:
    """
    Cliente MCP SSE mínimo para o Burp Suite MCP Server.

    Implementa o transporte SSE do Model Context Protocol (MCP):
    1. Conecta via GET /sse (text/event-stream)
    2. Obtém endpoint de mensagens do evento 'endpoint'
    3. Envia tool calls via POST JSON-RPC 2.0
    4. Lê respostas da stream SSE
    """

    def __init__(self, host: str = BURP_MCP_HOST, port: int = BURP_MCP_PORT):
        self.base_url = f"http://{host}:{port}"
        self.message_url: Optional[str] = None
        self._response_queue: queue.Queue = queue.Queue()
        self._sse_thread: Optional[threading.Thread] = None
        self._connected = False
        self._stop_event = threading.Event()
        self._request_id = 0
        self.logger, _ = configurar_logger("burp_mcp_client")

    def connect(self) -> bool:
        """Estabelece conexão SSE e obtém endpoint de mensagens."""
        endpoint_event = threading.Event()

        def _sse_reader():
            try:
                with requests.get(
                    f"{self.base_url}/sse",
                    headers={"Accept": "text/event-stream"},
                    stream=True,
                    timeout=SSE_TIMEOUT,
                ) as resp:
                    resp.raise_for_status()
                    event_type = None
                    for raw_line in resp.iter_lines(decode_unicode=True):
                        if self._stop_event.is_set():
                            break
                        if not raw_line:
                            event_type = None
                            continue
                        if raw_line.startswith("event:"):
                            event_type = raw_line[6:].strip()
                        elif raw_line.startswith("data:"):
                            data = raw_line[5:].strip()
                            if event_type == "endpoint":
                                self.message_url = f"{self.base_url}{data}"
                                self._connected = True
                                endpoint_event.set()
                                self.logger.info(f"MCP endpoint: {self.message_url}")
                            else:
                                # Resposta de tool call
                                try:
                                    msg = json.loads(data)
                                    self._response_queue.put(msg)
                                except json.JSONDecodeError:
                                    pass
            except Exception as e:
                self.logger.error(f"SSE error: {e}")
                endpoint_event.set()  # desbloqueia o connect()

        self._sse_thread = threading.Thread(target=_sse_reader, daemon=True)
        self._sse_thread.start()

        if not endpoint_event.wait(timeout=SSE_TIMEOUT):
            self.logger.error("Timeout aguardando endpoint MCP")
            return False
        return self._connected

    def disconnect(self):
        """Encerra a conexão SSE."""
        self._stop_event.set()
        self._connected = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def call_tool(self, tool_name: str, arguments: dict, timeout: int = TOOL_TIMEOUT) -> Optional[dict]:
        """
        Chama uma tool MCP e retorna o resultado.

        Parâmetros:
            tool_name: Nome da tool (ex: 'GetProxyHttpHistory')
            arguments: Argumentos da tool como dict
            timeout: Segundos de espera pela resposta

        Retorna:
            dict com o resultado, ou None em caso de erro/timeout
        """
        if not self._connected or not self.message_url:
            self.logger.error("Cliente MCP não conectado")
            return None

        req_id = self._next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        try:
            requests.post(
                self.message_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        except Exception as e:
            self.logger.error(f"Erro ao enviar tool call '{tool_name}': {e}")
            return None

        # Aguarda resposta na fila SSE
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                msg = self._response_queue.get(timeout=1.0)
                if msg.get("id") == req_id:
                    if "error" in msg:
                        self.logger.warning(f"Tool '{tool_name}' retornou erro: {msg['error']}")
                        return None
                    return msg.get("result")
                else:
                    # Não é nossa resposta, devolve à fila
                    self._response_queue.put(msg)
            except queue.Empty:
                continue

        self.logger.warning(f"Timeout aguardando resposta de '{tool_name}'")
        return None

    def get_proxy_history(self, count: int = HISTORY_LIMIT, offset: int = 0) -> list[dict]:
        """Retorna histórico do proxy HTTP."""
        result = self.call_tool("GetProxyHttpHistory", {"count": count, "offset": offset})
        if not result:
            return []
        return _parse_mcp_content(result)

    def get_proxy_history_regex(self, regex: str, count: int = 50) -> list[dict]:
        """Retorna entradas do histórico que correspondem ao regex."""
        result = self.call_tool("GetProxyHttpHistoryRegex", {"regex": regex, "count": count, "offset": 0})
        if not result:
            return []
        return _parse_mcp_content(result)

    def send_http1_request(self, raw_request: str, hostname: str, port: int, https: bool) -> Optional[str]:
        """Envia requisição HTTP/1.1 via Burp e retorna a resposta bruta."""
        result = self.call_tool("SendHttp1Request", {
            "content": raw_request,
            "targetHostname": hostname,
            "targetPort": port,
            "usesHttps": https,
        })
        if not result:
            return None
        contents = _parse_mcp_content(result)
        return contents[0] if contents else None

    def set_intercept(self, enabled: bool):
        """Habilita ou desabilita a intercepção do proxy."""
        self.call_tool("SetProxyInterceptState", {"intercepting": enabled})

    def initialize(self) -> bool:
        """Envia handshake MCP initialize."""
        if not self._connected or not self.message_url:
            return False
        req_id = self._next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ethical-redteam-skill", "version": "1.0.0"},
            },
        }
        try:
            requests.post(self.message_url, json=payload, timeout=10)
        except Exception:
            pass
        # Consome resposta do initialize
        try:
            self._response_queue.get(timeout=5)
        except queue.Empty:
            pass
        return True


def _parse_mcp_content(result: dict) -> list:
    """Extrai conteúdo textual de um resultado MCP."""
    items = []
    content = result.get("content", [])
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                items.append(c.get("text", ""))
    return items


# ── Analisador Web (Community) ──────────────────────────────────────────────────

class WebAppAnalyzer:
    """
    Analisador de aplicações web usando as ferramentas Community do Burp MCP.

    Executa dois tipos de análise:
    1. Passiva: examina histórico de proxy interceptado
    2. Ativa: envia probes HTTP para caminhos comuns
    """

    def __init__(self, client: BurpMCPClient, target_url: Optional[str] = None):
        self.client = client
        self.target_url = target_url
        self.target_host = None
        self.target_port = 443
        self.target_https = True
        self.achados: list[dict] = []
        self.logger, _ = configurar_logger("burp_webanalyzer")

        if target_url:
            parsed = urlparse(target_url)
            self.target_host = parsed.hostname
            self.target_https = parsed.scheme == "https"
            self.target_port = parsed.port or (443 if self.target_https else 80)

    def analisar_historico(self) -> list[dict]:
        """Análise passiva: examina o histórico de proxy do Burp."""
        console.print("[cyan]→ Coletando histórico do proxy Burp...[/cyan]")
        historico = self.client.get_proxy_history(count=HISTORY_LIMIT)

        if not historico:
            console.print("[yellow]⚠  Histórico de proxy vazio. Configure o browser para usar Burp como proxy (127.0.0.1:8080)[/yellow]")
            return []

        console.print(f"[green]✓ {len(historico)} entradas no histórico[/green]")
        achados = []

        for entrada in historico:
            if not isinstance(entrada, str):
                continue
            novos = self._analisar_entrada(entrada)
            achados.extend(novos)

        # Deduplicar por descrição + URL
        vistos = set()
        unicos = []
        for a in achados:
            chave = (a["descricao"], a.get("url", ""))
            if chave not in vistos:
                vistos.add(chave)
                unicos.append(a)

        self.achados.extend(unicos)
        return unicos

    def _analisar_entrada(self, entrada: str) -> list[dict]:
        """Analisa uma entrada do histórico de proxy."""
        achados = []
        linhas = entrada.split("\n")

        url = ""
        headers_req: dict[str, str] = {}
        headers_resp: dict[str, str] = {}
        em_resposta = False
        status_code = 0

        for linha in linhas:
            # Linha de requisição (primeira linha HTTP)
            m = re.match(r"^(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\s+(\S+)\s+HTTP", linha)
            if m:
                url = m.group(2)
                continue

            # Linha de status de resposta
            m = re.match(r"^HTTP/\S+\s+(\d+)", linha)
            if m:
                status_code = int(m.group(1))
                em_resposta = True
                continue

            # Separador request/response (linha em branco dupla)
            if linha.strip() == "" and not em_resposta:
                continue

            # Parse de headers
            if ":" in linha:
                nome, _, valor = linha.partition(":")
                nome = nome.strip().lower()
                valor = valor.strip()
                if em_resposta:
                    headers_resp[nome] = valor
                else:
                    headers_req[nome] = valor

        # Montar URL completa
        host = headers_req.get("host", self.target_host or "")
        url_completa = f"{'https' if self.target_https else 'http'}://{host}{url}" if host else url

        # 1. Verificar headers de segurança ausentes (em respostas)
        if em_resposta and status_code in (200, 301, 302, 304):
            for header_nome, info in SECURITY_HEADERS.items():
                if header_nome not in headers_resp:
                    achados.append({
                        "tipo": "header_ausente",
                        "descricao": info["descricao"],
                        "url": url_completa,
                        "evidencia": f"Header '{header_nome}' ausente na resposta",
                        "cvss": info["cvss"],
                        "severidade": calcular_severidade_cvss(info["cvss"]),
                        "cwe": info["cwe"],
                        "recomendacao": f"Adicionar header '{header_nome}' nas respostas HTTP",
                    })

        # 2. Verificar servidor exposto
        server = headers_resp.get("server", "")
        if server and re.search(r"[\d.]+", server):
            achados.append({
                "tipo": "server_disclosure",
                "descricao": f"Versão do servidor exposta: {server}",
                "url": url_completa,
                "evidencia": f"Server: {server}",
                "cvss": 5.3,
                "severidade": "Média",
                "cwe": "CWE-200",
                "recomendacao": "Ocultar versão do servidor (ServerTokens Prod / server_tokens off)",
            })

        # 3. Verificar cookies inseguros
        for set_cookie in [v for k, v in headers_resp.items() if k == "set-cookie"]:
            cookie_lower = set_cookie.lower()
            for flag, (desc, cvss, cwe) in COOKIE_CHECKS.items():
                if flag not in cookie_lower:
                    nome_cookie = set_cookie.split("=")[0].strip()
                    achados.append({
                        "tipo": "cookie_inseguro",
                        "descricao": desc,
                        "url": url_completa,
                        "evidencia": f"Set-Cookie: {set_cookie[:100]}",
                        "cvss": cvss,
                        "severidade": calcular_severidade_cvss(cvss),
                        "cwe": cwe,
                        "recomendacao": f"Adicionar flag '{flag}' ao cookie '{nome_cookie}'",
                    })

        # 4. Verificar dados sensíveis na URL
        for pattern, desc, cvss, cwe in SENSITIVE_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE) or re.search(pattern, entrada, re.IGNORECASE):
                achados.append({
                    "tipo": "dado_sensivel",
                    "descricao": desc,
                    "url": url_completa,
                    "evidencia": f"Padrão detectado: {pattern[:50]}",
                    "cvss": cvss,
                    "severidade": calcular_severidade_cvss(cvss),
                    "cwe": cwe,
                    "recomendacao": "Mover dados sensíveis para o corpo da requisição (POST) ou headers",
                })
                break

        # 5. HTTP puro (sem HTTPS)
        if headers_req.get("host") and not self.target_https and not url.startswith("https"):
            achados.append({
                "tipo": "http_sem_criptografia",
                "descricao": "Aplicação acessível via HTTP não criptografado",
                "url": url_completa,
                "evidencia": "Requisição trafegando em HTTP claro",
                "cvss": 5.9,
                "severidade": "Média",
                "cwe": "CWE-319",
                "recomendacao": "Implementar redirect 301 para HTTPS e habilitar HSTS",
            })

        # 6. CORS permissivo
        cors = headers_resp.get("access-control-allow-origin", "")
        if cors == "*":
            achados.append({
                "tipo": "cors_permissivo",
                "descricao": "CORS wildcard (*) permite requisições de qualquer origem",
                "url": url_completa,
                "evidencia": "Access-Control-Allow-Origin: *",
                "cvss": 6.5,
                "severidade": calcular_severidade_cvss(6.5),
                "cwe": "CWE-942",
                "recomendacao": "Restringir CORS a origens específicas e confiáveis",
            })

        return achados

    def probing_ativo(self) -> list[dict]:
        """Probing ativo: testa caminhos sensíveis no alvo via SendHttp1Request."""
        if not self.target_host:
            console.print("[yellow]⚠  Alvo não definido — use --target para probing ativo[/yellow]")
            return []

        console.print(f"\n[cyan]→ Probing ativo em {self.target_host}:{self.target_port}...[/cyan]")
        achados = []
        encontrados = []

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            t = p.add_task(f"Testando {len(PROBE_PATHS)} caminhos sensíveis...", total=len(PROBE_PATHS))

            for caminho in PROBE_PATHS:
                raw_request = (
                    f"GET {caminho} HTTP/1.1\r\n"
                    f"Host: {self.target_host}\r\n"
                    f"User-Agent: Mozilla/5.0 (compatible; SecurityScanner/1.0)\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                )

                resposta = self.client.send_http1_request(
                    raw_request=raw_request,
                    hostname=self.target_host,
                    port=self.target_port,
                    https=self.target_https,
                )

                if resposta:
                    status = _extrair_status(resposta)
                    tamanho = len(resposta)

                    if status in (200, 403) and tamanho > 50:
                        # 200 = exposto, 403 = existe mas bloqueado (ainda é achado)
                        encontrados.append(caminho)
                        cvss = 7.5 if status == 200 else 4.3
                        achados.append({
                            "tipo": "caminho_sensivel",
                            "descricao": f"Caminho sensível acessível: {caminho} (HTTP {status})",
                            "url": f"{'https' if self.target_https else 'http'}://{self.target_host}{caminho}",
                            "evidencia": f"HTTP {status} — {tamanho} bytes",
                            "cvss": cvss,
                            "severidade": calcular_severidade_cvss(cvss),
                            "cwe": "CWE-538",
                            "recomendacao": f"Restringir acesso a '{caminho}', verificar se é necessário expô-lo",
                        })

                p.advance(t)

        if encontrados:
            console.print(f"[red]⚠  {len(encontrados)} caminhos sensíveis encontrados: {encontrados[:5]}...[/red]")
        else:
            console.print("[green]✓ Nenhum caminho sensível óbvio exposto[/green]")

        # Probe: verificar métodos HTTP permitidos (OPTIONS)
        options_req = (
            f"OPTIONS / HTTP/1.1\r\n"
            f"Host: {self.target_host}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        resposta_options = self.client.send_http1_request(
            options_req, self.target_host, self.target_port, self.target_https
        )
        if resposta_options:
            allow = re.search(r"(?i)^Allow:\s*(.+)$", resposta_options, re.MULTILINE)
            if allow:
                metodos = allow.group(1)
                if any(m in metodos.upper() for m in ["PUT", "DELETE", "TRACE", "CONNECT"]):
                    achados.append({
                        "tipo": "metodos_http_perigosos",
                        "descricao": f"Métodos HTTP perigosos habilitados: {metodos.strip()}",
                        "url": f"{'https' if self.target_https else 'http'}://{self.target_host}/",
                        "evidencia": f"Allow: {metodos.strip()}",
                        "cvss": 6.5,
                        "severidade": "Média",
                        "cwe": "CWE-650",
                        "recomendacao": "Desabilitar PUT, DELETE, TRACE e CONNECT no servidor web",
                    })

        self.achados.extend(achados)
        return achados

    def gerar_resumo(self) -> dict:
        """Gera resumo estatístico dos achados."""
        por_severidade = {"Crítica": 0, "Alta": 0, "Média": 0, "Baixa": 0, "Informativa": 0}
        por_tipo: dict[str, int] = {}

        for a in self.achados:
            sev = a.get("severidade", "Informativa")
            if sev in por_severidade:
                por_severidade[sev] += 1
            tipo = a.get("tipo", "outro")
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

        return {
            "total_achados": len(self.achados),
            "por_severidade": por_severidade,
            "por_tipo": por_tipo,
            "score_risco": _calcular_score_risco(por_severidade),
        }


def _extrair_status(resposta: str) -> int:
    """Extrai o código de status HTTP de uma resposta bruta."""
    m = re.match(r"HTTP/\S+\s+(\d+)", resposta)
    return int(m.group(1)) if m else 0


def _calcular_score_risco(por_severidade: dict) -> str:
    """Calcula um score de risco geral baseado na distribuição de severidades."""
    score = (
        por_severidade.get("Crítica", 0) * 10 +
        por_severidade.get("Alta", 0) * 7 +
        por_severidade.get("Média", 0) * 4 +
        por_severidade.get("Baixa", 0) * 1
    )
    if score >= 30:
        return "CRÍTICO"
    elif score >= 15:
        return "ALTO"
    elif score >= 5:
        return "MÉDIO"
    elif score > 0:
        return "BAIXO"
    return "INFORMATIVO"


# ── Verificação de Conectividade ────────────────────────────────────────────────

def verificar_burp_disponivel(host: str = BURP_MCP_HOST, port: int = BURP_MCP_PORT) -> bool:
    """Verifica se o Burp MCP Server está acessível."""
    try:
        resp = requests.get(f"http://{host}:{port}", timeout=3)
        return True
    except requests.ConnectionError:
        return False
    except Exception:
        return True  # porta respondeu com algum erro HTTP, Burp está rodando


# ── Interface CLI ───────────────────────────────────────────────────────────────

def main():
    """Ponto de entrada do módulo Burp MCP."""
    parser = argparse.ArgumentParser(
        description="Web App Scanner via Burp Suite MCP (Community Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Verificar se Burp MCP está rodando
  python scripts/burp_mcp.py --check

  # Análise passiva do histórico de proxy
  python scripts/burp_mcp.py --mode history --output scan_output/

  # Probing ativo + histórico de proxy
  python scripts/burp_mcp.py --mode full --target https://alvo.com --output scan_output/

Pré-requisito:
  1. Burp Suite rodando com extensão MCP carregada
  2. Browser configurado com proxy 127.0.0.1:8080
  3. Navegar no alvo para gerar tráfego no histórico
        """,
    )
    parser.add_argument("--target", help="URL do alvo (ex: https://alvo.com)")
    parser.add_argument(
        "--mode", choices=["history", "active", "full"], default="history",
        help="Modo: history=passivo, active=probes, full=ambos (padrão: history)"
    )
    parser.add_argument("--output", default="scan_output", help="Diretório de saída")
    parser.add_argument("--check", action="store_true", help="Apenas verifica conectividade com Burp MCP")
    parser.add_argument("--no-intercept", action="store_true", help="Não altera o estado de intercepção do proxy")
    parser.add_argument("--skip-disclaimer", action="store_true")
    parser.add_argument(
        "--burp-host", default=BURP_MCP_HOST,
        help=f"Host do Burp MCP (padrão: {BURP_MCP_HOST})"
    )
    parser.add_argument(
        "--burp-port", type=int, default=BURP_MCP_PORT,
        help=f"Porta do Burp MCP (padrão: {BURP_MCP_PORT})"
    )
    args = parser.parse_args()

    # Apenas verificar conectividade
    if args.check:
        console.print(f"\n[bold]Verificando Burp MCP em {args.burp_host}:{args.burp_port}...[/bold]")
        if verificar_burp_disponivel(args.burp_host, args.burp_port):
            console.print("[bold green]✅ Burp MCP Server acessível[/bold green]")
            console.print("[dim]Dica: Verifique a aba MCP no Burp Suite para confirmar que está habilitado[/dim]")
        else:
            console.print("[bold red]❌ Burp MCP Server NÃO está acessível[/bold red]")
            console.print("\n[yellow]Para ativar:[/yellow]")
            console.print("  1. Abra o Burp Suite")
            console.print("  2. Carregue a extensão MCP: Extensions → Add → Java → mcp-server-all.jar")
            console.print("  3. Vá na aba 'MCP' e habilite o servidor (porta padrão: 9876)")
            console.print("  4. Build da extensão: git clone https://github.com/portswigger/mcp-server && ./gradlew embedProxyJar")
        return

    # Disclaimer
    logger, _ = configurar_logger("burp_mcp_auth")
    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    # Verificar disponibilidade
    if not verificar_burp_disponivel(args.burp_host, args.burp_port):
        console.print(Panel(
            "[bold red]❌ Burp Suite MCP Server não está disponível[/bold red]\n\n"
            "[yellow]Execute primeiro:[/yellow]\n"
            "  1. Abra o Burp Suite\n"
            "  2. Carregue a extensão MCP (Extensions → Add → mcp-server-all.jar)\n"
            "  3. Habilite na aba MCP (porta 9876)\n\n"
            "[dim]Verifique: python scripts/burp_mcp.py --check[/dim]",
            border_style="red",
            title="Burp MCP Offline"
        ))
        sys.exit(1)

    # Conectar via MCP SSE
    console.print(Panel(
        f"[bold green]🕷  Burp Suite MCP — Web App Scanner[/bold green]\n"
        f"Modo: [yellow]{args.mode}[/yellow]"
        + (f" | Alvo: [cyan]{args.target}[/cyan]" if args.target else ""),
        border_style="green"
    ))

    client = BurpMCPClient(host=args.burp_host, port=args.burp_port)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
        t = p.add_task("Conectando ao Burp MCP Server via SSE...")
        connected = client.connect()
        p.remove_task(t)

    if not connected:
        console.print("[bold red]❌ Falha ao conectar via MCP SSE[/bold red]")
        console.print("[yellow]Certifique-se que o servidor MCP está habilitado na aba MCP do Burp Suite[/yellow]")
        sys.exit(1)

    client.initialize()
    console.print("[bold green]✓ Conectado ao Burp MCP Server[/bold green]")

    # Desabilitar intercepção para não bloquear probes
    if not args.no_intercept:
        client.set_intercept(False)
        console.print("[dim]→ Intercepção do proxy desabilitada para esta sessão[/dim]")

    # Executar análise
    analyzer = WebAppAnalyzer(client, target_url=args.target)
    todos_achados = []

    if args.mode in ("history", "full"):
        achados_passivos = analyzer.analisar_historico()
        todos_achados.extend(achados_passivos)
        console.print(f"[green]✓ Análise passiva: {len(achados_passivos)} achados[/green]")

    if args.mode in ("active", "full"):
        achados_ativos = analyzer.probing_ativo()
        todos_achados.extend(achados_ativos)
        console.print(f"[green]✓ Probing ativo: {len(achados_ativos)} achados[/green]")

    client.disconnect()

    resumo = analyzer.gerar_resumo()

    # Exibir tabela de resultados
    tabela = Table(title="🕷  Resultados — Burp MCP (Community)", border_style="cyan")
    tabela.add_column("Severidade", style="bold")
    tabela.add_column("Quantidade", style="green", justify="right")
    tabela.add_column("Exemplo", style="dim")

    for sev in ["Crítica", "Alta", "Média", "Baixa", "Informativa"]:
        qtd = resumo["por_severidade"].get(sev, 0)
        if qtd > 0:
            exemplo = next(
                (a["descricao"][:60] for a in todos_achados if a.get("severidade") == sev), ""
            )
            cor = {"Crítica": "red", "Alta": "orange3", "Média": "yellow", "Baixa": "blue", "Informativa": "dim"}.get(sev, "")
            tabela.add_row(f"[{cor}]{sev}[/{cor}]", str(qtd), exemplo)

    console.print(tabela)
    console.print(f"\n[bold]Score de Risco: [red]{resumo['score_risco']}[/red][/bold]")

    # Salvar resultado no formato do pipeline
    resultado = {
        "modulo": "burp_mcp_community",
        "alvo": args.target or "proxy_history",
        "modo": args.mode,
        "timestamp_inicio": datetime.now().isoformat(),
        "timestamp_fim": datetime.now().isoformat(),
        "fonte": "Burp Suite MCP Server (Community)",
        "achados": todos_achados,
        "resumo": resumo,
        "nota": (
            "Análise realizada com Burp Suite Community Edition. "
            "Para scanner ativo completo (SQLi, XSS automático, IDOR), use Burp Pro + GetScannerIssues."
        ),
    }

    caminho = salvar_json(
        resultado,
        f"{(args.target or 'proxy_history').replace('/', '_').replace(':', '_').replace('.', '_')}_burp_mcp",
        args.output
    )
    console.print(f"\n[bold green]✅ Resultados salvos: {caminho}[/bold green]")
    console.print(
        "[dim]→ Use este arquivo com analyzer.py: "
        f"python scripts/analyzer.py --scan {caminho}[/dim]"
    )


if __name__ == "__main__":
    main()
