# Modos de uso do projeto Garage 665

Este documento explica como continuar o projeto sem depender do chat ou da máquina original.

## Série v10 — mesmo estúdio em externas e internas

Prévia local sem cobrança:

```bash
./scripts/gerar_previews_panamera_v10.sh
```

Novo perfil com teto canônico via GPT Image 2 high:

```bash
./scripts/executar_perfil_serie_v10_api.sh
```

Três internas, somente após revisar as máscaras em
`trabalhos/panamera/serie-v10/interiores-api/preparo`:

```bash
./scripts/executar_interiores_serie_v10_api.sh painel-instrumentos
```

Após a aprovação, substitua o argumento por `interior-amplo`,
`interior-motorista` ou `todos`. Cada resultado existente é ignorado para
impedir cobrança duplicada.

## Modo 1 — continuar neste Mac

1. Abra a pasta do projeto.
2. Confirme que a branch `main` está atualizada.
3. Leia `COMECE-AQUI.md` antes de trabalhar.
4. Use os ambientes `.venv` e `.venv-mask` já instalados.
5. Faça somente a etapa indicada no estado atual.
6. Valide técnica e visualmente antes de avançar.
7. Commit e push depois de cada alteração validada.

Comandos de sincronização:

```bash
git pull --ff-only
git status
```

## Modo 2 — usar em outro computador

```bash
git clone https://github.com/Mozabr/Repo-Est-dio-Garage-665.git
cd Repo-Est-dio-Garage-665
bash scripts/configurar_novo_computador.sh
```

Depois, leia nesta ordem:

1. `COMECE-AQUI.md`;
2. `HANDOFF.md`;
3. `ESTADO-ATUAL.md`;
4. o documento da versão ativa, atualmente `27-pipeline-material-v6f.md`.

Os pesos dos modelos e ambientes virtuais não estão no GitHub; o instalador os reconstrói nas versões registradas. As imagens, máscaras, relatórios, prompts e doador pago necessários à retomada estão versionados.

## Modo 3 — continuar em outra conta ou chat

1. Dê ao novo agente acesso ao repositório.
2. Informe que o repositório é a fonte de verdade.
3. Cole o conteúdo de `PROMPT-PARA-RETOMAR.md`.
4. Exija que o agente leia os documentos antes de executar comandos.
5. Não permita uma nova chamada de API se o doador correspondente já existir.
6. Peça que toda decisão seja registrada e enviada ao GitHub.

## Modo 4 — validação local sem custo de API

Para reconstruir e auditar a composição determinística do Studio v2:

```bash
bash scripts/executar_studio_v2.sh
```

Esse comando não aprova automaticamente o v6f e não substitui a comparação visual.

## Modo 5 — geração paga pela OpenAI

Use somente quando a etapa exigir explicitamente um novo doador e não houver arquivo bruto equivalente. Configure a chave apenas no Terminal atual:

```bash
export OPENAI_API_KEY="sua-chave"
```

Nunca grave a chave em arquivos do projeto. Antes de executar, confira o script: ele deve bloquear duplicação quando a resposta bruta já existir. Cada superfície deve ser tratada isoladamente e aprovada antes da próxima.

## Modo 6 — recomposição com um doador existente

Este é o modo atual do capô v6f. Ele não faz nova chamada à API. A candidata v25, com key frontal suave no centro do capô, pode ser reproduzida com:

```bash
./scripts/executar_recomposicao_capo_v6f_v25.sh
```

O script usa o doador já pago, transfere somente luminância alinhada, preserva geometria/cor/textura da fonte, executa os gates e só cria o quadro completo quando a validação técnica passa. A passagem técnica não substitui a aprovação visual humana.

## Modo 7 — diagnóstico local v11 reprovado

Este comando não chama a API. Ele reproduz apenas o diagnóstico v11, reprovado visualmente por aparência fosca:

```bash
./scripts/executar_lateral_continua_v6f.sh
```

O resultado v11 nunca é entrega. Para avançar, use o modo pago M13 abaixo.

## Modo 8 — executar uma única chamada paga M13

Com `OPENAI_API_KEY` disponível no mesmo Terminal:

```bash
./scripts/executar_teste_m13_api_v6f.sh
```

Esse comando já foi executado: não o execute novamente. O bruto em `M13-paralama-proximo-api-v02/doador-bruto-api-rejeitado-como-imagem.png` é a trava de cobrança. A candidata atual, recalibrada localmente sem nova chamada, está em `M13-paralama-proximo-api-v03/candidato-quadro-completo.png`.

## Fluxo de versionamento

Depois de uma alteração aprovada:

```bash
git status
git add <arquivos-da-etapa>
git commit -m "Descreva objetivamente a alteração"
git push
```

Não use `git add .` sem revisar, não versione `.env`, chaves, ambientes virtuais ou pesos de modelos. Diferencie nos documentos e nomes de arquivos: `diagnostico`, `candidato`, `aprovado` e `reprovado`.

## Formatos finais

- Master e Feed: 4096 × 3072.
- Story horizontal: 3840 × 2160.
- Webmotors: 1920 × 1440.

Todos devem derivar do mesmo master aprovado.
