"""
Script para corrigir a estrutura do projeto automaticamente
Executa: python fix_project.py
"""

import os
import shutil
from pathlib import Path

def criar_estrutura():
    """Cria a estrutura correta de pastas"""
    
    pastas = [
        'core',
        'models',
        'utils',
        'web/templates',
        'web/static',
        'data'
    ]
    
    print("Criando pastas...")
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"{pasta}/")
    
    print()

def criar_init_files():
    """Cria __init__.py em cada módulo"""
    
    modulos = [
        'core/__init__.py',
        'models/__init__.py',
        'utils/__init__.py',
        'web/__init__.py'
    ]
    
    print("Criando __init__.py...")
    for modulo in modulos:
        Path(modulo).touch()
        print(f"{modulo}")
    
    print()

def reorganizar_arquivos():
    """Move arquivos para o local correto"""
    
    print("Reorganizando arquivos...")
    
    movimentos = [
        ('core_logger.py', 'core/logger.py'),
        ('file_mover.py', 'core/file_mover.py'),
        ('nlp_classifier.py', 'core/nlp_classifier.py'),
        ('rules_engine.py', 'core/rules_engine.py'),
        
        ('embeddings.py', 'models/embeddings.py'),
        ('loader.py', 'models/loader.py'),
        
        ('path_utils.py', 'utils/path_utils.py'),
        ('text_processing.py', 'utils/text_processing.py'),
        
        ('web_app.py', 'web/web_app.py'),
        ('web_app_fixed.py', 'web/web_app.py'),  
        ('dashboard.html', 'web/templates/dashboard.html'),
        ('style.css', 'web/static/style.css'),
    ]
    
    for origem, destino in movimentos:
        if os.path.exists(origem):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            
            shutil.move(origem, destino)
            print(f"{origem} → {destino}")
        else:
            print(f"{origem} não encontrado")
    
    print()

def limpar_cache():
    """Remove cache Python"""
    
    print("Limpando cache Python...")
    
    # Remover __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_dir)
            print(f"Removido {cache_dir}")
    
    # Remover .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                os.remove(pyc_file)
                print(f"Removido {pyc_file}")
    
    print()

def verificar_estrutura():
    """Verifica se a estrutura está correta"""
    
    print("Verificando estrutura...")
    
    arquivos_esperados = [
        'main.py',
        'config.py',
        'requirements.txt',
        'core/__init__.py',
        'core/logger.py',
        'core/file_mover.py',
        'core/nlp_classifier.py',
        'core/rules_engine.py',
        'models/__init__.py',
        'models/embeddings.py',
        'models/loader.py',
        'utils/__init__.py',
        'utils/path_utils.py',
        'utils/text_processing.py',
        'web/__init__.py',
        'web/web_app.py',
        'web/templates/dashboard.html',
        'web/static/style.css',
    ]
    
    tudo_ok = True
    for arquivo in arquivos_esperados:
        if os.path.exists(arquivo):
            print(f"{arquivo}")
        else:
            print(f"{arquivo} - NÃO ENCONTRADO")
            tudo_ok = False
    
    print()
    
    if tudo_ok:
        print("Estrutura está PERFEITA!")
    else:
        print("Existem arquivos faltando. Verifique acima.")
    
    return tudo_ok

def main():
    print("=" * 50)
    print("🔧 CORRIGINDO ESTRUTURA DO PROJETO")
    print("=" * 50)
    print()
    
    criar_estrutura()
    criar_init_files()
    reorganizar_arquivos()
    limpar_cache()
    
    ok = verificar_estrutura()
    
    print("=" * 50)
    if ok:
        print("Projeto está pronto para usar!")
        print()
        print("Próximos passos:")
        print("1. python main.py organizar    # Organizar Downloads")
        print("2. python main.py dashboard    # Abrir Dashboard")
        print("3. python main.py stats        # Ver Estatísticas")
    else:
        print("Por favor, corrija os arquivos faltantes acima.")
    print("=" * 50)

if __name__ == '__main__':
    main()