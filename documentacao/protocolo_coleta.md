# Protocolo de coleta e avaliação

## Primeiro piloto funcional

1. Fechar aplicativos de câmera, usar iluminação frontal e executar `python codigo/orla_interacao.py --camera 0`.
2. Verificar uma face e índices na tela. Pressionar ESPAÇO e olhar reto, olhos abertos, durante o ajuste numérico de um segundo.
3. Seguir cada instrução com movimento leve; retornar ao centro quando solicitado. Na piscada, aguardar FECHAR e reabrir.
4. Anotar em quais etapas houve reconhecimento incorreto, demora ou expiração. Q encerra; registrar nome da pasta de logs.
5. Esse piloto orienta ajustes. Não contar os mesmos dados ajustados como teste independente.

## Avaliação final planejada

Proposta: seis pessoas, duas condições de luz, cinco ações, três repetições = 180 tentativas. Duas pessoas para desenvolvimento e quatro para teste. Isso é planejamento, não uma coleta já realizada. Se a amostra for menor, informar a quantidade efetiva.

Obter concordância dos participantes. Usar códigos P01, P02 etc. Sem documento, fotografia prévia ou dado de pagamento real. Um observador acompanha ações e tempos; se houver gravação externa para anotação, pedir autorização específica e não publicar por padrão.

Anotar o começo da ação real, não apenas o momento em que o app solicitou. O ajuste numérico grava a referência em calibracoes.txt. A pessoa precisa estar de frente nessa etapa. O log registra tempo relativo ao início da captura; para uma anotação temporal mais precisa, pode-se avaliar vídeo de FPS constante conhecido e referenciar seus tempos. Não usar o evento previsto como rótulo verdadeiro.

Manter tentativas positivas e negativas. Negativas: movimento contrário, não se mover, piscar fora da etapa, ficar de olhos fechados, sair do quadro ou incluir outra pessoa. Uma etapa que expirou deve constar como tentativa não reconhecida; não apagar erros.

Preencher `dados/tentativas.csv`, conforme o arquivo de instruções dos dados, e executar `python codigo/avaliar_sessoes.py`. Essa ferramenta recusa sobreposições, participantes nos dois grupos e intervalos vazios. O observador deve conferir que o alvo anotado é a etapa real da interface.

## Parâmetros

Alterar apenas `configuracao.py`, com justificativa baseada nas curvas do desenvolvimento. Guardar uma cópia dos parâmetros com os resultados (o app já faz isso). Não mudar fórmulas/limiares após consultar o teste e depois anunciar esse mesmo teste como independente.

H representa deslocamento horizontal normalizado do nariz; V representa posição vertical relativa a olhos e boca. Eles não medem graus. Evitar movimentos extremos que façam o detector frontal perder a face. Se um parâmetro só funcionar numa pessoa, registrar a limitação.

## Comparação de equalização

Preferir processar a mesma gravação autorizada duas vezes, com e sem `--equalizar`, usando mesmo FPS, regras e limites. Não comparar pessoas/iluminações diferentes como se a única mudança fosse o pré-processamento. Resultados de imagens estáticas e de vídeos devem ficar separados.

## Critérios a discutir na apresentação

Acertos e falhas por ação; aceitação indevida nas negativas; latência somente nos acertos; expirações separadas; desempenho do equipamento; efeito da iluminação; risco de confundir inclinação, expressão e identidade. Gráficos precisam apontar a origem dos dados.

### Comparação com limites realmente iguais

Para isolar o efeito da equalização em vídeo, executar as duas condições com `--sem-ajuste`, mesmo arquivo, FPS e configuracao.py. Sem essa opção, cada execução calcula sua própria referência e a comparação mede também o efeito do ajuste. O ensaio estático avaliar_imagens.py já usa parâmetros fixos iguais.
