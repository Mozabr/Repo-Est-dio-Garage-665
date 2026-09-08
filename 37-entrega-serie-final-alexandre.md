# Entrega da série final — Alexandre / Garage 665

## Autoridade visual aprovada

A frontal anexada pelo usuário em 08/09/2026 foi congelada sem alteração em
`trabalhos/panamera/previews-validacao-v12/externas/frontal-aprovada-anexo.png`.
Ela substitui as V05 e V06 como autoridade visual da vista frontal. O arquivo
mantém a leitura aprovada dos vincos, do brilho metálico, do para-brisa, do
estúdio e da placa Garage 665.

## Conjunto

O pacote possui sete vistas externas e três internas:

1. dianteira 3/4;
2. frontal;
3. perfil;
4. dianteira 3/4 oposta;
5. perfil oposto;
6. traseira 3/4;
7. traseira 3/4 oposta;
8. interior amplo;
9. painel e instrumentos;
10. interior do motorista.

Cada vista contém uma cópia da prévia aprovada, um master PNG 4096 × 3072 e
três derivados sRGB: Feed 4096 × 3072, Story horizontal 3840 × 2160 e
Webmotors 1920 × 1440. Os derivados nascem do mesmo master; não há uma nova
interpretação generativa para cada formato.

## Execução

```bash
./scripts/finalizar_serie_panamera_alexandre.sh
```

Destino: `entregas/panamera-serie-final-alexandre`. O arquivo
`MANIFESTO-SHA256.txt` permite verificar se alguma imagem foi alterada durante
o envio.

## Limitação declarada

Os masters 4096 × 3072 são ampliações Lanczos das fontes aprovadas em 4:3. Não
devem ser descritos como captura óptica 4K nativa. A ampliação não redesenha o
carro e não cria detalhes novos.

