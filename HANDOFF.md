# Continuidade do projeto Garage 665

Atualizado em 06/09/2026. Este documento é o ponto de entrada para continuar o trabalho em outra conta ou computador.

## Situação real

O projeto está em piloto técnico e nenhuma imagem está aprovada para publicação. O foco atual é a vista `dianteira-3-4` da Panamera. O Studio H, a geometria do veículo, as máscaras, o doador bruto já pago e todas as tentativas locais v6f estão preservados no repositório.

O último doador do GPT Image 2 foi registrado com 1.164 correspondências, 86,60% de inliers, erro P95 de 1,707 px e deslocamento máximo de 0,281 px. Nenhum pixel fora da máscara foi alterado. O RGB e a textura fina gerados pela IA não são usados na recomposição.

Ainda não existe candidato v6f aprovado para publicação. A v25 é a melhor candidata técnica atual e aguarda aprovação visual humana. Ela acrescenta uma key frontal elíptica apenas em Lab L, concentrada no centro do capô, sem substituir RGB, cromia, geometria ou microtextura da fotografia. Obteve 1,547° no gate agregado de matiz, microtextura RMS 0,734, intervalo luminoso exatamente no limite seguro de 110 e zero alteração fora do capô. A tentativa mais forte de 16 Lab L foi rejeitada pelo gate antes da reintegração; a candidata usa pico de 14 Lab L.

## Próximo passo exato

1. Abrir lado a lado a fonte, v23 e v25 em 100%:
   - `trabalhos/panamera/refinamento-dianteira-v6e/preparo/alvo-crop-2048x1024.png`
   - `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v23-quadro-completo.png`
   - `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v25-quadro-completo.png`
2. Registrar aprovação ou rejeição visual explícita da v25.
3. Não chamar a API outra vez para o capô.
4. Somente depois da aprovação visual do capô, avançar na ordem M13, M14 e M15 da lateral.
5. Somente após capô e lateral aprovados, produzir um master 4096 × 3072 e derivar os outros formatos.

## Não repetir a chamada paga

O arquivo abaixo já existe e é o doador pago válido:

`trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/doador-especular-bruto-api.png`

O script `scripts/executar_teste_capo_v6f.sh` bloqueia uma segunda execução quando encontra esse arquivo. Para os ajustes atuais use somente `scripts/transferir_material_v6f.py`, por meio de uma cópia versionada do perfil, preservando os diagnósticos existentes.

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
