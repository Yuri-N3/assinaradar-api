# Roteiro do vídeo — 5 minutos e 50 segundos

Antes de gravar, execute `docker compose up --build -d`, aguarde os serviços ficarem saudáveis e abra os dois Swaggers. Deixe os exemplos de JSON preparados. Use dados de demonstração e anote os IDs retornados.

| Tempo | Conteúdo | Ação na tela |
| --- | --- | --- |
| 0:00–0:40 | Objetivo: controlar gastos com serviços digitais e simular economia | Mostrar título e explicar um caso de uso |
| 0:40–1:30 | Arquitetura: cadastro, análise, SQLite e serviço externo | Mostrar `arquitetura.png` e indicar os fluxos HTTP |
| 1:30–2:20 | Frankfurter: consulta pública, sem chave, taxa e data; conversão tratada na aplicação | Mostrar seção API externa do README e GET `/cotacoes/USD` |
| 2:20–3:50 | API secundária em Docker: demonstrar todas as quatro operações | Mostrar `docker compose ps`; executar resumo, categorias, projeção e economia no Swagger 8001 |
| 3:50–5:20 | API principal em Docker: demonstrar CRUD e análise integrada | Executar POST, GET, PUT, análise e DELETE no Swagger 8000; a cotação já foi demonstrada |
| 5:20–5:50 | Fechar a demonstração de análises e mostrar os repositórios | Alternar os demais tipos de análise, apontar READMEs e Dockerfiles |

Na versão atual existem três componentes próprios. Mostre no fluxograma que o front-end tem contêiner/repositório próprio e encaminha as chamadas à API principal. No bloco final, demonstre rapidamente o painel, a projeção e a simulação; mantenha a demonstração de todas as rotas das duas APIs no Swagger. O vídeo deve continuar abaixo de seis minutos.

## Pontos para explicar com suas palavras

- O problema é a dificuldade de enxergar o custo combinado de várias assinaturas, especialmente quando algumas são anuais ou cobradas em outra moeda.
- O banco pertence à API principal; o componente de análise é independente e recebe somente os dados necessários ao cálculo.
- Os preços anuais são rateados em 12 meses. A projeção é uma estimativa a preços constantes, não um calendário de pagamentos.
- A simulação não cancela contratos. Ela calcula o impacto de remover determinados itens.
- Cotações têm data de referência e podem diferir do câmbio efetivo de um cartão.
- O volume Docker mantém os dados após reiniciar os contêineres.

Ensaie antes da gravação para caber no limite. Não inclua o tempo de download e construção das imagens. Confira o áudio e o acesso aos links do vídeo e dos três repositórios antes de entregar.
