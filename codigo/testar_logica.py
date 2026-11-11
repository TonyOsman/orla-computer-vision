"""Testes determinísticos com medidas sintéticas. NÃO medem acurácia em pessoas."""

from pathlib import Path
import numpy as np
from configuracao import SEQUENCIA, PARAMETROS
from metodos import (eye_aspect_ratio, medir_pontos, classificar, nova_sessao,
                     atualizar_sessao, nova_calibracao, atualizar_calibracao)

RAIZ = Path(__file__).resolve().parent.parent


def observacao(classe="CENTRO", ear=0.30, valida=True):
    return {"valida": valida, "classe": classe,
            "medidas": {"ear": ear, "horizontal": 0.0, "vertical": 0.55}}


def alimentar(estado, classe, tempo, duracao=0.6, ear=0.30, valida=True):
    eventos = []
    for i in range(int(duracao / 0.05)):
        tempo += 0.05
        evento = atualizar_sessao(estado, observacao(classe, ear, valida), tempo)
        if evento:
            eventos.append(evento)
    return tempo, eventos


def executar_testes():
    resultados = []
    def registrar(nome, passou, detalhe):
        resultados.append((nome, "PASSOU" if passou else "FALHOU", detalhe))

    eye = np.array([[0, 0], [1, -1], [3, -1], [4, 0], [3, 1], [1, 1]], dtype=float)
    registrar("EAR conhecido", abs(eye_aspect_ratio(eye) - 0.5) < 0.000001, "Esperado 0.5")
    registrar("Olho degenerado", eye_aspect_ratio(np.zeros((6, 2))) is None, "Sem divisao por zero")
    coords = np.zeros((68, 2), dtype=float)
    coords[36:42] = eye * 10 + [80, 100]
    coords[42:48] = eye * 10 + [180, 100]
    coords[48], coords[54], coords[30] = [110, 200], [190, 200], [150, 155]
    m = medir_pontos(coords)
    m2 = medir_pontos(coords * 2 + [31, 27])
    registrar("Escala e translacao", all(abs(m[k] - m2[k]) < 0.000001 for k in m), "Razoes invariantes nesta geometria")
    registrar("Pontos invalidos", medir_pontos(np.zeros((5, 2))) is None, "Quantidade incorreta rejeitada")
    for h, v, alvo in [(-0.25, 0.55, "ESQUERDA"), (0.25, 0.55, "DIREITA"),
                       (0, 0.30, "CIMA"), (0, 0.85, "BAIXO"), (0, 0.55, "CENTRO"),
                       (0.25, 0.85, "AMBIGUO")]:
        registrar("Regra " + alvo, classificar({"horizontal": h, "vertical": v}) == alvo, "Medidas sinteticas conhecidas")
    estado, tempo = nova_sessao(0), 0.0
    for alvo in SEQUENCIA[:-1]:
        tempo, _ = alimentar(estado, alvo, tempo)
    tempo, _ = alimentar(estado, "CENTRO", tempo, ear=0.30)
    tempo, _ = alimentar(estado, "CENTRO", tempo, duracao=0.15, ear=0.10)
    tempo, _ = alimentar(estado, "CENTRO", tempo, duracao=0.15, ear=0.30)
    registrar("Fluxo completo", estado["status"] == "CONCLUIDA", "Sequencia sintetica de 10 etapas")
    estado = nova_sessao(0)
    alimentar(estado, "DIREITA", 0)
    registrar("Movimento errado", estado["indice"] == 0, "Direita nao atende centro")
    estado = nova_sessao(0)
    atualizar_sessao(estado, observacao(), 0.1)
    atualizar_sessao(estado, observacao(), 1.0)
    registrar("Lacuna temporal", estado["indice"] == 0 and estado["reposicionar"], "Tempo sem frames nao conta sustentacao")
    estado = nova_sessao(0)
    estado["indice"] = 9
    t, _ = alimentar(estado, "CENTRO", 0, ear=0.30)
    t, _ = alimentar(estado, "CENTRO", t, duracao=1.6, ear=0.10)
    alimentar(estado, "CENTRO", t, ear=0.30)
    registrar("Olhos fechados demais", estado["status"] != "CONCLUIDA", "Nao confundir fadiga com piscada")
    estado = nova_sessao(0)
    estado["indice"] = 9
    t, _ = alimentar(estado, "CENTRO", 0, ear=0.30)
    t, _ = alimentar(estado, "CENTRO", t, duracao=0.15, ear=0.10)
    atualizar_sessao(estado, observacao(valida=False), t + 0.05)
    alimentar(estado, "CENTRO", t + 0.05, ear=0.30)
    registrar("Perda de rosto na piscada", estado["status"] != "CONCLUIDA", "Evento parcial descartado")
    estado = nova_sessao(0)
    atualizar_sessao(estado, observacao(), 21.0)
    registrar("Prazo da etapa", estado["status"] == "EXPIRADA", "Espera nao e ilimitada")
    estado = nova_sessao(0)
    atualizar_sessao(estado, observacao(), 0.1)
    atualizar_sessao(estado, observacao(), 0.1)
    registrar("Relogio repetido", estado["status"] == "INTERROMPIDA", "Timestamp nao crescente rejeitado")
    estado = nova_sessao(0)
    alimentar(estado, "CENTRO", 0, valida=False)
    registrar("Observacao invalida", estado["indice"] == 0, "Nenhuma etapa avancou")
    estado = nova_sessao(0)
    estado["indice"] = 9
    alimentar(estado, "CENTRO", 0, duracao=0.9, ear=0.10)
    registrar("Comecar de olhos fechados", estado["status"] != "CONCLUIDA", "Abertura inicial obrigatoria")
    estado, parametros = nova_calibracao(0), PARAMETROS.copy()
    obs = observacao(ear=0.28)
    obs["medidas"]["vertical"] = 0.40
    for i in range(24):
        estado, evento = atualizar_calibracao(estado, obs, i * 0.05, parametros)
        if evento == "CALIBRADA":
            break
    registrar("Referencia numerica neutra", estado["status"] == "ATIVA" and
              classificar(obs["medidas"], parametros) == "CENTRO", "Sem fotografia ou identidade")
    registrar("EAR relativo", abs(parametros["ear_fechado"] - 0.196) < 0.000001 and
              abs(parametros["ear_aberto"] - 0.238) < 0.000001, "70% e 85% da abertura de referencia")
    estado = nova_calibracao(0)
    estado, _ = atualizar_calibracao(estado, obs, 0.1, parametros)
    estado, _ = atualizar_calibracao(estado, observacao(valida=False), 0.2, parametros)
    registrar("Calibracao perde face", estado["amostras"] == [], "Descarta amostras parciais")
    estado = nova_calibracao(0)
    estado, _ = atualizar_calibracao(estado, obs, 0.1, parametros)
    alterada = observacao()
    alterada["medidas"]["horizontal"] = 0.5
    estado, _ = atualizar_calibracao(estado, alterada, 0.2, parametros)
    registrar("Calibracao instavel", len(estado["amostras"]) == 1 and estado["status"] == "CALIBRANDO", "Movimento nao estabelece referencia")
    estado = nova_sessao(0)
    estado["indice"] = 5
    alimentar(estado, "CIMA", 0, ear=0.18)
    registrar("Direcao independente do EAR", estado["indice"] == 6,
              "Inclinacao nao exige abertura frontal dos olhos")
    estado = nova_sessao(0)
    alimentar(estado, "CENTRO", 0, ear=0.18)
    registrar("Centro exige olhos abertos", estado["indice"] == 0,
              "Abertura continua obrigatoria no centro")
    estado = nova_sessao(0)
    estado["indice"] = 5
    atualizar_sessao(estado, observacao("CIMA", ear=0.18), 0.1)
    atualizar_sessao(estado, observacao("CIMA", ear=0.18, valida=False), 0.2)
    alimentar(estado, "CIMA", 0.2, ear=0.18)
    registrar("Perda de face ainda bloqueia direcao", estado["indice"] == 5 and estado["reposicionar"],
              "EAR separado nao elimina retorno seguro ao centro")
    saida = RAIZ / "resultados/testes_logica.csv"
    with open(saida, "w", encoding="utf-8") as arquivo:
        arquivo.write("teste;resultado;detalhe\n")
        for linha in resultados:
            arquivo.write(";".join(linha) + "\n")
    for linha in resultados:
        print(" | ".join(linha))
    assert all(r[1] == "PASSOU" for r in resultados), "Existe teste com falha."
    print(len(resultados), "testes da logica passaram. Nao equivalem a validacao humana.")
    return resultados


if __name__ == "__main__":
    executar_testes()
