# Auditoria de convergência v7 — base correta para a entrega

> **Substituída em 07/09/2026:** por decisão explícita do usuário, o M11 v6 passou a ser a autoridade visual e geométrica do quadro v8. Para continuar, use `30-harmonizacao-integral-v8.md`. Este arquivo permanece como histórico da auditoria.

Data: 07/09/2026. A candidata M13 v03 foi retirada da posição de melhor versão. Nenhuma candidata desta auditoria está aprovada para publicação.

## Resultado da varredura

Foram revisadas as gerações integrais v6, v6b e v6c, os masters anteriores do estúdio, os capôs v21–v25, as laterais contínuas v01–v11 e as composições M13 API v02–v03.

A imagem percebida pelo usuário como o resultado mais próximo do ideal é:

`trabalhos/panamera/refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png`

SHA-256: `070d60d6bd07c24649c7ee2edd22577b9b53ef643e062c329e9b47bdeab0564b`

Ela passa a ser a **referência visual de convergência** por apresentar a melhor combinação já obtida de contato com o piso, sombra, exposição do carro, integração tonal com a sala e leitura de verniz automotivo.

## Por que ela não pode ser a autoridade do veículo

Essa imagem é uma resposta bruta integral da API. Embora seja visualmente convincente, a chamada alterou pixels fora da máscara e pode ter reinterpretado carroceria, rodas, vidros, placa, emblemas e proporções. Portanto, ela orienta aparência, iluminação e integração, mas nenhum detalhe físico seu pode substituir a fotografia original.

## Três autoridades separadas

1. **Identidade e geometria:** `refinamento-dianteira-v6c/alvo-estudio-h/dianteira-3-4/alvo-edicao-2048x1536.png`.
2. **Capô e comportamento da pintura:** `refinamento-dianteira-v6f/teste-capo-doador/capo-material-v6f-v25-quadro-completo.png`, aprovado pelo usuário.
3. **Integração visual:** `refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png`, somente como referência de luz, sombra e acabamento.

A comparação sem rótulos está em `trabalhos/panamera/auditoria-convergencia-v7/comparacao-tres-referencias.png`, na ordem: integração v6, capô v25, autoridade original.

## Diagnóstico dos desvios restantes

- O Studio H tem uma fonte luminosa fisicamente clara, mas aparece grande e dominante demais no enquadramento.
- A candidata v6 mais natural não possui uma fonte de teto visível e coerente com todos os reflexos.
- O capô v25 preserva a identidade, mas o para-brisa, teto e lateral ainda exibem céu, fachada e piso externos.
- A lateral M13 v03 remove parte do reflexo do paralama, porém não forma um material contínuo com as portas ainda intocadas; isoladamente, lê como remendo.
- O tratamento por superfície continua correto, mas a aprovação deve ocorrer sobre uma prévia conjunta M13+M14+M15 produzida a partir da mesma autoridade, mantendo relatórios separados por máscara.

## Direção v7 para concluir hoje

1. Congelar enquadramento, geometria, rodas, faróis, emblemas, placa e vãos da autoridade original.
2. Manter o capô v25 sem nova geração.
3. Usar a v6 apenas como referência fotométrica do verniz e da integração com o piso.
4. Tratar paralama e portas como uma família luminosa contínua, mas conservar máscaras e gates independentes.
5. Reduzir reflexos urbanos reconhecíveis sem apagar toda a informação especular; a pintura deve continuar metálica e brilhante.
6. Tratar teto e vidros somente depois da lateral; o vidro permanece translúcido e não vira preto.
7. Ajustar o estúdio depois do carro, preservando o logo oficial aplicado deterministicamente sobre placa física com quatro afastadores e sombra curta.
8. Gerar um único master 4096 × 3072 e derivar Feed, Story horizontal e Webmotors desse master.

## Gate de fidelidade

Nenhum resultado pode avançar se alterar geometria ou detalhes protegidos, usar RGB/textura da IA no carro, exibir halo de máscara, criar aparência fosca, manter objetos urbanos reconhecíveis nos reflexos ou divergir cromaticamente da fotografia de autoridade.

## Primeira prévia v7

Foi produzida localmente, sem nova chamada paga, em `trabalhos/panamera/refinamento-dianteira-v7/previa-lateral-conjunta-v01/candidato-quadro-completo.png`. Ela restaura a retenção cromática da lateral para 89,19% da fonte, mantém diferença média de luminância em 10,61 Lab L, P95 em 31, microtextura RMS 2,20 e zero mudança fora da máscara. É um diagnóstico de continuidade da pintura, não uma entrega: teto e vidros ainda mantêm reflexos externos e serão tratados nas etapas seguintes.
