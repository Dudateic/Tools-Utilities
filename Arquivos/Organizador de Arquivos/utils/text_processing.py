import re
import unicodedata


def normalizar(texto):
    """
    Normaliza o texto removendo acentos e convertendo para minúsculas
    """
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode()
    return texto.lower()


def limpar_texto(texto):
    """
    Limpa o texto removendo caracteres especiais e espaços extras
    """
    texto = normalizar(texto)
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def extrair_palavras_chave(nome_arquivo):
    """
    Extrai palavras-chave do nome de um arquivo
    """
    texto = limpar_texto(nome_arquivo)
    return texto.split()


def remover_extensao(nome_arquivo):
    """Remove a extensão do arquivo"""
    return os.path.splitext(nome_arquivo)[0]


def obter_extensao(nome_arquivo):
    """Obtém apenas a extensão do arquivo"""
    return os.path.splitext(nome_arquivo)[1].lower()


def padronizar_nome(nome_arquivo):
    """
    Padroniza o nome do arquivo:
    - Remove acentos
    - Converte para minúsculas
    - Substitui espaços por underscores
    """
    nome_sem_ext, ext = os.path.splitext(nome_arquivo)
    nome_padronizado = normalizar(nome_sem_ext)
    nome_padronizado = re.sub(r"\s+", "_", nome_padronizado)
    nome_padronizado = re.sub(r"[^\w]", "", nome_padronizado)
    return nome_padronizado + ext


def dividir_nome_arquivo(nome_arquivo):
    """
    Divide o nome do arquivo em seus componentes:
    - nome base
    - extensão
    """
    nome, ext = os.path.splitext(nome_arquivo)
    return {
        "nome_completo": nome_arquivo,
        "nome": nome,
        "extensao": ext.lstrip("."),
        "extensao_com_ponto": ext
    }


def combinar_nome_arquivo(nome, extensao):
    """Combina nome e extensão em um nome de arquivo"""
    if not extensao.startswith("."):
        extensao = "." + extensao
    return nome + extensao


import os