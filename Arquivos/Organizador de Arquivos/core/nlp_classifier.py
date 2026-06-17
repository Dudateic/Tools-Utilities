import spacy
from core.rules_engine import carregar_regras
from utils.text_processing import normalizar, extrair_palavras_chave
from config import DEFAULT_CATEGORIES

try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo spaCy não encontrado. Execute: python -m spacy download pt_core_news_sm")
    nlp = None


def classificar(nome_arquivo: str) -> str:
    """
    Classifica um arquivo baseado em seu nome.
    Usa regras customizadas + NLP spaCy.
    """
    
    regras = carregar_regras()
    
    if not regras:
        regras = DEFAULT_CATEGORIES
    
    texto = normalizar(nome_arquivo)
    palavras = extrair_palavras_chave(nome_arquivo)
    
    melhor_categoria = "outros"
    score_maximo = 0
    
    for categoria, palavras_chave in regras.items():
        if categoria == "outros":
            continue
        
        score = 0
        
        for palavra in palavras_chave:
            if palavra.lower() in texto:
                score += 2
            
            for p in palavras:
                if palavra.lower() in p.lower():
                    score += 1
        
        if score > score_maximo:
            score_maximo = score
            melhor_categoria = categoria
    
    if nlp and score_maximo == 0:
        melhor_categoria = _classificar_com_nlp(texto, regras)
    
    return melhor_categoria


def _classificar_com_nlp(texto: str, regras: dict) -> str:
    """Usa spaCy NLP para melhorar a classificação"""
    
    try:
        doc = nlp(texto)
        tokens = [t.lemma_ for t in doc]
        
        melhor = "outros"
        score_max = 0
        
        for categoria, palavras in regras.items():
            if categoria == "outros":
                continue
            
            score = 0
            for palavra in palavras:
                if palavra.lower() in tokens:
                    score += 1
            
            if score > score_max:
                score_max = score
                melhor = categoria
        
        return melhor
    
    except Exception as e:
        print(f"Erro ao usar NLP: {str(e)}")
        return "outros"


def sugerir_categoria(nome_arquivo: str) -> dict:
    """
    Retorna sugestões de categoria com scores
    """
    
    regras = carregar_regras()
    if not regras:
        regras = DEFAULT_CATEGORIES
    
    texto = normalizar(nome_arquivo)
    sugestoes = {}
    
    for categoria, palavras_chave in regras.items():
        if categoria == "outros":
            continue
        
        score = 0
        for palavra in palavras_chave:
            if palavra.lower() in texto:
                score += 1
        
        if score > 0:
            sugestoes[categoria] = score
    
    sugestoes_ordenadas = dict(sorted(sugestoes.items(), key=lambda x: x[1], reverse=True))
    
    return sugestoes_ordenadas