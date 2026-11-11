# Protocolo de avaliação

## Piloto funcional realizado

O piloto final de 10/11/2026 utilizou um participante, iluminação frontal e movimentos leves. Cada tentativa começou com calibração numérica em posição frontal, seguida pelas quatro direções, retornos ao centro e piscada. Das cinco tentativas calibradas, três concluíram a sequência e duas foram reiniciadas.

O participante confirmou a correspondência dos avanços com as ações realizadas. Esse autorrelato global e os eventos registrados demonstram funcionamento no piloto, sem constituir rotulagem independente ou estimativa de acurácia. Os dados resumidos estão em `resultados/piloto_calibrado.json` e `resultados/piloto_resumo.csv`.

## Avaliação independente proposta

A avaliação planejada compreende seis participantes, duas condições de iluminação, cinco ações e três repetições: 180 tentativas. Dois participantes seriam destinados ao desenvolvimento e quatro ao teste. Essa coleta ainda não foi realizada; o número é planejamento, não resultado.

Os participantes são identificados por códigos, sem documentos ou dados de pagamento. O procedimento depende de concordância dos participantes. Eventuais gravações externas para anotação exigem autorização específica; o aplicativo registra apenas medidas e eventos.

Um observador registra a ação efetivamente realizada e seus instantes inicial e final, independentemente da previsão do algoritmo. A referência temporal é o início da captura. Em vídeos, a análise requer FPS constante conhecido. O evento detectado não é utilizado como seu próprio rótulo verdadeiro.

As tentativas positivas abrangem a ação solicitada. As negativas incluem movimento contrário, ausência de movimento, piscada fora da etapa, fechamento prolongado, saída do quadro e múltiplas faces. Expirações permanecem registradas como falhas de reconhecimento.

## Formato e processamento

A tabela `dados/tentativas.csv` contém os rótulos, conforme o esquema em `dados/LEIA-ME.md`. Cada intervalo pertence a uma única etapa e não atravessa reinícios. O avaliador recusa sobreposições, intervalos vazios e participantes presentes simultaneamente em desenvolvimento e teste.

Execução a partir da raiz do projeto:

```bash
.venv/bin/python codigo/avaliar_sessoes.py
```

A tabela entregue não contém tentativas rotuladas independentemente; portanto, o avaliador não calcula uma taxa de acerto humano.

## Controle dos parâmetros

Os parâmetros estão em `codigo/configuracao.py`; cada execução registra a configuração utilizada. A seleção de limiares pertence ao conjunto de desenvolvimento. Ajustes posteriores à consulta do teste invalidam sua independência e exigem uma nova avaliação.

H e V são razões geométricas 2D, não ângulos. A calibração estima referências numéricas por sessão. O detector frontal pode perder a face em inclinações excessivas, limitando a interpretação das medidas.

## Comparação de equalização

A comparação utiliza o mesmo vídeo autorizado, FPS, regras e limites, variando somente `--equalizar`. As duas condições usam `--sem-ajuste`, evitando que referências recalculadas alterem outro fator do experimento. O ensaio estático em `codigo/avaliar_imagens.py` já mantém parâmetros fixos entre os modos.

## Métricas previstas

Reconhecimento por ação, aceitação indevida nas tentativas negativas, latência nos acertos, expirações e tempo de processamento. Resultados de imagens estáticas permanecem separados dos resultados de movimentos. Gráficos e totais devem ser rastreáveis às observações e configurações correspondentes.
