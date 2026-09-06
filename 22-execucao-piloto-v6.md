# Execução do piloto v6 — dianteira 3/4

Data: 06/09/2026.

## Estado da etapa

- Rig congelado: `GARAGE665-RIG-V6-A`.
- Resolução de edição: 2048 × 1536, sRGB, sem corte.
- Modelo de profundidade: Depth Anything V2 Small, revisão `5426e4f0f36572d16453bbda7a8389317b1bef99`, Apache-2.0.
- Máscaras: nove superfícies separadas; contenção fora do veículo e sobre detalhes protegidos passou com zero pixels.
- Prompts: gerados a partir do mesmo rig e protegidos por hash.
- Geração integral do veículo: proibida.
- Master 4K: somente depois da aprovação em 2048 × 1536.

## Resultado do primeiro ensaio

O ensaio interno sem máscara nativa foi reprovado. O modelo limpou o capô, mas também reconstruiu perspectiva, vidro e proporções. O registro geométrico ultrapassou o limite de 12 px e nenhum pixel dessa geração foi incorporado ao master.

Conclusão: para o carro final, usar exclusivamente `images.edit` do GPT Image 2 com a máscara alfa aplicada à fotografia de autoridade. A imagem gerada continua sendo apenas uma proposta; a trava determinística e a recomposição de baixa frequência continuam obrigatórias.

O teste local de identidade da recomposição passou: zero pixel alterado fora da
máscara; deriva média de cromia Lab a/b de 0,018 e 0,002; RMS de microdetalhe
5,102 na fonte e 5,104 na saída. A mesclagem normalizada também passou com zero
alteração fora da união das máscaras e 17.856 pixels de transição tratados sem
somar duas edições.

O processo Codex atual não recebe a variável `OPENAI_API_KEY` exportada em outra
janela do Terminal. Por segurança, a chave não foi copiada nem solicitada no chat.
O executor `scripts/executar_teste_m11_v6.sh` deve ser disparado no mesmo Terminal
em que a variável já está disponível; ele faz uma única chamada mascarada M11,
arquiva a resposta bruta, trava os pixels e executa a recomposição.

## Gate de aprovação por superfície

1. A saída deve registrar sobre a fonte sem exceder 12 px e com pelo menos 60% de inliers.
2. Zero pixel fora da máscara pode ser alterado.
3. Emblemas, faróis, rodas, sensores, vincos e limites de painel permanecem da fotografia.
4. A direção da key permanece acima/frente/esquerda em toda a série.
5. Céu, nuvens, árvores, prédios, cabos, rua e faixas amarelas desaparecem da superfície editada.
6. A cor não pode mudar de família; o relatório de recomposição mede a deriva de cromia.
7. A microtextura não pode colapsar; comparar RMS de detalhe antes/depois.
8. Aprovam-se capô, teto, lateral e vidros separadamente antes de compor no estúdio.

## Ordem de execução

1. `M11-capo-centro`.
2. `M12-capo-lateral-distante` e `M12-capo-lateral-proxima`, sempre partindo da mesma fonte.
3. Mesclar as três propostas do capô sem acumular edições.
4. `M10-teto-pintura`.
5. `M13-paralama-proximo`.
6. `M14-portas-superiores` e `M15-portas-inferiores`.
7. `M16-para-brisa` e `M17-vidros-laterais`.
8. Compor no estúdio, reconstruir sombras e avaliar em 100% e 200%.
9. Testar Real-ESRGAN com denoise baixo e comparar contra Lanczos.
10. Somente após aprovação, exportar 4096 × 3072, 3840 × 2160 e 1920 × 1440.

## Regra de continuidade

Todas as superfícies são geradas a partir da fotografia de autoridade original, nunca do resultado da etapa anterior. Nas áreas de transição, candidatos aprovados são mesclados em uma única passagem com pesos normalizados. Isso evita acúmulo de reconstrução e deriva entre painéis.
