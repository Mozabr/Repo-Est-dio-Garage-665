# Modos de uso do projeto Garage 665

Este documento explica como continuar o projeto sem depender do chat ou da máquina original.

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

## Modo 7 — reproduzir a candidata lateral v11

Este comando não chama a API. Ele reconstrói a seleção contínua M13+M14+M15, neutraliza a reflexão externa quente, recupera a resposta do verniz somente em Lab L e reintegra o resultado sobre o quadro v25 aprovado:

```bash
./scripts/executar_lateral_continua_v6f.sh
```

Avalie apenas `trabalhos/panamera/refinamento-dianteira-v6f/lateral-material/M13M14M15-lateral-continua-v11/candidato-quadro-completo.png`. O doador arquivado com `rejeitado-diagnostico` nunca é entrega e não deve ser aplicado diretamente.

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
