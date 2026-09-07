# Lateral seletiva v6f — candidata v11

## Decisão

A lateral não pode ser substituída integralmente: isso cria aparência de recorte, tinta fosca e halos nas proteções. A v06 preservou a fotografia e tratou somente a reflexão quente do ambiente externo. A candidata v11 mantém essa base e recupera a leitura brilhante do verniz por luminância, sem alterar a identidade cromática ou a geometria.

## Processo

1. Une as três máscaras revisadas em uma superfície contínua.
2. Detecta dentro dessa superfície apenas pixels claros com componente Lab b quente e posição compatível com a reflexão de rua.
3. Suaviza a luminância dessa seleção em baixa frequência.
4. Neutraliza a cromia contaminante usando a âncora de basecoat do próprio carro.
5. Reinsere exclusivamente a microtextura da fotografia.
6. Calcula o detalhe luminoso já existente entre duas escalas de desfoque e o reforça somente em Lab L.
7. Aplica duas keys elípticas largas e com bordas suaves no ombro da carroceria, simulando um softbox grande sem desenhar uma faixa rígida.
8. Copia todos os pixels externos diretamente do quadro v25 aprovado.

Um doador fotométrico foi gerado para estudar a forma de luz, mas alterou detalhes e foi rejeitado como imagem. Ele está arquivado como `doador-fotometrico-rejeitado-diagnostico.png`; nenhum RGB, textura ou geometria dele integra a v11.

## Resultado técnico

- status: `technical_pass_visual_approval_required`;
- pixels alterados dentro da superfície: 93.473;
- pixels alterados fora da seleção: 0;
- amplitude P95–P05 em Lab L: 75;
- clipping quase branco: 0%;
- RMS de microtextura: 2,054;
- transformação geométrica: nenhuma;
- elementos protegidos alterados: 0;
- RGB/textura gerados usados: não.

## Arquivos

- candidato: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v11/candidato-quadro-completo.png`;
- crop de inspeção: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v11/candidato-crop.png`;
- QA: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v11/qa-material.json`;
- configuração: `config/rig-material-lateral-v6f.json`;
- configuração congelada: `config/rig-material-lateral-v6f-v11.json`;
- execução local: `scripts/executar_lateral_continua_v6f.sh`.

## Próximo gate

A v11 não é entrega aprovada. Ela precisa de inspeção humana em 100%, principalmente no brilho do ombro, continuidade entre paralama e portas e preservação dos vãos. Após aprovação explícita, congelar a lateral e iniciar teto/vidros. Se rejeitada, alterar somente os parâmetros de luminância do clear-coat, nunca gerar o carro inteiro.
