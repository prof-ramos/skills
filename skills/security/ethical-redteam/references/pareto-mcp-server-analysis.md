# Análise Pareto: PortSwigger MCP Server

> **Referência:** https://github.com/portswigger/mcp-server
> **Contexto:** Integração ao `ethical-redteam-skill` (Python + OSINT + Nmap + Relatórios)

---

## O que é o PortSwigger MCP Server?

Extensão Java para o **Burp Suite** que expõe as capacidades da ferramenta via **Model Context Protocol (MCP)**, permitindo que clientes AI (como Claude Desktop) controlem o Burp Suite por linguagem natural.

---

## Análise Pareto: Dificuldade × Benefício

Princípio aplicado: **quais 20% de esforço entregam 80% do valor?**

### Diagrama de Quadrantes

```
BENEFÍCIO
Alto │  [B] Scanner Web     │  [A] ★ QUICK WIN ★
     │  Request Intercept   │  Proxy + MCP Bridge
     │  Vuln Detection      │  Claude → Burp IA
     │                      │
─────┼──────────────────────┼───────────────────── DIFICULDADE
     │  [D] Baixo impacto   │  [C] Alto custo
Baixo│  Relatórios Burp     │  CI/CD + Docker
     │  Export apenas       │  Pipeline automático
     │                      │
          Baixa                   Alta
```

### Tabela de Funcionalidades por Quadrante

| ID | Funcionalidade | Dificuldade (1-10) | Benefício (1-10) | Quadrante | Prioridade |
|----|---------------|-------------------|-----------------|-----------|------------|
| F1 | Instalar extensão Burp + build Gradle | 4 | 9 | A | ★ Alta |
| F2 | Configurar MCP bridge (SSE → Stdio) | 3 | 9 | A | ★ Alta |
| F3 | Conectar Claude ao Burp via MCP | 3 | 10 | A | ★ Alta |
| F4 | Scanner web ativo (proxy HTTP) | 5 | 9 | A/B | ★ Alta |
| F5 | Intercepção de requests em tempo real | 6 | 8 | B | Media |
| F6 | Detecção de vulnerabilidades (OWASP Top 10) | 6 | 9 | B | Media |
| F7 | Integração com pipeline Python existente | 7 | 7 | B/C | Media |
| F8 | Burp Pro (licença paga) | 2* | 10 | A* | Condicional |
| F9 | Docker + headless Burp | 8 | 6 | C | Baixa |
| F10 | CI/CD pipeline automatizado | 9 | 5 | C | Baixa |
| F11 | Export de relatórios Burp → reporter.py | 4 | 4 | D | Descartável |

`* Custo financeiro, não técnico`

---

## Detalhamento: Quadrante A — Quick Wins (80% do valor, 20% do esforço)

### F1 + F2 + F3 — Setup Base (≈ 2–3 horas)

**O que faz:**
- Compila a extensão com `./gradlew embedProxyJar`
- Carrega o JAR no Burp Suite (Extensions → Add → Java)
- Claude passa a controlar o Burp via MCP: interceptar tráfego, disparar scans, analisar respostas

**Por que é quick win:**
- Repositório já está pronto e funcional
- Não requer mudanças no código Python existente
- Claude Desktop suporta MCP nativamente
- O `ethical-redteam-skill` ganha um módulo de **web app testing** que hoje não tem

**Pré-requisitos:**
```
- Java JDK 17+ no PATH
- Burp Suite (Community = limitado; Pro = completo)
- Claude Desktop instalado
- Burp rodando como proxy local (:8080)
```

### F4 — Scanner Web Ativo

**Ganho imediato:** Adiciona ao skill atual (OSINT + Nmap) a camada de **web application scanning**, o maior gap da ferramenta hoje.

**Sem MCP server:** A skill atual não tem scanning de aplicações web (apenas portas/serviços via Nmap).

---

## Análise de Gaps: Skill Atual vs. Com MCP Server

| Capacidade | Skill Atual | Com MCP Server |
|-----------|------------|----------------|
| Recon OSINT | ✅ DNS, WHOIS, crt.sh | ✅ |
| Enumeração subdomínios | ✅ subfinder | ✅ |
| Port scanning | ✅ Nmap | ✅ |
| **Web app scanning** | ❌ Ausente | ✅ Burp Scanner |
| **Request intercept** | ❌ Ausente | ✅ Burp Proxy |
| **Auth bypass testing** | ❌ Ausente | ✅ via Burp |
| **SQLi / XSS / IDOR** | ❌ Ausente | ✅ Burp Active Scan |
| Análise CVSS | ✅ | ✅ |
| Relatórios OWASP | ✅ | ✅ + dados Burp |

**Conclusão do gap:** O MCP Server preenche o maior buraco da skill: **web application testing**.

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Burp Community limita scanner | Alta | Alto | Usar Burp Pro ou Burp Free features apenas |
| Java não configurado no PATH | Media | Medio | Script de verificação (já existe `check-deps.sh`) |
| Conflito porta 9876 com TOR | Baixa | Baixo | Configurar porta alternativa no Burp MCP tab |
| Burp exposto fora de localhost | Baixa | Alto | Default já é 127.0.0.1 — manter assim |
| Dependência de GUI Burp | Media | Medio | Burp headless disponível no Pro |

---

## Recomendação Pareto

```
IMPLEMENTAR AGORA (Quadrante A):
  ✅ F1 — Build + instalação da extensão
  ✅ F2 — Configuração do MCP bridge
  ✅ F3 — Integração Claude ↔ Burp
  ✅ F4 — Scanner web ativo

  Esforço: ~3 horas | ROI: +60% capacidade da skill

IMPLEMENTAR DEPOIS (Quadrante B):
  🔄 F5 — Intercepção interativa
  🔄 F6 — Tuning de detecção OWASP
  🔄 F7 — Integração pipeline Python

  Esforço: ~8 horas | ROI: +25% refinamento

DESCARTAR (Quadrante C/D):
  ❌ F9 — Docker headless (complexidade alta, ganho marginal)
  ❌ F10 — CI/CD pipeline (over-engineering para uso manual)
  ❌ F11 — Export de relatórios Burp (reporter.py já satisfaz)
```

---

## Próximos Passos Concretos

```bash
# 1. Clonar e compilar
git clone https://github.com/portswigger/mcp-server
cd mcp-server
./gradlew embedProxyJar

# 2. Carregar no Burp Suite
# Extensions → Add → Java → selecionar build/libs/mcp-server-all.jar

# 3. Verificar MCP tab no Burp
# Host: 127.0.0.1, Port: 9876

# 4. Adicionar ao check-deps.sh
# Verificar se Burp + MCP estão respondendo em 127.0.0.1:9876

# 5. Atualizar SKILL.md com nova capacidade: web-app-scanning
```

---

## Conclusão

O **PortSwigger MCP Server** entrega o maior benefício com o menor esforço para este projeto:

> **3 horas de setup** → **+60% de capacidade** (web app testing completo via Burp + Claude)

O único custo real não-técnico é o **Burp Suite Pro** (≈ $499/ano) para ter o scanner ativo completo. Com a versão Community, o ganho já é significativo para interceptação e análise manual assistida por IA.

**Veredicto Pareto: IMPLEMENTAR** — está claramente no Quadrante A.
