"""Parâmetros iniciais de engenharia, ainda sujeitos à avaliação com voluntários."""

PARAMETROS = {
    "horizontal_centro": 0.0,
    "lateral": 0.13,
    "vertical_cima": 0.43,
    "vertical_baixo": 0.72,
    "ear_fechado": 0.21,
    "ear_aberto": 0.25,
    "sustentacao_s": 0.35,
    "piscada_min_s": 0.06,
    "piscada_max_s": 1.20,
    "intervalo_max_s": 0.35,
    "etapa_max_s": 20.0,
    "sessao_max_s": 180.0,
    "face_min_fracao": 0.12,
    "face_max_fracao": 0.85,
}

SEQUENCIA = ["CENTRO", "ESQUERDA", "CENTRO", "DIREITA", "CENTRO",
             "CIMA", "CENTRO", "BAIXO", "CENTRO", "PISCADA"]

INSTRUCOES = {
    "CENTRO": "Olhe de frente e mantenha os olhos abertos",
    "ESQUERDA": "Vire levemente para sua ESQUERDA",
    "DIREITA": "Vire levemente para sua DIREITA",
    "CIMA": "Incline levemente o rosto para CIMA",
    "BAIXO": "Incline levemente o rosto para BAIXO",
    "PISCADA": "De frente: abra, feche e reabra os olhos",
}
