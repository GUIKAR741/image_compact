"""."""

import math
import os
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


def adicioanr_chave_para_lexicon(
        lexicon, string_atual, indice, ultimo_id_encontrado
) -> None:
    """.

    Adicionando nova string (string_atual + "0",  string_atual + "1") ao lexicon
    """
    lexicon.pop(string_atual)
    lexicon[string_atual + "0"] = ultimo_id_encontrado

    if math.log2(indice).is_integer():
        for key_atual in lexicon:
            lexicon[key_atual] = "0" + lexicon[key_atual]

    lexicon[string_atual + "1"] = bin(indice)[2:]


def comprime_dados(bits_dados: str) -> str:
    """.

    Comprime bits_dados dados usando o algoritmo de compressão Lempel–Ziv–Welch
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
        adicioanr_chave_para_lexicon(lexicon, string_atual, indice, ultimo_id_encontrado)
        indice += 1
        string_atual = ""

    while string_atual != "" and string_atual not in lexicon:
        string_atual += "0"

    if string_atual != "":
        ultimo_id_encontrado = lexicon[string_atual]
        resultado += ultimo_id_encontrado

    return resultado


def adicionar_tamanho_arquivo(caminho_origem: str, comprimido: str) -> str:
    """.

    Adicionando tamanho do arquivo no inicio da string
    """
    tamanho_arquivo = os.path.getsize(caminho_origem)
    tamanho_arquivo_binario = bin(tamanho_arquivo)[2:]
    tamanho = len(tamanho_arquivo_binario)

    return "0" * (tamanho - 1) + tamanho_arquivo_binario + comprimido


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

            for elem in resultado_array_byte:
                arquivo_aberto.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("Arquivo não disponivel")
        sys.exit()


def comprimir(caminho_origem: str, caminho_destino: str) -> None:
    """.

    Ler arquivo original
    Comprimir arquivo
    Salvar arquivo comprimido no arquivo de destino
    """
    bits_dados = ler_arquivo_binario(caminho_origem)
    comprimido = comprime_dados(bits_dados)
    comprimido = adicionar_tamanho_arquivo(caminho_origem, comprimido)
    escrever_arquivo_binario(caminho_destino, comprimido)


if __name__ == "__main__":
    comprimir(sys.argv[1], sys.argv[2])
