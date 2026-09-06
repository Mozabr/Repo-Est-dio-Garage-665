# Teste oficial — Porsche Panamera Garage 665

> Nota de histórico: arquivos Webmotors 4K registrados neste relatório pertencem a testes anteriores. O padrão operacional atual está em `10-padroes-de-saida.md`: Feed 4096 × 3072, Story horizontal 3840 × 2160 e Webmotors 1920 × 1440.

## Foto selecionada

Origem: `WhatsApp Image 2025-11-24 at 09.57.06 (1).jpg`

Cópia preservada no projeto: `pilotos/panamera-oficial/panamera-frente-3-4-original.jpg`

Motivo da seleção: melhor combinação de ângulo dianteiro em três quartos, leitura da carroceria completa, rodas visíveis, emblema lateral híbrido e informação suficiente da pintura metálica.

## Diagnóstico do original

- arquivo recebido com 1280 × 960 px e compressão de WhatsApp, o que limita textura fina e amplia artefatos;
- reflexos fortes de céu e nuvens no para-brisa e capô;
- reflexos de postes, fios, prédios e fachada;
- pontos de luz solar dura e contraste irregular;
- contaminação azul do céu sobre a pintura grafite;
- áreas excessivamente escuras nas laterais;
- fundo urbano competitivo e sem padronização.

## Tratamento realizado

- substituição integral do ambiente pela placa `STUDIO_A`;
- remoção dos reflexos identificáveis do ambiente externo;
- reconstrução de reflexos longos e suaves de softboxes;
- preservação da textura e do flake metálico;
- sombra de contato baseada nos pneus e no assoalho;
- manutenção das rodas multirraios e pinças verdes;
- manutenção dos faróis, para-choque, grade, emblemas e placa já ocultada;
- calibração final da pintura para recuperar o subtom frio do grafite original.

## Versões

- `panamera-estudio-v01.png`: primeira composição completa.
- `panamera-estudio-v02-cor-ajustada.png`: segunda passagem restrita à fidelidade de cor.
- `panamera-estudio-v03-multirreferencia-4x3.png`: reconstrução em 4:3 usando quatro fotos do mesmo veículo para validar cor, metálico, brilho, carroceria e detalhes; nova versão recomendada.
- `panamera-estudio-profissional-sem-logo-v04.png`: reconstrução no ciclorama profissional com estrutura real de iluminação e parede vazia.
- `panamera-estudio-profissional-placa-v04.png`: versão 4 com o PNG oficial composto posteriormente como placa física; versão recomendada para direção de ambiente e marca.
- `panamera-estudio-limpo-sem-logo-v05.png`: correção específica que remove todos os equipamentos de iluminação e estruturas visíveis.
- `panamera-estudio-limpo-placa-v05.png`: versão 5 com teto limpo e logo oficial composto como placa física; nova versão recomendada.
- `comparativo-panamera-original-v1-v2.jpg`: original, versão 1 e versão 2 lado a lado.
- `comparativo-panamera-original-v03-4x3.jpg`: comparação direta entre original e versão 3.

## Bloco específico usado no primeiro tratamento

```text
Vehicle color lock: retain the exact dark graphite metallic gray paint of the original image, including its subtle cool undertone and fine metallic flake. Judge color from the least contaminated midtone body areas, especially the lower door and shaded panels. Do not recolor, brighten toward silver, darken toward black, shift toward blue, green, brown, or neutral gray, change saturation, or change metallic-flake density. All body panels must remain the same original paint color under neutral studio light.

Correct the damaging outdoor-light artifacts on the vehicle—cloud and sky reflections, power-line and building reflections, patchy glare, harsh sun hotspots, color contamination, hologram-like streaks, and uneven contrast—so it looks genuinely photographed in this professional studio. Do not make the paint flat or synthetic.
```

## Prompt da segunda passagem

```text
Correct only the metallic body-paint color so it matches the original Porsche paint more faithfully under neutral 5200 K studio illumination. Restore the subtle cool blue-gray/graphite undertone visible in the least contaminated midtone panels of the original. Keep the paint dark graphite metallic, not silver and not black. Preserve fine metallic flake, realistic tonal variation, panel curvature, and all existing soft studio reflections.

Change only the calibrated hue and tonal balance of the painted body panels. Keep absolutely everything else unchanged: exact vehicle geometry, body style and roofline, camera, crop, scale, position, wheels, tires, green brake calipers, lights, grille, intakes, Porsche crest, E-Hybrid badge, plate area, glass, mirrors, trim, panel gaps, studio room, wall logo, floor, shadows, reflections, lighting, sharpness, and texture.
```

## Terceira passagem: protocolo multirreferência

A versão 3 utilizou simultaneamente:

- a fotografia-alvo dianteira em três quartos;
- a placa de estúdio horizontal 4:3;
- uma vista frontal do mesmo veículo;
- uma vista traseira do mesmo veículo;
- uma vista lateral do mesmo veículo.

As vistas adicionais foram usadas somente para conferir a pintura real nas áreas menos contaminadas por céu e reflexos, preservar a carroceria Sport Turismo, rodas, pinças verdes, emblemas e proporções. O fundo e os ângulos dessas imagens não foram utilizados.

## Avaliação

O tratamento eliminou as interferências externas sem transformar a pintura em uma superfície lisa de render. A versão 4 melhora principalmente o realismo do ambiente: ciclorama com textura e assimetria naturais, piso de estúdio, equipamentos superiores visíveis e iluminação fisicamente explicável. O logo não foi gerado; o PNG oficial foi aplicado intacto, com espessura discreta e sombra de contato.

A versão 5 elimina totalmente softboxes, painéis, trilhos, estruturas e fontes luminosas do enquadramento. A iluminação continua perceptível somente por seus efeitos naturais no veículo, na parede e no piso. Essa passa a ser a regra obrigatória para todas as imagens.

## Saídas da versão 5

- Master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v05.png` — 1448 × 1086 px.
- Feed: `entregas/panamera-oficial/porsche-panamera-frente-3-4-feed-1440x1080-v05.jpg` — 1440 × 1080 px.
- Story: `entregas/panamera-oficial/porsche-panamera-frente-3-4-story-1920x1080-v05.jpg` — 1920 × 1080 px horizontal.
- Webmotors: `entregas/panamera-oficial/porsche-panamera-frente-3-4-webmotors-1920x1440-v05.jpg` — 1920 × 1440 px.

## Saídas da versão 4

- Master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v04.png` — 1448 × 1086 px.
- Feed: `entregas/panamera-oficial/porsche-panamera-frente-3-4-feed-1440x1080-v04.jpg` — 1440 × 1080 px.
- Story: `entregas/panamera-oficial/porsche-panamera-frente-3-4-story-1920x1080-v04.jpg` — 1920 × 1080 px horizontal.
- Webmotors: `entregas/panamera-oficial/porsche-panamera-frente-3-4-webmotors-1920x1440-v04.jpg` — 1920 × 1440 px.

## Saídas da versão 3

- Master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v03.png` — 1448 × 1086 px.
- Feed: `entregas/panamera-oficial/porsche-panamera-frente-3-4-feed-4x3-v03.jpg` — 1440 × 1080 px.
- Story: `entregas/panamera-oficial/porsche-panamera-frente-3-4-story-16x9-v03.jpg` — 1920 × 1080 px horizontal.
- Webmotors: `entregas/panamera-oficial/porsche-panamera-frente-3-4-webmotors-1920x1440-v03.jpg`.

Não é tecnicamente correto declarar fidelidade colorimétrica de 100% a partir de JPEGs comprimidos do WhatsApp e de uma reconstrução generativa. A versão 3 representa a melhor correspondência visual possível com o material disponível. Para comprovar fidelidade absoluta, o fluxo definitivo deve usar o arquivo original da câmera, referência de cor e uma camada recortada do carro preservada sem regeneração.

## Teste técnico 4K — versão 6

A versão com o tampa-placa foi exportada em 4096 × 3072 px e 3840 × 2160 px para validar dimensões, enquadramentos, compressão e o novo padrão de entrega. Ela não deve ser considerada uma reconstrução de detalhe 4K nativo, pois a fotografia recebida da Panamera tem apenas 1280 × 960 px e compressão de WhatsApp. Ampliação não recupera informação óptica que não existe no arquivo original.

Arquivos em `entregas/panamera-oficial-4k/`:

- master PNG 4096 × 3072;
- feed JPEG 4096 × 3072;
- Story horizontal JPEG 3840 × 2160;
- Webmotors principal JPEG 4096 × 3072;
- Webmotors compatível JPEG 1920 × 1440.

Para o padrão de qualidade 4K definitivo, o arquivo de entrada deve ter idealmente 12 MP ou mais, sem passagem pelo WhatsApp, com foco correto, baixa compressão e exposição preservando as altas luzes.

## Iluminação e reflexos naturais — versão 7

A versão 7 refaz especificamente a interação entre o estúdio e os materiais do veículo. O capô recebe uma reflexão difusa larga e contínua; teto e para-brisa recebem transições mais suaves; para-lamas e portas mostram fontes laterais alongadas com intensidade gradual; cromados, vidros, plásticos, pneus e pintura respondem de maneiras distintas. Foram removidas as grandes formas geométricas e a granulação metálica uniforme que denunciavam tratamento artificial.

O logo da parede e o tampa-placa foram aplicados depois da correção, sem regeneração.

Arquivos recomendados:

- master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v07.png`;
- master 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-master-4096x3072-v07.png`;
- feed 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-feed-4k-4096x3072-v07.jpg`;
- Story 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-story-4k-3840x2160-v07.jpg`;
- Webmotors 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-webmotors-4k-4096x3072-v07.jpg`.

Para o melhor resultado possível nos próximos lotes, enviar os arquivos originais da câmera ou do celular sem passagem pelo WhatsApp.

## Naturalidade da luz e acabamento da pintura — versões 8 a 10

As versões 8 e 9 reduziram a aparência de iluminação padronizada: o reflexo principal do capô deixou de funcionar como uma faixa gráfica, teto e para-brisa ficaram mais contidos e os painéis laterais passaram a apresentar variações suaves e ligeiramente assimétricas. A versão 9 também recebeu uma correção direcionada contra hologramas e padrões artificiais na pintura.

Na inspeção em tamanho real da exportação 4K ainda apareceu uma microtextura ondulada residual. A versão 10 acrescenta um acabamento técnico com suavização seletiva das áreas de baixa frequência e preservação de bordas, faróis, emblemas, rodas, grade e demais elementos de alto contraste. A exportação final não recebe nitidez artificial agressiva.

Arquivos recomendados:

- master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v10.png`;
- master 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-master-4096x3072-v10.png`;
- feed 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-feed-4k-4096x3072-v10.jpg`;
- Story 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-story-4k-3840x2160-v10.jpg`;
- Webmotors 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-webmotors-4k-4096x3072-v10.jpg`;
- Webmotors compatível: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-webmotors-compativel-1920x1440-v10.jpg`.

O logo da parede e o tampa-placa continuam sendo os arquivos oficiais compostos em pós-produção, sem redesenho generativo. A entrega tem dimensões 4K, mas a informação óptica de origem continua limitada pelo JPEG de 1280 × 960 px recebido via WhatsApp.

## Verniz metálico e fixação física do logo — versão 13

A fotografia externa adicional do mesmo veículo passou a controlar exclusivamente a cor e o comportamento do material. A pintura foi ajustada para grafite escuro frio com verniz automotivo mais profundo, brilho especular moderado e flake metálico extremamente fino nos meios-tons. Elementos externos da referência, como céu, nuvens, árvores, prédio e fiação, não foram transferidos para o estúdio.

Depois da correção generativa, uma etapa técnica seletiva reduziu padrões ondulados residuais sem reforço agressivo de nitidez. O logo oficial foi aplicado diretamente no master 4K como placa rígida de pequena espessura, com oclusão de contato junto às bordas e sombra curta de baixa opacidade, simulando fixação com espaçadores próximos à parede.

Arquivos recomendados:

- master: `entregas/panamera-oficial/porsche-panamera-frente-3-4-master-v13.png`;
- master 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-master-4096x3072-v13.png`;
- feed 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-feed-4k-4096x3072-v13.jpg`;
- Story 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-story-4k-3840x2160-v13.jpg`;
- Webmotors 4K: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-webmotors-4k-4096x3072-v13.jpg`;
- Webmotors compatível: `entregas/panamera-oficial-4k/porsche-panamera-frente-3-4-webmotors-compativel-1920x1440-v13.jpg`.
