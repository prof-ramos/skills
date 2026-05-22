# Guia de Ética e Conformidade Legal

> **Esta SKILL é destinada exclusivamente para testes de segurança autorizados em ambientes controlados.**

## 1. Princípios Fundamentais

### 1.1 Autorização Prévia (Authorization First)

Nunca execute qualquer teste sem autorização **escrita e documentada** do proprietário legal do sistema.
A autorização deve especificar:

- **Escopo:** Quais sistemas, IPs, domínios estão autorizados
- **Janela temporal:** Datas e horários permitidos
- **Profundidade:** Quais tipos de teste são permitidos
- **Ponto de contato:** Pessoa responsável do lado do cliente
- **Procedimento de emergência:** Como agir se causar impacto inadvertido

### 1.2 Rules of Engagement (RoE)

Documente formalmente antes de iniciar:

```markdown
## Rules of Engagement — [Nome do Projeto]

**Cliente:** ___________________________
**Testador:** __________________________
**Período:** De ___ / ___ / ___ até ___ / ___ / ___
**Escopo autorizado:**
  - IPs/Ranges: ________________________
  - Domínios: _________________________
  - Aplicações: _______________________
**Escopo PROIBIDO:**
  - _________________________________
**Tipos de teste autorizados:** [ ] Passivo  [ ] Ativo  [ ] Exploração
**Contato de emergência:** _____________
**Assinatura do cliente:** _____________
```

### 1.3 Princípio do Mínimo Dano

- Prefira **reconhecimento passivo** sempre que possível
- Evite testes que possam **derrubar serviços** (DoS não autorizado)
- Documente **cada ação** para auditoria posterior
- **Pare imediatamente** se detectar impacto não previsto

---

## 2. Marco Legal Brasileiro

### Lei 12.737/2012 (Lei Carolina Dieckmann)
Tipifica crimes informáticos. Acesso não autorizado a sistemas é crime com pena de **detenção de 3 meses a 1 ano**.

### Marco Civil da Internet (Lei 12.965/2014)
Define direitos e deveres no uso da internet. Pentest sem autorização viola os artigos de proteção à privacidade.

### LGPD (Lei 13.709/2018)
Durante testes, dados pessoais encontrados devem ser protegidos e reportados, não armazenados.

### Código Penal — Art. 154-A
*"Invadir dispositivo informático alheio, conectado ou não à rede de computadores, mediante violação indevida de mecanismo de segurança..."*
Pena: **reclusão de 1 a 4 anos**, e multa.

---

## 3. Legislação Internacional Relevante

| País | Lei | Pena Máxima |
|------|-----|-------------|
| EUA | CFAA (Computer Fraud and Abuse Act) | 10-20 anos de prisão |
| Reino Unido | Computer Misuse Act 1990 | 10 anos |
| União Europeia | Directive 2013/40/EU | Harmonização entre países |
| Austrália | Criminal Code Act 1995 | 10 anos |

---

## 4. Boas Práticas Operacionais

### 4.1 Antes do Teste
- [ ] Contrato assinado com escopo detalhado
- [ ] NDA (Non-Disclosure Agreement) em vigor
- [ ] Comunicação com equipe interna de segurança do cliente
- [ ] Backup do ambiente de teste (se aplicável)

### 4.2 Durante o Teste
- [ ] Logs de todas as ações habilitados
- [ ] Janelas de teste respeitadas
- [ ] Comunicação imediata de achados críticos ao cliente
- [ ] Nenhum dado exfiltrado para fora do escopo

### 4.3 Após o Teste
- [ ] Relatório entregue apenas ao cliente autorizado
- [ ] Dados coletados descartados conforme acordo
- [ ] Sessão de debriefing com o cliente
- [ ] Acompanhamento das correções (se contratado)

---

## 5. Programas de Bug Bounty

Ao participar de programas de Bug Bounty (HackerOne, Bugcrowd, etc.):

1. **Leia o escopo completo** antes de iniciar qualquer teste
2. **Respeite os limites de taxa** (rate limiting) definidos pelo programa
3. **Reporte responsavelmente:** Nunca divulgue publicamente antes do prazo acordado
4. **Não acesse dados reais de usuários**, mesmo que encontre a vulnerabilidade
5. **Documente com evidências mínimas suficientes** — não colete mais do que o necessário

### Plataformas Reconhecidas
- [HackerOne](https://hackerone.com)
- [Bugcrowd](https://bugcrowd.com)
- [Intigriti](https://intigriti.com)
- [Open Bug Bounty](https://openbugbounty.org)
- [Programa de Bug Bounty do Governo Federal Brasileiro](https://www.gov.br/seguranca)

---

## 6. Certificações Recomendadas

| Certificação | Emissor | Foco |
|---|---|---|
| OSCP | Offensive Security | Pentest Prático |
| CEH | EC-Council | Hacking Ético |
| eJPT | eLearnSecurity | Junior Pentest |
| BSCP | PortSwigger | Web Security |
| GPEN | GIAC | Pentest Avançado |

---

*Última atualização: 2025 | Ethical Red Team Skill v1.0.0*
