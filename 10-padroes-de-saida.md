# Padrões de saída — Garage 665

## Regra geral obrigatória

- Toda fotografia aprovada deve partir de um master 4K.
- O master 4:3 obrigatório é 4096 × 3072 px.
- Cada vista aprovada gera exatamente três entregas: Feed 4K 4:3, Story 4K 16:9 horizontal e Webmotors 1920 × 1440 horizontal.
- A exigência de 4K se aplica ao master, Feed e Story. A saída Webmotors permanece em 1920 × 1440 px por ser o padrão operacional definido para a plataforma.
- A ampliação deve usar interpolação de alta qualidade, controle de nitidez e inspeção visual em 100%.
- Não considerar um arquivo como 4K apenas porque suas dimensões foram aumentadas: textura da pintura, emblemas, rodas, faróis, contornos e logo precisam permanecer limpos e naturais.
- Sempre que possível, produzir o tratamento a partir do arquivo original da câmera ou celular, sem compressão de WhatsApp.

## Feed

- Proporção: 4:3.
- Resolução principal: 4096 × 3072 px, horizontal.
- Formato: JPEG sRGB.
- Qualidade: 95–97, amostragem 4:4:4.
- Manter o veículo completo dentro da área segura.

## Story

- Resolução principal: 3840 × 2160 px.
- Orientação: horizontal.
- Proporção: 16:9.
- Formato: JPEG sRGB.
- Qualidade: 95–97, amostragem 4:4:4.

## Webmotors

- Resolução obrigatória: 1920 × 1440 px.
- Orientação: horizontal.
- Proporção: 4:3.
- Formato: JPEG sRGB.
- Qualidade: 95–97, amostragem 4:4:4.

## Master de tratamento

- Preservar em PNG ou TIFF sRGB, com mínimo de 4096 × 3072 px para enquadramentos 4:3.
- Gerar os três formatos sempre a partir do master aprovado.
- Nunca usar um arquivo já comprimido para produzir outro formato.
- Não alterar cor, brilho metálico, flake ou contraste local do veículo entre canais; apenas reenquadrar e redimensionar.

## Convenção de nomes

```text
marca-modelo-ano-angulo-master-v01.png
marca-modelo-ano-angulo-feed-4k-4096x3072-v01.jpg
marca-modelo-ano-angulo-story-4k-3840x2160-v01.jpg
marca-modelo-ano-angulo-webmotors-1920x1440-v01.jpg
```
