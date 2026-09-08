# Previews multivista v12 — conjunto para validação

## Entrega desta rodada

Foram criadas seis externas e três internas em 1448 × 1086, todas usando a
master `teste 05` como referência do Studio G. A dianteira 3/4 aprovada foi
copiada para a mesma pasta, formando uma folha de sete externas.

- externas: `trabalhos/panamera/previews-validacao-v12/externas`;
- internas: `trabalhos/panamera/previews-validacao-v12/interiores`;
- folha externa: `01-folha-externas.jpg`;
- folha interna: `02-folha-interiores.jpg`;
- prompt: `prompts/v12/preview-multivista-imagegen-v01.txt`.

Modo de geração: ferramenta integrada de geração/edição de imagens, usada para
prévia visual. Estas imagens não são as masters GPT Image 2 API e não são
entregas publicáveis antes da validação.

## Leitura inicial

- O estúdio, teto contínuo, enquadramento geral e temperatura estão coerentes na
  série.
- Perfil e as duas traseiras apresentam a direção mais consistente desta rodada.
- A frontal contém uma divisão tonal retangular no centro do capô e precisa de
  refinamento localizado.
- A dianteira 3/4 oposta possui reflexos geométricos ainda fortes no capô.
- Badge, lettering, desenho fino das rodas, instrumentos e textos devem ser
  comparados com os originais a 100% antes de qualquer master.
- O logo gerado nas candidatas não é autoridade. Na finalização, a placa e a
  arte oficial devem ser reaplicadas deterministicamente.
- As internas agora mostram apenas superfícies off-white plausíveis do estúdio
  através dos vidros. A vista próxima ao volante não exibe sala inteira nem
  placa na parede.

## Falha v11 anterior

O teste pago mascarado de perfil foi reprovado: a master dianteira 3/4 contaminou
a geometria do perfil dentro da máscara. O arquivo permanece arquivado somente
para auditoria e a resposta bruta impede cobrança duplicada. Não reutilizar essa
imagem nem repetir a chamada.

## Próximo gate

O usuário deve validar primeiro a direção conjunta das duas folhas. Depois:

1. selecionar as vistas visualmente aprovadas;
2. corrigir a frontal e qualquer detalhe divergente de forma localizada;
3. substituir logo/badges/textos pelo conteúdo documental original quando
   necessário;
4. gerar 4096 × 3072 apenas das vistas aprovadas;
5. derivar Feed, Story e Webmotors do mesmo master.

## Correções V02 — frontal e interna motorista

Em 08/09/2026 foram executadas duas edições localizadas com a ferramenta
integrada de imagem, mantendo as V01 arquivadas:

- `externas/frontal-candidata-v02-capo-corrigido.png`: removida a divisão
  retangular e as duas emendas verticais artificiais do centro do capô; a
  leitura agora é de uma única chapa curva com reflexão ampla de softbox;
- `interiores/interior-motorista-candidata-v02-studio-soft.png`: removida a
  mancha dura de sol sobre o banco e reduzidos os highlights direcionais; o
  interior passa a usar iluminação difusa neutra compatível com a master;
- `03-folha-externas-identificada-v02.jpg`: comparação das sete externas com a
  dianteira 3/4 aprovada identificada na primeira posição;
- `04-folha-interiores-identificada-v02.jpg`: comparação das três internas com
  a interna motorista V02 na terceira posição;
- prompts e referências: `prompts/v12/correcoes-frontal-interior-v02.txt`.

As V02 são candidatas de validação, não masters publicáveis. Antes da chamada
paga, conferir em 100% a ótica dos faróis, o brasão, instrumentos, costuras,
controles e o tamanho do tampa-placa. A base financeira está em
`36-custos-gpt-image-2.md`.

## Frontal V04 — recuperação de detalhe

A frontal V02 eliminou a divisão do capô, mas foi reprovada por suavizar detalhes
do capô e do restante do carro. A V04 corrige isso por recomposição contida:

- arquivo: `externas/frontal-candidata-v04-capo-detalhe-final.png`;
- comparativo ampliado: `frontal-v03-detail-lock/comparacao-capo-v01-v02-v04.jpg`;
- máscara auditável: `frontal-v03-detail-lock/mascara-capo-contida.png`;
- relatório: `frontal-v03-detail-lock/qa-v04.json`;
- rotina: `scripts/recompor_capo_frontal_v12.py`.

A V02 fornece apenas a direção contínua da iluminação. A banda fina de detalhe
vem da V01, enquanto as duas bordas artificiais verticais são excluídas dessa
transferência. Todo pixel fora da máscara é copiado da V01. O relatório registra
zero mudança externa e razão de microdetalhe 0,9796, aproximadamente 98% da
referência. A folha `03-folha-externas-identificada-v02.jpg` foi atualizada para
mostrar a V04 no segundo quadro.

A primeira recomposição V03 foi arquivada como rejeitada porque recuperou também
as emendas e criou uma transição escura ao redor do brasão. Ela existe somente
para auditoria em `frontal-v03-detail-lock/frontal-v03-rejeitada.png` e não deve
ser usada como entrada de produção.
