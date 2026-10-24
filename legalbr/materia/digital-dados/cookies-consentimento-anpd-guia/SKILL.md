---
id: "fb5a1a4b-3813-4928-96a0-7961ebcadac4"
name: "cookies-consentimento-anpd-guia"
title: "Cookies + Consentimento (ANPD Guia 2022 + LGPD)"
category: "materia"
materia: "digital-dados"
documentType: null
version: 2
sourcePath: "legalbr/materia/digital-dados/cookies-consentimento-anpd-guia/SKILL.md"
triggers:
  - "cookies LGPD"
  - "guia ANPD cookies"
  - "consentimento cookies"
  - "banner cookies"
  - "cookie wall"
  - "rastreador online"
  - "dark patterns"
  - "LGPD legítimo interesse cookies"
  - "identificadores online"
description: "Usar para pesquisar ou analisar: Cookies + Consentimento (ANPD Guia 2022 + LGPD). Combinar com o protocolo LegalBR e conferir fontes oficiais antes de aplicar."
verifiedAt: null
status: "a conferir"
sources: []
---

# Cookies + Consentimento

Antes de usar, ler o [protocolo LegalBR](../../../SKILL.md). Este arquivo não foi integralmente verificado; confirmar fundamentos em fontes oficiais.

## Verificação operacional de cookies e evidências

Adição de 22/10/2026; organização de compliance adaptada conforme
[proveniência](references/PROVENIENCIA.md), Apache-2.0.

**Escopo:** URL/domínios, ambiente, páginas/fluxos, data, navegador, região,
login e versão do banner/CMP/política. Não alegue auditoria técnica se só recebeu
texto ou captura. Sem acesso ao site ou logs, entregue roteiro e marque o
funcionamento como **desconhecido**. Não publique política nem altere CMP/site.

### Inventário observado, não lista genérica de fornecedores

| Nome/identificador | Domínio e fornecedor | Tipo (cookie/pixel/SDK/storage) | Finalidade e dados | Destinatários/países | Duração observada | Base proposta e justificativa | Evidência/data | Responsável |
|---|---|---|---|---|---|---|---|---|
| [realmente observado ou informado, distinguindo ambos] | [ou desconhecido] | [tipo] | [ou a confirmar] | [ou desconhecidos] | [sessão/expiração ou não verificada] | [por operação, sujeita à análise] | [rede/storage/configuração/log com origem] | [confirmado ou a designar] |

Inclua rastreadores server-side e integrações apenas quando houver evidência;
ausência no navegador não prova ausência no servidor. Redija a política a partir
do inventário validado; não invente Google/Meta, prazos, países ou controlador.
Oculte dados pessoais nos registros de teste antes de compartilhar evidências.

### Teste reproduzível do banner

Em ambiente autorizado, sem alterar produção, registre requisições e armazenamento
em sessão limpa e após recarregar/navegar em cada cenário:
1. Primeira visita, antes de qualquer escolha.
2. Rejeitar não necessários.
3. Aceitar somente uma categoria (verificar as demais).
4. Aceitar todos.
5. Reabrir preferências e revogar; verificar o comportamento posterior.

Confronte execução observada, escolhas registradas e inventário. Teste se
rastreadores **baseados em consentimento** ficam inativos antes do aceite e após
recusa/revogação; um botão visualmente correto não prova bloqueio efetivo.
Verifique opções acessíveis, rejeição e gerenciamento sem destaque manipulativo,
finalidades claras, granularidade, link da política, registro da escolha e meio
simples de alterá-la. Registre também falhas, rotas não testadas e limitações.

### Conclusão e plano de ação

| Requisito/fonte | Evidência e cenário | Status | Risco | Ação | Responsável/prazo | Reteste |
|---|---|---|---|---|---|---|
| [lei, recomendação ANPD ou critério interno] | [observada ou ausente] | [atendido / não atendido / desconhecido / não aplicável com motivo] | [fundamentado] | [correção/prova] | [confirmados ou a definir] | [pendente/evidência] |

Sem teste de execução, bloqueio permanece desconhecido; sem inventário, não
conclua adequação da política. Achado crítico ou lacuna material exige revisão
jurídica/técnica, não "site conforme". Sugestão de correção não é implementação.

### Calibração jurídica obrigatória

Leia o restante como material de referência, não como regra automática. A base
legal depende da operação concreta; nem todo cookie de terceiro exige, só por
ser de terceiro, consentimento. Não trate legítimo interesse como dispensa de
análise. **LGPD arts. 7º–10** e **Guia ANPD, pp. 17–26** orientam essa avaliação.
O guia é orientativo; recomendações de interface (pp. 29–33) não devem ser
apresentadas como lei autônoma que fixa dimensões exatas de botões. Referências
estrangeiras dependem de incidência própria e não são lei brasileira.

Fontes oficiais consultadas em 22/10/2026; revalidar no caso:
- [LGPD, texto compilado](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm).
- [ANPD — Guia de cookies](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf).

Não presuma adequação internacional, prazos de incidentes, regras para crianças
ou sanções a partir de sínteses abaixo: verifique norma oficial vigente e escopo.
A revisão deste fluxo não constitui validação integral das demais teses do acervo.

## Marco legal

- **LGPD** (Lei 13.709/2018);
- **Guia Orientativo ANPD "Cookies e Proteção de Dados Pessoais"** (18/10/2022);
- **GDPR + ePrivacy Directive (UE)**: referência;
- **EDPB Guidelines**: boas práticas;
- **Marco Civil da Internet** (Lei 12.965);
- **CDC** (relação de consumo);
- **Resoluções ANPD** específicas.

## Conceito de cookie

| | Conteúdo |
|---|---|
| **Cookie** | Pequeno arquivo de texto armazenado no dispositivo do usuário |
| **Função** | Identificar + memorizar preferências + rastrear |
| **Dado pessoal?** | **Frequentemente sim**: quando associado a identificador único |
| **Identificadores online** (LGPD 5 I) | Dado pessoal |
| **Trackers + pixels** | Equiparam-se |

## Classificação por finalidade

| Categoria | Conteúdo | Base legal típica |
|---|---|---|
| **Estritamente necessários** | Imprescindíveis ao funcionamento (login, carrinho, segurança) | Execução de contrato + legítimo interesse |
| **Funcionalidade** | Memorizar preferências (idioma, configurações) | Consentimento ou legítimo interesse |
| **Analítico/desempenho** | Estatísticas de uso | Análise contextual de consentimento ou legítimo interesse; anonimização não se presume |
| **Publicidade/marketing** | Direcionamento + remarketing | **Consentimento** (regra) |
| **Terceiros** | Cookies de provedores externos | Base por finalidade/operação + transparência |

## Classificação por duração

| | Conteúdo |
|---|---|
| **Sessão** | Apagados ao fechar navegador |
| **Persistentes** | Permanecem por período definido |
| **First-party** | Do próprio site |
| **Third-party** | De terceiros (analytics + adtech) |

## Bases legais (LGPD 7)

| Base | Aplicação a cookies |
|---|---|
| **Consentimento** (I) | Avaliar por finalidade; obter antes do tratamento que depender desta base |
| **Cumprimento de obrigação legal** (II) | Casos específicos |
| **Execução de contrato** (V) | Cookies essenciais ao serviço |
| **Legítimo interesse** (IX) | Estritamente necessários + alguns funcionais (após balancing test) |
| **Exercício regular de direitos** (VI) | Limitado |

## Princípio do consentimento (LGPD 8)

| | Conteúdo |
|---|---|
| **Livre** | Sem pressão |
| **Informado** | Política clara |
| **Inequívoco** | Manifestação positiva |
| **Específico** | Por finalidade |
| **Revogável** | A qualquer tempo |
| **Granular** | Por categoria de cookie |
| **Documentado** | Provas de consentimento |

## Banner de cookies: boas práticas ANPD

### Estrutura recomendada

| | Conteúdo |
|---|---|
| **Primeira camada** | Aviso conciso + 3 botões equivalentes |
| **Segunda camada** | Detalhamento + opções granulares |
| **Botões** | "Aceitar todos" + "Recusar todos" + "Gerenciar/Personalizar", sem destaque manipulativo ao aceite |
| **Padrão** | Cookies baseados em consentimento **NÃO** habilitados por padrão |
| **Política de cookies** | Link claro |
| **Linguagem** | Portuguesa + clara |

### O que evitar (dark patterns)

| | Conteúdo |
|---|---|
| **Botão "Aceitar" maior** | Desigualdade visual |
| **Sem opção "Recusar"** na primeira camada | Contraria recomendação do Guia ANPD |
| **Cookies baseados em consentimento habilitados** por padrão | Incompatível com essa base |
| **Cookie walls** sem alternativa real | Coerção |
| **Informação em idioma estrangeiro** apenas | Inadequado |
| **Granularidade excessiva** confusa | Manipulação |
| **Cookies baseados em consentimento antes de consentir** | Incompatível com essa base |
| **Mudança de preferências difícil** | Vedado |

## Cookie walls

| | Conteúdo |
|---|---|
| **Conceito** | "Aceite cookies ou não acesse" |
| **EDPB (UE)** | Vedados em geral (consentimento não-livre) |
| **ANPD** | Vedados quando único acesso a serviços essenciais |
| **Permissível** | Em conteúdo premium opcional com alternativa real |

## Política de cookies (conteúdo)

| | Conteúdo |
|---|---|
| **Tipos** de cookies usados | Listagem |
| **Finalidades** | Por categoria |
| **Duração** | Sessão / persistente / quanto tempo |
| **Terceiros** | Quem recebe (Google, Meta, etc.) |
| **Transferências internacionais** | Indicar |
| **Direitos do titular** | LGPD 18 |
| **Como gerenciar** | Browser + ferramentas |
| **Contato encarregado** | Comunicação |

## DPIA + rastreamento

| | Conteúdo |
|---|---|
| **Recomendado** | Em rastreamento massivo + perfilamento |
| **Crianças** | Cuidado especial (LGPD 14) |
| **Decisão automatizada** | Análise específica (LGPD 20) |
| **Direitos do titular** | Garantidos |

## Vendor + adtech

| | Conteúdo |
|---|---|
| **Google Analytics** | Caso UE: GA4 sob escrutínio (transferência EUA) |
| **Meta Pixel** | Análise para perfilamento |
| **DPA com cada fornecedor** | Necessário |
| **CMP** (Consent Management Platform) | Recomendada |
| **TCF IAB** | Padrão internacional |

## Transferência internacional

| | Conteúdo |
|---|---|
| **LGPD art. 33** | Bases legais para transferência |
| **País adequado** | ANPD avalia |
| **Cláusulas contratuais** | Padronizadas |
| **Consentimento específico** | Para transferência |
| **EUA** | Sem decisão de adequação (atenção) |
| **UE** | Reconhecida como **adequada** (Res. CD/ANPD 32/2026, adequação recíproca Brasil-UE): fluxo livre |

## Sanções por descumprimento

| | Conteúdo |
|---|---|
| **ANPD multa** | Até R$ 50M ou 2% receita |
| **Advertência** | Com prazo |
| **Publicização** | Da infração |
| **Bloqueio** | De dados |
| **CDC** | Aplicação concomitante |
| **Cível** | Dano material + moral |

## Direitos do titular (LGPD 18)

| | Conteúdo |
|---|---|
| **Acesso** aos dados | Direito |
| **Correção** | Direito |
| **Exclusão** | Direito |
| **Portabilidade** | Direito |
| **Informação** | Direito |
| **Revogação** | Direito |
| **Não consentimento** | Direito |
| **Decisão automatizada** | Direito a revisão |

## Direitos x cookies

| | Conteúdo |
|---|---|
| **Acesso** | Quais cookies armazenados + finalidades |
| **Exclusão** | Pode pedir + browser oferece |
| **Revogação** | Cookies não-necessários removidos |
| **Portabilidade** | Limitada |

## Crianças + adolescentes (LGPD 14)

| | Conteúdo |
|---|---|
| **Consentimento específico** | Pelos pais/responsáveis |
| **Best interest** | Critério |
| **Verificação de idade** | Recomendada |
| **Marketing direcionado** | Limitado |
| **ECA** | Aplicação concomitante |

## Mobile + apps

| | Conteúdo |
|---|---|
| **Identificadores móveis** (IDFA, GAID) | Equiparam-se a cookies |
| **App tracking** | Consentimento |
| **iOS ATT** (App Tracking Transparency) | Modelo |
| **Android** | Privacy Sandbox |
| **SDKs** | Configuração + consentimento |

## CMP: Consent Management Platform

| | Conteúdo |
|---|---|
| **Funções** | Banner + registro + gestão |
| **Exemplos** | OneTrust, Cookiebot, AdOpt, GoAdopt |
| **Logs** | Auditoria |
| **TCF IAB** | Compatibilidade |
| **Customização** | Por jurisdição |

## Aspectos práticos para sites brasileiros

| | Conteúdo |
|---|---|
| **Inicial** | Verifique cookies em uso |
| **Mapeamento** | Lista + propósito |
| **Política** | Atualizada |
| **CMP** | Implementada |
| **Documentação** | Logs de consentimento |
| **Revisão** | Periódica |

## Comparativo internacional

| | Conteúdo |
|---|---|
| **UE: ePrivacy + GDPR** | Mais rígido |
| **EUA: CCPA + state laws** | Opt-out predominante |
| **Brasil: LGPD + ANPD** | Híbrido |
| **Reino Unido: ICO** | Pós-Brexit alinhado UE |
| **Argentina** | Lei própria |

## Tendências 2024-2026

| | Conteúdo |
|---|---|
| **Cookieless future** | Browsers eliminando 3rd party |
| **Privacy Sandbox (Chrome)** | Em implementação |
| **Server-side tracking** | Resposta técnica |
| **Identidade universal** | Substitutos |
| **Reforço ANPD** | Fiscalização |
| **DSA UE** | Influência |

## Erros a evitar

- Habilitar **cookies baseados em consentimento** antes de obtê-lo;
- **Cookie wall** sem alternativa real (consentimento não-livre);
- Botão "Aceitar" **maior** que "Recusar" (dark pattern);
- Não oferecer **"Recusar"** na primeira camada;
- Não permitir **revogação** simples + acessível;
- Aplicar **legítimo interesse** para **publicidade** sem análise;
- Esquecer **CMP** + documentação dos consentimentos;
- Não atualizar **política** de cookies + lista usados;
- Tratar identificadores móveis como **não-cookies** (equiparam-se);
- Esquecer **DPIA** em rastreamento massivo;
- Aplicar consentimento **genérico** para todas categorias (deve ser granular);
- Ignorar **direitos do titular** (LGPD 18) por gestão complicada de cookies.
