# Continuidade do projeto Garage 665

Atualizado em 07/09/2026. Este documento é o ponto de entrada para continuar o trabalho em outra conta ou computador.

## Situação real

A vista `dianteira-3-4` da Panamera foi aprovada visualmente na harmonização v07
e exportada em `entregas/panamera-v8-aprovada/dianteira-3-4`. As seis externas
restantes e as três internas estão em preview e ainda não foram aprovadas como
masters. O Studio H, a geometria do veículo, as máscaras, os doadores brutos já
pagos e todas as tentativas locais v6f/v8 estão preservados no repositório.

O último doador do GPT Image 2 foi registrado com 1.164 correspondências, 86,60% de inliers, erro P95 de 1,707 px e deslocamento máximo de 0,281 px. Nenhum pixel fora da máscara foi alterado. O RGB e a textura fina gerados pela IA não são usados na recomposição.

Por decisão explícita do usuário, o M11 v6 passou a ser a autoridade visual e
geométrica do quadro v8. A candidata
`trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v07-clearcoat-final/candidato-quadro-completo.png`
foi aprovada; os doadores integrais já estão arquivados e não devem ser gerados
novamente. Processo e saídas em `31-master-v8-e-previews-serie.md`.

## Próximo passo exato

1. Ler `30-harmonizacao-integral-v8.md` e `31-master-v8-e-previews-serie.md`.
2. Não refazer a v07 nem a master dianteira 3/4: ambas já estão concluídas.
3. Abrir `trabalhos/panamera/previews-serie-v8/01-previews-externas.jpg` e `02-previews-interiores.jpg`.
4. Obter aprovação humana dos ângulos e seleções antes de criar novas masters.
5. Adaptar o tratamento v07 separadamente a cada externa aprovada, preservando todo elemento fora da máscara.
6. Nas internas, manter o interior original e decidir separadamente qualquer tratamento do ambiente visível pelos vidros.

## Não repetir a chamada paga

O arquivo abaixo já existe e é o doador pago válido do capô:

`trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/doador-especular-bruto-api.png`

O script `scripts/executar_teste_capo_v6f.sh` bloqueia uma segunda execução quando encontra esse arquivo. O novo script M13 possui uma trava independente: depois de criar `M13-paralama-proximo-api-v02/doador-bruto-api-rejeitado-como-imagem.png`, ele também bloqueia qualquer repetição paga.

## Regras que não podem mudar

- O carro é documento; o estúdio é direção de arte.
- Geometria, rodas, esterçamento, faróis, emblemas, vidros, maçanetas, vãos, badges e proporções vêm da fotografia Garage 665.
- A fotografia-base fornece a direção de cor Lab a/b e toda a microtextura.
- A IA pode fornecer apenas luminância alinhada em uma máscara de superfície.
- O exterior da máscara precisa ter zero pixels alterados.
- A pintura deve parecer metálica com verniz polido, nunca fosca, acetinada ou envelopada.
- Vidros mantêm a transparência original e recebem apenas redução plausível de reflexos.
- A arte oficial do logo é composta depois; não deve ser redesenhada pela IA. A placa da parede precisa ser matte, fisicamente afastada e fixada por quatro suportes discretos.
- Tampa-placa deve respeitar exatamente o quadrilátero medido na foto.
- Uma superfície por chamada e aprovação antes de avançar.
- Não gerar cada formato separadamente.

## Padrão de saída congelado

- Master e Feed: 4096 × 3072, 4:3.
- Story: 3840 × 2160, 16:9 horizontal.
- Webmotors: 1920 × 1440, 4:3 horizontal.
- Todas as saídas derivam do mesmo master aprovado.

Os JPEGs originais da Panamera têm 1280 × 960. Portanto, a saída 4K é uma ampliação controlada, não detalhe nativo de câmera. Não prometer fidelidade física absoluta de cor sem RAW e cartela de cor.

## Instalação em outro computador

Requisitos: macOS ou Linux, Git, Python 3.11 e espaço para aproximadamente 1 GB de pesos locais. Na raiz do clone:

```bash
bash scripts/configurar_novo_computador.sh
```

Os ambientes virtuais e pesos não são enviados ao GitHub. O script recria os dois ambientes e baixa versões fixadas/validadas de BiRefNet, ViTMatte, Depth Anything V2 Small e SAM 2.1 Small. Se a API for necessária em uma etapa futura, configure `OPENAI_API_KEY` somente no ambiente local; nunca em arquivo versionado.

## Mapa do projeto

- `ESTADO-ATUAL.md`: histórico técnico completo e limitações.
- `27-pipeline-material-v6f.md`: arquitetura v6f.
- `config/pipeline-v6f.json`: regras da chamada do capô.
- `config/perfil-material-v6f.json`: perfil experimental atual e gates.
- `config/superficies-carroceria-v6f.json`: máscaras e ordem da lateral.
- `config/rig-iluminacao-studio-v6b.json`: rig de luz congelado.
- `prompts/v6f/`: prompts e manifesto com hashes.
- `estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png`: sala ativa.
- `referencias/originais-panamera/`: as dez fotografias recebidas.
- `referencias/panamera-cor-estudio/`: referências classificadas; a referência azul é proibida para cor.
- `trabalhos/panamera/refinamento-dianteira-v6f/`: doador, tentativas, máscaras e relatórios.
- `integracoes/`: fontes, revisões, licenças e hashes dos modelos.

## Comandos seguros de validação

O fluxo determinístico anterior, que não usa API, pode ser repetido com:

```bash
bash scripts/executar_studio_v2.sh
```

Ele serve para validar ambiente e composição, não para substituir a aprovação do v6f. Antes de qualquer nova chamada paga, leia o relatório `qa-api.json` e confirme se o doador necessário já está arquivado.
