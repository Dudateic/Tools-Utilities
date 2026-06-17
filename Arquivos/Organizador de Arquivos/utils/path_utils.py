import os


def gerar_caminho_seguro(diretorio, nome_arquivo):
    """
    Gera um caminho seguro para o arquivo, evitando conflitos de nome.
    Se o arquivo já existe, adiciona um número ao nome.
    """
    
    os.makedirs(diretorio, exist_ok=True)
    
    caminho_completo = os.path.join(diretorio, nome_arquivo)
    
    if not os.path.exists(caminho_completo):
        return caminho_completo
    
    nome, extensao = os.path.splitext(nome_arquivo)
    contador = 1
    
    while True:
        novo_nome = f"{nome}_{contador}{extensao}"
        novo_caminho = os.path.join(diretorio, novo_nome)
        
        if not os.path.exists(novo_caminho):
            return novo_caminho
        
        contador += 1


def criar_categoria_dir(base_dir, categoria):
    """Cria o diretório de categoria se não existir"""
    categoria_dir = os.path.join(base_dir, categoria)
    os.makedirs(categoria_dir, exist_ok=True)
    return categoria_dir


def validar_caminho(caminho):
    """Valida se o caminho é seguro (evita path traversal)"""
    abs_path = os.path.abspath(os.path.expanduser(caminho))
    
    if ".." in caminho:
        return False
    
    return True