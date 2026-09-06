# Pesquisa técnica — relighting e preservação de detalhes

Data: 06/09/2026. Escopo: Panamera dianteira 3/4 e futura série Garage 665.

## Conclusão executiva

O problema atual não é apenas recorte. O carro e o estúdio possuem assinaturas de luz incompatíveis. O fundo usa luz ampla, neutra e difusa; partes do teto, capô, vidros, para-lama e lateral ainda carregam céu azul, fachada, luz solar direta e reflexos lineares do local original. Nas regiões já reconstruídas, o modelo removeu informação urbana, mas também alisou microdetalhes e criou faixas de luz pouco relacionadas entre si.

Um prompt maior não resolve isso sozinho. O fluxo recomendado é híbrido:

1. GPT Image 2 em qualidade alta, uma superfície por chamada;
2. mapas auxiliares de profundidade, normais, material e iluminação;
3. geração tratada somente como proposta de luz e remoção semântica;
4. recomposição determinística dos detalhes originais;
5. harmonização, sombra e super-resolução como etapas separadas;
6. aprovação da dianteira 3/4 antes de liberar qualquer outra vista.

## O que a documentação oficial esclarece

- `gpt-image-2` é o modelo de imagem indicado para geração e edição de alta qualidade e aceita entradas de imagem em alta fidelidade.
- No GPT Image 2, `input_fidelity` deve ser omitido: todas as imagens de entrada já são processadas em alta fidelidade.
- A máscara da API é uma orientação para o modelo e não uma trava exata de pixels. A contenção externa que já existe no projeto continua obrigatória.
- O guia recomenda declarar explicitamente o que muda e o que permanece, repetir os invariantes em cada iteração e fazer mudanças pequenas em vez de sobrecarregar uma única chamada.
- Saídas acima do limite de confiabilidade de aproximadamente 2560 × 1440 são tratadas como experimentais. Para o piloto 4:3, a edição deve ocorrer preferencialmente em 2048 × 1536; o master 4096 × 3072 nasce depois da aprovação.

Fontes oficiais:

- https://developers.openai.com/api/docs/models/gpt-image-2
- https://developers.openai.com/api/docs/guides/image-generation
- https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- https://github.com/openai/openai-imagegen-demo

## Repositórios recomendados

### Produção

#### Depth Anything V2 Small

- Repositório: https://github.com/DepthAnything/Depth-Anything-V2
- Função: mapa de profundidade relativo para conservar volume, separação entre teto, vidro, capô, para-lama e piso.
- Motivo da escolha: o checkpoint Small é Apache-2.0; Base, Large e Giant possuem restrições diferentes e não entram no fluxo comercial.
- Execução: ambiente separado; o repositório declara suporte a MPS, portanto é o candidato mais simples para o Apple M5.
- Papel no GPT Image 2: imagem auxiliar identificada como mapa geométrico; não substitui a foto original.

#### Real-ESRGAN

- Repositório: https://github.com/xinntao/Real-ESRGAN
- Licença: BSD-3-Clause.
- Função: recuperar nitidez perceptiva e reduzir artefatos do JPEG do WhatsApp depois da composição aprovada.
- Preset inicial: `realesr-general-x4v3`, denoise baixo, comparação A/B e redução para exatamente 4096 × 3072.
- Restrição: é restauração aprendida, não recuperação de informação verdadeira. Letras, emblemas, faróis e rodas devem ser comparados e podem ser recolocados da camada protegida.

### Laboratório controlado

#### Marigold

- Repositório: https://github.com/prs-eth/Marigold
- Funções úteis: normais de superfície; decomposição em albedo, shading e residual não difuso; estimativa de roughness e metallicity.
- Ganho esperado: separar cor/material da iluminação, evitando que o GPT transforme o cinza metálico em uma superfície lisa ou plástica.
- Licença: código Apache-2.0; pesos usam licença própria RAIL++-M e precisam de revisão jurídica antes de produção comercial.
- Uso recomendado: gerar mapas auxiliares e métricas, nunca substituir diretamente os pixels do carro.

#### IC-Light

- Repositório: https://github.com/lllyasviel/IC-Light
- Licença do código: Apache-2.0.
- Função: gerar uma hipótese coerente de relighting condicionada pelo fundo do estúdio.
- Correção da avaliação anterior: o repositório informa que o BRIA RMBG 1.4 do demo é não comercial, mas permite substituí-lo por outro recortador. O projeto Garage 665 já usa BiRefNet.
- Restrição operacional: fluxo orientado a CUDA/Linux; não deve ser instalado no ambiente principal do Mac M5.
- Uso seguro: extrair do candidato apenas um campo de iluminação de baixa frequência. Não usar a saída RGB como carro final, pois o modelo pode alterar material e detalhes.

#### libcom

- Repositório: https://github.com/bcmi/libcom
- Licença do projeto: Apache-2.0; revisar cada peso usado.
- Módulos úteis: PCTNet/LBM para harmonização, HarmonyScore para pontuação, GPSDiffusion para sombra e localização de regiões incompatíveis.
- Uso seguro: laboratório Linux isolado. Comparar e pontuar composições; aplicar correções leves por máscara. Não aceitar reposicionamento, mudança de pose ou reconstrução integral.

#### DiffusionLight

- Repositório: https://github.com/DiffusionLight/DiffusionLight
- Licença do código: MIT.
- Função: estimar um HDR environment map a partir do estúdio vazio.
- Ganho esperado: transformar a direção de luz do estúdio em uma referência única para teto, capô e lateral, evitando faixas de softbox contraditórias.
- Restrição: CUDA/OpenEXR e dependências de difusão; laboratório, não núcleo do Mac.

## Ferramentas descartadas

- `Haian-Jin/Neural_Gaffer`: o próprio projeto informa resolução-base de 256 × 256 e falhas de identidade em objetos detalhados. Inadequado para rodas, faróis, emblemas e pintura automotiva.
- `Fanghua-Yu/SUPIR`: a licença proíbe uso comercial sem acordo específico. Não integrar no projeto de cliente.
- `DSINE`: tecnicamente bom para normais, mas a licença dos artefatos disponíveis precisa de revisão e o Marigold oferece mais mapas no mesmo conjunto.
- geração integral por ControlNet, FLUX, ComfyUI ou vista sintética: continua excluída como fonte final porque aumenta deriva entre ângulos.

## Arquitetura proposta v6

### 1. Fonte

- Solicitar o arquivo original do telefone/câmera, sem WhatsApp, sempre que possível.
- Converter uma cópia para sRGB e 2048 × 1536.
- Preservar o original e seus hashes.

### 2. Máscaras por material e painel

- `M10-teto-pintura`;
- `M11-capo-centro`;
- `M12-capo-laterais`;
- `M13-paralama-proximo`;
- `M14-portas-superiores`;
- `M15-portas-inferiores`;
- `M16-para-brisa`;
- `M17-vidros-laterais`;
- `M18-cromados-e-espelho`;
- `M19-detalhes-protegidos`.

Capô e lateral não devem mais ser tratados como polígonos enormes. Separar os painéis permite que cada reflexo acompanhe sua curvatura e evita a aparência de pintura fosca ou faixa triangular.

### 3. Pacote de referências por chamada

- Imagem 1: fotografia de autoridade, única fonte de geometria e identidade;
- Imagem 2: estúdio vazio oficial `STUDIO_G`;
- Imagem 3: referência da mesma Panamera/cor, apenas para conferir material e pigmento;
- Imagem 4: mapa de normais ou profundidade, explicitamente descrito como guia geométrico e não como aparência;
- máscara alfa aplicada somente à Imagem 1.

### 4. Rig de iluminação congelado

- key light: softbox muito grande, acima e à esquerda da câmera, fora do quadro;
- reflexão da key: fita ampla, curva e contínua; bordas suaves; nunca triângulo reto ou retângulo branco;
- fill direito: aproximadamente dois stops abaixo da key;
- preenchimento frontal: fraco, suficiente apenas para grade e para-choque;
- piso: bounce neutro de baixa intensidade;
- parede, luz e piso: temperatura de cor neutra consistente;
- nenhum céu, nuvem, prédio, cabo, árvore, pessoa, automóvel ou faixa amarela.

### 5. Edição GPT Image 2

- modelo fixado: `gpt-image-2-2026-04-21`;
- `quality="high"`;
- `input_fidelity`: omitir;
- `size="2048x1536"` para o piloto 4:3;
- `output_format="png"`;
- uma superfície por chamada;
- dois candidatos por superfície; nunca acumular uma tentativa reprovada;
- a referência de estúdio e o texto do rig permanecem idênticos em todas as chamadas.

### 6. Preservação de detalhe

Não inserir a saída do GPT diretamente com 100% de opacidade. O novo compositor deve:

1. realinhar a saída ao original;
2. remover reflexos semânticos apenas dentro da máscara;
3. extrair do original uma camada de microdetalhe de alta frequência;
4. bloquear bordas de reflexos urbanos para que fios/prédios não retornem;
5. recolocar grão metálico, textura, pequenos relevos e vincos protegidos;
6. transferir apenas o campo de iluminação de baixa frequência do IC-Light/GPT;
7. aplicar feather interno guiado por borda, sem halo externo;
8. medir cor e nitidez antes/depois.

### 7. Integração e 4K

- executar PCTNet/HarmonyScore apenas como comparação de laboratório;
- criar sombra física separada por pneus, underbody e projeção ampla;
- manter logo e tampa-placa determinísticos;
- testar Real-ESRGAN somente depois da aprovação do master 2048 × 1536;
- gerar 4096 × 3072 e, a partir dele, Story e Webmotors.

## Prompt-base recomendado por superfície

```text
ROLE OF EACH INPUT
Image 1 is the authority source. It is the only authority for the exact vehicle,
camera, perspective, paint color, body geometry and equipment.
Image 2 is the exact target studio and the authority for illumination direction,
neutral color temperature and reflected environment.
Image 3 is identity/material reference only for this same vehicle and paint;
do not copy its camera, background, exposure or reflections.
Image 4 is a surface-normal/depth guide only; do not reproduce its colors.

EDIT SCOPE
Change only the transparent area of the supplied mask: [SURFACE NAME].
Keep every other pixel and object unchanged.

TARGET
Remove identifiable outdoor reflections from this surface and reconstruct the
same photographed metallic dark-gray paint under the exact studio lighting of
Image 2. Preserve the original panel curvature, shut lines, creases, metallic
flake, clear-coat depth, microtexture, local exposure and paint hue.

LIGHTING
Reflect one very large overhead-front-left diffused softbox as a broad curved
ribbon that follows the surface normals continuously. Use soft highlight rolloff,
no clipped white, and a right-side fill about two stops weaker. Add only weak
neutral floor bounce. The highlight must change width and intensity gradually
across the panel and continue naturally toward neighboring panels.

FORBIDDEN
No sky, cloud, tree, building, cable, pole, person, car, yellow pavement line or
recognizable outdoor object. No straight triangular highlight, pasted rectangle,
hard light-strip, mirror finish, matte/flat paint, plastic CGI surface, excessive
denoise, artificial sharpening or invented detail.

INVARIANTS
Do not change the Porsche model, silhouette, proportions, panel boundaries,
headlights, wheels, tires, brakes, badges, lettering, sensors, grille, mirror,
glass shape, camera angle, framing or background. Do not recolor the vehicle.
```

## Ordem recomendada do próximo piloto

1. Corrigir teto e vidros laterais, ainda incompatíveis com o estúdio.
2. Refazer capô em três máscaras guiadas por normais, eliminando a faixa triangular.
3. Refazer lateral em upper/lower doors e para-lama, mantendo continuidade.
4. Harmonizar para-choque, espelho e cromados com intensidade baixa.
5. Compor no estúdio e ajustar a sombra.
6. Rodar avaliação lado a lado e aprovar em 100% e 200%.
7. Testar super-resolução controlada.
8. Congelar o preset v6 e somente então expandir para os outros ângulos.

