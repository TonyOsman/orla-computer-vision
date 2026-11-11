# Rastreabilidade das técnicas

## Técnicas centrais

| Parte | Evidência de aula | O que foi adaptado |
|---|---|---|
| Imagem como matriz, leitura, conversão, redimensionamento | Lab01 IntroPID | Enquadramento e exibição na Orla |
| Operações de pixels, recorte | Lab01/Lab02 | Casos de iluminação e composição de controles |
| Histograma e equalização | Lab03 | Comparação controlada antes/depois |
| Webcam e laço OpenCV | Lab03/Lab12 | Instruções e registro de medidas |
| Detector frontal dlib e predictor de 68 pontos | Lab12 | Uso dos pontos em uma interação guiada |
| EAR e distâncias com math.dist | Lab12, detector de fadiga | Contar abrir-fechar-abrir, com tempo mínimo/máximo |
| Contorno, texto e estados | Lab11/Lab12 | Tela, progresso, reinício e interrupções |
| time.perf_counter | Lab13, exemplo de vídeo | Durações reais e tempo de processamento |
| Matplotlib, plots, histogramas | Lab01/Lab03 | Análise das medições |

As regras H e V são adaptações autorais de coordenadas, distâncias e condicionais. Os laboratórios fornecem os fundamentos de detecção e landmarks, não um classificador pronto das quatro direções. Não há estimador 3D.

## Código auxiliar

Leitura/escrita de texto, listas, dicionários, zip, funções, condições e asserts são Python básico, pré-requisito do curso. `Path` aparece no Lab13. `sys.argv` serve apenas para escolher entrada de execução, não é algoritmo de visão. Exportação `savefig` registra os gráficos exigidos no enunciado; não adiciona método de processamento. `imwrite` é exemplificado nos labs. Não há framework adicional no aplicativo.

Os PDFs foram diagramados externamente ao projeto: ReportLab não faz parte da implementação de visão computacional nem dos requisitos do app. O notebook usa ambiente Jupyter, sugerido pelo professor. A imagem NASA é somente dado de ensaio, sem utilizar algoritmos do scikit-image.

## Não utilizados

DeepFace, InsightFace, FaceNet, embeddings de identidade, estimadores 3D, solvePnP, detectores de deepfake, modelos de emoção, TensorFlow/PyTorch, APIs de IA, Flask, FastAPI, Streamlit, React, RabbitMQ e criptografia própria.

O escopo da implementação restringe-se às operações e fundamentos identificados na tabela. O uso de uma biblioteca não implica adoção de todos os seus algoritmos.

## Ajuste numérico por sessão

Acrescentado após o piloto de limites fixos: listas de medidas, média aritmética com sum/len, intervalo de estabilidade com min/max e condicionais. Não utiliza novo modelo, foto de referência, reconhecimento de identidade ou biblioteca adicional. Frações e margens são decisões autorais a avaliar.

## Referências

- [Lab01 — imagens](https://arnaldojr.github.io/cognitivecomputing/aulas/PDI/lab01/IntroPID.html)
- [Lab03 — histogramas e webcam](https://arnaldojr.github.io/cognitivecomputing/aulas/PDI/lab03/atividade3.html)
- [Lab11 — interação](https://arnaldojr.github.io/cognitivecomputing/aulas/PDI/lab15/EventMouse.html)
- [Lab12 — dlib e EAR](https://arnaldojr.github.io/cognitivecomputing/aulas/PDI/lab16/dlib2.html)
- [Lab13 — temporização](https://arnaldojr.github.io/cognitivecomputing/aulas/PDI/lab17/mediapipe.html)
