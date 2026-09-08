# Base de custo — GPT Image 2

Atualizado em 08/09/2026. Valores em USD, antes de impostos, conversão cambial
e tarifas do cartão.

## Preços oficiais usados

Na API padrão, o GPT Image 2 custa por milhão de tokens:

- entrada de texto: US$ 5;
- entrada de imagem: US$ 8;
- entrada de imagem em cache: US$ 2;
- saída de imagem: US$ 30.

O calculador oficial informa, para qualidade `high`:

- 1024 × 1024: US$ 0,211 por imagem de saída;
- 1024 × 1536 ou 1536 × 1024: US$ 0,165 por imagem de saída.

Esses valores por imagem cobrem apenas a saída. Uma edição também cobra o texto
do prompt e cada imagem de referência recebida. O valor exato da entrada depende
das dimensões e da quantidade de referências.

Fontes oficiais:

- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/models/gpt-image-2
- https://developers.openai.com/api/docs/guides/image-generation

## Planejamento da Panamera

O conjunto possui dez fotos: sete externas e três internas. A dianteira 3/4 já
tem master aprovada, portanto restam nove masters caso ela não seja cobrada de
novo.

| Cenário | Saídas high 1536 × 1024 | Custo de saída | Mais entradas |
|---|---:|---:|---:|
| Um passe nas 10 fotos | 10 | US$ 1,650 | sim |
| Um passe nas 9 restantes | 9 | US$ 1,485 | sim |
| Dois passes nas 10 fotos | 20 | US$ 3,300 | sim |
| Três passes nas 10 fotos | 30 | US$ 4,950 | sim |

Para não subestimar as referências de identidade e estúdio, a reserva prática
recomendada é de **US$ 2,50 a US$ 3,50 para um passe completo de dez fotos**.
Essa faixa é uma estimativa operacional, não uma tarifa fixa; a cobrança real
aparece no campo `usage` de cada resposta da API.

## Regra para 4K

O GPT Image 2 aceita tamanhos personalizados com lados múltiplos de 16, até
3840 px no lado maior e até 8.294.400 pixels. Portanto 4096 × 3072 não pode ser
solicitado diretamente. Para 4:3, o maior tamanho exato dentro desses limites é
3264 × 2448; a master de entrega 4096 × 3072 deve ser derivada localmente e
auditada depois da geração. Acima de 2560 × 1440, a documentação classifica os
tamanhos como experimentais, por isso o custo deve ser confirmado no calculador
oficial antes de processar o lote completo.

## Política para controlar gasto

1. validar previews antes de qualquer master paga;
2. fazer uma chamada por vista e arquivar resposta e `usage`;
3. impedir repetição se a resposta bruta já existir;
4. aprovar uma externa e uma interna como pilotos;
5. somente então liberar as demais;
6. criar Feed, Story e Webmotors localmente a partir da mesma master, sem nova
   chamada à API.

