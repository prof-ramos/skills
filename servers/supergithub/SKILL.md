---
name: supergithub
description: >-
  Gerenciador avançado de repositórios GitHub via API REST. Use para: listar,
  arquivar, deletar, criar, atualizar repositórios e gerenciar topics. Suporta
  operações em lote. Ideal para automação de manutenção de repositórios,
  cleanup, padronização de topics e organização de projetos GitHub.
license: MIT
compatibility: Requer Python 3.7+, requests, e um GitHub Personal Access Token com permissões repo e delete_repo.
metadata:
  author: prof-ramos
  version: "1.0.0"
---

# SuperGitHub - GitHub Repository Manager

Ferramenta Python para gerenciar repositórios GitHub via API REST com operações avançadas em lote.

## Funcionalidades

- **Listar**: repositórios com filtros avançados
- **Arquivar/Desarquivar**: repositórios
- **Deletar**: repositórios (com confirmação de segurança)
- **Criar**: novos repositórios
- **Atualizar**: configurações (nome, descrição, visibilidade)
- **Topics**: gerenciar tags/categorias
- **Lote**: operações em múltiplos repositórios

## Pré-requisitos

```bash
# Verificar Python
python3 --version

# Instalar dependências
pip install requests
```

## Configuração

```bash
# Criar token em: https://github.com/settings/tokens
# Permissões: repo, delete_repo
export GH_TOKEN='ghp_seu_token_aqui'
```

## Uso via CLI

```bash
# Listar repositórios
python gh_cli.py list --details

# Arquivar repositório
python gh_cli.py archive usuario repo-name

# Deletar com confirmação
python gh_cli.py delete usuario repo-name --yes

# Atualizar descrição
python gh_cli.py update usuario repo-name --description "Nova descrição"

# Gerenciar topics
python gh_cli.py topics add usuario repo-name --topics "python,automation"
```

## Uso como Biblioteca

```python
from github_repo_manager import GitHubRepoManager

gh = GitHubRepoManager()  # Usa GH_TOKEN do ambiente

# Listar repos
repos = gh.list_repos(per_page=10)

# Arquivar
gh.archive_repo("usuario", "repo-antigo")

# Deletar (requer confirm=True)
gh.delete_repo("usuario", "repo-teste", confirm=True)
```

## Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `gh_cli.py` | CLI interativo completo |
| `github_repo_manager.py` | Biblioteca Python core |
| `workflow_organizer.py` | Automação de organização |
| `setup.sh` | Script de instalação |

Consulte [README.md](./README.md) para documentação completa.
