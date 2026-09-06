# Piloto v5 — Panamera dianteira 3/4

Atualizado em 06/09/2026. Candidato técnico em revisão visual; não publicar sem aprovação humana.

## Resultado desta etapa

- Novo estúdio vazio `STUDIO_G` com câmera 4:3 fixa, ciclorama off-white, piso cinza acetinado e iluminação ampla superior/esquerda.
- Suporte de parede fosco, com espessura, quatro afastadores metálicos e sombra curta de contato.
- Logo oficial aplicado do arquivo transparente aprovado; não foi redesenhado pela geração. Os realces do arquivo foram comprimidos e foi adicionada uma sombra curta para leitura de emblema elevado.
- Para-brisa, capô e lateral tratados separadamente por máscaras locais.
- Capô: remoção de fios, prédios, céu e vegetação; substituição por reflexo amplo de softbox.
- Lateral: remoção do piso amarelo e do ambiente urbano; substituição por gradiente neutro contínuo.
- Vidro: reflexo reduzido sem transformar o para-brisa em uma superfície preta; cabine e volante continuam legíveis.
- Sombra de contato recalculada com os dois pneus e o contorno inferior do veículo.
- Tampa-placa aplicada no quadrilátero medido da tarja preta original, sem ampliar a área coberta.

## Política de fidelidade

O modelo generativo foi usado somente para reconstruir reflexos dentro das três máscaras autorizadas e para criar o estúdio vazio. O carro final não é uma geração integral. Após cada geração, o resultado foi realinhado à fotografia e reinserido deterministicamente.

A auditoria `qa-fidelidade-fonte.json` verificou 1.087.038 pixels protegidos e encontrou zero alteração RGB fora da união das máscaras de para-brisa, capô e lateral. Faróis, rodas, pneus, pinças, emblemas, grades, vincos externos e geometria fora dessas áreas continuam sendo os pixels da fotografia.

Isso comprova contenção digital, não certificação física da tinta. A foto original não contém cartela ColorChecker nem arquivo RAW; portanto não é correto prometer fidelidade colorimétrica absoluta. A amostra de pintura protegida usada na composição teve Delta E 2000 igual a 0 em relação à fonte tratada.

## Arquivos principais

- Master sem perdas: `trabalhos/panamera/studio-v5-dianteira-3-4/dianteira-3-4/master-4096x3072.png`
- Feed 4:3: `formatos/feed-4096x3072.jpg`
- Story horizontal 16:9: `formatos/story-horizontal-3840x2160.jpg`
- Webmotors: `formatos/webmotors-1920x1440.jpg`
- Estúdio vazio oficial: `estudio-mestre/STUDIO_G-cyclorama-placa-matte-v05-oficial.png`
- Configuração reproduzível: `config/piloto-dianteira-v5-final.json`
- Prompts: `prompts/09-capo-reflexos-estudio.txt`, `prompts/10-lateral-reflexos-estudio.txt` e `prompts/11-estudio-v5-placa-matte.txt`.

## Limites que permanecem

- A fonte mede 1280 × 960. O master 4096 × 3072 é uma ampliação controlada, não captura 4K nativa.
- Reflexos reconstruídos são uma interpretação fisicamente plausível de estúdio; a informação real escondida pelos reflexos externos não pode ser recuperada da fotografia.
- Pequenas reflexões originais permanecem em áreas não autorizadas nesta etapa, principalmente molduras, espelho e vidro lateral. Removê-las exige novas máscaras e uma rodada separada de aprovação.
- O estúdio `STUDIO_G` e o tratamento v5 não substituem a série ativa v03 até aprovação visual do piloto.

## Regra para a série

Depois da aprovação, congelar o fundo `STUDIO_G`, posição do logo, luz, câmera, escala, baseline, intensidade de sombra, tampa-placa e exportações. Cada nova vista recebe máscaras próprias; nunca gerar novamente o carro inteiro nem o estúdio por fotografia.
