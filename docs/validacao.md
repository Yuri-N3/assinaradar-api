# Validação

Verificação realizada em 24/09/2026 com Python 3.12 no Windows.

## Executado

- **16 testes da API principal aprovados**: CRUD, filtros, paginação, persistência entre inicializações, validação, integração controlada de câmbio, erros de serviço e Swagger.
- **9 testes da API secundária aprovados**: cálculos, agrupamento, projeção, economia, carteira vazia, arredondamento e validação.
- **Comunicação HTTP real entre dois processos**: cadastro, leitura, alteração, exclusão e as quatro análises passaram.
- **Consulta externa real**: GET de USD para BRL na Frankfurter passou, com taxa e data devolvidas pela API principal.
- **Fluxo completo com moeda estrangeira**: cadastro em USD, conversão e análise pelo serviço secundário passaram.

Os testes automatizados de integração usam respostas controladas para serem reproduzíveis. A verificação com a API pública foi adicional; cotações futuras podem mudar e a disponibilidade do provedor é externa ao projeto.

O ambiente emitiu um aviso de descontinuação no cliente HTTP de testes do Starlette. Não houve falha; o aviso se refere à futura migração do cliente de testes, não a uma operação do AssinaRadar.

## Validação Docker em 25/09/2026

- Imagens construídas com Docker Desktop 29.8.0 e iniciadas com `docker compose up --build -d --wait`; ambos os serviços ficaram saudáveis.
- Verificados por HTTP: Swagger/OpenAPI, CRUD, quatro análises integradas, quatro rotas da secundária e cotação externa real. Persistência confirmada após `docker compose restart api`. Registros de teste removidos ao final.
- Publicação concluída: https://github.com/Yuri-N3/assinaradar-api e https://github.com/Yuri-N3/assinaradar-analytics.
- Gravar, revisar e publicar o vídeo de até seis minutos.

## Limites do MVP

Aplicação local, de usuário único e sem autenticação. Cancelamentos não são enviados a fornecedores. Não há pagamentos reais, atualização automática da próxima cobrança, previsão de impostos ou câmbio de cartão. A simulação usa os preços cadastrados e as cotações de referência disponíveis no momento da consulta.

## Interface visual — 25/09/2026

Verificados no navegador: carregamento do painel, cadastro pelo formulário, atualização dos totais, edição de valor e simulação de economia. Os dados de teste foram removidos após a verificação.

## Auditoria e separação dos componentes — 25/09/2026

25 testes automatizados aprovados (16 da principal e 9 da secundária). Três contêineres saudáveis. Verificação HTTP pelo proxy Nginx aprovada: Swagger, CRUD, quatro análises, cotação real e persistência após reinício. Projeção visual de seis meses verificada no navegador. Os registros pré-existentes foram preservados; somente registros criados pela verificação foram excluídos. Front-end publicado em https://github.com/Yuri-N3/assinaradar-web.
