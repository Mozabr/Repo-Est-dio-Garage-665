# Estúdio Garage 665 — implementação v2

Data: 05/09/2026. Estado: piloto técnico em revisão; não confundir testes de
integridade com aprovação estética ou fidelidade física de cor.

## O que foi implementado

- BiRefNet oficial, com snapshot fixado e pesos safetensors locais.
- ViTMatte oficial via Transformers, refinando uma trimap na resolução original.
- Seleção por região do veículo e retenção do maior componente para excluir outros carros.
- Alpha contínuo, sem dilatação automática de toda a silhueta.
- Descontaminação restrita aos pixels mistos próximos da borda; interior opaco intacto.
- Composição em luz linear e alpha premultiplicado para evitar halos na transformação.
- Sombras usando a projeção do piso e pontos dos pneus de cada fotografia.
- Tampa-placa oficial projetada nos quatro cantos medidos, com trava fora da região.
- ColorChecker Detection por segmentação e Colour Science/CIEDE2000.
- Conversão de perfil ICC para sRGB antes de compor, não apenas mudança da etiqueta.
- Composição diretamente no master 4096 × 3072; prévia reduzida depois.
- Feed 4096 × 3072, Story horizontal 3840 × 2160 e Webmotors 1920 × 1440,
  derivados do mesmo master, com perfil sRGB incorporado.

## Estúdio e placa na parede

Ativo: `estudio-mestre/STUDIO_F-placa-fisica-v03-oficial.png`.

A sala e a placa vazia foram desenvolvidas com a ferramenta integrada de geração
de imagens, em três iterações. O arquivo-base nativo mede 1448 × 1086; o estúdio
foi ampliado para o master. Ele é um cenário sintético e não uma fotografia
de um espaço real. A parede tem textura discreta, o piso é fosco, e a placa possui
espessura aparente, fixadores e sombra. A arte oficial não foi regenerada.

O arquivo-base é ampliado antes da aplicação da arte, para aproveitar a resolução
do PNG original do logo. A iluminação neutra da placa modula discretamente a
impressão. A geometria medida e a transformação ficam no JSON ao lado do estúdio.

As sete fotos externas usam exatamente o mesmo arquivo de estúdio e uma escala de
enquadramento por vista. Não se criaram ângulos novos do carro. Isso não
representa uma plataforma giratória calibrada em 3D: as perspectivas originais
ainda variam e precisam ser padronizadas na próxima captação.

Os cinco presets estão em `config/estudio-v2.json`; a traseira totalmente frontal
continua sem fotografia de teste. A entrada inclui frontal, dianteiras 3/4,
perfis e traseiras 3/4. Nenhum ângulo ausente foi inventado.

## Arquivos para revisão

- `trabalhos/panamera/studio-v2/serie-comparativa.jpg`: série em grade.
- Em cada vista: `preview.png`, `master-4096x3072.png` e pasta `formatos/`.
- `alpha-birefnet.png`, `trimap.png`, `alpha-final.png`: máscaras auditáveis.
- `carro-rgba.png`: RGB original com alpha refinado, antes da descontaminação.
- `comparativo.jpg`: original, recorte e composição.
- `qa.json`: fonte, hashes, geometria da placa e diferença de cor.
- `verificacao.json`: resultado das verificações automáticas.
- `calibracao-disponivel.json`: nenhuma cartela foi encontrada na foto fornecida.

## Operação

O ambiente já está instalado em `.venv-mask`. Para repetir sem custo de API:

```bash
bash scripts/executar_studio_v2.sh
```

Para reconstruir o ambiente em outra máquina com Python 3.11:

```bash
python3.11 -m venv .venv-mask
.venv-mask/bin/python -m pip install -r requirements-mask.txt -r requirements-studio.txt
.venv-mask/bin/python scripts/baixar_modelos_studio.py --weights
bash scripts/executar_studio_v2.sh
```

O download usa a revisão já registrada, sem acompanhar mudanças automáticas no
modelo. A inferência usa somente arquivos locais. O código de modelo do BiRefNet
exige `trust_remote_code`, mas é carregado do snapshot fixado em disco; o handler
de serviço remoto não é usado.

Configuração das fotos: `config/piloto-v2.json`. Cada imagem precisa de ROI,
pontos de contato no chão e quadrilátero da tampa-placa, medidos na foto original.
Não copie coordenadas entre fotos. Para refinar manualmente, salve uma cópia da
trimap e adicione `trimap_override` na configuração da vista com esse caminho
relativo ao projeto. Use somente preto 0, cinza 128 e branco 255, na resolução
original. Mudanças na foto, ROI, modelo ou trimap invalidam o cache correspondente.
Não altere os arquivos de saída automática para usá-los como entrada.

## O que as métricas comprovam

O erro RGB nas áreas opacas protegidas é medido antes da transformação geométrica.
Delta E é medido em regiões nativas selecionadas da pintura. Valores zero indicam
preservação da foto original; não comprovam a cor real sob iluminação neutra.
Redimensionamento e JPEG da entrega introduzem diferenças normais de amostragem.

O teste também valida contenção da tampa-placa, alpha fracionário, dimensões,
ICC, área segura do Story e distância entre veículo e placa da parede.

Retomada em 06/09/2026: a configuração das três vistas anteriores foi preservada
em `config/piloto-v2-tres-vistas.json`. Duas novas vistas têm revisão da geometria
da tampa-placa explicitamente pendente: traseira-3-4 e perfil-oposto. Nelas, o
suporte escuro interfere na comparação automática com a tarja preta. O relatório
não certifica correspondência exata dessas placas e não autoriza publicação.

## Limitações que ainda impedem a aprovação final

1. Os reflexos de céu, nuvens e fachada permanecem na pintura e nos vidros.
2. A luz solar dura da fotografia não corresponde perfeitamente à luz da sala.
3. O WhatsApp reduziu as fotos para 1280 × 960; ampliar não recupera detalhe real.
4. A cor física não pode ser calibrada sem referência capturada na mesma luz.
5. Sombras são composições plausíveis, não sombras medidas por reconstrução 3D.

O piloto v2 melhora infraestrutura, recorte e marca. Não deve ser vendido como
remoção de reflexos concluída. A edição generativa dos carros está desativada.
IC-Light/libcom continuam opções de laboratório, não dependências de produção.
O repositório awesome-gpt-image-2 continua como referência criativa de prompts.

## Próxima captação para o resultado publicável

Obter originais da câmera em RAW/ProRAW ou JPEG sem envio comprimido. Fotografar
o carro em local coberto, com painéis neutros grandes que ocultem fachadas e
objetos refletidos. Fontes difusas laterais/superiores devem ser instaladas com
suportes adequados; um polarizador ajuda dependendo do ângulo, mas não remove
todos os reflexos de metal, vidro ou verniz em todas as direções.

Fixar câmera, exposição, balanço de branco, focal e marcas de posição. Fotografar
uma cartela de cor na mesma iluminação. Fazer pares registrados com o polarizador
em duas posições para escolher o equilíbrio entre cor e brilho; compensar a perda
de exposição. Evitar neutralização indiscriminada do efeito metálico.

Usar tampa-placa física com a arte oficial. Capturar frontal, três quartos dos dois
lados, perfis e traseira. O efeito de trocar os reflexos mantendo fidelidade
máxima passa a depender muito menos de retoques após a captura.

Para detectar a cartela:

```bash
.venv-mask/bin/python scripts/calibrar_captacao.py foto-com-cartela.jpg --saida calibracao.json
```

O ajuste opcional exige um JSON com 24 valores sRGB de referência correspondentes
à cartela e ao iluminante escolhidos. A matriz é apenas estimada: precisa de uma
foto independente da cartela para validação antes de aplicar a toda a sessão.

Os scripts de composição recebem JPEG/PNG/TIFF que o Pillow consiga ler. Arquivos
RAW/ProRAW precisam primeiro ser revelados em um aplicativo de fotografia, com o
perfil de câmera adequado, e exportados para um formato de entrada compatível.
O master deste piloto é PNG RGB de 8 bits; os cálculos de composição usam ponto
flutuante. Não foi implementado um revelador RAW neste projeto.

## Fontes e licenças registradas

- https://github.com/ZhengPeng7/BiRefNet — código/model card MIT.
- https://github.com/hustvl/ViTMatte — implementação de referência.
- https://huggingface.co/hustvl/vitmatte-small-composition-1k — checkpoint Apache-2.0 segundo o model card.
- https://github.com/colour-science/colour — BSD-3-Clause.
- https://github.com/colour-science/colour-checker-detection — caminho de segmentação BSD-3-Clause; YOLO não usado.
- https://github.com/opencv/opencv — Apache-2.0 para a versão adotada.
- https://github.com/facebookresearch/sam2 — assistente de seleção já instalado.

Prompts de construção: `prompts/04-estudio-placa-fisica.txt`.
