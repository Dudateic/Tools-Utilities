import json
import os
from config import RULES_PATH, DEFAULT_CATEGORIES


def carregar_regras():
    """Carrega as regras de classificação do arquivo JSON"""
    
    if not os.path.exists(RULES_PATH):
        salvar_regras(DEFAULT_CATEGORIES)
        return DEFAULT_CATEGORIES
    
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return DEFAULT_CATEGORIES


def salvar_regras(regras):
    """Salva as regras no arquivo JSON"""
    
    os.makedirs(os.path.dirname(RULES_PATH), exist_ok=True)
    
    with open(RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(regras, f, indent=4, ensure_ascii=False)


def adicionar_regra(categoria, palavra):
    """Adiciona uma palavra-chave a uma categoria"""
    
    regras = carregar_regras()
    
    if categoria not in regras:
        regras[categoria] = []
    
    if palavra not in regras[categoria]:
        regras[categoria].append(palavra)
        salvar_regras(regras)
        return True
    
    return False


def remover_regra(categoria, palavra):
    """Remove uma palavra-chave de uma categoria"""
    
    regras = carregar_regras()
    
    if categoria in regras and palavra in regras[categoria]:
        regras[categoria].remove(palavra)
        salvar_regras(regras)
        return True
    
    return False


def criar_categoria(categoria):
    """Cria uma nova categoria"""
    
    regras = carregar_regras()
    
    if categoria not in regras:
        regras[categoria] = []
        salvar_regras(regras)
        return True
    
    return False


def deletar_categoria(categoria):
    """Deleta uma categoria"""
    
    regras = carregar_regras()
    
    if categoria in regras and categoria != "outros":
        del regras[categoria]
        salvar_regras(regras)
        return True
    
    return False


def sugerir_categoria(nome_arquivo, regras=None):
    """Sugere a melhor categoria para um arquivo"""
    
    if regras is None:
        regras = carregar_regras()
    
    nome = nome_arquivo.lower()
    melhor = "outros"
    score_maximo = 0
    
    for categoria, palavras in regras.items():
        if categoria == "outros":
            continue
        
        score = 0
        for palavra in palavras:
            if palavra.lower() in nome:
                score += 2
        
        if score > score_maximo:
            score_maximo = score
            melhor = categoria
    
    return melhor


def obter_categorias():
    """Retorna lista de todas as categorias"""
    
    regras = carregar_regras()
    return list(regras.keys())


def obter_palavras_categoria(categoria):
    """Retorna as palavras-chave de uma categoria"""
    
    regras = carregar_regras()
    return regras.get(categoria, [])