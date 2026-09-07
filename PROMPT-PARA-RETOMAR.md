# Prompt para retomar em outro chat ou agente

Copie o texto abaixo somente depois de disponibilizar o repositório para a nova ferramenta:

```text
Continue o projeto de tratamento fotográfico Garage 665 a partir do estado real registrado no repositório. Antes de executar qualquer ação, leia integralmente README.md, COMECE-AQUI.md, HANDOFF.md, ESTADO-ATUAL.md e 27-pipeline-material-v6f.md. Depois valide os arquivos e relatórios citados nesses documentos.

Não reinicie o projeto e não repita etapas concluídas. O foco atual é a vista dianteira 3/4 da Porsche Panamera, no pipeline de material v6f. O capô v25 foi aprovado visualmente pelo usuário e está congelado. A lateral v11 passou tecnicamente, mas foi reprovada visualmente por aparência ainda fosca e deve permanecer apenas como diagnóstico. A próxima ação autorizada é uma única chamada paga M13 por `./scripts/executar_teste_m13_api_v6f.sh`. O script usa o snapshot gpt-image-2-2026-04-21 em qualidade alta, bloqueia repetição e transfere somente Lab L do doador contido. M14 e M15 permanecem bloqueadas até a aprovação explícita de M13.

O carro é documento e o estúdio é direção de arte. Preserve geometria, cor registrada, textura fotográfica, rodas, esterçamento, faróis, emblemas, badge E-Hybrid, vidros, interior, maçanetas, vãos e proporções. IA pode fornecer somente luminância alinhada dentro de uma máscara revisada. Exija zero mudança fora da máscara. Não use RGB ou textura fina gerados no resultado. Não deixe a pintura fosca, acetinada, envelopada ou uniforme.

Depois da aprovação visual explícita de M13, prepare e execute M14; depois da aprovação de M14, prepare M15. Só então avance para teto e vidros, sempre a partir da fonte de autoridade. O vidro deve continuar translúcido e apenas perder reflexos externos reconhecíveis. Não avance silenciosamente se uma etapa falhar. Ao final, gere um único master/Feed 4096x3072, Story horizontal 3840x2160 e Webmotors 1920x1440. Não gere os formatos separadamente.

Registre toda decisão, parâmetros, hashes, métricas e arquivos novos no repositório. Diferencie com clareza: aprovado, candidato, diagnóstico e reprovado. Não descreva a saída ampliada como 4K nativo e não prometa cor física absoluta porque as fontes não têm RAW nem ColorChecker.
```
