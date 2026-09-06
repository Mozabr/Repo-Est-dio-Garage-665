# Diagnóstico e direção de tratamento — dianteira-3-4
06/09/2026 · análise da fotografia, não aprovação de uma versão retocada.

## Conclusão
O principal obstáculo não é uma cor errada isolada: são reflexos urbanos
reconhecíveis sobre uma superfície metálica brilhante, além de luz solar que
não corresponde à sala. Um balanço de branco global não resolve isso.
O objetivo deve ser manter a aparência do material e os detalhes reais,
substituindo apenas reflexos incompatíveis — não apagar todo o brilho.

## Base mensurada
- Arquivo original: WhatsApp Image 2025-11-24 at 09.57.06 (1).jpg.
- JPEG RGB de 1280 × 960 com perfil ICC; medições convertidas para sRGB.
- Sem metadados úteis de câmera, exposição, focal ou balanço de branco.
- Caixa do carro na máscara: x=57–1173, y=214–804, na foto original.
- 480.175 pixels com alpha ≥254 e 17.212 pixels mistos de borda.
- 0,099% dos pixels opacos têm algum canal ≥250; 2,459% têm todos ≤5.
  São limiares no JPEG, incluem peças pretas e tarja: não diagnosticam clipping RAW.
- Código de pintura e referência física de cor: desconhecidos.
- A versão no estúdio aplica escala uniforme de aproximadamente 2,567×;
  não existe novo detalhe real por ter sido ampliada para 4096 × 3072.

Arquivo completo, com coordenadas, amostras e hash: [mapa-dados.json](mapa-dados.json).
Os polígonos são anotações aproximadas para planejar o trabalho, não máscaras
prontas para editar. Eles se sobrepõem e precisam de refinamento por painel.

## Mapa de intervenção
| Região | O que existe na foto | Tratamento proposto | O que não alterar |
|---|---|---|---|
| R1 Para-brisa | Céu e nuvens; parte da cabine oculta | Reflexos mais simples e suaves em teste próprio | Contorno, tonalidade do vidro, partes visíveis da cabine |
| R2 Capô | Céu, fios e construções misturados ao brilho | Trechos localizados, com reflexão ampla e coerente com a sala | Emblema, vincos, junções e textura metálica |
| R3 Portas/lateral | Faixa clara do piso e escura da fachada | Tratar cada painel separadamente | Maçanetas, frisos, emblema e-hybrid e curvas |
| R4 Para-choque pintado | Reflexo horizontal do exterior | Limpeza localizada com transição de luz contínua | Sensores, grades, LEDs e cromados |
| R5 Faróis | Lentes, módulos e reflexos sobrepostos | Proteção estrutural prioritária | Desenho óptico, contorno, número e formato dos elementos |
| R6 Rodas/pneus | Raios finos, pinças verdes, relevo do pneu | Conservar a fotografia | Geometria, freios, letras e desgaste |
| R7 Tampa-placa | Tarja preta já medida | Aplicar arte oficial por perspectiva | Quadrilátero original e bordas do suporte |

R1 e R2 são os primeiros alvos. Não usar o polígono inteiro do capô para gerar
sem antes excluir emblema, vincos e junções. Rodas, faróis e detalhes exigem
proteção adicional mesmo quando caem dentro de uma região maior.

## Cor: o que as amostras dizem
Na faixa metálica selecionada, a mediana sRGB é aproximadamente (158,176,180);
no trecho de capô, (146,160,168); no trecho lateral escuro, (14,18,21).
Essas diferenças ilustram iluminação e reflexos. Nenhum desses valores é uma
“cor oficial” para preencher a lataria. Não converter a carroceria para um HEX,
não usar cromado como cartão cinza e não neutralizar todo o azul indiscriminadamente.

A avaliação de acabamentos metálicos depende de ângulo e aparência, não apenas
de uma amostra RGB. Fonte técnica: [X-Rite — medição de acabamentos automotivos](https://www.xrite.com/learning-color-education/using-our-solutions/measuring-effect-finishes-paint).

## Ordem de execução recomendada
1. Manter a fotografia e o piloto fiel como referências imutáveis.
2. Refinar máscaras separadas para vidro, cada painel pintado e detalhes protegidos.
3. Fazer um primeiro teste SOMENTE no para-brisa e comparar contorno e cabine.
4. Testar um trecho do capô sem emblema; remover objetos refletidos reconhecíveis,
   mantendo gradação, brilho e textura. A reconstrução deve ficar identificada.
5. Comparar os trechos aprovados antes de estender a intervenção às portas.
6. Ajustar exposição/cor apenas nas áreas aprovadas. Não escolher agora um ganho
   de balanço de branco absoluto que a fotografia não permite calibrar.
7. Conferir sombra de contato, direção de luz e brilho do piso na composição.
8. Aplicar tampa-placa oficial após escala; não pedir para IA escrever a marca.
9. Produzir os três formatos a partir de um master aprovado.

O recurso de remoção de reflexos da Adobe é descrito para fotografias feitas
através de vidro; não é uma solução comprovada para a lataria deste carro.
[Documentação Adobe](https://helpx.adobe.com/uk/photoshop/desktop/repair-retouch/clean-restore-images/remove-reflections.html).

## Critérios de aprovação do teste
- Nenhum detalhe estrutural adicionado, removido ou deslocado.
- Fora da máscara efetiva, comparação exata antes de escala/compressão.
- Comparação ampliada de emblemas, raios, faróis e frisos.
- Nenhum céu, fachada ou fio reconhecível nas áreas efetivamente tratadas.
- Reflexos amplos continuam descrevendo a curvatura; pintura não fica fosca/plástica.
- Avaliação de cor por painel e entre fotos, não Delta E global como selo de fidelidade.
- Registrar diferenças nas áreas reconstruídas: não exigir Delta E zero nelas,
  pois isso entraria em contradição com alterar iluminação/reflexos.
- Preservar defeitos e estado de conservação reais; não confundir reflexo com risco.
- Identificar incerteza quando o reflexo encobre informação que não pode ser recuperada.

## Direção para a placa da parede
Suporte de alumínio grafite acetinado, espessura aparente discreta, quatro
espaçadores metálicos e afastamento da parede. Emblema como peça fina recortada
aplicada sobre o suporte: espessura de borda, sombra de contato curta e
iluminação compartilhada. A arte original tem brilhos já desenhados: tratá-la
como impressão em peça rígida é mais coerente do que inventar metal extrudado.

Os candidatos gerados são estudos visuais. Não substituem automaticamente o
estúdio v03. Antes de integrar, validar texto e contorno do logo contra o PNG
oficial; para produção, manter/reaplicar essa arte por composição determinística.
A primeira vista geral v04 ainda ficou próxima demais da solução anterior.
O detalhe ampliado serve para aprovar material e fixação, não um novo enquadramento
para fotos de carro.

## Estado desta etapa
Nenhum pixel do carro foi retocado e nenhuma série anterior foi substituída.
O diagnóstico organiza o primeiro teste localizado, sem apresentar reconstrução
generativa como recuperação exata da pintura real.

