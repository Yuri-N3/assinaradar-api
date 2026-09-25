# Validação

Verificações realizadas em 24 e 25/09/2026, com Python 3.12, Windows e Docker Engine 29.8.0.

## Testes automatizados

Foram aprovados 25 testes:

- **API principal — 16 testes:** cadastro, consulta, edição, exclusão, filtros, paginação, persistência, validação de entradas, integração de câmbio, tratamento de falhas e Swagger.
- **API de análise — 9 testes:** resumo, categorias, projeção, economia, carteira vazia, arredondamento e validação.

Os testes usam bancos temporários e respostas externas controladas. O cliente de testes do Starlette emitiu um aviso de descontinuação, sem falhas na execução.

## Integração e Docker

Os três serviços foram construídos e iniciados com `docker compose up --build -d --wait`. Todos passaram nas verificações de saúde.

Foram verificados por HTTP, através do proxy Nginx:

- Documentação Swagger e esquema OpenAPI.
- Cadastro, consulta, edição e exclusão de assinaturas.
- As quatro operações da API de análise.
- Cotação real de USD para BRL e análise de uma assinatura em dólar.
- Persistência no SQLite após `docker compose restart api`.

A consulta externa foi testada separadamente dos testes automatizados. Sua disponibilidade e os valores das cotações dependem do provedor.

## Interface

Foram conferidos no navegador o formulário de cadastro, a edição de valores, a atualização dos totais, a simulação de economia e o gráfico de projeção de seis meses. Os registros usados nos testes foram removidos; os cadastros existentes foram preservados.

## Repositórios

- Interface: https://github.com/Yuri-N3/assinaradar-web
- API principal: https://github.com/Yuri-N3/assinaradar-api
- API de análise: https://github.com/Yuri-N3/assinaradar-analytics

## Limites e entrega

O sistema é local, de usuário único e sem autenticação. Não realiza pagamentos nem cancela contratos com fornecedores. A próxima cobrança precisa ser atualizada no cadastro. As projeções mantêm os preços e o câmbio constantes, sem impostos ou reajustes.

A gravação e a publicação do vídeo de até seis minutos continuam pendentes.
