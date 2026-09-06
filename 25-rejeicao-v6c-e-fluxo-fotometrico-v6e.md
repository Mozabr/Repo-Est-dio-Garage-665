# Rejeição v6c e fluxo fotométrico v6e

Status: v6c rejeitada; v6e preparada e validada, aguardando uma geração de crop.

## O que ocorreu na imagem anexada

`geracao-bruta-api.png` é a resposta integral da API, não uma entrega. O GPT
reinterpretou quase o quadro inteiro: 3.035.847 pixels mudaram fora da máscara
do capô. A roda, a placa, o vidro, a posição do carro e o acabamento fosco são
consequências dessa reinterpretação global.

A trava local restaurou todos os pixels externos à máscara, mas a geração ainda
falhou no registro: 311 correspondências, 75,88% de inliers e deslocamento
máximo de 19,94 px contra limite de 12 px. O processo encerrou corretamente
antes de criar um resultado final. A v6c não pode ser publicada nem reaproveitada.

## Por que só reforçar o prompt não basta

A máscara da Image API orienta o modelo, mas não garante que a resposta bruta
seja idêntica fora dela. Portanto, nenhuma versão bruta deve ser avaliada como
resultado. A preservação precisa ser imposta depois da API, por composição local
e comparação de pixels.

O teste determinístico v6d confirmou a trava total dos elementos, porém deixou
o capô excessivamente uniforme e sem resposta especular suficiente. Ele também
fica reprovado visualmente. Sua utilidade foi provar que roda, placa, vidro e
estúdio podem permanecer matematicamente intactos.

## Arquitetura v6e

1. Recorta somente a região técnica do capô em 1024 × 512 e amplia para
   2048 × 1024 para a API. O carro inteiro deixa de ser o assunto da geração.
2. A máscara editável continua restrita ao capô e protege o emblema. Roda,
   faróis, placa, vidro e estúdio aparecem apenas como contexto opaco.
3. O prompt agora pede explicitamente verniz automotivo polido e resposta
   especular controlada. Ele proíbe acabamento matte, satin, cinza uniforme,
   airbrush e eliminação total de reflexos.
4. A referência externa de outro carro foi removida desta chamada. A própria
   fotografia é a única autoridade de pintura; o Studio H orienta somente luz.
5. O registro ficou mais rígido: mínimo de 70% de inliers e máximo de 8 px no
   crop ampliado. Uma resposta deslocada é descartada antes da mistura.
6. A recomposição aceita apenas 50% da luz de baixa frequência, limita a mudança
   a 10 Lab L e reinsere 97% do microdetalhe fotografado.
7. Ao voltar ao quadro completo, todos os pixels fora da máscara integral do
   capô são copiados novamente da base. Assim, roda, ângulo de direção, placa,
   vidro, carroceria e estúdio não podem mudar no arquivo final.

## Validação

O pré-voo v6e passou em todos os dez controles. O ensaio de identidade do crop
teve 3.500 correspondências, 100% de inliers, deslocamento zero e zero mudança
fora da máscara. A reintegração ao quadro completo também registrou zero mudança
externa ao capô.

O arquivo integral da API passa a se chamar
`diagnostico-resposta-integral-nao-usar.png`, evitando que seja confundido com
a entrega. O único arquivo que deverá ser avaliado é
`capo-v6e-quadro-completo.png`, e somente se os gates forem aprovados.
