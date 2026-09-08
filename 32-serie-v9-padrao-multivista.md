# Série Panamera v9 — padrão multivista Studio H

Atualizado em 07/09/2026. Estado: perfil em calibração; nenhuma nova master liberada.

## Regra de consistência

Todas as externas e internas devem pertencer ao mesmo ensaio Studio H. Isso não
significa copiar o mesmo desenho de reflexo entre ângulos: o reflexo do teto deve
se deslocar com a câmera e com a orientação de cada painel. Permanecem congelados
o rig a 5200 K, a key ampla acima/frente/esquerda, o fill direito cerca de -2 EV,
o bounce neutro discreto, o ciclorama, o piso, a placa física e o logo oficial.

Cada vista usa três autoridades independentes:

1. fotografia original: identidade, geometria, peças, cor-base e microtextura;
2. master v07 aprovada: direção de luz e leitura do verniz;
3. Studio H: ambiente, temperatura, piso, parede e marca.

A resposta de imagem nunca é publicada diretamente. Ela é doadora de luz; a
recomposição descarta RGB e textura gerados, preserva os pixels de detalhes e
exige zero alteração fora da união revisada.

## Calibração do perfil

O perfil foi escolhido primeiro porque expõe teto, ombro, portas e vidros em uma
única vista. O doador visual de diagnóstico acertou a linguagem de estúdio, mas
deslocou o quadro em 25,880 px. Foi arquivado, nunca promovido a entrega.

A recomposição v02 usa luminância alinhada de baixa/média frequência, devolve a
microtextura da fotografia e neutraliza a reflexão amarela inferior com a própria
porta superior como referência cromática. Passou nos gates:

- 1.240 correspondências e 71,69% de inliers;
- zero pixel alterado fora da máscara;
- diferença luminosa média 3,748 Lab L e P95 10;
- 0,039% de novos quase-brancos;
- cromia resultante 87,15% da fonte, com redução localizada da contaminação externa.

Arquivos:

- comparação: `trabalhos/panamera/serie-v9/perfil/comparacao-perfil-v01.jpg`;
- candidato contido v02: `trabalhos/panamera/serie-v9/perfil/candidato-v02-material/candidato-perfil-v01.png`;
- relatório: `trabalhos/panamera/serie-v9/perfil/candidato-v02-material/qa-perfil-v01.json`;
- prompt: `prompts/v9/perfil-doador-studio-h-v01.txt`.

O doador atual foi criado pela ferramenta integrada somente para validar a
arquitetura. O caminho oficial pelo snapshot GPT Image 2 da API está preparado e
ainda não foi executado, pois a chave do Terminal do usuário não está disponível
no processo Codex. Com a chave disponível no Terminal:

```bash
./scripts/executar_perfil_serie_v9_api.sh
```

O comando tem trava de cobrança: se a resposta bruta já existir, ele encerra sem
fazer nova chamada.

## Externas restantes

Depois da aprovação do perfil API, repetir a arquitetura por vista, nesta ordem:

1. perfil;
2. frontal;
3. dianteira 3/4 oposta;
4. traseira 3/4;
5. traseira 3/4 oposta;
6. perfil oposto.

Cada ângulo precisa de máscara própria de pintura, vidro e detalhes. Não reutilizar
polígonos do perfil em outra câmera. O tampa-placa é aplicado deterministicamente
depois da recomposição.

## Interiores

O interior não será recortado e colocado numa sala. Painel, volante, bancos,
costuras, telas, instrumentos e materiais permanecem integralmente da fotografia.
O Studio H aparece apenas de forma plausível nas áreas externas visíveis por
para-brisa/janelas e como reflexão larga e suave em telas, black piano e metais.

Fluxo por interior:

1. máscara exclusiva do exterior visto através do vidro;
2. máscara independente de reflexos em superfícies brilhantes;
3. proteção absoluta de textos, instrumentos, telas, brasões, botões e costuras;
4. composição do ambiente neutro Studio H através do vidro;
5. correção luminosa localizada a 5200 K;
6. aprovação em preview antes da master.

Não inserir placa/logo no enquadramento interno quando a câmera não aponta para a
parede correspondente; consistência física vale mais que repetir a marca em toda
foto.
