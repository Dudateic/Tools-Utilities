import os
import pickle
from config import MODEL_PATH


class ModelLoader:
    """Gerencia carregamento e salvamento de modelos"""
    
    @staticmethod
    def salvar_modelo(modelo, nome="default"):
        """Salva um modelo em disco"""
        try:
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            
            modelo_path = MODEL_PATH.parent / f"{nome}.bin"
            
            with open(modelo_path, "wb") as f:
                pickle.dump(modelo, f)
            
            print(f"Modelo salvo: {modelo_path}")
            return True
        
        except Exception as e:
            print(f"Erro ao salvar modelo: {str(e)}")
            return False
    
    @staticmethod
    def carregar_modelo(nome="default"):
        """Carrega um modelo do disco"""
        try:
            modelo_path = MODEL_PATH.parent / f"{nome}.bin"
            
            if not os.path.exists(modelo_path):
                print(f"Modelo não encontrado: {modelo_path}")
                return None
            
            with open(modelo_path, "rb") as f:
                modelo = pickle.load(f)
            
            print(f"Modelo carregado: {modelo_path}")
            return modelo
        
        except Exception as e:
            print(f"Erro ao carregar modelo: {str(e)}")
            return None
    
    @staticmethod
    def modelo_existe(nome="default"):
        """Verifica se um modelo existe"""
        modelo_path = MODEL_PATH.parent / f"{nome}.bin"
        return os.path.exists(modelo_path)
    
    @staticmethod
    def listar_modelos():
        """Lista todos os modelos disponíveis"""
        try:
            modelos_dir = MODEL_PATH.parent
            if not os.path.exists(modelos_dir):
                return []
            
            modelos = [f[:-4] for f in os.listdir(modelos_dir) if f.endswith('.bin')]
            return modelos
        
        except Exception as e:
            print(f"Erro ao listar modelos: {str(e)}")
            return []
    
    @staticmethod
    def deletar_modelo(nome="default"):
        """Deleta um modelo"""
        try:
            modelo_path = MODEL_PATH.parent / f"{nome}.bin"
            
            if os.path.exists(modelo_path):
                os.remove(modelo_path)
                print(f"Modelo deletado: {modelo_path}")
                return True
            else:
                print(f"Modelo não encontrado: {modelo_path}")
                return False
        
        except Exception as e:
            print(f"Erro ao deletar modelo: {str(e)}")
            return False


# Funções de compatibilidade com código antigo
def salvar_modelo(modelo):
    """Compatibilidade com API antiga"""
    return ModelLoader.salvar_modelo(modelo)


def carregar_modelo():
    """Compatibilidade com API antiga"""
    return ModelLoader.carregar_modelo()