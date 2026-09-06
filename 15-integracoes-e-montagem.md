# Integrações e montagem do pipeline fiel

## Resultado que este projeto deve perseguir

Não existe promessa tecnicamente honesta de fidelidade de 100% quando um modelo generativo redesenha o veículo inteiro. A fidelidade documental vem de manter os pixels originais do carro e limitar a geração às áreas explicitamente mascaradas.

Neste projeto, “100% fiel” significa:

- geometria, rodas, pneus, freios, faróis, grades, emblemas, textos, vincos, sensores, escapamentos e acessórios vêm da fotografia original;
- a cor-base é medida e comparada com as fotografias reais;
- somente fundo, reflexos externos identificáveis e sombra externa podem ser reconstruídos;
- a parte do carro que não precisa de correção é recolocada sobre qualquer resultado da IA;
- o tampa-placa e o logo são montados por perspectiva, nunca gerados.

Reflexos já gravados na pintura e nos vidros não possuem uma verdade oculta recuperável numa fotografia JPEG. Nesses pontos, o resultado pode ser visualmente muito fiel, mas continua sendo uma reconstrução. A captação futura com luz difusa, arquivo original e filtro polarizador reduz muito essa incerteza.

## Repositórios aprovados

### Núcleo de produção

1. `openai/openai-python`
   - função: cliente oficial para chamar o endpoint de edição de imagens;
   - uso: enviar fotografia e máscara ao GPT Image 2;
   - licença: Apache-2.0;
   - endereço: <https://github.com/openai/openai-python>.

2. `facebookresearch/sam2`
   - função: produzir a primeira máscara do veículo e máscaras de grupos grandes;
   - uso: recorte inicial de carro, rodas, vidros e região externa;
   - licença: Apache-2.0 para código e checkpoints, com licenças separadas apenas para fontes do demo;
   - endereço: <https://github.com/facebookresearch/sam2>.

3. `ZhengPeng7/BiRefNet`
   - função: gerar matte de alta resolução para contorno, pneus, espelhos e vãos;
   - uso: segunda opinião de máscara; o operador combina o melhor de SAM 2 e BiRefNet;
   - licença do repositório: MIT;
   - endereço: <https://github.com/ZhengPeng7/BiRefNet>.

4. `opencv/opencv`
   - função: composição determinística, transformada de quatro pontos do tampa-placa, máscaras e medição;
   - uso: nenhuma geometria ou marca depende de geração;
   - licença: Apache-2.0;
   - endereço: <https://github.com/opencv/opencv>.

### Laboratório controlado

5. `bcmi/libcom`
   - função: testar harmonização, sombra, reflexão e métricas de composição;
   - uso: produzir candidatos ou pontuar composições, nunca substituir a aprovação visual nem redesenhar o carro;
   - ambiente: Linux, Python 3.10 e PyTorch 2.6 ou superior segundo o projeto;
   - licença do projeto: Apache-2.0; conferir também as licenças de cada peso usado;
   - endereço: <https://github.com/bcmi/libcom>.

### Biblioteca de referência de prompt

6. `YouMind-OpenLab/awesome-gpt-image-2`
   - função: inspiração e catálogo de estruturas de prompt;
   - uso: consultar padrões de descrição, mas não copiar a biblioteca inteira para a produção;
   - autoridade: comunidade; prompts não substituem máscara, composição nem validação;
   - endereço: <https://github.com/YouMind-OpenLab/awesome-gpt-image-2>.

## Repositórios que não entram na produção

- `compphoto/Intrinsic`: tecnicamente interessante para decomposição e remoção de especularidade, porém a implementação é declarada para uso acadêmico e possui proteção de propriedade intelectual. Pode ser estudada, mas não usada no fluxo comercial sem licença específica.
- `lllyasviel/IC-Light`: pode redesenhar materiais e há risco de licença associado ao BRIA RMBG usado no fluxo de recorte. Não é necessário para resolver o problema e fica excluído.
- pipelines de ControlNet, FLUX, ComfyUI ou geração de vista: não entram no núcleo porque incentivam reconstrução do veículo, deriva entre ângulos e mudança de cor.

## Estrutura implementada

```text
Projeto-Tratativa-Garage-665/
├── config/pipeline.json
├── integracoes/repositorios-aprovados.json
├── prompts/01-fundo-estudio.txt
├── prompts/02-reflexos-localizados.txt
├── prompts/03-correcao-local.txt
├── scripts/preparar_entrada.py
├── scripts/editar_com_gpt_image_2.py
├── scripts/aplicar_tampa_placa.py
├── scripts/exportar_formatos.py
├── requirements-core.txt
├── estudio-mestre/
├── assets/
└── entregas/
```

Os repositórios externos não devem ser copiados para dentro da pasta principal. Eles ficam em ambientes separados, com a versão e a licença registradas em `integracoes/repositorios-aprovados.json`. Isso evita conflito de dependências e torna o pipeline auditável.

## Comandos do fluxo principal

Executar a partir da pasta `Projeto-Tratativa-Garage-665`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-core.txt
```

Preparar uma cópia de trabalho sem alterar a fotografia recebida:

```bash
python scripts/preparar_entrada.py "/caminho/foto-original.jpg" "trabalhos/VEICULO/VISTA/entrada-3264x2448.png"
```

Depois de criar uma máscara PNG RGBA do mesmo tamanho:

```bash
python scripts/editar_com_gpt_image_2.py \
  --imagem "trabalhos/VEICULO/VISTA/entrada-3264x2448.png" \
  --mascara "trabalhos/VEICULO/VISTA/M02-fundo-editavel.png" \
  --prompt "prompts/01-fundo-estudio.txt" \
  --saida "trabalhos/VEICULO/VISTA/candidato-fundo-01.png"
```

Aplicar o tampa-placa depois de medir os quatro cantos:

```bash
python scripts/aplicar_tampa_placa.py \
  --imagem "trabalhos/VEICULO/VISTA/master-sem-placa.png" \
  --ponto X1,Y1 --ponto X2,Y2 --ponto X3,Y3 --ponto X4,Y4 \
  --saida "trabalhos/VEICULO/VISTA/master-com-placa.png"
```

Gerar as três entregas a partir do master aprovado:

```bash
python scripts/exportar_formatos.py \
  "trabalhos/VEICULO/VISTA/master-4096x3072.png" \
  --saida "entregas/VEICULO/VISTA"
```

SAM 2, BiRefNet e libcom não são necessários para o primeiro piloto. Ao incorporá-los, clonar cada um fora deste projeto, criar um ambiente virtual exclusivo, testar uma versão e registrar o commit aprovado no inventário antes de liberar em produção. Não atualizar automaticamente dependências ou checkpoints.

## Montagem, passo a passo

### Etapa 1 — preparar a estação

1. Usar Python 3.10 ou superior em um ambiente virtual exclusivo. Em Macs que ainda possuam Python 3.9, o projeto fixa temporariamente `openai==2.48.0`, última versão compatível, até a atualização do Python.
2. Instalar `requirements-core.txt`.
3. Configurar `OPENAI_API_KEY` no ambiente; nunca salvar a chave no projeto.
4. Validar o fluxo principal primeiro, sem SAM 2, BiRefNet ou libcom: máscara manual bem feita é melhor que automação mal conferida.
5. Instalar SAM 2 e BiRefNet em ambientes separados somente quando houver uma máquina adequada para PyTorch. Libcom deve ficar num laboratório Linux separado.

### Etapa 2 — congelar o estúdio

1. Aprovar cinco placas-mestre: dianteira 3/4, perfil, traseira 3/4, frontal/traseira simétrica e detalhes.
2. Remover logo do fundo-base; aplicar o PNG oficial depois.
3. Congelar arquitetura, linha do horizonte, piso, temperatura de cor, contraste e posição de câmera.
4. Criar uma versão 4:3 com área segura central compatível com o corte 16:9 horizontal.
5. Nunca pedir à IA um estúdio novo para cada foto.

### Etapa 3 — preparar um novo veículo

1. Criar uma pasta com identificador único: `ANO-MARCA-MODELO-COR-CHASSIS4`.
2. Copiar os arquivos originais sem regravar e calcular o hash de cada um.
3. Separar as vistas: frontal, dianteiras 3/4, perfis, traseiras 3/4, traseira e detalhes.
4. Eleger uma foto de autoridade para cada saída; outras fotos servem apenas para conferir identidade e cor.
5. Fazer correção global leve de balanço de branco e exposição, sem clarear seletivamente a pintura.
6. Normalizar uma cópia 4:3 para 3264 × 2448 com `scripts/preparar_entrada.py`; esse é o maior 4:3 exato dentro do limite atual de pixels do modelo. Construir as máscaras sobre essa cópia. O original permanece intocado.

### Etapa 4 — construir as máscaras

Para cada fotografia, criar PNGs do mesmo tamanho:

- `M01-carro-completo`: veículo inteiro, para recolocação final;
- `M02-fundo-editavel`: somente o que pode virar estúdio;
- `M03-pintura-reflexos`: apenas reflexos externos identificáveis na pintura;
- `M04-vidros-reflexos`: apenas reflexos externos identificáveis nos vidros;
- `M05-detalhes-bloqueados`: rodas, pneus, freios, faróis, grades, emblemas, letras, maçanetas, sensores, escapamentos e vincos;
- `M06-sombra-externa`: área externa de contato e sombra projetada;
- `Q01-placa`: quatro pontos do quadrilátero original, na ordem superior esquerdo, superior direito, inferior direito, inferior esquerdo.

SAM 2 cria a seleção inicial. BiRefNet ajuda no matte fino. O operador deve revisar em 200% e corrigir bordas manualmente. Como a máscara da API é orientação e não trava pixel a pixel, `M01` e `M05` são recolocadas depois da geração.

Na máscara enviada à API, a área transparente indica o que pode ser alterado e a área opaca indica preservação. Imagem e máscara devem ser PNG, ter o mesmo tamanho e menos de 50 MB.

### Etapa 5 — substituir o fundo

1. Usar a fotografia do ângulo como primeira imagem.
2. Usar `M02-fundo-editavel` como máscara com canal alfa.
3. Usar o prompt `prompts/01-fundo-estudio.txt`.
4. Solicitar no máximo três candidatos.
5. Reprovar qualquer candidato que mude contorno, altura, entre-eixos, rodas, faróis ou placa.
6. Compor por cima a camada original do carro recortada por `M01`.

### Etapa 6 — retirar os reflexos de rua

1. Trabalhar sobre a composição aprovada, nunca sobre uma cadeia de tentativas.
2. Editar pintura e vidros em chamadas separadas com `M03` e `M04`.
3. Usar `prompts/02-reflexos-localizados.txt`.
4. Misturar a proposta gerada somente dentro da máscara, começando com baixa opacidade.
5. Recolocar integralmente `M05-detalhes-bloqueados` a partir da fotografia original.
6. Comparar a cor em áreas de meia-luz não afetadas por reflexo. Se a mudança for perceptível, reprovar.
7. Depois de duas falhas, voltar à composição aprovada; não acumular gerações.

### Etapa 7 — sombra, logo e tampa-placa

1. Preservar a oclusão curta original sob pneus e carroceria.
2. Criar apenas a sombra externa compatível com o piso e a direção do estúdio.
3. Aplicar o logo oficial por composição, sem regenerar tipografia.
4. Aplicar o tampa-placa no quadrilátero `Q01`, mantendo exatamente tamanho, inclinação e perspectiva da área coberta na foto.
5. Manter a assinatura interna com margem proporcional entre 8% e 12%, sem esticar o logo.

O utilitário `scripts/aplicar_tampa_placa.py` recebe os quatro pontos de `Q01` e faz a transformação de perspectiva. Portanto, o arquivo interno de 1800 × 520 não determina o tamanho final: quem determina são os quatro pontos medidos em cada fotografia.

### Etapa 8 — validar a série

Colocar todas as vistas lado a lado e conferir:

1. mesma tonalidade e brilho de verniz;
2. mesmos faróis, rodas, pinças, frisos e emblemas;
3. mesma versão de carroceria e acessórios;
4. fundo, horizonte, piso e luz pertencendo ao mesmo estúdio;
5. nenhum céu, árvore, prédio, poste, fio, pessoa ou carro refletido;
6. nenhum retângulo artificial de softbox desenhado na pintura;
7. tampa-placa coerente com a perspectiva de cada foto.

Uma vista reprovada é refeita a partir da fotografia original, sem usar outra vista gerada como referência principal.

### Etapa 9 — gerar os três arquivos

1. Aprovar um master 4096 × 3072 em PNG sRGB.
2. Manter o veículo inteiro dentro da área segura do corte central 16:9.
3. Executar `scripts/exportar_formatos.py`.
4. Conferir:
   - Feed: 4096 × 3072, 4:3 horizontal;
   - Story: 3840 × 2160, 16:9 horizontal;
   - Webmotors: 1920 × 1440, 4:3 horizontal.
5. Não gerar novamente o carro para mudar a proporção. Os três arquivos derivam do mesmo master aprovado.

## Ordem prática de implantação

1. Validar o fluxo com uma única vista frontal da Panamera.
2. Validar dianteira 3/4 e comparar com a frontal.
3. Validar perfil e traseira 3/4.
4. Só então automatizar máscaras com SAM 2/BiRefNet.
5. Rodar dez veículos diferentes como lote-piloto.
6. Medir taxa de reprovação por geometria, cor, recorte, reflexo, placa e fundo.
7. Liberar produção apenas quando nenhuma imagem aprovada tiver deriva de identidade.

O ganho principal não virá de um prompt mais longo. Virá da combinação de máscaras pequenas, pixels originais recolocados, fundos congelados e portões de aprovação objetivos.
