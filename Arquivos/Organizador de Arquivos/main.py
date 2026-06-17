import click
from core.file_mover import organizar_downloads
from core.rules_engine import carregar_regras
from web.web_app import app
import os


@click.group()
def cli():
    """Organizador de Arquivos - IA-powered file organizer"""
    pass


@cli.command()
def organizar():
    """Organiza arquivos na pasta Downloads"""
    click.echo("🚀 Iniciando organização de arquivos...")
    try:
        organizar_downloads()
        click.echo("Organização concluída!")
    except Exception as e:
        click.echo(f"Erro: {str(e)}", err=True)


@cli.command()
def dashboard():
    """Inicia o dashboard web"""
    click.echo("🌐 Iniciando dashboard em http://localhost:5000")
    app.run(debug=True, port=5000)


@cli.command()
def stats():
    """Exibe estatísticas de organização"""
    regras = carregar_regras()
    click.echo("\nEstatísticas:")
    click.echo(f"Total de categorias: {len(regras)}")
    for categoria, palavras in regras.items():
        click.echo(f"  • {categoria}: {len(palavras)} palavras-chave")


if __name__ == "__main__":
    cli()