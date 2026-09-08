# Estado de retomada — Garage 665
Atualizado em 08/09/2026. A dianteira 3/4 `teste 05` está aprovada; as previews
v10 das demais vistas foram reprovadas como resultado visual.

## Conjunto atual para validação — previews v12

Após a falha geométrica do perfil API v11, foi criado um conjunto novo de
validação com a ferramenta integrada de imagem: seis externas, três internas e
a master `teste 05`, todas organizadas em
`trabalhos/panamera/previews-validacao-v12`. As folhas de decisão são
`01-folha-externas.jpg` e `02-folha-interiores.jpg`. Perfil e traseiras mostram
a direção mais consistente; a frontal ainda tem uma divisão tonal artificial no
capô. Nenhuma candidata v12 é master ou entrega publicável. Ler
`35-previews-validacao-v12.md` antes de finalizar.

## Etapa ativa — série v11 com lock integral da master `teste 05`

O usuário reprovou as previews v10 porque elas só compartilhavam o fundo: a
Panamera ainda mantinha iluminação e reflexos urbanos. A v11 substitui esse
fluxo. `teste 05` agora controla sala, teto, parede, piso, placa, temperatura,
contraste, sombra e resposta do verniz; a fotografia original de cada vista
continua controlando geometria, cor base e todos os detalhes do carro.

O primeiro e único teste pago autorizado é o perfil em 1600 × 1200:
`./scripts/executar_externa_serie_v11_api.sh perfil`. A API usa o snapshot
`gpt-image-2-2026-04-21`, qualidade high, uma máscara conservadora e trava local
de zero alteração fora do veículo. O resultado é candidato e deve ser conferido
em `comparacao-master-alvo-candidata.jpg`; não executar outras vistas nem criar
4K antes da aprovação. Ler `34-padrao-mestre-teste-05-v11.md`.

## Histórico substituído — estúdio canônico v10

A master `teste 05` substitui o Studio H como autoridade da arquitetura: teto
off-white contínuo, sem painel luminoso retangular visível. O perfil API v9 foi
aprovado como direção de acabamento lateral, mas seu teto não será propagado.
As seis externas foram recompostas no Studio G canônico e ainda aguardam
tratamento local dos reflexos urbanos.

As três internas agora usam uma máscara exclusiva do exterior visto pelos
vidros. A geração direta que recriou volante/painel foi classificada apenas como
referência visual. A prévia corrigida do painel mantém a fotografia do volante,
instrumentos e textos fora da máscara e mostra somente parede neutra desfocada.
Estado, comandos e gates estão em `33-estudio-canonico-v10.md`.

## Marco aprovado — master dianteira 3/4 e previews da série

O usuário aprovou visualmente a candidata v07. A master sRGB 4096 × 3072 e seus
três formatos foram gerados em `entregas/panamera-v8-aprovada/dianteira-3-4` pelo
comando `./scripts/finalizar_master_panamera_v8.sh`. É uma ampliação Lanczos da
fonte 2048 × 1536, não detalhe 4K nativo, e nenhuma chamada paga foi repetida.

Também foram geradas prévias das seis externas restantes e das três internas em
`trabalhos/panamera/previews-serie-v8`. As externas ainda têm reflexos urbanos e
validam somente composição antes do tratamento por ângulo; as internas estão
fotograficamente preservadas. Ler `31-master-v8-e-previews-serie.md` antes de
criar outra master.

## Etapa ativa — série multivista v9

Por orientação do usuário, as demais externas e internas também devem parecer
capturadas no mesmo Studio H. O perfil é a calibração inicial. Um doador visual
confirmou a direção, mas não é publicável por deslocamento geométrico; a
recomposição contida v02 preserva a fonte e passou tecnicamente. O caminho
oficial GPT Image 2 API está pronto em `./scripts/executar_perfil_serie_v9_api.sh`
e aguarda execução no Terminal que possui `OPENAI_API_KEY`. Não avançar em lote
nem criar novas masters antes de aprovar o perfil. Ler
`32-serie-v9-padrao-multivista.md`.

## Etapa atual — harmonização integral v8 sobre o M11 v6

Por decisão explícita do usuário em 07/09/2026, `refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png` passou a ser a autoridade visual e geométrica do quadro atual. A regra anterior da v7, que a tratava somente como referência, foi substituída. A fotografia original continua arquivada para auditoria e a cor física absoluta não pode ser certificada sem RAW/ColorChecker.

Foi criado um doador integral com a ferramenta de imagem e ele foi registrado com 1.403 correspondências, 82,97% de inliers e deslocamento máximo de 0,802 px. O RGB, a textura fina, a geometria e a cromia gerados foram descartados da candidata conservadora; somente luminância Lab L de baixa frequência foi transferida nas máscaras M10 e M13–M17, com M19 protegida.

As harmonizações v01 e v02 passaram nos gates automáticos, mas foram reprovadas visualmente por emenda no para-lama. A v03 eliminou a emenda, mas foi reprovada pelo usuário por aparência ainda fosca. Um segundo doador de clear-coat foi criado; a v06 recuperou highlights do próprio M11 v6, porém falhou por 0,501% de quase-brancos. A candidata v07 comprime somente novos highlights acima de Lab L=239 e passou: zero mudança fora da união, zero em detalhes protegidos, diferença média 2,267 Lab L, P95 6, quase-brancos 0,080% e razão de cromia 1,010. Arquivo para aprovação: `trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v07-clearcoat-final/candidato-quadro-completo.png`. Processo completo em `30-harmonizacao-integral-v8.md`.

## Histórico substituído — auditoria v7 concluída; referência visual v6 recuperada

O usuário aprovou visualmente o capô v25. A lateral foi retomada em uma máscara contínua M13+M14+M15. As tentativas v01–v04 foram rejeitadas por aparência uniforme, escurecimento e leitura do contorno. Um novo doador fotométrico foi gerado e arquivado apenas como diagnóstico; sua geometria, RGB e textura são proibidos no resultado.

A v06 estabeleceu a neutralização seletiva da reflexão quente/externa na metade inferior da lateral. As v07–v11 acrescentaram um passe determinístico de clear-coat somente em Lab L. A v11 foi reprovada por continuar fosca. A chamada M13 real passou pelo pré-voo 17/17 e gerou o doador pago. A composição v02 foi reprovada por mancha clara. A v03 passou tecnicamente, mas foi retirada da posição de melhor versão em 07/09/2026 porque o resultado conjunto não se aproximou do ideal lembrado pelo usuário. Ela permanece apenas como diagnóstico e não libera M14 isoladamente.

A auditoria histórica identificou `refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png` como a referência visual mais próxima do ideal. Ela não é autoridade de identidade, pois é uma resposta bruta que reinterpretou pixels externos. A direção v7 usa três fontes com papéis diferentes: fotografia original para identidade, capô v25 para pintura aprovada e v6 bruta apenas para integração fotométrica. Processo completo em `29-auditoria-convergencia-v7.md`.

A primeira prévia conjunta v7 da lateral foi criada sem nova chamada paga. Ela preserva 89,19% da cromia da fonte, contra aproximadamente 16% na v11, e registra zero mudança fora da máscara. Continua como diagnóstico porque teto, para-brisa e vidros laterais ainda não foram tratados.

### Atualização de retomada — candidata v25

O doador novo já foi gerado e não deve ser cobrado novamente. A calibração local avançou até v25. A métrica de cor separa o diagnóstico pixel a pixel do gate robusto de direção cromática agregada do basecoat. A v25 acrescenta somente uma key frontal suave no centro do capô, com pico de 14 Lab L, e passou tecnicamente: desvio agregado de matiz 1,547°, microtextura RMS 0,734, amplitude luminosa 110, 86,60% de inliers, erro P95 1,707 px, deslocamento máximo 0,281 px e zero mudança fora do capô. Não há clipping quase branco. A tentativa de pico 16 foi barrada por amplitude 111. A v25 foi aprovada visualmente pelo usuário e permanece congelada como base da lateral.

O v6f separa geometria, cromia, microtextura e iluminação. A IA fornece somente
luminância alinhada; o RGB e a textura gerados são descartados. Lab a/b agora é
copiado da fonte, e a microtextura vem exclusivamente da fotografia. O pré-voo
passou em 10/10 controles. O ensaio com o doador v6e preservou 99,98% da cromia,
limitou a mudança média de matiz a 0,21°, manteve zero alteração fora da máscara
e passou no gate de microtextura, mas foi corretamente rejeitado: contraste
especular intermediário 5,14 contra mínimo 9,00.

O novo prompt de doador exige clear-coat polido com key ampla, ombro especular e
faixa escura de separação. O comando pago único é
`./scripts/executar_teste_capo_v6f.sh`; há trava contra repetição/cobrança dupla e
o resultado só é reintegrado se todos os gates passarem. A lateral já está
preparada em M13, M14 e M15, mas fica bloqueada até a aprovação visual do capô.
Fluxo completo em `27-pipeline-material-v6f.md`.

## Última leitura — material da pintura v6e

Diagnóstico quantitativo salvo em `26-leitura-material-pintura-v6e.md`. A v6e
removeu parte importante da leitura urbana, mas produz aparência de envelopamento:
cromia média 12,86 → 2,08 (-83,8%), estrutura intermediária RMS 17,78 → 9,30,
microtextura RMS 2,72 → 5,35 e pixels quase brancos 0,003% → 4,83%. O resultado
combina highlight amplo demais, perda de profundidade do verniz e grão sintético.

A lateral original também exige tratamento coordenado: amplitude conjunta de
173 Lab L; portas superiores com L médio 52,24 e inferiores com 120,77 devido à
reflexão literal do chão/rua. Próxima arquitetura recomendada: usar a IA somente
como doadora de luminância alinhada; manter cromia e microtextura fotográficas;
separar basecoat, metallic flake e clear-coat; processar M13–M15 sob o mesmo rig.
Nenhuma nova geração foi executada nesta etapa e a v6e segue reprovada pelo gate
geométrico de 10,36 px contra limite de 8 px.

## Última etapa — v6c rejeitada; crop fotométrico v6e pronto

A resposta bruta v6c alterou 3.035.847 pixels fora da máscara, virou a roda,
reinterpretou placa/vidros/carroceria e deixou a pintura fosca. A trava restaurou
o exterior da máscara, mas o gate rejeitou a geração por deslocamento de
19,94 px contra limite de 12 px. Não houve resultado final v6c aprovado.

O ensaio local v6d preservou geometricamente todos os elementos, mas também foi
reprovado visualmente por uniformizar demais o capô. O novo fluxo v6e envia à API
somente um crop 2:1 do capô, usa apenas o Studio H como referência luminosa,
proíbe acabamento matte/satin e exige verniz polido com resposta especular. O
gate ficou mais rígido: 70% de inliers e no máximo 8 px no crop ampliado.

Na reintegração, todos os pixels fora do capô são copiados da imagem-base.
Roda, esterçamento, placa, vidros, faróis, carroceria e estúdio têm garantia
local de zero alteração no arquivo final. Pré-voo 10/10 e ensaio de identidade
3.500 correspondências, 100% de inliers e deslocamento zero. Detalhes em
`25-rejeicao-v6c-e-fluxo-fotometrico-v6e.md`. Próximo comando único:
`./scripts/executar_teste_capo_v6e.sh`. Avaliar apenas
`capo-v6e-quadro-completo.png`; o arquivo de resposta integral é diagnóstico e
nunca deve ser tratado como entrega.

## Última etapa — correção estrutural do capô v6c

O candidato v6b do centro do capô foi REPROVADO retroativamente pelo novo gate:
61 correspondências, 44,26% de inliers e 28,74 px de deslocamento contra limite
de 12 px. A geração havia redesenhado/deslocado a Panamera e o fluxo antigo
recortava essas coordenadas incompatíveis, criando o remendo visível.

A v6c corrige a arquitetura. O carro original já está posicionado no Studio H
no alvo 2048 × 1536 antes da chamada; o capô agora usa uma única máscara física
`M11U-capo-integral`, com emblema, faróis, vincos e perímetro protegidos. O prompt
e o rig exigem uma única envoltória luminosa suave, sem divisão central ou reflexo
literal do teto. A recomposição limita a luz a 62%, delta máximo de 14 Lab L e
reinsere 90% do microdetalhe original.

O pré-voo passou em 10/10 controles e o ensaio local de registro passou com
3.500 correspondências, 100% de inliers, deslocamento zero e nenhuma mudança
fora da máscara. Diagnóstico completo em `24-correcao-capo-integral-v6c.md` e
métricas em `trabalhos/panamera/refinamento-dianteira-v6c/diagnostico-capo-v6c.json`.
Próximo e único comando pago autorizado nesta etapa:
`./scripts/executar_teste_capo_integral_v6c.sh`. Não avançar para outras
superfícies ou 4K antes da aprovação visual do capô.

## Última etapa — foco na dianteira-3-4
Studio H criado como candidato em
`estudio-mestre/STUDIO_H-photo-bay-v06-oficial.png`. O ambiente agora possui um
único teto difusor contínuo fisicamente visível, ciclorama realista, piso fosco a
acetinado e placa matte com logo oficial aplicado separadamente. O rig candidato
é `GARAGE665-RIG-V6-B`, com prompts em `prompts/v6b`. A auditoria do estúdio
passou em todos os gates: 4096x3072, praticamente zero clipping, lado esquerdo
14,656 L acima do direito, parede 15,252 L acima do piso e logo não regenerado.
Documentação em `23-estudio-h-rig-v6b.md`.

A prévia com o carro antigo está em
`trabalhos/panamera/studio-v6b-dianteira-3-4-preview/dianteira-3-4/master-4096x3072.png`.
Ela valida enquadramento e sala, não os reflexos do carro: teto/vidros/lateral
ainda pertencem ao tratamento v5. O próximo teste válido é M11 capô-centro com
Studio H pelo `scripts/executar_teste_m11_v6b.sh`.

Execução v6 iniciada e documentada em `22-execucao-piloto-v6.md`. O rig candidato
`GARAGE665-RIG-V6-A` foi congelado em `config/rig-iluminacao-studio-v6.json`:
key ampla acima/frente/esquerda, fill direito -2 EV, preenchimento frontal -3 EV,
bounce neutro -3,5 EV e balanço de branco 5200 K. A edição trabalha em 2048x1536
e o 4K só será criado depois da aprovação.

Depth Anything V2 Small foi instalado localmente em versão fixa
`5426e4f0f36572d16453bbda7a8389317b1bef99`; licença Apache-2.0 e hashes estão em
`integracoes/modelos-lock-v6.json`. Os mapas de profundidade e normal aproximada
estão em `trabalhos/panamera/refinamento-dianteira-v6/guias`. Nove máscaras por
superfície foram geradas em `refinamento-dianteira-v6/mascaras`: zero pixel fora
do veículo e zero sobre detalhes protegidos. O pré-voo passou em 8/8 verificações.

O primeiro ensaio de M11 capô-centro feito sem a máscara nativa da API foi
REPROVADO: 704 correspondências, 73,15% de inliers, mas deslocamento máximo de
17,72 px contra limite de 12 px. Nenhum pixel foi incorporado. Isso comprova que
o ensaio integrado sem máscara não deve ser usado no master. O próximo teste
válido deve ser feito por `images.edit` do GPT Image 2, usando
`scripts/executar_teste_m11_v6.sh` em um processo que tenha `OPENAI_API_KEY`.
Depois, `recompor_superficie_v6.py` transfere somente luz de baixa frequência e
reinsere microdetalhe fotográfico; `mesclar_superficies_v6.py` impede acúmulo nas
transições. A chave do Terminal do usuário não está exposta ao processo Codex
atual, portanto nenhuma chamada paga v6 foi realizada até aqui.

Validação local da recomposição concluída: zero mudança fora da máscara, cromia
Lab média a/b 0,018/0,002 no teste de identidade e RMS de microdetalhe
5,102 -> 5,104. A mesclagem normalizada passou com zero mudança fora da união e
sem soma cumulativa nas transições. O ensaio válido M11 está pronto para uma
única execução pelo `scripts/executar_teste_m11_v6.sh` no Terminal que possui a
chave.

Pesquisa v6 registrada em `21-pesquisa-relighting-e-detalhe.md` e
`integracoes/candidatos-relighting-v2.json`. Diagnóstico: o piloto v5 ainda
mistura assinaturas de luz externa no teto/vidros/molduras e perde microdetalhe
nas grandes máscaras de capô/lateral. Próxima arquitetura aprovada para teste:
GPT Image 2 high em 2048x1536, uma superfície por chamada, com mapas auxiliares;
recomposição de microdetalhe original; Depth Anything V2 Small e Real-ESRGAN como
candidatos de produção; Marigold, IC-Light, libcom e DiffusionLight somente em
laboratório isolado. Nenhum desses repositórios foi instalado nesta pesquisa.

Atualização v5: novo candidato 4K concluído em
`trabalhos/panamera/studio-v5-dianteira-3-4/dianteira-3-4/master-4096x3072.png`.
O estúdio `STUDIO_G` usa ciclorama off-white, piso acetinado, luz ampla à esquerda
e suporte fosco com quatro afastadores. O logo oficial foi aplicado separadamente,
sem regeneração, com brilho comprimido e sombra curta de emblema elevado.
Para-brisa, capô e lateral foram reconstruídos somente dentro das máscaras v4;
a auditoria em `refinamento-dianteira-v8-final-source/qa-fidelidade-fonte.json`
confirma 1.087.038 pixels protegidos e zero alteração fora das três máscaras.
As saídas feed 4096x3072, story horizontal 3840x2160 e Webmotors 1920x1440
foram exportadas. Guia completo em `20-piloto-v5-dianteira-3-4.md`.
Este é um candidato técnico aguardando aprovação visual e não substitui a série v03.

Atualização posterior: referências novas classificadas em config/referencias-panamera.json
e 19-referencias-e-mascaras.md. A referência azul é proibida para cor.
Máscaras internas implementadas e refinadas em config/refinamento-dianteira-v2.json.
Saídas em trabalhos/panamera/refinamento-dianteira-v2; v1 preservada.
Dois testes de vidro pela ferramenta integrada. Último teste contido em
trabalhos/panamera/refinamento-dianteira-v2-teste02/para-brisa-teste-mascarado.png;
comparacao-para-brisa.jpg e revisao-visual.json na mesma pasta.
Zero alterações fora da máscara comprovadas. Não aprovado: vidro escurecido,
restos de reflexão/transições junto a limpadores e detalhes da cabine.
Capô e portas têm máscaras preparadas, mas não foram retocados. NÃO aplicar à
série nem executar alterações de cor com base em fotografias de outros carros.
Orientação mais recente: vidro não pode ficar extremamente escuro. Teste04
equilibrado em trabalhos/panamera/refinamento-dianteira-v4-vidro-equilibrado:
70% do tratamento localizado + 30% do vidro original em luz linear, Delta L
médio -4,33 e zero mudanças fora da máscara. Prévia no estúdio em
trabalhos/panamera/studio-v2-vidro-v4/dianteira-3-4/preview.png. Candidato
preferido, aguardando aprovação visual; série ativa ainda não substituída.
As anotações abaixo descrevem a etapa anterior, antes desses testes locais.
Diagnóstico em trabalhos/panamera/diagnostico-dianteira-3-4/ANALISE.md e
mapa-dados.json: sete regiões anotadas, amostras de aparência e limitações de cor.
Nenhum pixel do carro foi retocado nessa etapa. A prioridade atual é testar
reflexos do para-brisa e depois capô, com máscaras refinadas e detalhes protegidos;
as duas placas pendentes da série não são o foco imediato solicitado.
Novo estudo de suporte: estudio-mestre/STUDIO_F-suporte-v04-detalhe-candidato.png.
Vista geral candidata: estudio-mestre/STUDIO_F-placa-fisica-v04-candidato.png.
Gerados pela ferramenta integrada; prompts em prompts/05-suporte-parede-v04.txt.
O detalhe amplia a leitura de bordas, fixadores e contato do emblema. É um estudo
de fabricação com arte reinterpretada pela geração, não um logo vetorial exato.
Não foi integrado ao cenário ativo: v03 e suas sete entregas continuam intactos.

## Ponto exato
Foram concluídas as sete vistas externas disponíveis da Panamera, sem inventar
novos ângulos. As três fotos de interior continuam originais. Não executar
novamente o fluxo generativo legado para reconstruir o veículo.

## Padrão preservado
- Estúdio: GARAGE665_STUDIO_F_V03, placa escura aparente com fixadores e sombra.
- Arte oficial do logo aplicada separadamente; sala sintética, não espaço fotografado.
- SHA256 do estúdio: e6532a6f1b495a585e558ebd21925d5e7180eb48766cba2a975b5de665068d4a.
- Master e feed: 4096 × 3072, 4:3.
- Story: 3840 × 2160, 16:9 HORIZONTAL, conforme solicitação registrada.
- Webmotors: 1920 × 1440, horizontal, 4:3.
- Todas as versões saem do mesmo master. Não gerar cada formato separadamente.
- Os originais medem 1280 × 960: as entregas maiores são ampliadas, não 4K nativo.
- Primeiras três configurações verificadas idênticas à cópia
  config/piloto-v2-tres-vistas.json.

## Integrações ativas
BiRefNet + ViTMatte locais e fixados por revisão; OpenCV para composição e placa;
Colour Science para comparação de cor. O detector de cartela está disponível,
mas não houve cartela nas fotos fornecidas. Dependências verificadas sem conflitos.
Prompts e base de estúdio já existem; não recriar o estúdio a cada foto.
awesome-gpt-image-2 é referência de prompts, não um mecanismo de fidelidade.
IC-Light e libcom não fazem parte do processamento ativo.

## Entregas e evidências
Em trabalhos/panamera/studio-v2:
- serie-comparativa.jpg: grade das sete vistas.
- Sete pastas de vistas, com master, preview, comparativo e máscaras.
- 21 JPEGs nas pastas formatos.
- qa-serie.json: fontes, hashes e medições.
- verificacao.json: passed_with_review_pending, visual_approval false.

Foi observado zero de alteração RGB no interior opaco protegido ANTES de escala
e compressão. Isso comprova preservação da fotografia, não cor física da pintura.
A revisão visual da grade confirmou consistência do cenário e reflexos urbanos
ainda presentes. Não converter essas métricas em uma nota de “100% fiel”.

## Pendências reais
1. Reflexos de nuvens, prédios, pessoas e piso original ainda visíveis. Não resolvidos.
2. Luz solar original não corresponde completamente ao estúdio.
3. Tampa-placa de traseira-3-4 e perfil-oposto precisa de revisão manual:
   IoU com preto original 0,9420 e 0,8473. O suporte escuro interfere na medição.
   As demais vistas com placa superaram 0,95; perfil não tem placa visível.
4. Não há foto traseira frontal para validar esse preset.
5. Revisão estética final de bordas, sombras, placa e série permanece pendente.

## Próximo trabalho, sem repetir o concluído
Revisar especificamente as duas placas sinalizadas. Para eliminar reflexos de
forma publicável, obter arquivos originais de câmera e preferencialmente uma
nova captação com ambiente/painéis neutros e cartela. Retoque localizado das
fotos atuais é alternativa, mas qualquer reconstrução de material deve ficar
separada da versão fiel e passar por comparação detalhada. Não descrever esse
retoque como recuperação exata de informação que não está na foto.

Guia completo: 17-estudio-v2.md. Configuração ativa: config/piloto-v2.json.
Rotina local: bash scripts/executar_studio_v2.sh. Não exige API para repetir
este processamento. O script antigo redireciona ao atual; a opção de legado
existe só para recuperação e não deve ser ativada inadvertidamente.
