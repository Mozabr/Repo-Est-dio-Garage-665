# Fluxo recorrente — novos veículos

## Configuração única

1. Receber o logo oficial em PNG transparente ou SVG. **Concluído: PNG transparente de 1080 × 1080 px.**
2. Criar as cinco placas-mestre da sala branca. **Em andamento: `STUDIO_A` criado e validado com o Porsche 991.**
3. Aprovar arquitetura, piso, logo, temperatura de cor e posição das luzes.
4. Congelar essas placas como referências permanentes; não regenerá-las por veículo.

## A cada novo veículo

1. Receber todos os arquivos originais, sem compressão de WhatsApp.
2. Classificar cada foto pelo ângulo `STUDIO_A` a `STUDIO_E`.
3. Corrigir exposição e perspectiva antes da composição.
4. Editar uma imagem por vez usando o carro, a placa-mestre correta e o logo oficial como entradas separadas.
5. Comparar com o original em 100% usando o checklist de fidelidade.
6. Corrigir apenas uma falha por iteração.
7. Guardar o master 4K sem sobrescrever o original e exportar as três saídas obrigatórias: Feed 4096 × 3072 (4:3 horizontal), Story 3840 × 2160 (16:9 horizontal) e Webmotors 1920 × 1440 (4:3 horizontal).

## Informações mínimas que acompanham cada envio

- marca, modelo, versão e ano;
- cor oficial da pintura, se conhecida;
- ordem desejada do carrossel;
- regra da placa: manter, desfocar ou substituir por placa institucional;
- indicação de qualquer avaria que precisa continuar visível;
- foto escolhida como capa, se já definida.

## Convenção de nomes

```text
entrada:  marca-modelo-ano-angulo-original.ext
prova:    marca-modelo-ano-angulo-prova-v01.png
aprovado: marca-modelo-ano-angulo-final-v01.jpg
```

## Observação operacional

O logo não deve depender apenas da geração. Se houver qualquer divergência visual, a versão final deve receber o arquivo oficial como composição exata na pós-produção, preservando a identidade da marca sem aproximações.
