# Master aprovada v8 e previews da série Panamera

Atualizado em 07/09/2026.

## Decisão aprovada

O usuário aprovou visualmente a harmonização v07 da vista dianteira 3/4. A fonte
congelada desta entrega é:

`trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v07-clearcoat-final/candidato-quadro-completo.png`

Ela foi ampliada deterministicamente por Lanczos para um único master sRGB
4096 × 3072. A fonte de 2048 × 1536 não permite declarar detalhe 4K nativo. Não
houve nova geração por IA e nenhum doador pago foi repetido.

## Entrega aprovada — dianteira 3/4

- Master: `entregas/panamera-v8-aprovada/dianteira-3-4/master-4096x3072.png`
- Feed: `entregas/panamera-v8-aprovada/dianteira-3-4/formatos/feed-4096x3072.jpg`
- Story horizontal: `entregas/panamera-v8-aprovada/dianteira-3-4/formatos/story-horizontal-3840x2160.jpg`
- Webmotors: `entregas/panamera-v8-aprovada/dianteira-3-4/formatos/webmotors-1920x1440.jpg`
- Auditoria: `entregas/panamera-v8-aprovada/dianteira-3-4/qa-exportacao.json`

Reprodução no Terminal:

```bash
./scripts/finalizar_master_panamera_v8.sh
```

## Previews para aprovação da série

Foram preparados nove previews: seis vistas externas ainda não aprovadas e as
três fotografias internas. A dianteira 3/4 aprovada foi excluída da grade.

As externas servem para aprovar seleção, enquadramento, escala, contato com o
piso, Studio H e tampa-placa. Elas ainda conservam os reflexos urbanos e não
devem ser confundidas com o acabamento final v07. Após a aprovação de cada
ângulo, o tratamento de luz/material será adaptado à superfície correspondente,
com gates de identidade antes da master.

As internas preservam a fotografia: nesta etapa há apenas conversão sRGB e
redimensionamento Lanczos. Não foi inventado um novo interior nem removido o
ambiente visto através dos vidros.

- Externas: `trabalhos/panamera/previews-serie-v8/01-previews-externas.jpg`
- Interiores: `trabalhos/panamera/previews-serie-v8/02-previews-interiores.jpg`
- Série completa: `trabalhos/panamera/previews-serie-v8/03-serie-completa-previews.jpg`
- Manifesto e hashes: `trabalhos/panamera/previews-serie-v8/manifesto-previews.json`

Reprodução no Terminal:

```bash
./scripts/gerar_previews_panamera_v8.sh
```

## Próxima decisão humana

Validar os seis enquadramentos externos e as três seleções internas. Não criar
as outras masters antes dessa aprovação. Para cada externa aprovada, tratar
reflexos, iluminação e material individualmente sem trocar rodas, esterçamento,
geometria, vidros, emblemas ou detalhes. Para cada interna aprovada, definir se a
entrega será somente correção fotográfica conservadora ou se o ambiente externo
visível pelos vidros deverá ser mascarado separadamente.
