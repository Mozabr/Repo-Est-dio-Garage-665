# Prompt para retomar em outro chat ou agente

Copie o texto abaixo somente depois de disponibilizar o repositório para a nova ferramenta. A atualização v11 abaixo substitui os fluxos multivista anteriores:

```text
Continue o projeto de tratamento fotográfico Garage 665 a partir do estado real registrado no repositório. Antes de executar qualquer ação, leia integralmente README.md, COMECE-AQUI.md, HANDOFF.md, ESTADO-ATUAL.md e 34-padrao-mestre-teste-05-v11.md. Depois valide os arquivos e relatórios citados nesses documentos. A master teste 05 é autoridade integral de sala, teto, parede, piso, placa, temperatura, contraste, sombra e resposta do verniz. A fotografia original de cada ângulo é autoridade de identidade, geometria, cor base e detalhes. As previews v10 foram reprovadas como resultado visual e servem somente de alvo técnico já posicionado no Studio G.

O primeiro teste ativo é exclusivamente o perfil em 1600x1200 pelo comando `./scripts/executar_externa_serie_v11_api.sh perfil`. Não execute a série em lote. Confira `trabalhos/panamera/serie-v11/perfil/api-v01/comparacao-master-alvo-candidata.jpg` e só avance após aprovação humana. A dianteira 3/4 teste 05 já está aprovada e não deve ser regenerada. O modelo fica fixo em `gpt-image-2-2026-04-21`, qualidade high.

Não reinicie o projeto e não repita etapas concluídas. O foco atual é a vista dianteira 3/4 da Porsche Panamera na harmonização integral v8. Leia também `30-harmonizacao-integral-v8.md`. Por decisão explícita do usuário, `refinamento-dianteira-v6/teste-M11-capo-centro-api/geracao-bruta-api.png` é a autoridade visual e geométrica do quadro atual. A candidata a avaliar é `refinamento-dianteira-v8/harmonizacao-integral-v07-clearcoat-final/candidato-quadro-completo.png`. Os doadores integrais já existem; nunca repita essas gerações nem chamadas pagas cujos doadores estejam arquivados.

O carro é documento e o estúdio é direção de arte. Preserve geometria, cor registrada, textura fotográfica, rodas, esterçamento, faróis, emblemas, badge E-Hybrid, vidros, interior, maçanetas, vãos e proporções. IA pode fornecer somente luminância alinhada dentro de uma máscara revisada. Exija zero mudança fora da máscara. Não use RGB ou textura fina gerados no resultado. Não deixe a pintura fosca, acetinada, envelopada ou uniforme.

A v07 já foi aprovada e a master dianteira 3/4 já foi exportada; não a refaça. Abra as folhas de contato em `trabalhos/panamera/previews-serie-v8` e prossiga somente após aprovação humana das vistas. As externas são previews de composição e ainda contêm reflexos urbanos; adapte o tratamento v07 por ângulo. As internas foram apenas convertidas para sRGB e redimensionadas. Para cada vista aprovada, gere um único master/Feed 4096x3072, Story horizontal 3840x2160 e Webmotors 1920x1440. Não gere os formatos separadamente.

Registre toda decisão, parâmetros, hashes, métricas e arquivos novos no repositório. Diferencie com clareza: aprovado, candidato, diagnóstico e reprovado. Não descreva a saída ampliada como 4K nativo e não prometa cor física absoluta porque as fontes não têm RAW nem ColorChecker.
```
