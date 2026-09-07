# Continuidade do projeto Garage 665

Atualizado em 06/09/2026. Este documento é o ponto de entrada para continuar o trabalho em outra conta ou computador.

## Situação real

O projeto está em piloto técnico e nenhuma imagem está aprovada para publicação. O foco atual é a vista `dianteira-3-4` da Panamera. O Studio H, a geometria do veículo, as máscaras, o doador bruto já pago e todas as tentativas locais v6f estão preservados no repositório.

O último doador do GPT Image 2 foi registrado com 1.164 correspondências, 86,60% de inliers, erro P95 de 1,707 px e deslocamento máximo de 0,281 px. Nenhum pixel fora da máscara foi alterado. O RGB e a textura fina gerados pela IA não são usados na recomposição.

Ainda não existe imagem aprovada para publicação. O capô v25 foi aprovado visualmente pelo usuário e é a base congelada da etapa atual. A lateral v11 passou nos gates automáticos, mas foi reprovada visualmente pelo usuário porque a pintura continuou fosca. Está autorizada uma nova chamada paga isolada para M13; M14 e M15 continuam bloqueadas até a aprovação humana de M13.

## Próximo passo exato

1. Disponibilizar `OPENAI_API_KEY` no mesmo Terminal da execução.
2. Executar uma única vez `./scripts/executar_teste_m13_api_v6f.sh`.
3. Abrir em 100% `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13-paralama-proximo-api-v02/candidato-quadro-completo.png`.
4. Registrar aprovação ou rejeição visual explícita de M13; não liberar M14 antes disso.
5. Não chamar novamente a API para o capô nem sobrescrever qualquer doador existente.
6. Somente após M13, M14, M15, teto e vidros aprovados, produzir o master 4096 × 3072 e derivar os demais formatos.

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
