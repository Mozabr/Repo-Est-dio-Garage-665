# Projeto de Tratativa de Imagens — Garage 665

> **Retomada em outra conta/computador:** comece por [COMECE-AQUI.md](COMECE-AQUI.md), leia [HANDOFF.md](HANDOFF.md) e a [harmonização integral v8](30-harmonizacao-integral-v8.md). Por decisão explícita do usuário, o M11 v6 é a autoridade visual e geométrica do quadro em desenvolvimento. A candidata atual é a v03; não repetir chamadas pagas já arquivadas.

## Fluxo ativo — estúdio v2 (06/09/2026)

Retomada registrada em [ESTADO-ATUAL.md](ESTADO-ATUAL.md): sete vistas externas,
21 exportações e duas tampa-placas com revisão pendente. Consultar esse arquivo
antes de continuar; ele diferencia o concluído das limitações ainda abertas.

O fluxo ativo foi substituído após a reprovação dos pilotos generativos. Use:

```bash
bash scripts/executar_studio_v2.sh
```

Integrações executadas: BiRefNet + ViTMatte, OpenCV com alpha premultiplicado,
Colour Science e detecção de ColorChecker por segmentação. Os snapshots dos
modelos e seus hashes estão em `integracoes/modelos-lock.json`.

O novo estúdio usa uma placa retangular com espessura, quatro fixadores e sombra
de afastamento da parede. A arte oficial é aplicada por composição no master.
Confira `17-estudio-v2.md` e `trabalhos/panamera/studio-v2/serie-comparativa.jpg`.

**Estado: piloto técnico, não aprovado para publicação.** As fotos da Panamera
são JPEGs de 1280 × 960 e ainda contêm reflexos urbanos. Preservar seus pixels
não equivale a remover esses reflexos nem a certificar a cor física da pintura.
A exportação 4096 × 3072 é ampliada; não é detalhe nativo 4K.

O comando antigo `finalizar_piloto_panamera.sh` também encaminha para o fluxo
local v2, sem chamadas pagas. As recomendações de versões v05–v13 e os estados
"aprovado" abaixo são registros históricos, superados por esta seção.

## Objetivo

Criar um padrão fotográfico premium e reconhecível para a Garage 665 sem que os veículos pareçam recortados ou gerados por inteligência artificial.

O princípio central é simples: **o carro é documento; o ambiente é direção de arte**. Carroceria, rodas, pneus, faróis, emblemas, placas, vidros, interior, proporções e sinais reais de uso nunca devem ser reinventados.

## Diagnóstico inicial

- O feed atual da Garage 665 tem boa intenção de padronização, mas o fundo cinza repetitivo, a iluminação uniforme e alguns recortes/reflexos fazem o carro parecer inserido em um cenário sintético.
- A referência Cavalli Motors trabalha melhor a percepção de valor por meio de enquadramentos fechados, textura real, contraste controlado e detalhes do veículo.
- As 30 imagens recebidas têm resolução suficiente para um fluxo premium: 10 fotos do CLA 250, 10 do Porsche 991 e 10 da Rampage, todas com 4032 × 3024 px.
- O material original contém bons detalhes, mas há luz solar dura em parte das fotos, reflexos de fachada, outros veículos, QR code e comunicação visual de outra loja.

## Direção recomendada

1. Fotografar o veículo de forma consistente, mesmo nos três locais.
2. Corrigir luz, cor, perspectiva e distrações antes de qualquer recurso generativo.
3. Usar IA apenas de forma localizada para limpeza de fundo — nunca para redesenhar o carro.
4. Na produção definitiva, priorizar fundos reais fotografados na Garage 665 e composições com máscara precisa.
5. Exportar nos padrões aprovados: feed 4:3, Story 16:9 horizontal e Webmotors 1920 × 1440 px.

## Entregáveis deste início de projeto

- Direção visual e regras de preservação.
- Protocolo de captação para os três locais.
- Fluxo de produção e exportação.
- Prompt-base para limpeza localizada.
- Checklist de qualidade.
- Piloto do Porsche 991 para validar a direção.

## Estrutura

- `01-direcao-visual.md`: aparência, composição e limites.
- `02-protocolo-captacao.md`: como fotografar em cada local.
- `03-fluxo-producao.md`: processo da entrada à entrega.
- `04-prompt-base.md`: especificação reutilizável de edição.
- `07-prompt-mestre-estudio-branco.md`: prompt definitivo para o novo estúdio Garage 665.
- `08-fluxo-estudio-recorrente.md`: processo para receber e tratar novos veículos.
- `10-padroes-de-saida.md`: dimensões e proporções para feed, Story e Webmotors.
- `11-padrao-tampa-placa.md`: desenho e aplicação do tampa-placa oficial Garage 665.
- `12-analise-panamera-conjunto-completo.md`: leitura técnica das dez fotografias do veículo.
- `13-prompt-frontal-final.md`: prompt e acabamento aprovados para a vista frontal.
- `14-protocolo-serie-fiel.md`: protocolo consolidado para impedir deriva entre ângulos, padronizar o tampa-placa e fixar as três saídas obrigatórias.
- `15-integracoes-e-montagem.md`: arquitetura aprovada, repositórios selecionados e implantação completa do pipeline.
- `16-piloto-panamera-sam2.md`: estado do piloto, comando único e critérios de aprovação.
- `config/pipeline.json`: regras e parâmetros bloqueados da produção.
- `integracoes/repositorios-aprovados.json`: registro auditável das dependências e exclusões.
- `prompts/`: prompts operacionais separados por máscara e finalidade.
- `scripts/editar_com_gpt_image_2.py`: chamada única de edição mascarada pela API.
- `scripts/editar_com_gpt_image_2.py` reaplica a resposta somente dentro da máscara; fora dela, os pixels originais ficam travados.
- `scripts/preparar_entrada.py`: normaliza a cópia de trabalho em PNG 3264 × 2448.
- `scripts/criar_mascara_inicial.py`: cria um rascunho de máscara e uma prévia para revisão manual.
- `scripts/criar_mascara_sam2.py`: cria a máscara de produção do carro com o SAM 2 oficial.
- `scripts/criar_mascara_poligonos.py`: cria máscaras localizadas e auditáveis para reflexos.
- `scripts/compor_estudio.py`: combina o carro preservado com uma placa-mestre fixa e sombra-base.
- `scripts/aplicar_tampa_placa.py`: aplica o tampa-placa no quadrilátero medido da foto.
- `scripts/aplicar_logo_parede.py`: monta o logo oficial como placa física no master 4K.
- `scripts/criar_master_4k.py`: amplia o resultado 4:3 aprovado para o master 4096 × 3072.
- `scripts/finalizar_piloto_panamera.sh`: executa a única chamada de API e gera todas as entregas do piloto.
- `scripts/exportar_formatos.py`: deriva Feed, Story horizontal e Webmotors do mesmo master.
- `requirements-core.txt`: dependências leves do fluxo principal.
- `requirements-mask.txt`: ambiente isolado Python 3.11 para SAM 2 e PyTorch.
- `05-checklist-qualidade.md`: aprovação técnica e visual.
- `06-inventario-referencias.md`: leitura das 30 imagens recebidas.
- `pilotos/`: original e primeira prova de conceito.
- `assets/`: arquivos oficiais de marca usados como referência.
- `estudio-mestre/`: placas aprovadas da sala branca Garage 665.
- `fundos-reais/`: espaço reservado para as placas reais de ambiente.
- `entregas/`: arquivos finais aprovados.

## Referências observadas

- [Garage 665](https://www.instagram.com/garage_665/)
- [Cavalli Motors](https://www.instagram.com/cavalli_motors/)

Análise realizada em 4 de setembro de 2026.

O prompt de estúdio foi atualizado com princípios selecionados da biblioteca [awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2): papéis explícitos para cada imagem de entrada, variáveis reutilizáveis, descrição física do ambiente, câmera e iluminação, preservação detalhada do produto, composição definida e lista objetiva de falhas proibidas.

## Estado atual

- Logo oficial recebido e arquivado em `assets/logo-garage-665-transparente.png`.
- Transparência confirmada; arquivo PNG sRGB de 1080 × 1080 px.
- Nova placa `STUDIO_A` profissional criada em 4:3, com ciclorama, piso e equipamentos de iluminação fisicamente plausíveis.
- Fluxo validado com o Porsche 991 em `pilotos/porsche-991-estudio-branco-logo-v01.png`.
- Comparativo de processo disponível em `pilotos/comparativo-fluxo-estudio-v01.jpg`.
- Primeiro teste com veículo oficial da Garage 665 concluído em `pilotos/panamera-oficial/`.
- Para a Panamera, a versão recomendada de ambiente e marca passou a ser `panamera-estudio-limpo-placa-v05.png`.
- O logo oficial nunca mais será regenerado: a sala e o carro são produzidos com parede vazia, e o PNG aprovado é aplicado depois como placa física.
- Softboxes, painéis, trilhos, luminárias e qualquer equipamento de estúdio ficam obrigatoriamente fora do enquadramento.
- Tampa-placa oficial criado em `assets/tampa-placa/tampa-placa-garage-665-horizontal-v03.png`, com prova aplicada à Panamera.
- Novo padrão obrigatório: master e Feed 4096 × 3072, Story horizontal 3840 × 2160 e Webmotors horizontal 1920 × 1440.
- Primeiro teste técnico de dimensões 4K da Panamera disponível em `entregas/panamera-oficial-4k/`; a reconstrução de detalhe nativo depende do arquivo original sem compressão de WhatsApp.
- A versão recomendada da Panamera passou a ser a v13, com verniz metálico calibrado pela fotografia real do veículo, microtextura artificial reduzida e logo oficial montado diretamente no master 4K como placa rígida fixada próxima à parede.
- O teste frontal consolidado está em `entregas/panamera-frontal-4k/porsche-panamera-frontal-master-4096x3072-v02.png`.
