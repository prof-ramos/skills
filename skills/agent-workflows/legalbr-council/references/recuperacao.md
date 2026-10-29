# Recuperação local e rastreabilidade

O helper lê apenas o frontmatter de todos os arquivos em `forma/` e `materia/`; usa `name`, `title`, `triggers`, `description` e `materia`. O TSV é conferido quanto à cobertura e paridade dos campos indexados. Descrição e gatilhos, ausentes no TSV atual, vêm sempre do arquivo. Índice ausente, inválido ou defasado aciona o mesmo percurso local; nada é regenerado automaticamente. O helper não é um índice vetorial e não procura sinônimos implícitos.

Prioridade: termos no nome/título/gatilhos, depois descrição/área. Empates são estáveis por caminho. Se nenhum cabeçalho corresponder, pesquisar corpos em disco, mantendo o mesmo limite na saída. Metadados não suportados são excluídos e os caminhos aparecem em `skipped_paths`: uma lista não vazia deve ser investigada, não tratada como catálogo completo. O parser admite escalares e listas simples utilizados no catálogo, não YAML arbitrário. Não carrega arquivos via links que saiam do catálogo.

`--form` exige o slug real; um slug inexistente retorna erro. Omissão da forma não implica que o helper reconheça automaticamente o tipo documental. O agente deve escolher a forma a partir do objetivo ou declarar que não encontrou. Não adivinhar caminhos: consultar o catálogo. `--area` é filtro exato; removê-lo para teses conexas de outros ramos. Não tratar a ordem como força jurídica.

Cada resultado registra caminho relativo canônico, nome, UUID/versão disponíveis, hash do texto lido e origem do match. Sem `--include-content`, ler os arquivos selecionados antes de citar seu conteúdo. Com essa opção, o texto integral limita-se à seleção. Todos os registros dizem `legal_verification: not performed`: isso nunca muda em função do score, data ou domínio de URL.

Termos de pesquisa não são repetidos na saída, mas palavras correspondentes podem aparecer em `matched_terms`. Use exclusivamente vocabulário jurídico genérico. O helper não grava logs, não envia rede e não lê documentos de clientes. A shell ou o runtime ainda podem registrar argumentos/stdin; a minimização precede o comando. Não passar dados sigilosos mesmo por stdin.

Arquivo instalado isoladamente pode não ter o acervo. Informar o caminho de um checkout existente e autorizado. Sem Python, usar busca local por metadados (`rg`/leitura de índice) e ler apenas a shortlist, registrando manualmente origem. Sem acervo nem rede, trabalhar somente com arquivos fornecidos e registrar a limitação. Nenhum fallback baixa dados privados ou instala dependências.
