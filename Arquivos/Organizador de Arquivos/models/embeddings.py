from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from config import EMBEDDINGS_CACHE_PATH


class EmbeddingsManager:
    """Gerencia os embeddings de texto usando TF-IDF"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='portuguese')
        self.carregado = False
    
    def treinar_textos(self, textos):
        """Treina o vetorizador com uma lista de textos"""
        try:
            matriz = self.vectorizer.fit_transform(textos)
            self.salvar_cache()
            return matriz
        except Exception as e:
            print(f"Erro ao treinar textos: {str(e)}")
            return None
    
    def transformar(self, texto):
        """Transforma um texto em vetor TF-IDF"""
        try:
            if not self.carregado:
                self.carregar_cache()
            return self.vectorizer.transform([texto])
        except Exception as e:
            print(f"Erro ao transformar texto: {str(e)}")
            return None
    
    def transformar_multiplos(self, textos):
        """Transforma múltiplos textos em vetores"""
        try:
            if not self.carregado:
                self.carregar_cache()
            return self.vectorizer.transform(textos)
        except Exception as e:
            print(f"Erro ao transformar textos: {str(e)}")
            return None
    
    def salvar_cache(self):
        """Salva o vetorizador em cache"""
        try:
            os.makedirs(os.path.dirname(EMBEDDINGS_CACHE_PATH), exist_ok=True)
            with open(EMBEDDINGS_CACHE_PATH, 'wb') as f:
                pickle.dump(self.vectorizer, f)
        except Exception as e:
            print(f"Erro ao salvar cache: {str(e)}")
    
    def carregar_cache(self):
        """Carrega o vetorizador do cache"""
        try:
            if os.path.exists(EMBEDDINGS_CACHE_PATH):
                with open(EMBEDDINGS_CACHE_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                self.carregado = True
        except Exception as e:
            print(f"Erro ao carregar cache: {str(e)}")
    
    def obter_termos(self):
        """Retorna os termos do vocabulário"""
        try:
            return self.vectorizer.get_feature_names_out()
        except Exception as e:
            print(f"Erro ao obter termos: {str(e)}")
            return []

embeddings_manager = EmbeddingsManager()