# Protocolo consolidado — série fiel Garage 665

## Diagnóstico dos testes `Teste panamera 01` e `Teste panamera 02`

Os dois arquivos têm boa direção de ambiente, mas não formam uma série fiel do mesmo veículo. Cada vista foi reconstruída generativamente como um carro novo. Entre a dianteira e a vista 3/4 mudam a largura aparente, os volumes do capô e do para-choque, a leitura dos faróis, o para-brisa, a pintura, o verniz e a iluminação. A vista 3/4 está mais brilhante e definida; a frontal está mais fosca, escura e achatada. O tampa-placa também funciona como um cartão de proporção própria, em vez de ocupar exatamente o quadrilátero coberto na foto original.

O fundo, a escala do logo e a linguagem da sala são aproveitáveis como direção. Os pixels dos carros não são aprovados como documento comercial fiel.

## Princípio obrigatório

O carro é documento; somente ambiente, reflexos externos identificáveis e sombra projetada podem ser reconstruídos. Nenhuma vista pode ser gerada do zero a partir das outras. Cada resultado começa na fotografia original daquele mesmo ângulo.

## Fluxo fixo por vista

1. Selecionar a fotografia original do ângulo e congelá-la como autoridade de geometria.
2. Usar outras vistas do mesmo veículo apenas para validar cor, versão, peças e material.
3. Corrigir exposição e balanço de branco antes da geração.
4. Produzir máscaras separadas para fundo, pintura, vidros, sombra e detalhes bloqueados.
5. Substituir somente o fundo com a placa-mestre compatível.
6. Recolocar sobre o resultado a camada original completa do veículo.
7. Fazer uma segunda edição somente no interior das máscaras de pintura e vidro para retirar céu, nuvens, prédios, árvores, postes e fios.
8. Misturar a proposta de reflexos em baixa intensidade, preservando textura e crominância do original.
9. Recolocar novamente rodas, pneus, freios, faróis, lanternas, grades, emblemas, textos, placa, frisos, maçanetas, sensores, escapamentos, contorno e vincos a partir da fotografia original.
10. Refazer apenas a sombra externa; preservar a oclusão curta junto aos pneus.
11. Aplicar logo da parede e tampa-placa oficiais de modo determinístico.
12. Conferir lado a lado com o original em 100% antes das exportações.

## Configuração bloqueada de geração

```json
{
  "model": "gpt-image-2-2026-04-21",
  "quality": "high",
  "size": "3264x2448",
  "output_format": "png"
}
```

O resultado aprovado em 3264 × 2448 — maior tamanho 4:3 exato dentro dos limites atuais do modelo — é ampliado de forma conservadora para o master 4096 × 3072. Não fazer várias gerações acumuladas sobre a versão anterior; se duas correções locais falharem, reiniciar a partir da composição aprovada com o carro original.

## Placas-mestre bloqueadas

- `STUDIO_A`: dianteira 3/4;
- `STUDIO_B`: perfil;
- `STUDIO_C`: traseira 3/4;
- `STUDIO_D`: frontal ou traseira simétrica;
- `STUDIO_E`: detalhes externos.

Arquitetura, horizonte, parede, piso, temperatura, contraste e posição do logo são congelados por versão do estúdio. Não gerar um novo fundo livremente para cada veículo.

## Saídas obrigatórias

- Feed: 4096 × 3072 px, 4:3 horizontal;
- Story: 3840 × 2160 px, 16:9 horizontal;
- Webmotors: 1920 × 1440 px, 4:3 horizontal.

As três saídas vêm do mesmo master aprovado. Cor, pintura, contraste local e detalhes do veículo não podem mudar entre os canais; apenas enquadramento e redimensionamento.

## Portões de aprovação

1. Geometria: comparação direta com a fotografia original.
2. Identidade: rodas, freios, faróis, grades, emblemas, textos e versão intactos.
3. Material: mesma cor-base, verniz brilhante e flake fino; sem aparência fosca ou plástica.
4. Reflexos: nenhum elemento externo identificável e nenhuma forma geométrica artificial de softbox.
5. Estúdio: placa correta, perspectiva coerente e repetição visual entre carros.
6. Tampa-placa: quadrilátero exatamente igual ao da área coberta na foto.
7. Arquivo: perfil sRGB incorporado, dimensões, nome e compressão corretos.

Qualquer falha de geometria ou identidade reprova a imagem, mesmo que o estúdio esteja visualmente bonito.
