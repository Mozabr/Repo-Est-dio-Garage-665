# Referências recebidas e refinamento local — 06/09/2026

## Papel de cada referência
| Arquivo | Uso permitido | Não transferir |
|---|---|---|
| a02d9525b5574f798ca809e501c1594c_1712087709889.jpg | Aparência qualitativa da pintura; brilho contínuo e contraste sob luz mais suave | Rodas, carroceria sedan, detalhes ou valor RGB absoluto |
| foto-Album-de-PORSCHE-PANAMERA-A-64e3bd567aaf7.webp | SOMENTE iluminação, reflexos amplos e sombra em estúdio | Cor azul, elementos ópticos, roda, plataforma, marca ou reflexo arco-íris do vidro |
| images.jpeg | Direção geral de composição limpa e fundo claro | Texto, marca, detalhes e textura; imagem pequena e publicitária, sem comprovação de captura real |
| PANAMERA_2.9_V6_E-HYBRID_4_PLATINUM_EDITION_PDK_01_999x750-e1693092930597.webp | Aparência qualitativa da pintura e reflexos alongados de luz interior | Rodas/pinças, acabamento, exposição global ou aparência excessivamente escura |
| porsche-panamera-turbo-s-e-hybrid-1642027483545_v2_3x4.jpg | Como a pintura reflete céu e piso; gradação de tons | Reflexos externos, carroceria, detalhes ópticos ou rodas |

A classificação de mesma cor nas referências vem do usuário; fotografias não
calibradas não confirmam igualdade de código de pintura. A cor de produção
permanece ancorada na foto da Garage 665, não em histogramas de outros carros.
A nossa Panamera é a carroceria alongada Sport Turismo visível na fonte. As
referências mostram outras configurações: nenhuma deve orientar reconstrução
de peças. Não inferir versão/ano mecânico somente pelos nomes dos arquivos.

## O que otimizar no estúdio
- Manter fundo neutro e piso fosco, mas reduzir a leitura de textura do cenário:
  nas referências de estúdio, a atenção está no carro, não no reboco ou piso.
- Modelar reflexos como faixas largas com transições suaves; não deixar a pintura
  uniformemente cinza/fosca. Capô e portas devem compartilhar a mesma direção
  aparente de luz.
- Manter uma sombra de contato curta e mais densa junto aos pneus; sombra de
  apoio sob a carroceria mais suave e contínua. Evitar halos que façam o carro flutuar.
- Não copiar a plataforma circular, a iluminação colorida no para-brisa nem
  a marca de outra loja.
- O suporte v04 é referência de material/fixação, não autorização para ampliar
  o logo até competir com o carro. Preservar posição e escala do cenário ativo
  quando integrá-lo, depois de validar a arte oficial.
- Não mudar cenário, exposição global, placa e toda a pintura no mesmo teste:
  isso impediria identificar qual intervenção realmente melhorou a imagem.

## Máscaras implementadas
Configuração: config/refinamento-dianteira-v1.json.
Revisão posterior: config/refinamento-dianteira-v2.json, com saídas em
trabalhos/panamera/refinamento-dianteira-v2. Ela estende a região inferior do
vidro e protege o traçado do volante em vez de uma elipse ampla. A v1 permanece
salva para comparação. Capô e portas mantêm as mesmas regiões conservadoras.
Saídas: trabalhos/panamera/refinamento-dianteira-v1/.
Foram traçadas quatro regiões locais: para-brisa, capô, porta dianteira e porta
traseira. Há exclusões para faróis, emblema, friso, maçanetas, e-hybrid, volante,
limpadores e vinco do capô. Tudo fora das regiões é protegido por padrão,
incluindo rodas, pneus, teto, placa e contorno externo.

A seleção do carro v2 foi reutilizada, não refeita nem alterada. O refinamento
desta etapa é das máscaras INTERNAS de intervenção. As regiões são conservadoras;
não representam cobertura exaustiva de todos os reflexos.

A transição ocorre para dentro da máscara (3 px de recuo + 5 px de transição,
na fonte 1280 × 960). As exclusões são reaplicadas como limites rígidos. Isso
evita que um desfoque da máscara contamine o emblema ou outras peças.

Convenções:
- *-editar.png: branco permite edição, preto protege.
- *-api-alpha.png: RGBA, transparência permite edição.
- protecao-completa.png: branco protege fora da união das regiões.
- *-preview.jpg e mapa-mascaras.jpg: sobreposição de diagnóstico, não resultado final.

Testes: zero pixels editáveis dentro das exclusões e zero fora do carro opaco.
Esses testes verificam contenção nas anotações, não substituem inspeção visual.
A revisão visual confirmou regiões conservadoras. O volante foi excluído;
isso pode deixar parte da nuvem junto dele, exigindo nova máscara seletiva,
e não deve ser resolvido apagando o volante.

## Primeiro ajuste
Teste generativo apenas no para-brisa, com fonte original + indicação visual
da região + referência azul usada somente para luz. A ferramenta integrada recebe
a indicação, não uma máscara rígida nativa. Por isso, sua resposta completa não
é publicável: deve passar por registro geométrico e reinserção determinística
somente na máscara efetiva, com teste de diferença zero fora dela.

Não foi autorizada mudança da cor da pintura pela referência azul. O teste do
vidro não altera a lataria na saída mascarada. Uma eventual sobra de nuvem,
mudança da cabine, faixa artificial na transição ou desalinhamento deve reprovar
o teste. A etapa seguinte é um trecho do capô, não a série inteira.

Resultado do primeiro teste: reprovado visualmente como acabamento final.
Houve redução das nuvens superiores, mas permaneceram textura nebulosa e
descontinuidade junto às áreas protegidas. As duas máscaras foram comparadas;
a mudança de máscara isolada não resolve a aparência do reflexo gerado.
Na v2, o alinhamento estimado desloca a região em menos de 1 pixel e a
reinserção mantém exatamente 1.184.550 pixels fora da máscara. Essa contenção
é comprovada, mas não equivale a realismo. Um segundo teste usa instrução de
reflexo de difusor contínuo, sem textura de nuvens.

Segundo teste salvo em trabalhos/panamera/refinamento-dianteira-v2-teste02.
A remoção do desenho das nuvens melhorou, mas o vidro ficou mais escuro e
suave. Permanecem reflexos/transições junto aos limpadores e detalhes protegidos
da cabine. Não aprovado para publicação. Pintura e peças fora da máscara
ficaram pixel a pixel iguais à fonte sRGB; não houve correção de cor da lataria.
Prompts: prompts/06-teste-para-brisa.txt e prompts/07-teste-para-brisa-difusor.txt,
ambos executados pela ferramenta integrada imagegen. Não foi feita chamada
pela API configurada no projeto. O estúdio e as sete entregas anteriores permanecem ativos.

### Terceiro e quarto testes — vidro translúcido
Após a orientação de não escurecer o vidro, o terceiro teste exigiu a mesma
luminosidade, transparência, tonalidade azul-cinza e visibilidade da cabine da
fonte, reduzindo o contraste dos reflexos em vez de eliminá-los. Ele foi gerado
pela ferramenta integrada com o prompt salvo em
prompts/08-vidro-translucido-reflexo-reduzido.txt.

O teste03 contido apresentou Delta L médio de -8,03 na representação Lab de 8
bits do arquivo, contra -43,60 no teste02 escuro. Para obter o vidro proposto,
o teste04 combina em luz linear 70% do tratamento localizado com 30% do vidro
original. Resultado: Delta L médio -4,33, Delta a +0,78 e Delta b -1,04 dentro
da máscara; zero mudança fora dela. Essas métricas descrevem aparência digital,
não transmissão física do vidro.

O candidato equilibrado está em
trabalhos/panamera/refinamento-dianteira-v4-vidro-equilibrado/.
A prévia isolada no estúdio está em trabalhos/panamera/studio-v2-vidro-v4/.
Nada foi promovido para a série ativa. Status: candidato preferido aguardando
aprovação visual; não aprovado para publicação.
