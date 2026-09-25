# Auditoria dos requisitos do MVP

Revisão do PDF `mvp back end.pdf`, páginas 1 a 6, e do projeto em 25/09/2026.

## Resultado

Os requisitos técnicos estão implementados. A entrega completa continua pendente do vídeo de até seis minutos e do envio dos links à instituição. Não é possível garantir nota: criatividade e apresentação dependem da avaliação docente. Os exemplos de código das aulas não foram disponibilizados, portanto não foi realizada uma comparação de similaridade com esse material.

## Arquitetura e organização

O núcleo segue o cenário 2: API principal, API secundária e API externa. A interface é um módulo adicional, agora separado em repositório e contêiner próprios. Há três componentes desenvolvidos e um externo. O Compose fica na raiz da API principal.

| Exigência | Evidência | Resultado |
| --- | --- | --- |
| Três ou mais módulos REST/GraphQL | Web → API → Analytics / Frankfurter | Atendido |
| Persistência SQLite/MySQL/PostgreSQL | SQLite com volume nomeado | Atendido |
| Python, quatro operações e Swagger na principal (2,0) | POST e GET /assinaturas; PUT e DELETE /assinaturas/{id}; /docs | Atendido |
| Interface consome GET, POST, PUT/PATCH, DELETE | app.js no repositório web | Atendido também na interface |
| README e imagem da arquitetura (1,0) | README.md e docs/arquitetura.png na principal | Atendido |
| Dockerfile por módulo e Compose na raiz (1,0) | Três Dockerfiles; compose.yaml na API principal | Atendido |
| Domínio distinto e extras (1,0) | Assinaturas digitais; filtros, paginação, projeção, economia e próximas cobranças | Implementado; criatividade sujeita à avaliação |
| Quatro rotas e Swagger na secundária (2,0) | POST /resumo, /categorias, /projecao, /economia; /docs | Atendido |
| README secundária (0,5) | Instalação local, Docker, exemplos e testes | Atendido |
| Dockerfile secundária (0,5) | Dockerfile na raiz, imagem executada | Atendido |
| API externa gratuita (0,5) | Frankfurter v2; consulta HTTP real pelo backend | Atendido |
| Cadastro, licença e endpoints externos (0,5) | README principal: sem chave/cadastro, MIT do software e termos dos dados | Atendido |
| Sem redirecionamento externo | Conversão no backend, resultado exibido no painel | Atendido |
| Repositório público por componente (1,0) | assinaradar-api, assinaradar-analytics, assinaradar-web | Três repositórios públicos publicados |
| Vídeo de até seis minutos | docs/roteiro-video.md | Pendente de gravação e publicação |

Os pontos indicam os pesos do enunciado, não uma nota atribuída ao trabalho.

## Correções e melhorias desta revisão

1. Separação da interface em seu próprio repositório e imagem Docker.
2. Proxy HTTP preserva o endereço http://localhost:8000/ e evita configuração de CORS no navegador.
3. Projeção visual acumulada com seleção de 3, 6, 12 ou 24 meses.
4. Destaque de próximas cobranças e datas passadas a revisar, sem afirmar que existe atraso de pagamento.
5. Atualizações concorrentes da lista são reagendadas; uma gravação não é silenciosamente ignorada enquanto o painel carrega.
6. Totais deixam de aparentar estar atualizados quando o carregamento falha; percentuais usam formato brasileiro.
7. Instruções de clonagem, arquitetura e roteiro revisados para três componentes próprios.

## Entrega

```text
Projeto: AssinaRadar
Interface: https://github.com/Yuri-N3/assinaradar-web
API principal: https://github.com/Yuri-N3/assinaradar-api
API secundária: https://github.com/Yuri-N3/assinaradar-analytics
API externa: https://frankfurter.dev/
Vídeo: inserir o link público após gravar (até 6 minutos)
```

A ausência do vídeo implica desconto de 2 pontos segundo o PDF. Duração acima do limite pode gerar desconto de até 1 ponto. Revise também se todos os cinco tópicos obrigatórios aparecem no vídeo.
