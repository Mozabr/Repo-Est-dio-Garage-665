# Estúdio canônico v10 — consistência externa e interna

## Decisão visual congelada

A master `teste 05` é a autoridade visual do ambiente. A geometria operacional
é a do Studio G: teto contínuo off-white, sem painel luminoso retangular
aparente. O Studio H e o teto com grande difusor visível permanecem no histórico,
mas estão reprovados para a série multivista.

Autoridade portátil no repositório:
`referencias/autoridades/panamera-master-estudio-canonico-v01.png`.

## Hierarquia de autoridade

1. A fotografia original de cada ângulo controla carro, câmera e detalhes.
2. A master aprovada controla sala, teto, placa, temperatura e direção da luz.
3. A lateral API v9 controla apenas a intenção de brilho/verniz da lateral; seu
   teto diferente não pode ser propagado.
4. Uma geração direta nunca é master. Ela pode doar luz ou fundo somente através
   de máscara revisada e trava de pixels.

## Validação das externas

As seis composições em
`trabalhos/panamera/previews-serie-v10-studio-canonico/externas` já usam o mesmo
teto contínuo, placa física e enquadramento de sala. Elas são previews de
composição. Ainda não são publicáveis porque preservam reflexos urbanos do teto,
capô, vidros e laterais originais. Cada ângulo deverá receber tratamento local
equivalente ao v8 aprovado, nunca uma regeneração integral do carro.

O rebase automático do perfil v01 foi reprovado: a geometria da geração não
coincidiu com a fonte e criou halo de recorte. Não usar
`serie-v10/perfil-studio-canonico-v01` como entrega.

## Validação das internas

As três gerações integradas em `serie-v10/interiores-candidatos/integrado` são
somente referências visuais. Elas recriaram detalhes do interior e não podem ser
promovidas a master.

O fluxo oficial preserva todos os pixels internos e deixa editável somente o
ambiente externo visto através dos vidros. No enquadramento próximo ao volante,
o estúdio aparece como parede off-white distante e desfocada; placa, logo, cantos
da sala e teto não devem aparecer. Isso elimina a leitura de cenário artificial
colocado perto do painel.

Prévia local sem cobrança:

```bash
./scripts/gerar_previews_panamera_v10.sh
```

Edição oficial GPT Image 2 high, três chamadas no máximo e trava individual
contra repetição:

```bash
./scripts/executar_interiores_serie_v10_api.sh
```

Antes da API, revisar os arquivos `revisao-mascara.jpg` em
`trabalhos/panamera/serie-v10/interiores-api/preparo`. Se uma máscara tocar
volante, instrumentos, painel ou molduras, ela deve ser corrigida antes da
chamada.

## Gates de aprovação

- zero pixel alterado fora da máscara;
- teto externo sempre contínuo, sem painel luminoso visível;
- nenhum detalhe, texto ou geometria do interior regenerado;
- parede vista pelo vidro com desfoque compatível com a profundidade de campo;
- sem rua, árvores, céu azul, placas ou carros residuais;
- sem halo nas bordas do vidro, pilares ou volante;
- externas sem reflexos urbanos e com verniz metálico coerente com a master;
- nenhuma master/exportação final antes da aprovação humana do ângulo.

## Auditoria visual de 08/09/2026

| Vista | Estúdio/teto | Identidade | Reflexos/fundo | Estado |
|---|---|---|---|---|
| dianteira 3/4 | aprovado | aprovado | aprovado na v07 | master existente; não refazer |
| frontal | coerente | preservada | reflexos urbanos no capô/vidro | preview, tratar |
| perfil | coerente no v10 | preservada | reflexos urbanos; fluxo API v10 pronto | próxima externa |
| dianteira 3/4 oposta | coerente | preservada | reflexos urbanos fortes | preview, tratar |
| traseira 3/4 | coerente | preservada | rua/árvores na pintura e vidro | preview, tratar |
| traseira 3/4 oposta | coerente | preservada | rua/céu na pintura e vidro | preview, tratar |
| perfil oposto | coerente | preservada | reflexos urbanos fortes | preview, tratar |
| interior amplo | parede canônica aplicada | pixels internos preservados | transição de vidro requer aprovação | candidata local |
| painel/instrumentos | parede distante, sem logo/sala inteira | volante e instrumentos preservados | melhorada; API contida preparada | candidata prioritária |
| interior motorista | direção correta | pixels internos preservados | ainda há cenário residual nas bordas | máscara em refinamento |

A folha consolidada atual é
`trabalhos/panamera/previews-serie-v10-studio-canonico/03-serie-completa-previews.jpg`.
Ela é uma folha de decisão, não uma entrega.
