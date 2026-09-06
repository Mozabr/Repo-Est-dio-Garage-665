# Studio H — photo bay e rig v6b

Data: 06/09/2026. Candidato técnico; aprovação visual pendente.

## Decisão

O Studio G foi substituído somente como referência candidata pelo Studio H. O
novo ambiente possui uma fonte luminosa fisicamente identificável: um único teto
difusor contínuo em tecido tensionado, com moldura periférica preta fina. Isso
elimina a ambiguidade que fazia o modelo desenhar barras, triângulos ou reflexos
sem origem coerente sobre teto e capô.

O Studio G e o master v5 permanecem preservados. Nenhuma imagem publicada foi
substituída.

## Estrutura congelada para o teste

- ciclorama off-white quente e neutro, com curvas contínuas;
- teto difusor único, sem divisão em barras;
- key superior ligeiramente à esquerda da câmera;
- fill esquerdo a -2 EV;
- fill direito a -3 EV;
- preenchimento frontal a -3,5 EV;
- bounce de piso a -4 EV;
- balanço de branco 5200 K;
- piso cinza médio-claro, fosco a acetinado e sem efeito espelho;
- painel de parede em metal preto fosco, 8 mm de espessura e quatro afastadores;
- logo oficial aplicado deterministicamente, sem redesenho por IA.

## Auditoria

O Studio H passou em todos os gates técnicos:

- master 4096 × 3072;
- branco estourado na amostra de teto: 0,00005%;
- parede esquerda 14,656 pontos L acima da direita;
- parede 15,252 pontos L acima do piso;
- piso dentro da faixa aprovada de luminância;
- logo não regenerado;
- acabamento e montagem física do suporte confirmados pelos metadados.

O arquivo 4K é ampliação determinística de uma base gerada em 1448 × 1086; não
é correto chamá-lo de captura 4K nativa.

## Leitura da Panamera gerada

A `geracao-bruta-api.png` trouxe integração visual superior, mas não é fonte de
identidade. Ela redesenhou o ambiente inteiro e pode ter reinterpretado carroceria,
vidros, rodas, letras e proporções fora da máscara. Deve ser usada apenas como
referência de integração e sombra.

Pontos positivos a conservar:

- contato de pneus e sombra mais natural;
- parede e carro na mesma faixa tonal;
- exposição mais controlada;
- metal menos recortado contra o fundo.

Pontos a corrigir por máscaras:

- divisão ainda muito reta entre as faixas de luz do capô;
- teto e vidro precisam refletir o mesmo difusor contínuo;
- lateral inferior ainda sugere ambiente externo espelhado;
- vidro deve manter a transparência original, sem ficar preto;
- faróis, rodas, emblemas e letras continuam vindo da fotografia de autoridade.

## Próximo gate

Gerar somente `M11-capo-centro` com o Studio H e o rig
`GARAGE665-RIG-V6-B`. Se aprovado, produzir as duas laterais do capô sempre a
partir da mesma fonte original e mesclar os três resultados sem acumular edições.
Somente depois seguir para teto, para-lama, portas e vidros.
