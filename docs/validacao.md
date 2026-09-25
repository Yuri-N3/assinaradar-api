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

## Pendente no ambiente de entrega

- Construir e executar as imagens com Docker. O executável Docker não estava disponível no ambiente de desenvolvimento; não se afirma que os contêineres foram testados.
- Conferir `docker compose ps`, interagir com as rotas nos dois Swaggers e verificar a persistência após reiniciar os contêineres.
- Publicar os componentes em dois repositórios públicos separados.
- Gravar, revisar e publicar o vídeo de até seis minutos.

## Limites do MVP

Aplicação local, de usuário único e sem autenticação. Cancelamentos não são enviados a fornecedores. Não há pagamentos reais, atualização automática da próxima cobrança, previsão de impostos ou câmbio de cartão. A simulação usa os preços cadastrados e as cotações de referência disponíveis no momento da consulta.
