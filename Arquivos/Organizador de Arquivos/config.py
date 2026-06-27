import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

RULES_PATH = DATA_DIR / "rules.json"
LOGS_PATH = DATA_DIR / "logs.json"
STATS_PATH = DATA_DIR / "stats.json"
MODEL_PATH = MODELS_DIR / "trained_model.bin"
EMBEDDINGS_CACHE_PATH = MODELS_DIR / "embeddings_cache.pkl"

DEFAULT_CATEGORIES = {
    "financeiro": ["boleto", "fatura", "nubank", "cartao", "pix", "pagamento", "nfe", "recibo"],
    "trabalho": ["curriculo", "cv", "vaga", "portifolio", "empresa", "proposta", "contrato"],
    "estudos": ["prova", "aula", "curso", "exercicio", "faculdade", "apostila", "resumo"],
    "mensagens": ["whatsapp", "telegram", "img", "screenshot", "print", "mensagem"],
    "outros": []
}

FLASK_DEBUG = True
FLASK_PORT = 5000

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"