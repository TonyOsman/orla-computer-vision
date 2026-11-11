# Dados e origem

`astronauta.png`: retrato de Eileen Collins, NASA, disponibilizado no acervo do scikit-image como imagem de domínio público. Origem do arquivo: https://raw.githubusercontent.com/scikit-image/scikit-image/v0.25.2/skimage/data/astronaut.png

Descrição e procedência: https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.astronaut

Usado somente em ensaio de leitura, detecção e pré-processamento. A biblioteca scikit-image não é usada pelo projeto. Esta imagem NÃO é uma foto previamente cadastrada, identidade de referência ou exemplo de movimento real.

`tentativas.csv`: tabela inicialmente sem observações, a preencher após coleta e rotulagem independentes. Não contém resultados humanos fictícios.

Colunas:

- `arquivo_frames`: caminho relativo para o log de uma execução, por exemplo `resultados/sessao_.../frames.csv`.
- `participante`: código como P01, sem nome.
- `grupo`: DESENVOLVIMENTO ou TESTE; uma pessoa não pode estar nos dois grupos.
- `condicao`: descrição curta, sem ponto e vírgula, como `luz_frontal_original`.
- `inicio_s`, `fim_s`: intervalo observado, incluindo início e excluindo fim. Início deve marcar o começo real da ação, não apenas a instrução.
- `acao_real`: ação anotada pelo observador; por exemplo ESQUERDA, DIREITA, CIMA, BAIXO, CENTRO, PISCADA ou SEM_MOVIMENTO.
- `alvo`: etapa solicitada pelo sistema naquele intervalo.

Exemplo de formato (não copiar como resultado real): `resultados/sessao_ID/frames.csv;P01;DESENVOLVIMENTO;luz_frontal;2.0;4.0;ESQUERDA;ESQUERDA`.

A avaliação compara eventos da sequência com os rótulos. Uma janela positiva contém ação_real igual ao alvo; uma negativa contém outra ação. O mesmo intervalo não pode ser contado duas vezes. Não atravessar reinícios nem mudanças de etapa na anotação. Rever manualmente caso a instrução e o movimento executado divirjam.

O aplicativo não grava imagens da câmera. Para rotulagem rigorosa, um observador deve acompanhar e registrar tempos; gravações independentes exigem autorização dos participantes e ficam fora do Git por padrão. Sem rótulo independente, os logs medem o funcionamento, não a acurácia.
