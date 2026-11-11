"""Avaliação de tentativas rotuladas por observador humano, sem gerar rótulos por IA."""

from pathlib import Path
from configuracao import SEQUENCIA

RAIZ = Path(__file__).resolve().parent.parent


def ler_tabela(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [linha.strip().split(";") for linha in arquivo if linha.strip()]
    if not linhas:
        raise ValueError("Tabela vazia: " + str(caminho))
    campos = linhas[0]
    dados = []
    for valores in linhas[1:]:
        if len(valores) != len(campos):
            raise ValueError("Quantidade incorreta de colunas em " + str(caminho))
        dados.append(dict(zip(campos, valores)))
    return dados


def executar():
    tentativas = ler_tabela(RAIZ / "dados/tentativas.csv")
    saida = RAIZ / "resultados/avaliacao_humana.csv"
    resultados = []
    grupos = {}
    intervalos = {}
    for tentativa in tentativas:
        participante = tentativa["participante"]
        grupo = tentativa["grupo"]
        if grupo not in ("DESENVOLVIMENTO", "TESTE"):
            raise ValueError("Grupo deve ser DESENVOLVIMENTO ou TESTE.")
        if participante in grupos and grupos[participante] != grupo:
            raise ValueError("Participante aparece em desenvolvimento e teste: " + participante)
        grupos[participante] = grupo
        inicio = float(tentativa["inicio_s"])
        fim = float(tentativa["fim_s"])
        if not 0 <= inicio < fim:
            raise ValueError("Intervalo inválido.")
        alvo = tentativa["alvo"]
        if alvo not in SEQUENCIA:
            raise ValueError("Alvo desconhecido: " + alvo)
        arquivo = (RAIZ / tentativa["arquivo_frames"]).resolve()
        if RAIZ not in arquivo.parents:
            raise ValueError("O log deve estar dentro do projeto.")
        for anterior in intervalos.get(str(arquivo), []):
            if inicio < anterior[1] and fim > anterior[0]:
                raise ValueError("Tentativas sobrepostas no mesmo log.")
        intervalos.setdefault(str(arquivo), []).append((inicio, fim))
        frames = ler_tabela(arquivo)
        janela = [f for f in frames if inicio <= float(f["tempo_s"]) < fim]
        if not janela:
            raise ValueError("Intervalo sem frames; não contabilizado como acerto.")
        if any(f["evento"] == "REINICIO" for f in janela):
            raise ValueError("Divida tentativas que atravessam um reinício.")
        eventos = [float(f["tempo_s"]) for f in janela if f["evento"] == "ETAPA_" + alvo]
        positiva = tentativa["acao_real"] == alvo
        aceitou = len(eventos) > 0
        resultado = ("ACERTO" if aceitou else "NAO_RECONHECIDA") if positiva else ("ACEITACAO_INDEVIDA" if aceitou else "REJEICAO_CORRETA")
        latencia = eventos[0] - inicio if positiva and aceitou else ""
        resultados.append([participante, grupo, tentativa["condicao"], tentativa["acao_real"],
                           alvo, int(positiva), int(aceitou), resultado, latencia, len(janela)])
    with open(saida, "w", encoding="utf-8") as arquivo:
        arquivo.write("participante;grupo;condicao;acao_real;alvo;positiva;aceitou;resultado;latencia_s;frames\n")
        for resultado in resultados:
            arquivo.write(";".join(str(v) for v in resultado) + "\n")
    if not resultados:
        print("Sem tentativas humanas rotuladas. Nenhuma acurácia humana foi calculada.")
    else:
        for grupo in ("DESENVOLVIMENTO", "TESTE"):
            r = [x for x in resultados if x[1] == grupo]
            positivas = [x for x in r if x[5] == 1]
            negativas = [x for x in r if x[5] == 0]
            print(grupo, "positivas reconhecidas", sum(x[6] for x in positivas), "/", len(positivas),
                  "negativas aceitas", sum(x[6] for x in negativas), "/", len(negativas))
    return resultados


if __name__ == "__main__":
    executar()
