import os

def renomear_arquivos(pasta, prefixo="", sufixo="", substituir=None, por=None, numerar=False):
    arquivos = sorted(os.listdir(pasta))
    contador = 1

    for nome in arquivos:
        caminho_antigo = os.path.join(pasta, nome)

        if os.path.isfile(caminho_antigo):
            nome_base, extensao = os.path.splitext(nome)

            novo_nome = nome_base

            if substituir and por is not None:
                novo_nome = novo_nome.replace(substituir, por)

            novo_nome = f"{prefixo}{novo_nome}{sufixo}"

            if numerar:
                novo_nome = f"{contador:03d}_{novo_nome}"
                contador += 1

            novo_nome += extensao

            caminho_novo = os.path.join(pasta, novo_nome)

            os.rename(caminho_antigo, caminho_novo)
            print(f"{nome} -> {novo_nome}")


pasta = "/caminho/da/sua/pasta"

renomear_arquivos(
    pasta,
    prefixo="IMG_",
    substituir="foto",
    por="imagem",
    numerar=True
)