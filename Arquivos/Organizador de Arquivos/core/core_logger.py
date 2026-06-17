import json
import os
from datetime import datetime
from config import LOGS_PATH, STATS_PATH


def registrar_log(nome_arquivo, categoria, status="sucesso"):
    """Registra a movimentação de um arquivo no log"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "arquivo": nome_arquivo,
        "categoria": categoria,
        "status": status
    }
    
    logs = []
    if os.path.exists(LOGS_PATH):
        try:
            with open(LOGS_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    
    logs.append(log_entry)
    
    with open(LOGS_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
    
    atualizar_stats(categoria)


def atualizar_stats(categoria):
    """Atualiza as estatísticas de organização"""
    
    stats = {}
    if os.path.exists(STATS_PATH):
        try:
            with open(STATS_PATH, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            stats = {}
    
    if categoria not in stats:
        stats[categoria] = 0
    stats[categoria] += 1
    
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)


def obter_logs():
    """Obtém todos os logs"""
    if not os.path.exists(LOGS_PATH):
        return []
    
    try:
        with open(LOGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def obter_stats():
    """Obtém as estatísticas"""
    if not os.path.exists(STATS_PATH):
        return {}
    
    try:
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}