# Demonstração no Swagger

Inicie os dois componentes. Em cada operação do Swagger, use **Try it out**, preencha os campos e clique em **Execute**. Anote os IDs devolvidos; não presuma que começam em 1 se já houver dados no banco.

## API secundária — porta 8001

Use o corpo abaixo em `/resumo` e `/categorias`:

```json
{
  "itens": [
    {"id": 1, "categoria": "produtividade", "valor_centavos_brl": 3000, "periodicidade": "mensal"},
    {"id": 2, "categoria": "lazer", "valor_centavos_brl": 12000, "periodicidade": "anual"}
  ]
}
```

- `/resumo`: mensal `40.00`, anual `480.00`.
- `/categorias`: produtividade `30.00` e 75%; lazer `10.00` e 25%.
- `/projecao`: acrescente `"meses": 6` ao objeto, no mesmo nível de `itens`; total `240.00`.
- `/economia`: acrescente `"excluir_ids": [1]`; economia mensal `30.00`, anual `360.00`, novo mensal `10.00`.

Os IDs deste exemplo são locais ao corpo enviado; a secundária não consulta os cadastros da API principal.

## API principal — porta 8000

### 1. Criar

Execute POST `/assinaturas`:

```json
{
  "nome": "Nuvem pessoal",
  "categoria": "Produtividade",
  "valor": "30.00",
  "moeda": "BRL",
  "periodicidade": "mensal",
  "proxima_cobranca": "2026-10-10",
  "ativo": true
}
```

Crie outra assinatura com nome `Editor de código`, valor `10.00`, moeda `USD` e categoria `Trabalho`. Observe o retorno 201 e guarde os IDs. As datas são exemplos e podem ser ajustadas para a demonstração.

### 2. Listar

Execute GET `/assinaturas` sem filtros. Depois experimente `categoria=produtividade`, `ativo=true`, `ordem=nome` e `limite=1`. Mostre `total`, `offset` e `itens`.

### 3. Atualizar

Execute PUT `/assinaturas/{assinatura_id}` com o ID de `Nuvem pessoal`, enviando todos os campos do cadastro e trocando o valor para `35.00`. Observe o retorno 200.

### 4. Consultar a API externa

Execute GET `/cotacoes/{moeda}` com `USD`. Mostre `taxa`, `data`, `fonte` e explique que a cotação não inclui encargos do cartão.

### 5. Analisar

Execute GET `/analises/{tipo}` para cada tipo:

- `resumo`: confira total em reais e as cotações utilizadas.
- `categorias`: veja a distribuição dos custos.
- `projecao`: informe `meses=6`.
- `economia`: em `excluir_ids`, use **Add item** e informe o ID de `Nuvem pessoal`. A economia mensal esperada dessa assinatura é `35.00`.

Deixe `excluir_ids` vazio nas outras análises. O valor total com USD depende da cotação disponível. Só assinaturas ativas entram no cálculo.

### 6. Excluir

Execute DELETE `/assinaturas/{assinatura_id}` com o ID criado para a demonstração. O retorno é 204 sem corpo. Execute GET novamente para confirmar. Evite excluir registros que queira manter.

## Verificações adicionais

- Valor negativo no POST: retorno 422 e nenhum registro novo.
- PUT com `ativo=false`: registro permanece no histórico, mas sai das análises.
- Reinicie os serviços sem remover o volume: os cadastros permanecem.
- Com analytics parado, o CRUD continua funcionando e `/analises/resumo` retorna 502.
- A API externa pode estar indisponível; nesse caso, mostre o erro e tente novamente depois. Não apresente uma cotação fictícia como real.
