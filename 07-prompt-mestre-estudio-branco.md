# Prompt mestre — Estúdio branco Garage 665

## Referência oficial de marca

Arquivo recebido e preservado em `assets/logo-garage-665-transparente.png`: PNG sRGB, 1080 × 1080 px, com canal alfa verdadeiro. O logo **não participa mais da geração por IA**. Ele é aplicado depois, sem redesenho, como uma placa física com espessura e sombra de contato controladas.

## Estratégia

Não recriar uma sala diferente a cada veículo. Primeiro, criar e aprovar um conjunto fixo de **placas-mestre do estúdio**. Depois, usar a placa correspondente ao ângulo da fotografia como referência de ambiente.

Placas recomendadas:

- `STUDIO_A`: dianteira em três quartos;
- `STUDIO_B`: perfil;
- `STUDIO_C`: traseira em três quartos;
- `STUDIO_D`: frontal ou traseira simétrica;
- `STUDIO_E`: detalhes externos.

O estúdio e o veículo são gerados sempre com a parede vazia. Depois da aprovação visual, o PNG oficial é composto de modo determinístico e idêntico em todas as placas. Se qualquer letra, número, contorno ou cor do logo mudar, a imagem é reprovada.

## Método aprovado para a placa física

- recortar apenas a transparência externa do PNG, sem alterar seu conteúdo;
- dimensionar proporcionalmente, sem perspectiva ou deformação;
- criar uma cópia escura deslocada aproximadamente 2 px para sugerir uma placa rígida de pequena espessura;
- adicionar oclusão de contato curta junto às bordas, com sombra neutra mais concentrada e deslocamento mínimo;
- adicionar uma segunda sombra muito suave e de baixa opacidade, equivalente a poucos milímetros de afastamento da parede;
- manter o logo original integral por cima dessas duas camadas;
- montar o logo diretamente no master 4K, usando o PNG oficial em alta resolução, para preservar contornos e tipografia;
- não adicionar halo, iluminação própria, neon, sombra longa, brilho inventado ou relevo regenerado.

## Variáveis do lote

```text
VEHICLE_VIEW = dianteira 3/4 | perfil | traseira 3/4 | frontal | traseira | detalhe
STUDIO_MASTER = STUDIO_A | STUDIO_B | STUDIO_C | STUDIO_D | STUDIO_E
OUTPUT_CROP = 4:3 horizontal | 16:9 horizontal
LOGO_PLACEMENT = composição posterior com o PNG oficial
```

## Papéis das imagens de entrada

```text
IMAGE_1: alvo da edição — fotografia original do veículo. É a única fonte autorizada para a identidade e todos os detalhes do carro.
IMAGE_2: referência fixa do ambiente — placa-mestre aprovada da sala branca no ângulo compatível e com a parede vazia.
IMAGE_3–5, quando disponíveis: vistas adicionais do mesmo veículo, usadas somente para validar pintura, peças e proporções.
```

## Prompt definitivo para inserção do veículo

```text
Use case: compositing
Asset type: fotografia comercial automotiva premium para o catálogo e Instagram da Garage 665

Tarefa principal:
Usando IMAGE_1 como alvo da edição, coloque o veículo fotografado dentro da sala branca mostrada em IMAGE_2. O resultado deve parecer uma fotografia real feita em um estúdio automotivo profissional da Garage 665, não uma imagem gerada por IA. Troque somente o ambiente ao redor do veículo. Preserve a câmera, o ponto de vista, a orientação, a escala e a posição do veículo de IMAGE_1. Não redesenhe nem reinterprete o carro.

Escopo de cada referência:
- IMAGE_1 controla exclusivamente o veículo: modelo, versão, carroceria, proporções, cor, acabamento, rodas, pneus, freios, faróis, lanternas, grade, entradas de ar, escapamentos, vidros, teto, retrovisores, emblemas, textos, placa, acessórios, interior visível, altura e postura.
- IMAGE_2 controla exclusivamente a sala: geometria, paredes, piso, linguagem arquitetônica, paleta, direção da luz e atmosfera.
- IMAGE_3–5 controlam somente a conferência do mesmo veículo. Não copiar fundos, ângulos ou reflexos externos dessas imagens.

Sala e arquitetura:
Sala automotiva ampla, limpa e fisicamente plausível; paredes branco-neutro fosco com textura muito sutil de pintura real; piso contínuo de epóxi ou concreto cinza muito-claro, acetinado e não espelhado; encontro entre parede e piso com curva de ciclorama discreta e ainda perceptível; teto e enquadramento completamente limpos; nenhuma janela, porta, móvel, pedestal, planta ou pessoa. Não usar branco puro estourado: manter gradações delicadas, microtextura, pequenas assimetrias e profundidade arquitetônica. **Nenhum equipamento de estúdio pode aparecer na imagem.**

Área da placa:
Manter a região central superior da parede vazia, limpa e bem iluminada para a composição posterior do logo. Não gerar logo, texto, letras, números, símbolo, placa ou marca-d’água.

Integração física do veículo:
O veículo deve repousar no piso com os quatro pneus em contato natural. Criar somente a sombra de contato necessária para integrá-lo à sala, respeitando o volume real do carro e a direção da iluminação. Preservar pequenas irregularidades realistas do pneu, pintura, vidro e metal. Os reflexos adicionados pela sala devem ser suaves, alongados e coerentes com fontes grandes posicionadas fora do enquadramento. Cada reflexo precisa acompanhar continuamente a curvatura real do painel, mudar de largura e intensidade de forma gradual e preservar os vincos estruturais da carroceria. Não criar um halo claro no contorno e não deixar o carro flutuando.

Iluminação:
Iluminação comercial automotiva suave e natural, sempre proveniente de fontes totalmente ocultas fora do enquadramento. Priorizar iluminação ambiente ampla, rebatida no teto e nas paredes, com contribuição discreta e ligeiramente desigual de grandes rebatedores laterais. Evitar a assinatura visual de um esquema perfeito e repetível: o capô deve receber uma gradação larga, de baixo contraste e bordas muito difusas, sem faixa central desenhada; teto e para-brisa devem ter reflexos reduzidos, como em uma captura com polarizador parcial; portas e para-lamas recebem variações tonais longas, suaves e não idênticas entre os lados. Preservar detalhes de grade e para-choque com preenchimento frontal fraco e rebatimento sutil do piso. Contraste moderado; altas luzes protegidas; pretos com detalhe; temperatura neutra entre 5100 K e 5300 K. A luz deve envolver o veículo e obedecer à geometria dos painéis, sem revelar a forma, a borda ou a posição exata da fonte. Sem luminárias visíveis, softboxes, painéis, trilhos, estruturas, fachos, flare, névoa, brilho de borda ou luz cinematográfica colorida.

Resposta da pintura:
A pintura deve manter profundidade de verniz: reflexão especular suave na superfície, cor real e flake fino abaixo. O flake metálico deve ser extremamente fino, aleatório e visível principalmente nos meios-tons iluminados, desaparecendo gradualmente nas sombras. Não aplicar granulação metálica uniforme em toda a carroceria. Diferenciar claramente metal pintado, vidro, cromados, rodas, borracha e plásticos. Proibir blocos geométricos, faixas brancas rígidas, reflexos espelhados simétricos, textura manchada, padrões ondulados, celulares, digitais ou repetitivos, hologramas, moiré, ruído ou aparência reptiliana.

Câmera e composição:
Preservar a perspectiva óptica da fotografia original. Aparência de câmera full-frame com lente normal/tele curta, sem distorção ultra-angular. Linhas verticais retas e horizonte nivelado. Composição {VEHICLE_VIEW}, veículo como protagonista absoluto, margens equilibradas e espaço seguro para cortes horizontais 4:3 e 16:9. O veículo deve ocupar aproximadamente 72% a 82% da largura útil, sem cortar para-choques, rodas, teto ou retrovisores, salvo quando IMAGE_1 for explicitamente uma foto de detalhe.

Tratamento fotográfico:
Fotografia editorial automotiva fotorrealista; gradação de cor neutra e sofisticada; nitidez natural; transição tonal suave; textura real de sensor e lente; microcontraste moderado; pintura com profundidade, sem aparência plástica; vidro transparente onde já era transparente; materiais distintos e críveis. Manter imperfeições verdadeiras que façam parte do veículo. Não ocultar avarias ou alterar o estado comercial do carro.

Invariantes críticos — repetir literalmente em toda iteração:
Mude somente o ambiente. Mantenha o veículo de IMAGE_1 pixel-fiel sempre que possível. Não altere carroceria, cor, proporções, distância entre eixos, bitolas, altura, stance, desenho ou posição das rodas, pneus, freios, faróis, lanternas, grades, tomadas de ar, escapamentos, emblemas, textos, placa, acessórios, vidros, espelhos ou interior visível. Não corrija, embeleze, complete, substitua nem invente partes do carro.

Proibições:
Sem carro genérico; sem mudança de modelo ou versão; sem rodas deformadas; sem pneus lisos; sem geometria derretida; sem painéis duplicados; sem faróis ou grades redesenhados; sem emblemas falsos; sem letras ilegíveis; sem placa alterada; sem reflexos incompatíveis; sem recorte serrilhado; sem halo; sem sombra genérica oval; sem piso espelhado; sem branco estourado; sem render 3D; sem HDR agressivo; sem oversharpening; sem pintura plastificada; sem desfoque artificial forte; sem granulação pesada; sem vinheta; sem pessoas; sem objetos extras; sem texto extra; sem marca-d’água; sem softboxes; sem painéis de luz; sem trilhos; sem estruturas de teto; sem luminárias ou fontes de luz visíveis.

Saída:
Uma única fotografia horizontal 4:3, limpa e pronta para catálogo, com aparência de captura real em estúdio. A parede deve permanecer vazia para receber o logo oficial em pós-produção. Nenhum layout gráfico, moldura, preço, legenda, logo ou texto gerado.
```

## Prompt de correção em caso de deriva

Usar apenas depois de identificar uma falha específica:

```text
Corrija somente [DESCREVER UMA ÚNICA FALHA]. Preserve todo o restante da imagem sem mudança. Reaplique as invariantes críticas: o veículo, suas proporções, peças, rodas, emblemas, textos, placa, reflexos estruturais, câmera e composição devem permanecer idênticos à fotografia original. Não faça melhorias adicionais.
```

## Critério de sucesso

A pessoa deve acreditar que o carro foi levado fisicamente ao mesmo estúdio Garage 665. A consistência vem da reutilização das placas-mestre e da composição exata do PNG oficial, nunca da regeneração do logo.
