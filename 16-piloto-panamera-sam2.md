# Piloto Panamera frontal — execução SAM 2 + GPT Image 2

## Estado atual

Uma chamada de API foi concluída. A resposta bruta alterou mais elementos do que o solicitado e não foi aprovada diretamente. Sem nova cobrança, a resposta foi reaproveitada apenas nas superfícies identificadas pelo SAM 2; os reflexos retangulares foram suavizados e o emblema original foi recolocado por recorte cromático. A versão de revisão atual é a `v09`.

O retorno da API não é aceito diretamente. O programa reaplica somente os pixels localizados dentro da máscara e restaura todo o restante a partir da composição anterior. Assim, detalhes fora da área autorizada ficam travados.

## Comando original da chamada

Executar no mesmo Terminal em que `OPENAI_API_KEY` foi configurada:

```bash
cd "/Users/kauanclaudinodossantos/Documents/Next-Assessoria/Clientes/Garage 665/Referencias/Projeto-Tratativa-Garage-665"
./scripts/finalizar_piloto_panamera.sh
```

O programa:

1. confirma que a chave está disponível;
2. impede uma segunda cobrança se já houver resultado;
3. realiza uma edição `gpt-image-2` em qualidade alta;
4. trava todos os pixels externos à máscara;
5. aplica o tampa-placa oficial no quadrilátero medido;
6. cria o master 4096 × 3072;
7. aplica o logo oficial sem regeneração;
8. exporta Feed 4096 × 3072, Story horizontal 3840 × 2160 e Webmotors 1920 × 1440.

## Arquivos para inspeção

- máscara do veículo: `trabalhos/panamera/frontal/M02-fundo-editavel-SAM2-v02.png`;
- prévia da máscara de reflexos: `trabalhos/panamera/frontal/preview-M03-M04-reflexos-localizados-FINAL.jpg`;
- composição antes da API: `trabalhos/panamera/frontal/composicao-estudio-SAM2-v02.png`;
- metadados e coordenadas: `trabalhos/panamera/frontal/manifesto.json`;
- entregas finais: `entregas/panamera-frontal-SAM2/`.

## Resultado para revisão

- master: `entregas/panamera-frontal-SAM2/panamera-frontal-master-4096x3072-v09.png`;
- Feed: `entregas/panamera-frontal-SAM2/v09/feed-4096x3072.jpg`;
- Story horizontal: `entregas/panamera-frontal-SAM2/v09/story-horizontal-3840x2160.jpg`;
- Webmotors: `entregas/panamera-frontal-SAM2/v09/webmotors-1920x1440.jpg`.

## Critério de aprovação

A primeira geração só é aprovada se a Panamera conservar exatamente a silhueta, os faróis, o escudo, as grades, os sensores, os retrovisores, o interior visível e o tom cinza metálico. A alteração autorizada é apenas a substituição dos reflexos externos reconhecíveis por reflexos largos e neutros do estúdio. Se a pintura ficar fosca, lisa como CGI ou mudar de tonalidade, a imagem é reprovada e a máscara/prompt deve ser corrigida antes de qualquer nova chamada.
