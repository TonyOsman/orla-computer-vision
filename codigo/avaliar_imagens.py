"""Ensaio de processamento em retrato público, sem inferência sobre movimentos reais."""

from pathlib import Path
import time
import cv2
import dlib
import numpy as np
from matplotlib import pyplot as plt
from metodos import observar
from orla_interacao import desenhar

RAIZ = Path(__file__).resolve().parent.parent


def executar():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(RAIZ / "modelos/shape_predictor_68_face_landmarks.dat"))
    imagem = cv2.imread(str(RAIZ / "dados/astronauta.png"))
    if imagem is None:
        raise ValueError("Imagem de ensaio ausente.")
    # Operações de pixel e composição de matrizes, como nos labs iniciais.
    escura = np.array(imagem * 0.45, dtype=np.uint8)
    muito_escura = np.array(imagem * 0.15, dtype=np.uint8)
    dupla = np.zeros((512, 1024, 3), dtype=np.uint8)
    dupla[:, :512] = imagem
    dupla[:, 512:] = imagem
    casos = [("original", imagem, 1), ("escura_045", escura, 1),
             ("escura_015", muito_escura, 1),
             ("sem_face", np.zeros(imagem.shape, dtype=np.uint8), 0), ("duas_faces", dupla, 2)]
    linhas = []
    observar(imagem, detector, predictor)  # aquecimento fora das medidas
    for nome, frame, esperado in casos:
        for equalizar in (False, True):
            for repeticao in range(3):
                tic = time.perf_counter()
                obs = observar(frame, detector, predictor, equalizar)
                ms = (time.perf_counter() - tic) * 1000
                linhas.append([nome, int(equalizar), repeticao + 1, esperado, obs["faces"],
                               int(obs["valida"]), obs["classe"], ms])
                if nome == "original" and not equalizar and repeticao == 0:
                    cv2.imwrite(str(RAIZ / "resultados/interface_ensaio.png"), desenhar(frame, obs, None, False, 0))
    with open(RAIZ / "resultados/ensaio_imagens.csv", "w", encoding="utf-8") as arquivo:
        arquivo.write("caso;equalizado;repeticao;faces_esperadas;faces_detectadas;valida;classe;processamento_ms\n")
        for linha in linhas:
            arquivo.write(";".join(str(v) for v in linha) + "\n")
    fig = plt.figure(figsize=(10, 5))
    for eq, rotulo in [(0, "Cinza original"), (1, "Cinza equalizado")]:
        tempos = []
        for nome, _, _ in casos:
            valores = [r[7] for r in linhas if r[0] == nome and r[1] == eq]
            tempos.append(sum(valores) / len(valores))
        plt.plot([c[0] for c in casos], tempos, marker="o", label=rotulo)
    plt.ylabel("Tempo medio de processamento (ms)")
    plt.xlabel("Ensaio controlado - 1 retrato, variantes e controles")
    plt.title("Tempo observado; 3 repeticoes por configuracao")
    plt.legend()
    plt.tight_layout()
    fig.savefig(RAIZ / "resultados/tempo_processamento.png", dpi=160)
    plt.close(fig)
    fig = plt.figure(figsize=(10, 4))
    gray = cv2.cvtColor(escura, cv2.COLOR_BGR2GRAY)
    plt.plot(cv2.calcHist([gray], [0], None, [256], [0, 256]), label="Escura 0.45")
    plt.plot(cv2.calcHist([cv2.equalizeHist(gray)], [0], None, [256], [0, 256]), label="Equalizada")
    plt.xlabel("Intensidade")
    plt.ylabel("Pixels")
    plt.title("Histograma do ensaio: equalizacao redistribui intensidades")
    plt.legend()
    plt.tight_layout()
    fig.savefig(RAIZ / "resultados/histograma.png", dpi=160)
    plt.close(fig)
    fig = plt.figure(figsize=(10, 5))
    for i, equalizar in enumerate((False, True)):
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        processada = cv2.equalizeHist(gray) if equalizar else gray
        faces = detector(processada, 0)
        visual = imagem.copy()
        for face in faces:
            cv2.rectangle(visual, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
        plt.subplot(1, 2, i + 1)
        plt.imshow(cv2.cvtColor(visual, cv2.COLOR_BGR2RGB))
        plt.title(("Equalizado" if equalizar else "Original") + f": {len(faces)} deteccoes")
        plt.axis("off")
    plt.tight_layout()
    fig.savefig(RAIZ / "resultados/deteccoes_comparadas.png", dpi=160)
    plt.close(fig)
    print("Ensaio concluído:", len(linhas), "execuções em 5 cenários, derivados de 1 retrato.")
    print("Não mede reconhecimento de movimentos ou desempenho em participantes.")
    return linhas


if __name__ == "__main__":
    executar()
