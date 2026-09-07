# Comece aqui — retomada do projeto Garage 665

Este arquivo permite continuar o projeto sem acesso ao chat original. Leia também `HANDOFF.md` e `ESTADO-ATUAL.md` antes de alterar qualquer imagem.

## Objetivo permanente

Criar uma série padronizada de fotografias da Garage 665 com aparência de estúdio profissional, preservando a identidade documental de cada carro. O veículo não pode ser redesenhado, reinterpretado, envelopado ou transformado em um modelo apenas parecido.

## Estado no momento da transferência

- Veículo: Porsche Panamera E-Hybrid cinza metálico.
- Vista em desenvolvimento: dianteira 3/4.
- Estúdio ativo: Studio H.
- Etapa: material da pintura v6f; capô aprovado e M13 v03 aguardando validação visual.
- Resultado final: ainda não aprovado para publicação.
- Doadores do capô e de M13: já gerados e arquivados; não repetir nenhuma chamada paga.
- Capô: v25 aprovada visualmente pelo usuário e congelada como base do quadro.
- Lateral: v11 foi reprovada por continuar fosca; a composição M13 v02 foi reprovada por uma mancha clara e a v03 aguarda validação visual.
- Vidros: devem manter transparência real e apenas reduzir reflexos; não escurecer artificialmente.
- Logo: arte oficial aplicada por composição sobre placa física matte com quatro fixadores; nunca pedir para a IA recriar o logo.
- Tampa-placa: aplicação por perspectiva limitada ao quadrilátero medido na fotografia.

## Arquivos que devem ser abertos primeiro

1. Fotografia/crop de autoridade:
   `trabalhos/panamera/refinamento-dianteira-v6e/preparo/alvo-crop-2048x1024.png`
2. Candidato local v18:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v18-crop.png`
3. Candidato local v25:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v25-quadro-completo.png`
4. Doador bruto já pago:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/doador-especular-bruto-api.png`
5. Métricas v18 e v20:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/qa-material-v6f-v18.json`
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/qa-material-v6f-v20.json`
6. Perfil em desenvolvimento:
   `config/perfil-material-v6f.json`
7. Sala ativa:
   `estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png`

## Leitura técnica já obtida

O doador está geometricamente bem alinhado:

- 1.164 correspondências;
- 86,60% de inliers;
- erro de reprojeção P95 de 1,707 px;
- deslocamento máximo de 0,281 px;
- zero alteração fora da máscara;
- RGB gerado descartado;
- textura fina gerada descartada.

A métrica de matiz foi corrigida sem apagar o diagnóstico antigo. O desvio pixel a pixel continua registrado, mas o gate usa agora a direção cromática agregada e ponderada do basecoat, excluindo os highlights neutralizados do verniz. A v25 passa com 1,547° de desvio agregado, microtextura RMS 0,734 e zero alteração fora do capô.

Histórico da calibração: v21 passou tecnicamente, mas ainda mostrou vestígios direcionais; v22 reduziu esses vestígios e foi reprovada por microtextura insuficiente; v23 recuperou textura fotográfica; v24 introduziu uma key frontal discreta; v25 concentrou e elevou essa key ao limite técnico seguro, sem clipping nem alteração cromática material. O usuário aprovou o capô v25. Na lateral, v01–v04 foram rejeitadas por uniformização e contorno de máscara. A v06 neutralizou somente a reflexão externa quente da metade inferior. As v07–v11 tentaram recuperar o clear-coat localmente, mas a v11 foi reprovada por aparência ainda fosca. O fluxo retorna à arquitetura paga por superfície: M13, depois M14 e M15, com aprovação entre chamadas.

## Ordem obrigatória de continuação

1. Executar uma única vez `./scripts/executar_teste_m13_api_v6f.sh` com `OPENAI_API_KEY` disponível no mesmo Terminal.
2. Abrir `M13-paralama-proximo-api-v03/candidato-quadro-completo.png` em 100% e comparar com o quadro v25 e a fotografia original.
3. Obter aprovação visual humana explícita de M13 antes de liberar M14.
4. Depois de M13, M14 e M15 aprovadas, avançar para teto/vidros, reduzindo reflexos sem escurecer a transparência.
5. Validar rodas, esterçamento, pneus, pinças, faróis, emblemas, badge E-Hybrid, maçanetas e vãos por comparação com a fonte.
6. Criar um único master 4096 × 3072.
7. Derivar Feed, Story horizontal e Webmotors desse mesmo master.
8. Só marcar como entrega depois de aprovação humana explícita.

## O que não fazer

- Não executar novamente `scripts/executar_teste_capo_v6f.sh` enquanto o doador bruto estiver presente.
- Não usar a imagem azul de Panamera como referência de cor.
- Não copiar geometria ou peças de outra Panamera.
- Não aplicar correção global de cor para compensar reflexos locais.
- Não transformar a tinta em acabamento matte ou satin.
- Não preencher o capô ou a lateral com uma cor uniforme.
- Não gerar o carro completo para corrigir uma superfície.
- Não alterar roda, ângulo da roda, altura, proporção, faróis, placa ou cabine.
- Não prometer cor física absoluta: não há RAW nem ColorChecker na captura original.
- Não declarar “4K nativo”: as fontes da Panamera têm 1280 × 960.

## Padrão visual congelado

- Direção da luz: key ampla acima/frente/esquerda; fill direito aproximadamente -2 EV; fill frontal -3 EV; bounce neutro -3,5 EV.
- Balanço de branco de referência: 5200 K.
- Capô: highlight amplo com ombro suave, separação escura controlada e verniz visível; sem faixa dura artificial.
- Lateral: faixa longa superior, volume no centro e bounce neutro discreto embaixo.
- Piso: cinza neutro fosco a levemente acetinado.
- Parede/ciclorama: off-white com textura e transições fotográficas discretas.
- Sombra de contato: coerente com pneus, peso e direção da luz; sem halo de recorte.
- Placa do logo: matte, espessura visível, afastamento curto da parede, sombra curta e quatro fixadores discretos.

## Saídas obrigatórias

- Master e Feed: 4096 × 3072, 4:3.
- Story: 3840 × 2160, 16:9 horizontal.
- Webmotors: 1920 × 1440, 4:3 horizontal.

## Instalação rápida

Depois de clonar o repositório, instalar Python 3.11 e executar:

```bash
bash scripts/configurar_novo_computador.sh
```

Esse comando recria os ambientes e baixa os pesos verificados que não cabem no GitHub. A chave OpenAI deve existir apenas no ambiente local. Para validar o pipeline determinístico sem cobrança:

```bash
bash scripts/executar_studio_v2.sh
```

## Critério de conclusão

O projeto só estará concluído quando todas as vistas aprovadas parecerem pertencer ao mesmo estúdio e ao mesmo carro, com pintura metálica coerente entre ângulos, reflexos plausíveis, detalhes preservados, logo físico natural, tampa-placa medida e três formatos derivados de um master único.
