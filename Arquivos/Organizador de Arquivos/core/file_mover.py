import os
import shutil
from pathlib import Path
from core.nlp_classifier import classificar
from core.core_logger import registrar_log
from utils.path_utils import gerar_caminho_seguro
from config import DOWNLOADS_DIR


def organizar_downloads():
    """Organiza arquivos na pasta Downloads"""
    
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"Pasta não encontrada: {DOWNLOADS_DIR}")
        return
    
    arquivos_movidos = 0
    erros = 0
    
    for arquivo in os.listdir(DOWNLOADS_DIR):
        caminho = os.path.join(DOWNLOADS_DIR, arquivo)
        
        if os.path.isdir(caminho) or arquivo.startswith("."):
            continue
        
        try:
            categoria = classificar(arquivo)
            
            destino_dir = os.path.join(DOWNLOADS_DIR, categoria)
            
            destino_final = gerar_caminho_seguro(destino_dir, arquivo)
            
            shutil.move(caminho, destino_final)
            
            registrar_log(arquivo, categoria, "sucesso")
            
            print(f"{arquivo} → {categoria}")
            arquivos_movidos += 1
            
        except Exception as e:
            registrar_log(arquivo, "desconhecido", f"erro: {str(e)}")
            print(f"Erro ao mover {arquivo}: {str(e)}")
            erros += 1
    
    print(f"\nResumo: {arquivos_movidos} movidos, {erros} erros")
    return arquivos_movidos, erros


def organizar_pasta_customizada(caminho_pasta):
    """Organiza arquivos em uma pasta customizada"""
    
    if not os.path.exists(caminho_pasta):
        print(f"Pasta não encontrada: {caminho_pasta}")
        return
    
    arquivos_movidos = 0
    
    for arquivo in os.listdir(caminho_pasta):
        caminho = os.path.join(caminho_pasta, arquivo)
        
        if os.path.isdir(caminho) or arquivo.startswith("."):
            continue
        
        try:
            categoria = classificar(arquivo)
            destino_dir = os.path.join(caminho_pasta, categoria)
            destino_final = gerar_caminho_seguro(destino_dir, arquivo)
            
            shutil.move(caminho, destino_final)
            registrar_log(arquivo, categoria, "sucesso")
            
            print(f"{arquivo} → {categoria}")
            arquivos_movidos += 1
            
        except Exception as e:
            print(f"Erro: {arquivo} - {str(e)}")
    
    return arquivos_movidos