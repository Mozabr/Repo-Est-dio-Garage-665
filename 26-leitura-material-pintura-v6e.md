# Leitura do material da pintura — v6e

Status: diagnóstico concluído; nenhuma nova geração executada nesta etapa.

## Arquivos analisados

- Base fotográfica: `refinamento-dianteira-v6e/preparo/alvo-crop-2048x1024.png`.
- Resposta integral v6e: `teste-capo-crop/diagnostico-resposta-integral-nao-usar.png`.
- Máscara: `preparo/mascara-editar-2048x1024.png`.
- Lateral original no Studio H: máscaras M13, M14 e M15 projetadas no quadro.

A resposta v6e continua formalmente rejeitada pelo registro geométrico: 938
correspondências, 79,42% de inliers e 10,36 px de deslocamento contra limite de
8 px. Seu aspecto pode orientar a próxima luz, mas seus pixels não devem ser
integrados ao master.

## Capô: evidência quantitativa

| Medida dentro do capô | Base | Gerado v6e | Leitura |
| --- | ---: | ---: | --- |
| Lab L médio | 145,42 | 165,48 | pintura globalmente clareada |
| Amplitude L p95–p05 | 83 | 116 | faixa de luz excessiva |
| Desvio de luz ampla | 17,25 | 34,85 | fonte dominante demais |
| Estrutura intermediária RMS | 17,78 | 9,30 | perda de relevo/verniz |
| Microtextura RMS | 2,72 | 5,35 | grão sintético quase duplicado |
| Cromia média | 12,86 | 2,08 | perda de aproximadamente 84% |
| Pixels quase brancos, L ≥ 240 | 0,003% | 4,83% | highlight perto do clipping |

O resultado não é simplesmente “pouco brilhante”. Ele combina uma mancha ampla
muito clara com regiões neutralizadas e uniformes. A transição macia demais,
somada à perda de cromia e de estrutura intermediária, faz o material parecer
vinil satin ou envelopamento. O grão fino maior não recupera o metallic flake:
ele se distribui de modo homogêneo e lê como ruído gerado.

## Lateral: estado atual

As máscaras M13–M15 somam 94.857 pixels. A amplitude luminosa conjunta chega a
173 Lab L. A parte superior das portas tem L médio 52,24, enquanto a parte
inferior chega a 120,77. Essa diferença vem da reflexão externa clara do chão,
fachada e linhas do estacionamento. A estrutura intermediária RMS da região
inferior é 48,87, muito acima dos 24,25 da região superior.

Visualmente, a lateral ainda contém uma faixa clara literal do ambiente externo.
Se o capô for neutralizado isoladamente, o carro continuará parecendo composto:
o capô responde como satin neutro e a lateral como verniz espelhando a rua.

## O que deve ser preservado

1. Pigmento/basecoat: tom cinza original, com pequena variação fria natural e
   limite de cromia; não usar RGB gerado como autoridade de cor.
2. Metallic flake: microdetalhe extraído da fotografia, não ruído criado pela IA.
3. Clear-coat: contraste especular intermediário, com uma faixa principal ampla,
   borda controlada e uma reflexão secundária mais fraca.
4. Geometria: vincos, linha central óptica, folgas, emblema, faróis, portas,
   rodas e câmera permanecem na fotografia-base.

## Arquitetura recomendada para a próxima versão

### Capô

Usar a resposta da IA somente como mapa de iluminação e reflexo, nunca como RGB
final. Extrair a luminância alinhada em bandas: luz ampla e resposta especular
intermediária. Recombinar essas bandas com cromia e microtextura da fotografia.
Rejeitar toda frequência fina criada pelo modelo.

Metas iniciais para validação:

- cromia média entre 5 e 9, sem queda para cinza neutro absoluto;
- estrutura intermediária RMS entre 13 e 17;
- microtextura RMS entre 2,5 e 3,2;
- amplitude p95–p05 entre 65 e 90 Lab L;
- pixels com L ≥ 240 abaixo de 0,25%;
- delta máximo de cor-base condicionado por CIEDE2000;
- uma reflexão principal e uma secundária, sem retângulo, cunha ou mancha única.

### Lateral

Processar paralama, portas superiores e portas inferiores separadamente, mas sob
um único rig. Substituir a faixa literal do chão por um gradiente horizontal de
wall-bank. Preservar folgas, maçanetas e emblema `e-hybrid` por máscara negativa.
Normalizar as sobreposições para não somar intensidade nas bordas.

### Continuidade capô–lateral

Criar um perfil único de material da pintura com limites de Lab, microtextura e
contraste especular. O capô recebe principalmente a softbox superior; a lateral,
principalmente o wall-bank. A direção muda com a normal da superfície, mas
pigmento, metallic flake, balanço de branco e densidade do verniz permanecem os
mesmos.

## Conclusão

O v6e acertou a ideia de remover a rua e produzir uma fonte ampla, mas errou o
modelo de material. O próximo avanço não depende de pedir “mais realismo” no
prompt. Depende de separar basecoat, metallic flake e clear-coat, limitar cada
banda por métricas e aceitar da IA somente o mapa de luz alinhado.
