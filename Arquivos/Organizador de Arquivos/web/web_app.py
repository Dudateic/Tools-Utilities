from flask import Flask, jsonify, request, render_template, send_file
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.core_logger import obter_logs, obter_stats
from core.rules_engine import (
    carregar_regras, salvar_regras, adicionar_regra, 
    remover_regra, criar_categoria, deletar_categoria
)
from core.nlp_classifier import classificar, sugerir_categoria
from core.file_mover import organizar_downloads, organizar_pasta_customizada
from config import RULES_PATH, LOGS_PATH, STATS_PATH, DOWNLOADS_DIR
import threading

BASE_DIR = Path(__file__).parent
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))
app.config['JSON_AS_ASCII'] = False


def load_json(path):
    """Carrega dados de um arquivo JSON"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_json(path, data):
    """Salva dados em um arquivo JSON"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



@app.route("/")
def dashboard():
    """Retorna o dashboard HTML"""
    return render_template("dashboard.html")


@app.route("/api/regras", methods=["GET"])
def get_regras():
    """Obtém todas as regras de classificação"""
    regras = carregar_regras()
    return jsonify(regras)


@app.route("/api/regras", methods=["POST"])
def add_regra_api():
    """Adiciona uma nova regra de classificação"""
    try:
        body = request.json
        categoria = body.get("categoria")
        palavra = body.get("palavra")
        
        if not categoria or not palavra:
            return jsonify({"erro": "categoria e palavra são obrigatórios"}), 400
        
        sucesso = adicionar_regra(categoria, palavra)
        
        if sucesso:
            return jsonify({"status": "ok", "mensagem": "Regra adicionada com sucesso"})
        else:
            return jsonify({"aviso": "Regra já existe"}), 409
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/regras/<categoria>/<palavra>", methods=["DELETE"])
def remover_regra_api(categoria, palavra):
    """Remove uma regra de classificação"""
    try:
        sucesso = remover_regra(categoria, palavra)
        
        if sucesso:
            return jsonify({"status": "ok", "mensagem": "Regra removida com sucesso"})
        else:
            return jsonify({"erro": "Regra não encontrada"}), 404
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/categorias", methods=["POST"])
def criar_categoria_api():
    """Cria uma nova categoria"""
    try:
        body = request.json
        categoria = body.get("categoria")
        
        if not categoria:
            return jsonify({"erro": "categoria é obrigatória"}), 400
        
        sucesso = criar_categoria(categoria)
        
        if sucesso:
            return jsonify({"status": "ok", "mensagem": "Categoria criada com sucesso"})
        else:
            return jsonify({"aviso": "Categoria já existe"}), 409
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/categorias/<categoria>", methods=["DELETE"])
def deletar_categoria_api(categoria):
    """Deleta uma categoria"""
    try:
        if categoria == "outros":
            return jsonify({"erro": "Não é possível deletar a categoria 'outros'"}), 400
        
        sucesso = deletar_categoria(categoria)
        
        if sucesso:
            return jsonify({"status": "ok", "mensagem": "Categoria deletada com sucesso"})
        else:
            return jsonify({"erro": "Categoria não encontrada"}), 404
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/logs", methods=["GET"])
def logs_api():
    """Retorna todos os logs de movimentação"""
    logs = obter_logs()
    return jsonify(logs)


@app.route("/api/stats", methods=["GET"])
def stats_api():
    """Retorna as estatísticas de organização"""
    stats = obter_stats()
    return jsonify(stats)


@app.route("/api/classificar", methods=["POST"])
def classificar_api():
    """Classifica um arquivo"""
    try:
        body = request.json
        nome_arquivo = body.get("nome_arquivo")
        
        if not nome_arquivo:
            return jsonify({"erro": "nome_arquivo é obrigatório"}), 400
        
        categoria = classificar(nome_arquivo)
        sugestoes = sugerir_categoria(nome_arquivo)
        
        return jsonify({
            "nome_arquivo": nome_arquivo,
            "categoria": categoria,
            "sugestoes": sugestoes
        })
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/organizar", methods=["POST"])
def organizar_api():
    """Inicia a organização de arquivos"""
    try:
        def executar_organizacao():
            try:
                organizar_downloads()
            except Exception as e:
                print(f"Erro na organização: {str(e)}")
        
        thread = threading.Thread(target=executar_organizacao)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "ok",
            "mensagem": "Organização iniciada em background"
        })
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/organizar-pasta", methods=["POST"])
def organizar_pasta_api():
    """Organiza uma pasta customizada"""
    try:
        body = request.json
        caminho = body.get("caminho")
        
        if not caminho:
            return jsonify({"erro": "caminho é obrigatório"}), 400
        
        if not os.path.exists(caminho):
            return jsonify({"erro": f"Pasta não encontrada: {caminho}"}), 404
        
        def executar():
            organizar_pasta_customizada(caminho)
        
        thread = threading.Thread(target=executar)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "status": "ok",
            "mensagem": "Organização iniciada"
        })
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/info", methods=["GET"])
def info_api():
    """Retorna informações do sistema"""
    return jsonify({
        "nome": "Organizador de Arquivos",
        "versao": "1.0.0",
        "downloads_dir": DOWNLOADS_DIR,
        "regras_carregadas": len(carregar_regras()),
        "logs_totais": len(obter_logs()),
    })


@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({"erro": "Rota não encontrada"}), 404


@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"erro": "Erro interno do servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)