# Pipeline de material v6f — pintura fiel e verniz de estúdio

Status: capô v25 aprovado e congelado; doador pago M13 já gerado; composição M13 v03 aguarda validação visual. Nada desta etapa está aprovado para publicação.

## Objetivo

O v6f separa elementos que as tentativas anteriores misturavam:

1. geometria e detalhes físicos vêm exclusivamente da fotografia-base;
2. direção de cor Lab a/b vem exclusivamente da fotografia-base;
3. microtextura e grão fino vêm exclusivamente da fotografia-base;
4. a IA fornece somente a distribuição de luz em luminância Lab L;
5. o RGB gerado e a textura fina gerada nunca entram no master.

Essa separação impede que o GPT Image transforme a pintura em envelopamento fosco, redesenhe a roda ou altere componentes do veículo.

## Diagnóstico que determinou os gates

O resultado v6e tinha cromia média 2,08 contra 12,86 na fonte, além de 4,83% de pixels quase brancos. O primeiro controle local v6f corrigia parte da cor, mas ainda suavizava demais a tinta. A calibração atual, ensaiada contra o doador antigo e propositalmente reprovado, registrou:

- cromia relativa: 99,98% da fonte;
- variação média de matiz: 0,21°;
- microtextura RMS: 1,59, dentro do intervalo permitido;
- pixels quase brancos: 0%;
- mudanças fora da máscara: zero;
- contraste especular intermediário RMS: 5,14, abaixo do mínimo 9,00.

Assim, o doador antigo fica bloqueado sem que seja necessário julgar “no olho”. Ele não possui estrutura de verniz suficiente.

## Processo operacional

### Etapa 1 — capô

O comando `./scripts/executar_teste_capo_v6f.sh` executa uma única chamada paga em 2048 × 1024, qualidade alta. O script:

1. verifica a chave e o pacote antes da chamada;
2. bloqueia repetição se o arquivo bruto já existir, evitando cobrança duplicada;
3. solicita um doador com key ampla, ombro especular controlado e faixa escura de separação;
4. registra o doador contra a fotografia;
5. descarta RGB e textura gerados;
6. transfere somente a luminância em bandas limitadas;
7. recoloca a cor Lab a/b e a microtextura da fonte;
8. interrompe automaticamente se qualquer gate falhar;
9. somente quando os gates passam, reintegra o capô ao quadro completo.

O arquivo para avaliação será `trabalhos/panamera/refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-quadro-completo.png`. Os arquivos que contêm `bruto`, `diagnostico`, `doador` ou `mapa` não são entregas.

### Gates obrigatórios do capô

- cromia média Lab: 10,5–14,5;
- cromia relativa à fonte: 82%–105%;
- mudança média de matiz: no máximo 3°;
- contraste especular intermediário RMS: 9–15;
- microtextura RMS: 1,5–3,0;
- amplitude luminosa P95–P05: 65–95;
- pixels quase brancos: no máximo 0,25%;
- mudanças fora da máscara: zero;
- RGB da IA usado no resultado: não;
- textura fina da IA usada no resultado: não.

A aprovação técnica não substitui a aprovação visual. O capô ainda deve apresentar verniz brilhante, transições contínuas, vincos naturais, emblema sem halo e integração coerente com para-lama, para-brisa e sala.

### Etapa 2 — lateral

A lateral já foi preparada em um crop comum 1536 × 1024. Como o capô v25 foi aprovado, a sequência fixa está liberada, uma superfície por vez:

1. M13 — para-lama próximo;
2. M14 — portas superiores;
3. M15 — portas inferiores.

Cada superfície terá uma chamada isolada e será recomposta a partir da mesma autoridade, nunca a partir do resultado gerado anterior. Os overlaps de feather serão normalizados na mesclagem, sem somar duas correções. Rodas, freios, vidros, maçanetas, badge e vãos de painéis permanecem protegidos.

O comando pago `./scripts/executar_teste_m13_api_v6f.sh` já foi executado e agora está bloqueado contra cobrança duplicada. O doador foi reaproveitado na composição local v03 somente como baixa frequência de Lab L. Novos gates impedem diferença média superior a 18 Lab L ou P95 superior a 50. M14 permanece bloqueada até aprovação visual explícita de M13.

O mesmo perfil aprovado no capô controlará a cor e o verniz da lateral. A forma da luz muda conforme a normal da superfície: faixa longa superior, transição de volume no centro e bounce neutro discreto embaixo. Não se copiará o mesmo desenho do highlight do capô para as portas.

### Etapa 3 — master e formatos

Somente depois de capô e três superfícies laterais passarem pelos gates e pela aprovação visual será criado um único master 4096 × 3072. Todas as saídas derivam desse master:

- feed: 4096 × 3072, 4:3;
- story horizontal: 3840 × 2160, 16:9;
- Webmotors: 1920 × 1440, 4:3 horizontal.

Não haverá nova geração independente por formato, pois isso destruiria a consistência do veículo.

## Arquivos de controle

- `config/pipeline-v6f.json`: chamada e regras do capô;
- `config/perfil-material-v6f.json`: decomposição de material e gates;
- `config/superficies-carroceria-v6f.json`: ordem e crop da lateral;
- `prompts/v6f/`: prompts versionados e hashes;
- `trabalhos/panamera/refinamento-dianteira-v6f/qa-preflight-v6f.json`: pré-voo 10/10;
- `trabalhos/panamera/refinamento-dianteira-v6f/preparo-lateral/qa-preparo-lateral.json`: inventário das três máscaras.

## Limite de fidelidade

O processo preserva os dados de cor registrados na imagem-base; ele não mede a cor física absoluta do veículo porque as fotos não contêm cartela de cor nem arquivo RAW. “Fiel” nesta etapa significa fidelidade verificável à fotografia fornecida, sem prometer recuperação de informação que a captura não registrou.
