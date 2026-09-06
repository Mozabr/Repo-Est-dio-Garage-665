# Correção do capô integral — v6c

Status: pacote técnico validado; uma nova geração paga ainda precisa ser executada e aprovada visualmente.

## Diagnóstico objetivo

O problema mais grave do ensaio v6b não era apenas a força da luz. A resposta
bruta da API redesenhou e deslocou o carro. A validação retroativa encontrou 61
correspondências, somente 44,26% de inliers e deslocamento máximo de 28,74 px.
O limite do projeto é 12 px e 60% de inliers. Portanto, aquele candidato está
formalmente reprovado e nenhum pixel dele deve entrar no master.

Além disso, o processo antigo gerava a Panamera fora do enquadramento final e
depois recortava as mesmas coordenadas para inserir o resultado. Isso explica a
aparência de remendo no centro do capô e a divergência de carroceria. A v6c
elimina essa arquitetura: a fotografia original já é posicionada no Studio H
antes da edição, e a API recebe exatamente essa composição final.

## Leitura do capô fotografado

A máscara unificada ocupa 93.785 pixels efetivos no alvo 2048 × 1536. O capô
original tem amplitude p95–p05 de 82,8 em Lab L. O terço junto ao para-brisa
chega a 90,0, o meio a 88,0 e o lado da câmera a 98,0. Após desfoque espacial, o
decil mais claro ainda aparece dividido em oito regiões. Esse padrão fragmentado
é coerente com céu, fachada e elementos urbanos refletidos; não com uma única
fonte difusa de estúdio.

O Studio H, por sua vez, tem parede esquerda 14,656 Lab L mais clara que a
direita, parede 15,252 Lab L acima do piso e praticamente nenhum branco
estourado. A resposta física desejada no capô é, portanto, assimétrica e suave:
uma única faixa/envoltória ampla proveniente do alto e levemente da esquerda,
com queda contínua para a frente e para a direita. O teto não pode aparecer como
um retângulo literal, divisão diagonal ou ilha cinza no centro.

## Alterações implementadas

1. `M11U-capo-integral` substitui as três máscaras generativas do capô. O capô é
   tratado como um painel metálico contínuo; o escudo Porsche, faróis, vincos e
   linha de fechamento continuam protegidos.
2. O alvo da edição já contém o carro original, na escala e posição finais do
   Studio H. O ambiente não será reconstruído pela chamada.
3. A guia de normais e a máscara foram projetadas para as coordenadas finais de
   2048 × 1536 sem modificar o alvo.
4. O prompt exige uma única envoltória luminosa de baixo contraste, sem linha
   central, cunha, recorte, reflexo literal do teto ou mudança de cinza.
5. O rig passa a ter meta de amplitude do capô entre 45 e 65 Lab L, uma a três
   regiões claras amplas e delta máximo de recomposição de 14 Lab L.
6. Toda resposta bruta passa por registro geométrico obrigatório. Menos de 60%
   de inliers ou mais de 12 px de deslocamento interrompe o processo antes da
   mistura.
7. A recomposição usa 62% da luz de baixa frequência proposta, reinsere 90% do
   microdetalhe fotografado e puxa a cromia ampla 88% de volta à fonte.

## Validação concluída

O pré-voo v6c passou em todos os dez controles: arquivos presentes, alvo e
máscaras em 2048 × 1536, alfa inverso correto para a API, hashes do rig e dos
prompts consistentes, máscara contida no veículo, detalhes protegidos intactos,
uma superfície por chamada e geração integral do carro bloqueada.

Um ensaio local de identidade teve 3.500 correspondências, 100% de inliers,
deslocamento zero e zero mudança fora da máscara. A pequena conversão interna de
cor ficou limitada à área editável; a geração real continuará sujeita à inspeção
visual em 200% antes de qualquer exportação 4K.

## Próxima execução

Executar uma única chamada do capô com
`./scripts/executar_teste_capo_integral_v6c.sh`. O resultado aprovado será o
arquivo `capo-integral-recomposto-v6c.png`. Ainda não executar teto, vidros,
laterais nem formatos finais antes da aprovação desse capô.
