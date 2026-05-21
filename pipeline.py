import os
import json
import requests
import time
import pandas as pd  # Importamos o Pandas com o apelido padrão 'pd'


def extrair_dados():
    # Em vez de puxar tudo de uma vez, quebramos por regiões para evitar o erro 400
    regioes = ["africa", "americas", "asia", "europe", "oceania"]
    dados_totais = []

    print("Iniciando a extração dos dados por região...")

    for regiao in regioes:
        url = f"https://restcountries.com/v3.1/region/{regiao}"
        print(f"Buscando dados da região: {regiao.capitalize()}...")

        try:
            resposta = requests.get(url)
            resposta.raise_for_status()

            dados_regiao = resposta.json()
            dados_totais.extend(
                dados_regiao
            )  # Junta a lista desta região na nossa lista total

            # Uma boa prática: esperar 1 segundo entre as requisições para não sobrecarregar a API
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro ao buscar a região {regiao}: {e}")
            # Se uma região falhar, continuamos tentando as outras
            continue

    if not dados_totais:
        print("❌ Falha crítica: Nenhuma região pôde ser extraída.")
        return None

    print(f"\nSucesso! Total de {len(dados_totais)} países encontrados no mundo.")

    # Garante que a pasta de destino existe
    os.makedirs("data/raw", exist_ok=True)

    # Salva o arquivo JSON consolidado
    caminho_destino = "data/raw/dados_paises.json"
    with open(caminho_destino, "w", encoding="utf-8") as f:
        json.dump(dados_totais, f, ensure_ascii=False, indent=4)

    print(f"Dados brutos consolidados salvos em: {caminho_destino}")
    return dados_totais


def transformar_dados():
    print("Iniciando a transformação e limpeza dos dados...")
    caminho_origem = "data/raw/dados_paises.json"

    # Garante que o arquivo bruto existe antes de tentar ler
    if not os.path.exists(caminho_origem):
        print("❌ Erro: Arquivo bruto não encontrado para transformação.")
        return

    # Carrega o JSON bruto usando Pandas
    # O pandas lê o JSON e tenta transformá-lo automaticamente em uma tabela (DataFrame)
    df = pd.read_json(caminho_origem)

    # Lista para guardar as linhas limpas que vamos extrair ao JSON complexo
    lista_paises_limpos = []

    # Fazemos um loop por cada país (linha) do DataFrame original para extrair os campos aninhados
    for index, linha in df.iterrows():
        # O nome do país vem dentro de um dicionário chamado 'name', na chave 'common'
        nome = linha["name"].get("common") if isinstance(linha["name"], dict) else None

        # A capital vem dentro de uma lista (ex: ['Brasília']). Pegamos o primeiro item da lista se ela existir.
        capital = (
            linha["capital"][0]
            if isinstance(linha["capital"], list) and len(linha["capital"]) > 0
            else "Não informada"
        )

        regiao = linha.get("region", "Desconhecida")
        populacao = linha.get("population", 0)
        area = linha.get("area", 0.0)

        # Cria um dicionário simples apenas com o que nos interessa
        dados_pais = {
            "nome": nome,
            "capital": capital,
            "regiao": regiao,
            "populacao": populacao,
            "area_km2": area,
        }
        lista_paises_limpos.append(dados_pais)

    # Transformamos nossa lista de dicionários limpos em um novo DataFrame do Pandas
    df_limpo = pd.DataFrame(lista_paises_limpos)

    # Tratamento de Dados (Data Cleaning)
    # Remove qualquer linha duplicada (caso a API tenha retornado o mesmo país duas vezes)
    df_limpo = df_limpo.drop_duplicates(subset=["nome"])

    # Ordena os países por nome para ficar bonito
    df_limpo = df_limpo.sort_values(by="nome").reset_index(drop=True)

    print("Transformação concluída!")
    print(
        f"Estrutura da tabela final:\n{df_limpo.head(5)}"
    )  # Mostra as 5 primeiras linhas no terminal

    return df_limpo


def carregar_dados(df_limpo):
    print("Iniciando a carga dos dados...")
    if df_limpo is None:
        print("❌ Erro: Não há dados para carregar.")
        return

    os.makedirs("data/processed", exist_ok=True)

    # Garante que a pasta de destino (processed) existe
    caminho_destino = "data/processed/paises_limpos.parquet"

    # Salva o DataFrame no formato Parquet
    df_limpo.to_parquet(caminho_destino, index=False)
    print(
        f"🚀 Sucesso absoluto! Dados limpos salvos em formato Parquet em: {caminho_destino}"
    )


if __name__ == "__main__":
    # 1. Executa a extração
    extrair_dados()

    # 2. Executa a transformação
    df_final = transformar_dados()

    # 3. Load
    carregar_dados(df_final)
