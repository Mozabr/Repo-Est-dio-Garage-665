# Comece aqui — retomada do projeto Garage 665

Este arquivo permite continuar o projeto sem acesso ao chat original. Leia também `HANDOFF.md` e `ESTADO-ATUAL.md` antes de alterar qualquer imagem.

## Objetivo permanente

Criar uma série padronizada de fotografias da Garage 665 com aparência de estúdio profissional, preservando a identidade documental de cada carro. O veículo não pode ser redesenhado, reinterpretado, envelopado ou transformado em um modelo apenas parecido.

## Estado no momento da transferência

- Veículo: Porsche Panamera E-Hybrid cinza metálico.
- Vista em desenvolvimento: dianteira 3/4.
- Estúdio ativo: Studio H.
- Etapa: material da pintura v6f, com foco no capô.
- Resultado final: ainda não aprovado para publicação.
- Doador do GPT Image 2: já gerado e arquivado; não repetir a chamada paga.
- Capô: variantes locais v08–v20 preservadas; v18 e v20 são as primeiras comparações recomendadas.
- Lateral: máscaras M13, M14 e M15 preparadas, mas bloqueadas até a aprovação do capô.
- Vidros: devem manter transparência real e apenas reduzir reflexos; não escurecer artificialmente.
- Logo: arte oficial aplicada por composição sobre placa física matte com quatro fixadores; nunca pedir para a IA recriar o logo.
- Tampa-placa: aplicação por perspectiva limitada ao quadrilátero medido na fotografia.

## Arquivos que devem ser abertos primeiro

1. Fotografia/crop de autoridade:
   `trabalhos/panamera/refinamento-dianteira-v6e/preparo/alvo-crop-2048x1024.png`
2. Candidato local v18:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v18-crop.png`
3. Candidato local v20:
   `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v20-crop.png`
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

A variante v20 passa nos controles atuais de cromia média, proporção de cromia, estrutura intermediária, baixa frequência, microtextura, amplitude luminosa, clipping, contenção e origem do material. Ela falha somente na métrica de diferença média de matiz por pixel: 6,326° contra limite de 3°.

Essa falha não deve ser simplesmente ignorada. A hipótese registrada é que a comparação pixel a pixel se tornou incompatível com o filtro espacial aplicado ao `a/b`. A próxima implementação deve acrescentar uma métrica robusta de direção cromática do basecoat, preservando o controle atual durante a validação e documentando a alteração.

## Ordem obrigatória de continuação

1. Comparar fonte, v18 e v20 em 100%, principalmente centro do capô, transição junto ao para-brisa, vincos, emblema e encontro com os para-lamas.
2. Corrigir e testar a métrica de matiz sem relaxar os outros gates.
3. Gerar novas variantes apenas por recomposição local com o doador existente.
4. Selecionar um candidato do capô somente quando passar por validação técnica e visual.
5. Reintegrar o capô aprovado no quadro 2048 × 1536, comprovando zero mudança fora da máscara.
6. Tratar a lateral na ordem M13, M14 e M15, sempre partindo da mesma fonte de autoridade.
7. Validar rodas, esterçamento, pneus, pinças, faróis, emblemas, badge E-Hybrid, maçanetas, vãos e vidros por comparação com a fonte.
8. Criar um único master 4096 × 3072.
9. Derivar Feed, Story horizontal e Webmotors desse mesmo master.
10. Só marcar como entrega depois de aprovação humana explícita.

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

