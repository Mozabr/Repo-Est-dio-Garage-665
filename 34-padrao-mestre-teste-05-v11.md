# Padrão mestre `teste 05` — série v11

## Correção de rumo

As previews v10 foram reprovadas em 08/09/2026 como resultado visual. Elas
confirmavam apenas enquadramento e arquitetura; o carro ainda carregava luz e
reflexos da rua. Não devem ser apresentadas, aprovadas ou exportadas como fotos
tratadas.

A partir da v11, `teste 05` é a autoridade integral do estúdio e não apenas uma
referência de fundo. O arquivo portátil e seu hash estão congelados em:

`referencias/autoridades/panamera-master-estudio-canonico-v01.png`

SHA-256:
`8fb6dfb73e162bf92d5baf418ccd43ca308dfadde87f9457bcada27fa2ccb27e`

## O que precisa ser idêntico em toda a série

- Studio G com teto plano off-white contínuo, sem painel retangular aparente;
- mesma parede, cyclorama, piso, placa matte e sombra curta dos afastadores;
- balanço neutro de aproximadamente 5200 K;
- key grande alta/frontal-esquerda; fill direito -2 EV; fill frontal -3 EV;
- sombras abertas, contraste moderado e contato natural dos pneus;
- pintura grafite metálica escura com clear-coat polido e highlights largos;
- vidros translúcidos, sem preto artificial e sem reflexos urbanos literais;
- mesma granulação fina e nitidez fotográfica da master.

## Autoridades que não podem ser misturadas

1. `teste 05`: ambiente, luz, contraste, sombra e resposta do verniz.
2. Fotografia original do ângulo: geometria, identidade, cor base e detalhes.
3. Preview v10 do ângulo: somente alvo técnico já posicionado no Studio G.
4. Resposta GPT Image 2: candidata; nunca aprovada automaticamente.

O teto de qualquer geração anterior diferente da master deve ser ignorado.

## Fluxo oficial e econômico

1. Gerar uma única candidata de calibração em 1600 × 1200, começando por
   `perfil`.
2. Conferir lado a lado com `teste 05` e a fotografia original.
3. Reprovar se houver roda virada, mudança de emblema, vidro preto, pintura
   matte, halo, recorte ou reflexo urbano residual.
4. Ajustar o prompt/configuração uma única vez.
5. Só então executar, uma a uma, as demais vistas externas.
6. Aplicar o mesmo lock luminoso aos interiores, com fundo desfocado visto pelos
   vidros e proteção integral de volante, instrumentos, textos e comandos.
7. Gerar masters 4096 × 3072 e derivados apenas após aprovação humana.

Nos interiores, o cenário generativo é limitado ao exterior visto pelos vidros.
Isso é indispensável para não recriar volante, instrumentos ou comandos. Depois
que o perfil externo estiver aprovado, a primeira calibração interna será a
vista crítica próxima ao volante:

```bash
./scripts/executar_interior_serie_v11_api.sh painel-instrumentos
```

Não existe opção `todos`: cada foto interna precisa de aprovação individual.

Primeiro comando pago da v11:

```bash
./scripts/executar_externa_serie_v11_api.sh perfil
```

O resultado fica em:

`trabalhos/panamera/serie-v11/perfil/api-v01/candidato-contido.png`

O script bloqueia uma segunda cobrança quando a resposta bruta já existe.

## Ordem após aprovação do perfil

```text
perfil → frontal → dianteira-3-4-oposta → traseira-3-4 →
traseira-3-4-oposta → perfil-oposto → interiores
```

A dianteira 3/4 aprovada (`teste 05`) não será regenerada.
