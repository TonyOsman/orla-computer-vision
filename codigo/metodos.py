"""Landmarks e EAR: adaptação do Lab12 de Arnaldo Jr. Regras 2D: autorais."""

from math import dist
import cv2
import numpy as np
from configuracao import PARAMETROS, SEQUENCIA


def eye_aspect_ratio(eye):
    # Mesma relação de distâncias ensinada no exemplo de fadiga.
    a = dist(eye[1], eye[5])
    b = dist(eye[2], eye[4])
    c = dist(eye[0], eye[3])
    if c <= 0:
        return None
    return (a + b) / (2.0 * c)


def medir_pontos(coords):
    if coords.shape != (68, 2):
        return None
    for ponto in coords:
        for valor in ponto:
            if not -1000000 < valor < 1000000:
                return None
    ear_esquerdo = eye_aspect_ratio(coords[42:48])
    ear_direito = eye_aspect_ratio(coords[36:42])
    olho_a = (coords[36] + coords[39]) / 2.0
    olho_b = (coords[42] + coords[45]) / 2.0
    centro_olhos = (olho_a + olho_b) / 2.0
    centro_boca = (coords[48] + coords[54]) / 2.0
    largura = dist(olho_a, olho_b)
    altura = centro_boca[1] - centro_olhos[1]
    if largura <= 1 or altura <= 1 or ear_esquerdo is None or ear_direito is None:
        return None
    # Coordenadas da imagem espelhada: sinal negativo corresponde à esquerda do usuário.
    horizontal = (coords[30][0] - centro_olhos[0]) / largura
    vertical = (coords[30][1] - centro_olhos[1]) / altura
    return {"ear": (ear_esquerdo + ear_direito) / 2.0,
            "horizontal": horizontal, "vertical": vertical}


def classificar(medidas, parametros=PARAMETROS):
    if medidas is None:
        return "INVALIDO"
    h = medidas["horizontal"] - parametros["horizontal_centro"]
    v = medidas["vertical"]
    lado = "CENTRO"
    altura = "CENTRO"
    if h < -parametros["lateral"]:
        lado = "ESQUERDA"
    elif h > parametros["lateral"]:
        lado = "DIREITA"
    if v < parametros["vertical_cima"]:
        altura = "CIMA"
    elif v > parametros["vertical_baixo"]:
        altura = "BAIXO"
    if lado != "CENTRO" and altura != "CENTRO":
        return "AMBIGUO"
    return lado if lado != "CENTRO" else altura


def observar(frame, detector, predictor, equalizar=False, parametros=PARAMETROS):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processada = cv2.equalizeHist(gray) if equalizar else gray
    faces = detector(processada, 0)
    observacao = {"faces": len(faces), "valida": False, "motivo": "SEM ROSTO",
                  "pontos": None, "caixa": None, "medidas": None, "classe": "INVALIDO"}
    if len(faces) != 1:
        if len(faces) > 1:
            observacao["motivo"] = "MAIS DE UM ROSTO"
        return observacao
    face = faces[0]
    x, y, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
    observacao["caixa"] = (x, y, x2, y2)
    altura, largura = gray.shape
    fracao = (x2 - x) / largura
    if x < 0 or y < 0 or x2 >= largura or y2 >= altura:
        observacao["motivo"] = "ENQUADRE O ROSTO INTEIRO"
        return observacao
    if not parametros["face_min_fracao"] <= fracao <= parametros["face_max_fracao"]:
        observacao["motivo"] = "AJUSTE A DISTANCIA DA CAMERA"
        return observacao
    shape = predictor(processada, face)
    coords = np.zeros((68, 2), dtype=float)
    for i in range(68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    medidas = medir_pontos(coords)
    observacao["pontos"] = coords
    observacao["medidas"] = medidas
    observacao["classe"] = classificar(medidas, parametros)
    observacao["valida"] = medidas is not None
    observacao["motivo"] = "OK" if medidas is not None else "PONTOS INVALIDOS"
    return observacao


def nova_sessao(agora):
    return {"inicio": agora, "inicio_etapa": agora, "ultimo_tempo": None,
            "indice": 0, "sustentando": None, "reposicionar": False,
            "piscada": "ABRIR", "fechou_em": None, "abriu_em": None,
            "status": "ATIVA", "concluidas": [], "interrupcoes": 0}


def nova_calibracao(agora):
    return {"status": "CALIBRANDO", "inicio": agora, "ultimo_tempo": None,
            "amostras": [], "indice": 0}


def atualizar_calibracao(estado, observacao, agora, parametros):
    # Referência numérica da sessão, sem foto ou cadastro de identidade.
    if agora - estado["inicio"] > parametros["etapa_max_s"]:
        estado["status"] = "EXPIRADA"
        return estado, "CALIBRACAO_EXPIRADA"
    anterior = estado["ultimo_tempo"]
    estado["ultimo_tempo"] = agora
    if anterior is not None and agora <= anterior:
        estado["status"] = "INTERROMPIDA"
        return estado, "TEMPO_INVALIDO"
    lacuna = anterior is not None and agora - anterior > parametros["intervalo_max_s"]
    if not observacao["valida"] or lacuna:
        estado["amostras"] = []
        return estado, ""
    m = observacao["medidas"]
    if m["ear"] < 0.15:
        estado["amostras"] = []
        return estado, ""
    estado["amostras"].append((agora, m["horizontal"], m["vertical"], m["ear"]))
    amostras = estado["amostras"]
    for coluna, limite in [(1, 0.10), (2, 0.12), (3, 0.08)]:
        valores = [a[coluna] for a in amostras]
        if max(valores) - min(valores) > limite:
            estado["amostras"] = [amostras[-1]]
            return estado, ""
    if len(amostras) >= 10 and agora - amostras[0][0] >= 1.0:
        h = sum(a[1] for a in amostras) / len(amostras)
        v = sum(a[2] for a in amostras) / len(amostras)
        ear = sum(a[3] for a in amostras) / len(amostras)
        parametros["horizontal_centro"] = h
        parametros["vertical_cima"] = v - 0.10
        parametros["vertical_baixo"] = v + 0.10
        parametros["ear_fechado"] = ear * 0.70
        parametros["ear_aberto"] = ear * 0.85
        return nova_sessao(agora), "CALIBRADA"
    return estado, ""


def limpar_parcial(estado):
    estado["sustentando"] = None
    estado["piscada"] = "ABRIR"
    estado["fechou_em"] = None
    estado["abriu_em"] = None


def atualizar_sessao(estado, observacao, agora, parametros=PARAMETROS):
    if estado["status"] != "ATIVA":
        return ""
    anterior = estado["ultimo_tempo"]
    estado["ultimo_tempo"] = agora
    if anterior is not None and agora <= anterior:
        estado["status"] = "INTERROMPIDA"
        return "TEMPO_INVALIDO"
    if agora - estado["inicio"] > parametros["sessao_max_s"]:
        estado["status"] = "EXPIRADA"
        return "SESSAO_EXPIRADA"
    if agora - estado["inicio_etapa"] > parametros["etapa_max_s"]:
        estado["status"] = "EXPIRADA"
        return "ETAPA_EXPIRADA"
    lacuna = anterior is not None and agora - anterior > parametros["intervalo_max_s"]
    if not observacao["valida"] or lacuna:
        if not estado["reposicionar"]:
            estado["interrupcoes"] += 1
        estado["reposicionar"] = True
        limpar_parcial(estado)
        return "REPOSICIONAR"
    medidas = observacao["medidas"]
    classe = observacao["classe"]
    if estado["reposicionar"]:
        if classe == "CENTRO" and medidas["ear"] >= parametros["ear_aberto"]:
            if estado["sustentando"] is None:
                estado["sustentando"] = agora
            if agora - estado["sustentando"] >= parametros["sustentacao_s"]:
                estado["reposicionar"] = False
                limpar_parcial(estado)
                return "RETOMADA"
        else:
            estado["sustentando"] = None
        return ""
    alvo = SEQUENCIA[estado["indice"]]
    concluiu = False
    if alvo == "PISCADA":
        if classe != "CENTRO":
            limpar_parcial(estado)
            return ""
        ear = medidas["ear"]
        if estado["piscada"] == "ABRIR":
            if ear >= parametros["ear_aberto"]:
                if estado["abriu_em"] is None:
                    estado["abriu_em"] = agora
                if agora - estado["abriu_em"] >= parametros["sustentacao_s"]:
                    estado["piscada"] = "FECHAR"
            else:
                estado["abriu_em"] = None
        elif estado["piscada"] == "FECHAR":
            if ear <= parametros["ear_fechado"]:
                estado["piscada"] = "REABRIR"
                estado["fechou_em"] = agora
        elif estado["piscada"] == "REABRIR":
            duracao = agora - estado["fechou_em"]
            if duracao > parametros["piscada_max_s"]:
                limpar_parcial(estado)
            elif ear >= parametros["ear_aberto"]:
                concluiu = duracao >= parametros["piscada_min_s"]
                if not concluiu:
                    limpar_parcial(estado)
    else:
        olhos_ok = alvo != "CENTRO" or medidas["ear"] >= parametros["ear_aberto"]
        if classe == alvo and olhos_ok:
            if estado["sustentando"] is None:
                estado["sustentando"] = agora
            concluiu = agora - estado["sustentando"] >= parametros["sustentacao_s"]
        else:
            estado["sustentando"] = None
    if concluiu:
        estado["concluidas"].append((alvo, agora - estado["inicio"]))
        estado["indice"] += 1
        estado["inicio_etapa"] = agora
        limpar_parcial(estado)
        if estado["indice"] == len(SEQUENCIA):
            estado["status"] = "CONCLUIDA"
        return "ETAPA_" + alvo
    return ""
