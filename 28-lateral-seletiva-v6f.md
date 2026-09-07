# Lateral seletiva v6f — doador M13 gerado; composição v03 em validação

## Decisão

A lateral não pode ser substituída integralmente: isso cria aparência de recorte, tinta fosca e halos nas proteções. A v11 preservou a geometria e passou nos gates automáticos, mas foi reprovada visualmente pelo usuário porque a pintura continuou fosca. O próximo teste volta ao fluxo GPT Image 2 previsto no v6f: uma superfície por chamada, começando por M13, e aproveitamento exclusivo da luminância do doador.

## Registro da v11 reprovada

O arquivo `M13M14M15-lateral-continua-v11/candidato-quadro-completo.png` permanece versionado somente para diagnóstico e comparação. Ele não deve ser publicado nem usado como fonte acumulativa para a nova tentativa.

## Processo M13 API v02

1. Usa `alvo-lateral-1536x1024.png` como autoridade e a máscara alfa revisada de M13.
2. Executa o snapshot `gpt-image-2-2026-04-21`, qualidade alta, com Studio H apenas como referência luminosa.
3. Gera uma única candidata e cria imediatamente o arquivo bruto que trava nova cobrança.
4. Reaplica a resposta da API somente dentro da máscara, copiando todos os demais pixels da autoridade.
5. Descarta o RGB e a textura fina gerados; transfere somente a baixa frequência de Lab L.
6. Recoloca a direção de cor e a microtextura da fotografia da Garage 665.
7. Executa gates de amplitude, cromia, matiz, microtextura, clipping e contenção.
8. Reintegra M13 sobre o quadro v25 aprovado, sem tocar em roda, farol, badge, vãos ou fundo.

## Pré-voo

O pré-voo local passou em 17/17 verificações com uma chave simulada apenas para testar o pacote. Nenhuma chamada foi realizada nesse teste e nenhum crédito foi consumido. A execução real exige `OPENAI_API_KEY` disponível no mesmo Terminal.

## Arquivos

- pipeline da chamada: `config/pipeline-v6f-lateral-m13.json`;
- perfil de transferência: `config/rig-material-lateral-v6f-api-m13.json`;
- prompt: `prompts/v6f/M13-paralama-doador-especular-v02.txt`;
- pré-voo: `scripts/validar_pacote_lateral_v6f.py`;
- execução paga única: `scripts/executar_teste_m13_api_v6f.sh`;
- candidato esperado: `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13-paralama-proximo-api-v02/candidato-quadro-completo.png`.

## Resultado e próximo gate

O doador pago M13 já foi gerado e está travado contra repetição. A composição v02 foi reprovada visualmente porque a transferência integral produziu mancha clara e contorno perceptível. A v03 reutiliza esse mesmo doador em mistura híbrida moderada com a fotografia e adiciona gates de diferença absoluta: média máxima 18 Lab L e P95 máximo 50. Ela passou com média 15,68, P95 41 e zero alteração externa. O próximo gate é exclusivamente a inspeção humana em 100% de `M13-paralama-proximo-api-v03/candidato-quadro-completo.png`. M14 continua bloqueada.
