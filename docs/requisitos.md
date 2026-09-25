# Requisitos do MVP

Referência: enunciado `mvp back end.pdf`, seis páginas. Arquitetura escolhida: cenário 2.

| Critério | Implementação / evidência | Situação |
| --- | --- | --- |
| Três módulos que se comunicam | API principal → API de análise e Frankfurter | Implementado |
| Persistência SQLite/MySQL/PostgreSQL | SQLite, arquivo configurável e volume Docker | Implementado |
| API principal Python + Swagger | FastAPI, `/docs` | Implementado |
| GET, POST, PUT/PATCH, DELETE | CRUD de `/assinaturas` | Implementado |
| README da principal | Instalação, rotas, regras, configuração e estrutura | Preparado |
| Imagem do fluxograma | `docs/arquitetura.png` | Preparado |
| Dockerfile principal | Dockerfile na raiz, usuário sem privilégios | Preparado; executar no Docker |
| Compose na raiz da principal | `compose.yaml` | Preparado; executar no Docker |
| Domínio e funcionalidades adicionais | Assinaturas digitais, filtros, paginação, projeção e economia | Implementado |
| Secundária com quatro rotas e Swagger | POST `/resumo`, `/categorias`, `/projecao`, `/economia` | Implementado |
| README secundária | Instalação local, Docker, contrato e testes | Preparado |
| Dockerfile secundária | Dockerfile na raiz do componente | Preparado; executar no Docker |
| API externa pública gratuita | Frankfurter v2 | Implementado |
| Documentar cadastro, licença e rotas externas | Seção API externa no README principal | Preparado |
| Consumir e tratar resposta sem redirecionar | `app/services.py` | Implementado |
| Repositórios públicos separados | Pastas independentes para publicação | Pendente de publicação |
| Organização e convenções | Módulos Python, testes e documentação separados | Implementado |
| Vídeo até seis minutos | `docs/roteiro-video.md` | Roteiro pronto; gravação pendente |

O recorte de assinaturas diferencia o produto de um painel genérico de ativos financeiros. A avaliação de criatividade é da instituição; a existência de funcionalidades extras não garante uma pontuação específica.

## Publicação dos componentes

Crie dois repositórios públicos vazios, `assinaradar-api` e `assinaradar-analytics`. Envie o conteúdo de cada pasta para seu respectivo repositório, mantendo Dockerfile e README na raiz. Não envie a pasta de entrega como um único repositório.

Exemplo para a API principal, após criar o repositório na sua conta e substituir `SEU_USUARIO`:

```powershell
cd assinaradar-api
git init
git add .
git commit -m "Implementa controle de assinaturas"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/assinaradar-api.git
git push -u origin main
```

Repita na outra pasta com a URL do repositório `assinaradar-analytics`. Os comandos são instruções para a etapa de publicação; os repositórios remotos não foram criados por este pacote.

## Mensagem de entrega

Substitua todos os campos antes de enviar:

```text
Olá, seguem os dados do MVP AssinaRadar:
Vídeo: [URL completa do vídeo]
Componente principal: https://github.com/SEU_USUARIO/assinaradar-api
Componente secundário: https://github.com/SEU_USUARIO/assinaradar-analytics
API externa: https://frankfurter.dev/
```
