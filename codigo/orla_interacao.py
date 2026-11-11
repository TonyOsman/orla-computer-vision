"""Interface local OpenCV: câmera somente quando solicitada explicitamente."""

from pathlib import Path
import sys
import time
import cv2
import dlib
import numpy as np
from configuracao import PARAMETROS, SEQUENCIA, INSTRUCOES
from metodos import observar, nova_sessao, nova_calibracao, atualizar_calibracao, atualizar_sessao

RAIZ = Path(__file__).resolve().parent.parent


def texto(tela, mensagem, x, y, escala=0.6, cor=(225, 230, 235)):
    cv2.putText(tela, mensagem, (x, y), cv2.FONT_HERSHEY_SIMPLEX, escala, cor, 1)


def desenhar(frame, obs, estado, equalizar, tempo, parametros=PARAMETROS):
    tela = np.zeros((720, 1120, 3), dtype=np.uint8)
    tela[:, :] = (24, 23, 20)
    cv2.rectangle(tela, (0, 0), (1119, 80), (35, 34, 28), -1)
    texto(tela, "ORLA", 28, 49, 1.1, (215, 222, 109))
    texto(tela, "INTERACAO FACIAL GUIADA", 160, 43, 0.65)
    texto(tela, "Cognitive Computing | GS 2026", 745, 43, 0.53)
    visual = frame.copy()
    if obs["caixa"]:
        x, y, x2, y2 = obs["caixa"]
        cv2.rectangle(visual, (x, y), (x2, y2), (175, 225, 100), 2)
    if obs["pontos"] is not None:
        for ponto in obs["pontos"]:
            cv2.circle(visual, (int(ponto[0]), int(ponto[1])), 1, (215, 220, 90), -1)
    # A exibição é redimensionada sem mudar as medidas já calculadas.
    h, w = visual.shape[:2]
    escala = min(650 / w, 480 / h)
    visual = cv2.resize(visual, (int(w * escala), int(h * escala)))
    tela[100:100 + visual.shape[0], 24:24 + visual.shape[1]] = visual
    texto(tela, "DEMONSTRACAO - PEDIDO FICTICIO", 710, 117, 0.53, (215, 222, 109))
    texto(tela, "Revisar solicitacao de documento", 710, 148, 0.54)
    texto(tela, "Finalidade: cadastro academico", 710, 177, 0.50)
    cv2.line(tela, (710, 200), (1090, 200), (75, 75, 65), 1)
    if estado is None:
        texto(tela, "PRONTO PARA INICIAR", 710, 240, 0.66)
        texto(tela, "Pressione ESPACO", 710, 275, 0.65)
        texto(tela, "Nao ha foto previa ou cadastro", 710, 315, 0.49)
        texto(tela, "de identidade nesta aplicacao.", 710, 342, 0.49)
    elif estado["status"] == "CALIBRANDO":
        texto(tela, "AJUSTE DA SESSAO", 710, 240, 0.66)
        texto(tela, "Olhe reto para a camera", 710, 285, 0.55)
        texto(tela, "Mantenha olhos abertos", 710, 315, 0.55)
        texto(tela, "e o rosto parado por 1 segundo", 710, 345, 0.51)
        amostras = estado["amostras"]
        estavel = min(1.0, tempo - amostras[0][0]) if amostras else 0.0
        texto(tela, f"Estavel: {estavel:.1f}/1.0 s | {len(amostras)}/10 frames", 710, 385, 0.47)
        restante = max(0, parametros["etapa_max_s"] - (tempo - estado["inicio"]))
        texto(tela, f"Prazo do ajuste: {restante:.1f} s", 710, 415, 0.49)
        texto(tela, "Sem salvar foto ou identidade", 710, 445, 0.49)
    elif estado["status"] == "ATIVA":
        alvo = "CENTRO" if estado["reposicionar"] else SEQUENCIA[estado["indice"]]
        texto(tela, f"ETAPA {estado['indice'] + 1} / {len(SEQUENCIA)}", 710, 240, 0.65)
        texto(tela, alvo, 710, 282, 0.95, (215, 222, 109))
        frase = INSTRUCOES[alvo]
        palavras = frase.split()
        linhas, linha = [], ""
        for palavra in palavras:
            if len(linha) + len(palavra) > 35:
                linhas.append(linha)
                linha = ""
            linha += palavra + " "
        linhas.append(linha)
        for i, linha in enumerate(linhas):
            texto(tela, linha, 710, 320 + i * 26, 0.52)
        if estado["reposicionar"]:
            texto(tela, "Reposicione para retomar", 710, 400, 0.53, (95, 190, 240))
        elif alvo == "PISCADA":
            texto(tela, "Fase: " + estado["piscada"], 710, 400, 0.58)
        restante = max(0, parametros["etapa_max_s"] - (tempo - estado["inicio_etapa"]))
        texto(tela, f"Etapa: restam {restante:.1f} s", 710, 440, 0.55)
        dica = ""
        if not obs["valida"]:
            dica = obs["motivo"]
        elif estado["reposicionar"]:
            dica = "Volte ao centro com olhos abertos"
        elif alvo != "PISCADA":
            if obs["classe"] == "AMBIGUO":
                dica = "Mova apenas um eixo por vez"
            elif obs["classe"] != alvo:
                dica = "Movimento ainda nao atingiu o limite"
            elif alvo == "CENTRO" and obs["medidas"]["ear"] < parametros["ear_aberto"]:
                dica = "Mantenha os olhos abertos"
            else:
                duracao = tempo - estado["sustentando"] if estado["sustentando"] is not None else 0
                dica = f"Mantenha: {min(duracao, parametros['sustentacao_s']):.2f}/{parametros['sustentacao_s']:.2f} s"
        texto(tela, dica, 710, 470, 0.45)
    else:
        texto(tela, estado["status"], 710, 240, 0.76, (215, 222, 109))
        texto(tela, f"Etapas observadas: {estado['indice']}/10", 710, 285, 0.55)
        texto(tela, "R reinicia a demonstracao", 710, 325, 0.53)
    texto(tela, "CAPTURA: " + obs["motivo"], 25, 610, 0.59)
    medidas = obs["medidas"]
    if medidas:
        texto(tela, f"EAR {medidas['ear']:.3f}   H {medidas['horizontal']:.3f}   V {medidas['vertical']:.3f}", 25, 640, 0.53)
        texto(tela, "Regra 2D: " + obs["classe"], 710, 505, 0.55)
    texto(tela, "Cinza equalizado" if equalizar else "Cinza original", 710, 540, 0.50)
    texto(tela, "Nao autentica identidade nem autoriza o pedido.", 25, 682, 0.55, (120, 200, 245))
    texto(tela, "ESPACO iniciar | R recalibrar | Q sair", 710, 675, 0.46)
    return tela


def ler_opcoes(argumentos):
    opcoes = {"fonte": None, "camera": False, "equalizar": False, "sem_janela": False,
              "fps": None, "sem_ajuste": False}
    i = 0
    while i < len(argumentos):
        item = argumentos[i]
        if item in ("--camera", "--video") and i + 1 < len(argumentos):
            if opcoes["fonte"] is not None:
                raise ValueError("Escolha somente uma fonte.")
            valor = argumentos[i + 1]
            opcoes["camera"] = item == "--camera"
            opcoes["fonte"] = int(valor) if opcoes["camera"] else valor
            i += 2
        elif item == "--fps" and i + 1 < len(argumentos):
            opcoes["fps"] = float(argumentos[i + 1])
            if not 0 < opcoes["fps"] <= 240:
                raise ValueError("FPS deve estar entre 0 e 240.")
            i += 2
        elif item == "--equalizar":
            opcoes["equalizar"] = True
            i += 1
        elif item == "--sem-ajuste":
            opcoes["sem_ajuste"] = True
            i += 1
        elif item == "--sem-janela":
            opcoes["sem_janela"] = True
            i += 1
        else:
            raise ValueError("Opção desconhecida ou incompleta: " + item)
    if opcoes["fonte"] is None:
        raise ValueError("Informe --camera 0 ou --video arquivo.mp4.")
    if opcoes["camera"] and opcoes["sem_janela"]:
        raise ValueError("A câmera exige janela visível. Modo sem janela só aceita arquivo.")
    if not opcoes["camera"] and opcoes["fps"] is None:
        raise ValueError("Informe --fps com a taxa real do vídeo de FPS constante.")
    return opcoes


def executar(opcoes):
    modelo = RAIZ / "modelos/shape_predictor_68_face_landmarks.dat"
    if not modelo.exists():
        raise ValueError("Modelo ausente. Siga modelos/INSTRUCOES.md.")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(modelo))
    cap = cv2.VideoCapture(opcoes["fonte"])
    if not cap.isOpened():
        cap.release()
        raise ValueError("Não foi possível abrir a câmera/vídeo. Verifique a fonte e as permissões.")
    fps = opcoes["fps"]
    pasta = RAIZ / "resultados" / time.strftime("sessao_%Y%m%d_%H%M%S")
    pasta.mkdir(parents=True, exist_ok=False)
    log = open(pasta / "frames.csv", "w", encoding="utf-8")
    log.write("frame;tempo_s;faces;valida;classe;ear;horizontal;vertical;estado;etapa;evento;processamento_ms\n")
    with open(pasta / "configuracao.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(str(PARAMETROS) + "\n" + str(opcoes) + "\n")
    inicio = time.perf_counter()
    parametros = PARAMETROS.copy()
    iniciar = nova_sessao if opcoes["sem_ajuste"] else nova_calibracao
    estado = iniciar(0.0) if opcoes["sem_janela"] else None
    numero = 0
    erro_captura = False
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                erro_captura = opcoes["camera"]
                break
            agora = time.perf_counter() - inicio if opcoes["camera"] else numero / fps
            if opcoes["camera"] and estado is None and agora > 180:
                print("Pré-visualização encerrada após 3 minutos sem iniciar.")
                break
            frame = cv2.flip(frame, 1)
            if frame.shape[1] > 800:
                frame = cv2.resize(frame, (800, int(frame.shape[0] * 800 / frame.shape[1])))
            tic = time.perf_counter()
            obs = observar(frame, detector, predictor, opcoes["equalizar"], parametros)
            evento = ""
            if estado and estado["status"] == "CALIBRANDO":
                estado, evento = atualizar_calibracao(estado, obs, agora, parametros)
                if evento == "CALIBRADA":
                    with open(pasta / "calibracoes.txt", "a", encoding="utf-8") as arquivo:
                        arquivo.write(str(agora) + ";" + str(parametros) + "\n")
            elif estado:
                evento = atualizar_sessao(estado, obs, agora, parametros)
            ms = (time.perf_counter() - tic) * 1000
            medidas = obs["medidas"] or {"ear": "", "horizontal": "", "vertical": ""}
            linha = [numero, agora, obs["faces"], int(obs["valida"]), obs["classe"],
                     medidas["ear"], medidas["horizontal"], medidas["vertical"],
                     estado["status"] if estado else "AGUARDANDO", estado["indice"] if estado else 0,
                     evento, ms]
            log.write(";".join(str(valor) for valor in linha) + "\n")
            numero += 1
            if not opcoes["sem_janela"]:
                cv2.imshow("Orla - interacao guiada", desenhar(frame, obs, estado, opcoes["equalizar"], agora, parametros))
                espera = 1 if opcoes["camera"] else max(1, int(1000 / fps - ms))
                key = cv2.waitKey(espera) & 0xFF
                if key == ord("q"):
                    break
                if key == ord(" ") and estado is None:
                    parametros = PARAMETROS.copy()
                    estado = iniciar(agora)
                if key == ord("r"):
                    log.write(";".join([str(numero), str(agora), "", "", "", "", "", "", "REINICIO", "0", "REINICIO", ""]) + "\n")
                    parametros = PARAMETROS.copy()
                    estado = iniciar(agora)
    finally:
        cap.release()
        log.close()
        if not opcoes["sem_janela"]:
            cv2.destroyAllWindows()
        if estado and estado["status"] in ("ATIVA", "CALIBRANDO"):
            estado["status"] = "INTERROMPIDA"
        with open(pasta / "resumo.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write("Falha de captura: " + str(erro_captura) + "\n")
            arquivo.write(str(estado) + "\n")
            arquivo.write("Somente medidas numéricas. Imagens não foram gravadas.\n")
    print("Resultados:", pasta)
    if erro_captura:
        raise ValueError("A câmera parou de fornecer frames. Sessão interrompida; consulte o resumo.")


if __name__ == "__main__":
    if not sys.argv[1:] or "--help" in sys.argv:
        print("python orla_interacao.py --camera 0 [--equalizar]")
        print("python orla_interacao.py --video arquivo.mp4 --fps 30 [--equalizar] [--sem-janela]")
        print("A câmera só é aberta com --camera. Nenhuma imagem é salva.")
        print("--sem-ajuste usa limites fixos, somente para comparação controlada.")
    else:
        try:
            executar(ler_opcoes(sys.argv[1:]))
        except KeyboardInterrupt:
            print("Execução interrompida; câmera liberada.")
        except (ValueError, RuntimeError, OSError, cv2.error) as erro:
            print("Erro:", erro)
            sys.exit(1)
