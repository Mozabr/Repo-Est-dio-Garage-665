# Lateral seletiva v6f — candidata v06

## Decisão

A lateral não pode ser substituída integralmente: isso cria aparência de recorte, tinta fosca e halos nas proteções. A solução v06 preserva a fotografia e trata somente a reflexão quente do ambiente externo na metade inferior dos painéis M13, M14 e M15.

## Processo

1. Une as três máscaras revisadas em uma superfície contínua.
2. Detecta dentro dessa superfície apenas pixels claros com componente Lab b quente e posição compatível com a reflexão de rua.
3. Suaviza a luminância dessa seleção em baixa frequência.
4. Neutraliza a cromia contaminante usando a âncora de basecoat do próprio carro.
5. Reinsere exclusivamente a microtextura da fotografia.
6. Copia todos os pixels externos diretamente do quadro v25 aprovado.

Um doador fotométrico foi gerado para estudar a forma de luz, mas alterou detalhes e foi rejeitado como imagem. Ele está arquivado como `doador-fotometrico-rejeitado-diagnostico.png`; nenhum RGB, textura ou geometria dele integra a v06.

## Resultado técnico

- status: `technical_pass_visual_approval_required`;
- pixels alterados dentro da seleção: 34.802;
- pixels alterados fora da seleção: 0;
- amplitude P95–P05 em Lab L: 62;
- clipping quase branco: 0%;
- RMS de microtextura: 1,978;
- transformação geométrica: nenhuma;
- elementos protegidos alterados: 0;
- RGB/textura gerados usados: não.

## Arquivos

- candidato: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v06/candidato-quadro-completo.png`;
- crop de inspeção: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v06/candidato-crop.png`;
- QA: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v06/qa-material.json`;
- configuração: `config/rig-material-lateral-v6f.json`;
- execução local: `scripts/executar_lateral_continua_v6f.sh`.

## Próximo gate

A v06 não é entrega aprovada. Ela precisa de inspeção humana em 100%, principalmente na faixa clara das portas, continuidade no paralama e preservação dos vãos. Após aprovação explícita, congelar a lateral e iniciar teto/vidros. Se rejeitada, alterar somente os parâmetros da seleção/reflexão, nunca gerar o carro inteiro.
