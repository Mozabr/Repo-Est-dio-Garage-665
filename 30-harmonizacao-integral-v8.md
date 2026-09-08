# Harmonização integral v8 — M11 v6 como autoridade visual

Data: 07/09/2026. Estado: candidata técnica, aguardando aprovação visual.

## Decisão que substitui a v7

Por decisão explícita do usuário, a imagem `trabalhos/panamera/refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png` passou de mera referência de convergência a **fonte visual e geométrica do quadro v8**. Seu SHA-256 é `070d60d6bd07c24649c7ee2edd22577b9b53ef643e062c329e9b47bdeab0564b`.

Isso não transforma a geração em prova física de cor. A fotografia original permanece arquivada para auditoria documental, mas nenhuma versão v8 pode mudar a posição, rodas, esterçamento, faróis, emblemas, vãos, placa, interior, logo ou composição presentes no M11 v6.

## Ferramentas e arquitetura

- GPT Image 2/ferramenta integrada: gerou uma única candidata integral usada apenas como **doador fotométrico**.
- OpenCV: registro ORB + homografia e transferência localizada.
- CIELAB: somente o canal L de baixa frequência do doador entra na candidata conservadora.
- Máscaras M10, M13–M17: teto, paralama, portas, para-brisa e vidros laterais.
- Máscara M19: detalhes protegidos copiados pixel a pixel do M11 v6.
- Máscara M20: exclui o veículo do registro pelo fundo.
- Prompt operacional: `prompts/v8/harmonizacao-integral-m11v6-v01.txt`.

O RGB, a textura fina, a geometria e a cromia gerados não entram na candidata v03. O doador bruto é diagnóstico, não entrega.

## Confirmação na documentação oficial

Em 07/09/2026 foi conferido na documentação oficial da OpenAI que:

- `gpt-image-2-2026-04-21` é snapshot válido do GPT Image 2;
- `quality: high` é aceito;
- em GPT Image 2, `input_fidelity` deve ser omitido porque todas as imagens de entrada já são processadas em alta fidelidade;
- `2048x1536` respeita os limites de tamanho e pode ser solicitado diretamente.

Fontes: https://developers.openai.com/api/docs/models/gpt-image-2 e https://developers.openai.com/api/docs/guides/image-generation.

## Resultados

### Doador integral v01

`trabalhos/panamera/refinamento-dianteira-v8/geracao-integral-doador-v01/geracao-bruta-candidata.png`

Visualmente convincente, mas proibido como entrega porque é uma reinterpretação integral. Registro: 1.403 correspondências, 82,97% de inliers e deslocamento máximo de 0,802 px.

### Contenção direta — reprovada

`geracao-integral-doador-v01/candidato-contido-carro.png` criou emendas de máscara. Fica apenas como diagnóstico.

### Harmonização v01 e v02 — reprovadas visualmente

Passaram nos gates automáticos, mas a M13 criou um remendo perceptível entre capô, para-lama e porta. Não usar como base.

### Harmonização v03 — candidata atual

`trabalhos/panamera/refinamento-dianteira-v8/harmonizacao-integral-v03/candidato-quadro-completo.png`

O ganho da M13 foi reduzido e as correções independentes passaram por convolução normalizada para evitar soma e descontinuidade. Métricas:

- zero alteração fora da união editável;
- zero alteração dentro da máscara de detalhes protegidos;
- diferença média de luminância: 3,783 Lab L;
- P95 da diferença de luminância: 10 Lab L;
- pixels quase brancos: 0,0065%;
- razão de cromia para o M11 v6: 1,014;
- RGB e textura gerados: não usados.

A candidata v03 precisa de aprovação visual. Ela é deliberadamente conservadora: vidros continuam translúcidos, teto e portas recebem mais luz, e a identidade do M11 v6 é mantida. Reflexos quentes residuais da parte inferior das portas não devem ser removidos com preenchimento uniforme; se forem reprovados, o próximo passe deve usar uma nova máscara contínua desenhada sobre a superfície física completa.

## Execução sem nova chamada paga

```bash
./scripts/executar_harmonizacao_integral_v8.sh
```

O comando reutiliza o doador já arquivado e grava a candidata e o relatório técnico em `harmonizacao-integral-v03`.

## Próxima decisão

1. Aprovar ou reprovar visualmente a v03.
2. Se aprovada, criar master 4096x3072 e derivar Feed, Story horizontal e Webmotors.
3. Se reprovada apenas na lateral inferior, redesenhar uma máscara contínua física e executar um passe local; não gerar novamente o carro inteiro.
4. Não alterar logo, placa, rodas ou outros detalhes na etapa de harmonização.
