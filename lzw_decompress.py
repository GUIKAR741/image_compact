"""."""

import math
import sys


def ler_arquivo_binario(caminho_arquivo: str) -> str:
    """.

    Lê o arquivo como bytes e retorna como uma string
    """
    resultado = ""
    try:
        with open(caminho_arquivo, "rb") as arquivo_binario:
            dados = arquivo_binario.read()
        for dado in dados:
            binario_atual = f"{dado:08b}"
            resultado += binario_atual
        return resultado
    except OSError:
        print("Arquivo não disponivel")
        sys.exit()


def descomprimir_dados(bits_dados: str) -> str:
    """.

    Descomprime bits_dados dados usando o algoritmo de compactação Lempel–Ziv–Welch
    e retorna o resultado como uma string
    """
    lexicon = {"0": "0", "1": "1"}
    resultado, string_atual = "", ""
    indice = len(lexicon)

    for i in range(len(bits_dados)):
        string_atual += bits_dados[i]
        if string_atual not in lexicon:
            continue

        ultimo_id_encontrado = lexicon[string_atual]
        resultado += ultimo_id_encontrado
        lexicon[string_atual] = ultimo_id_encontrado + "0"

        if math.log2(indice).is_integer():
            novoLex = {}
            for curr_key in list(lexicon):
                novoLex["0" + curr_key] = lexicon.pop(curr_key)
            lexicon = novoLex

        lexicon[bin(indice)[2:]] = ultimo_id_encontrado + "1"
        indice += 1
        string_atual = ""
    return resultado


def escrever_arquivo_binario(caminho_arquivo: str, para_escrever: str) -> None:
    """.

    Escreve para_escrever no arquivo
    """
    tamanho_byte = 8
    try:
        with open(caminho_arquivo, "wb") as arquivo_aberto:
            resultado_array_byte = [
                para_escrever[i: i + tamanho_byte]
                for i in range(0, len(para_escrever), tamanho_byte)
            ]

            if len(resultado_array_byte[-1]) % tamanho_byte == 0:
                resultado_array_byte.append("10000000")
            else:
                resultado_array_byte[-1] += "1" + "0" * (
                    tamanho_byte - len(resultado_array_byte[-1]) - 1
                )

            for elem in resultado_array_byte[:-1]:
                arquivo_aberto.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("Arquivo não disponivel")
        sys.exit()


def remover_prefixo(bits_dados: str) -> str:
    """.

    Remove prefixo do tamanho
    """
    contador = 0
    for letra in bits_dados:
        if letra == "1":
            break
        contador += 1

    bits_dados = bits_dados[contador:]
    bits_dados = bits_dados[contador + 1:]
    return bits_dados


def descomprimir(caminho_origem: str, caminho_destino: str) -> None:
    """.

    Ler arquivo original
    Descomprimir arquivo
    Salvar arquivo de destino
    """
    bits_dados = ler_arquivo_binario(caminho_origem)
    bits_dados = remover_prefixo(bits_dados)
    descomprimido = descomprimir_dados(bits_dados)
    escrever_arquivo_binario(caminho_destino, descomprimido)


if __name__ == "__main__":
    descomprimir(sys.argv[1], sys.argv[2])
