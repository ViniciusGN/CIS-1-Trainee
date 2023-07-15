import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def limpar_tela():
    input("Pressione Enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Los Angeles Crime Dataset (2020 -- Present)\n\n")

def observar_crimes_area(df):
    # Sabemos que há colunas em que há associação de código por descrição. Vamos separar essas colunas em outro arquivo
    id_area = df["AREA"]
    desc_area = df["AREA NAME"]

    # Criar um novo DataFrame com as colunas separadas
    cod_area = pd.DataFrame({'AREA_ID': id_area, 'AREA_NAME': desc_area})
    cod_area = cod_area.sort_values(by="AREA_ID", ascending=False) # Ordenar por código

    cod_area_plt = cod_area['AREA_NAME'].value_counts()
    cod_area_plt.plot(kind='bar', figsize=(12,9))
    plt.title('Frequência de Códigos de Área')
    plt.xlabel('Área')
    plt.ylabel('Quantidade de Ocorrências')

    plt.show()

    # Salvar apenas os valores únicos-> Uma bilioteca de id para area
    cod_area = cod_area.drop_duplicates() # Remover duplicatas
    cod_area.to_csv('cod_areas.csv', index=False) # Salvar em um novo arquivo

if __name__ == '__main__':
#------------------------------------------------ PARTE I
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Parte I: Data Acquisition")
    print("Los Angeles Crime Dataset (2020 -- Present)\n\n")
    crimes = pd.read_csv('Crime_Data_from_2020_to_Present.csv') #abrir o CSV

#------------------------------------------------ PARTE II
    op = 1
    while (op in range(1,6)):
        print("Parte II: Data Knowing")
        print("Item b - Para realizar uma avaliação rápida do dataset, escolha um número (1-5):\n1 - Ver as primeiras linhas")
        print("2 - o número de linhas e colunas do DataFrame\n3 - informações sobre as colunas e seus tipos de dados\n4 - estatísticas descritivas para as colunas numéricas")
        print("5 - Continuar")

        try:
            op = int(input("Digite o número: "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")
    
        
        if op == 1:
            print(crimes.head())      # Exibe as primeiras linhas do DataFrame
            limpar_tela()
        elif op == 2:
            print(crimes.shape)       # Retorna o número de linhas e colunas do DataFrame
            limpar_tela()
        elif op == 3:
            print(crimes.info())      # Fornece informações sobre as colunas e seus tipos de dados
            limpar_tela()
        elif op == 4:
            print(crimes.describe())  # Gera estatísticas descritivas para as colunas numéricas
            limpar_tela()
        elif op<1 or op>5:
            print("Opção inválida")
            op = 1
            limpar_tela()
        else:
            print("Continuando...")
            print("---Verificando as colunas---")
            colunas = crimes.columns
            print('Colunas: ', colunas)
            # Verificando crimes por area
            limpar_tela()
            break
            
    # Verificando valores nulos
    # print(crimes.isnull().sum())
#------------------------------------------------ PARTE III
    op2 = 1
    while (op2 in range(1,6)):
        print("Parte III: Data Exploration")
        print("Item b - Para realizar explorar o dataset, escolha um número (1-5):\n1 - Observar a frequencia de crimes por area")
        print("2 - Empty\n3 - Empty\n4 - Empty")
        print("5 - Continuar")
        
        try:
            op2 = int(input("Digite o número: "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")

        if op2 == 1:
            observar_crimes_area(crimes)  
            limpar_tela()
        elif op2 == 2:
            limpar_tela()
        elif op2 == 3:
            limpar_tela()
        elif op2 == 4:
            limpar_tela()
        elif op2<1 or op2>5:
            print("Opção inválida")
            op2 = 1
            limpar_tela()
        else:
            print("---Observar a frequencia de crimes por area---")
              

