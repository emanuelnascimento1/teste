import pandas as pd
import os  # Para verificar se o arquivo existe


def coletar_escolas():
    # URL da página da Wikipedia
    url = "https://pt.wikipedia.org/wiki/Resultados_do_Carnaval_do_Rio_de_Janeiro_em_2010"

    # Lê todas as tabelas da página com pandas
    tabelas = pd.read_html(url)

    # Exibe todas as tabelas para o usuário
    print("Tabelas disponíveis:")
    for i, tabela in enumerate(tabelas):
        print(f"{i}: {tabela.columns.tolist()}")  # Exibe o índice e o nome das colunas de cada tabela
    
    # Escolhe a tabela
    n_tabela = int(input("Digite o número da tabela que deseja visualizar: "))
    
    # Verifica se o número da tabela é válido
    if n_tabela < 0 or n_tabela >= len(tabelas):
        print("Número de tabela inválido.")
        return None

    # Define a tabela e exibe para o usuário
    tabela_selecionada = tabelas[n_tabela]
    print(f"Tabela selecionada (primeiras 5 linhas):")
    print(tabela_selecionada.head())  # Exibe as primeiras 5 linhas da tabela

    return tabela_selecionada


def salvar_escolas(escolas_revisao):
    # Nome do arquivo CSV
    nome_arquivo = "escolas_aprovadas.csv"

    # Verificar se o arquivo já existe
    if os.path.exists(nome_arquivo):
        # Ler o arquivo existente
        escolas_existentes = pd.read_csv(nome_arquivo)
    else:
        # Criar um DataFrame vazio se o arquivo não existir
        escolas_existentes = pd.DataFrame(columns=["Escola"])

    # Converter escolas_revisao para DataFrame (caso não seja)
    if not isinstance(escolas_revisao, pd.DataFrame):
        escolas_revisao = pd.DataFrame(escolas_revisao, columns=["Escola"])

    # Remover duplicatas: verificar quais escolas já estão no arquivo
    novas_escolas = escolas_revisao[~escolas_revisao["Escola"].isin(escolas_existentes["Escola"])]

    if not novas_escolas.empty:
        try:
            # Salvar apenas as novas escolas no arquivo CSV
            with open(nome_arquivo, 'a', encoding='utf-8') as f:
                novas_escolas.to_csv(f, index=False, header=f.tell() == 0)
            print(f"As novas escolas foram adicionadas ao arquivo '{nome_arquivo}'.")
        except Exception as e:
            print(f"Erro ao salvar no arquivo: {e}")
    else:
        print("Nenhuma escola nova para adicionar.")


# Primeira interação - Perguntar ao usuário se quer ver as tabelas
aprovacao_escolas = input("Deseja visualizar as tabelas disponíveis? (S/N): ").strip().upper()

if aprovacao_escolas == 'S':
    tabela = coletar_escolas()  # Coleta e exibe a tabela

    if tabela is not None:
        # Perguntar se deseja aprovar as escolas após visualizar a tabela
        aprovacao = input("Deseja aprovar a inclusão das escolas dessa tabela? (S/N): ").strip().upper()
        
        if aprovacao == 'S':
            # Supondo que a coluna com o nome das escolas seja 'Escola'
            try:
                escolas_revisao = tabela['Escola']
                salvar_escolas(escolas_revisao)  # Salva ou processa as escolas
            except KeyError:
                print("A coluna 'Escola' não foi encontrada na tabela selecionada. Verifique os dados.")
        else:
            print("Escolas descartadas.")
else:
    print("Nenhuma tabela será exibida ou aprovada.")
