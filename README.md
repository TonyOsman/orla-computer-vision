# Orla — interação facial guiada

**Tony Khaled Osman — RM 553050**

**Inacia dos Santos Silva — RM 553401**

Cognitive Computing, Computer Vision and IoT Systems — Professor Arnaldo Jr.

Protótipo local em Python que utiliza OpenCV e dlib para detectar uma face, estimar 68 pontos faciais e acompanhar quatro direções da cabeça e uma piscada completa. Integra o tema Orla por meio de uma solicitação fictícia de documento. Não reconhece identidade nem autoriza transações.

## Demonstração

Vídeo de um aluno demonstrando o funcionamento da aplicação. Clique na imagem para abrir o vídeo.

[![Demonstração da Orla por um aluno](documentacao/midia/demonstracao-orla.jpg)](https://github.com/TonyOsman/orla-computer-vision/blob/main/documentacao/midia/demonstracao-orla.mp4)

[Assistir à demonstração](https://github.com/TonyOsman/orla-computer-vision/blob/main/documentacao/midia/demonstracao-orla.mp4)

## Instalação — Ubuntu/Linux

Ambiente verificado: Python 3.12, Linux x86-64, webcam e sessão gráfica local. Windows e macOS não foram testados. Execute os comandos no terminal, na raiz do projeto, onde está este README. Após clonar o repositório, essa pasta é `orla-computer-vision`; no ZIP, ela se chama `orla`.

1. Instale os pré-requisitos do sistema (Ubuntu com Python 3.12):

```bash
sudo apt update
sudo apt install python3.12-venv python3.12-dev build-essential cmake libgl1 libglib2.0-0 wget bzip2
```

2. Crie o ambiente e instale as bibliotecas. Execute a próxima linha somente se a anterior terminar sem erro:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

A compilação do dlib pode demorar. A pasta `.venv` é criada localmente e não faz parte do repositório.

3. Baixe o modelo oficial de 68 pontos (necessário na cópia clonada; o ZIP de entrega já inclui o modelo):

```bash
wget -O modelos/shape_predictor_68_face_landmarks.dat.bz2 https://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d modelos/shape_predictor_68_face_landmarks.dat.bz2
```

Execute uma única vez, se `modelos/shape_predictor_68_face_landmarks.dat` ainda não existir. Confira o arquivo:

```bash
sha256sum modelos/shape_predictor_68_face_landmarks.dat
```

Resultado esperado: `fbdc2cb80eb9aa7a758672cbfdda32ba6300efe9b6e6c7a299ff7e736b11b92f`. Origem e condições de uso: `modelos/INSTRUCOES.md`.

## Executar

No terminal, na raiz do projeto:

```bash
.venv/bin/python codigo/orla_interacao.py --camera 0
```

Não é necessário ativar o ambiente para usar esse comando. No VS Code, abra a raiz do projeto e use **Terminal → Novo Terminal**. O argumento `--camera 0` seleciona a webcam; sem ele o script apenas exibe a ajuda. A câmera não é aberta durante instalação ou testes de lógica.

- **ESPAÇO:** iniciar; olhar de frente com olhos abertos até concluir a calibração.
- **R:** reiniciar e recalibrar.
- **Q:** encerrar e liberar a câmera.

Faça movimentos leves, com iluminação frontal e uma única pessoa no quadro. Feche outros aplicativos que utilizem a câmera. Se necessário, troque `0` pelo índice da câmera desejada. O programa salva medidas e eventos, mas não grava imagens. Exige sessão gráfica; não use OpenCV headless.

## Organização

| Pasta/arquivo | Conteúdo |
|---|---|
| `codigo/` | Aplicação, métodos, configuração, testes e scripts de avaliação |
| `notebooks/` | Notebook executado de análise dos resultados |
| `documentacao/` | Relatório PDF, rastreabilidade das técnicas e protocolo de avaliação |
| `dados/` | Imagem pública de ensaio, sua origem e tabela de rótulos |
| `modelos/` | Instruções de origem/licença e destino do download do modelo |
| `resultados/` | Gráficos, medidas, testes e resumo do piloto |
| `requirements.txt` | Dependências da aplicação |
| `requirements-notebook.txt` | Dependências adicionais para o notebook |

## Reproduzir a avaliação

Execute na raiz do projeto:

```bash
.venv/bin/python codigo/testar_logica.py
.venv/bin/python codigo/avaliar_imagens.py
.venv/bin/python codigo/avaliar_sessoes.py
```

O primeiro comando verifica 26 cenários de lógica. O segundo reproduz o ensaio de imagem e atualiza seus gráficos/tempos. O terceiro depende de rótulos independentes em `dados/tentativas.csv`; a tabela entregue está vazia e não produz uma taxa de acerto humano.

Para executar o notebook:

```bash
.venv/bin/python -m pip install -r requirements-notebook.txt
.venv/bin/python -m jupyterlab notebooks/analise_resultados.ipynb
```

## Resultados e limites

Os 26 testes de lógica passaram. O ensaio estático compreende cinco cenários derivados de um retrato público, dois modos de pré-processamento e três repetições: 30 execuções, não 30 pessoas. A equalização produziu falsos positivos adicionais nesse ensaio.

No piloto funcional de 10/11/2026 com um participante, três das cinco tentativas calibradas concluíram a sequência; duas foram reiniciadas. As conclusões levaram 13,351 s, 22,494 s e 17,997 s após a calibração. O participante confirmou movimentos leves e avanços correspondentes. São eventos do programa e autorrelato, sem rotulagem independente por ação: não representam acurácia populacional ou proteção antifraude.

O ajuste inicial calcula referências numéricas, sem foto cadastrada. O EAR frontal é exigido no centro e na preparação da piscada; os movimentos direcionais usam face válida, classe e sustentação. Inclinação excessiva, iluminação e perda de landmarks ainda podem interromper a sequência.

Referências às aulas, justificativas e limitações constam em `documentacao/rastreabilidade.md` e `documentacao/relatorio.pdf`.
