import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium
import webbrowser

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
    cod_area_plt.plot(kind='bar', figsize=(10,8))
    plt.title('Frequência de Crimes por Área')
    plt.xlabel('Área')
    plt.ylabel('Quantidade de Ocorrências')

    plt.show()

    # Salvar apenas os valores únicos-> Uma bilioteca de id para area
    cod_area = cod_area.drop_duplicates() # Remover duplicatas
    cod_area.to_csv('cod_areas.csv', index=False) # Salvar em um novo arquivo

def observar_crimes_tipo(df):
    id_crime= df["Crm Cd"]
    desc_crime = df["Crm Cd Desc"]

    # Criar um novo DataFrame com as colunas separadas
    cod_crime = pd.DataFrame({'Crm_Id': id_crime, 'Crm_Desc': desc_crime})
    cod_acod_crime = cod_crime.sort_values(by="Crm_Id", ascending=False) # Ordenar por código

    cod_crime_plt = cod_acod_crime['Crm_Desc'].value_counts()
    cod_crime_plt.plot(kind='bar', figsize=(10,8))
    plt.title('Frequência de Crimes por Tipo')
    plt.xlabel('Tipo de Crime')
    plt.ylabel('Quantidade de Ocorrências')

    # Salvar apenas os valores únicos-> Uma bilioteca de id para tipo de crime
    cod_crime = cod_crime.drop_duplicates() # Remover duplicatas
    cod_crime = cod_crime.sort_values(by="Crm_Id", ascending=False) # Ordenar por código
    cod_crime.to_csv('cod_crimes.csv', index=False) # Salvar em um novo arquivo

    plt.show()

def observar_crimes_vitima(df):
    # Sabemos que há colunas em que há associação de código por descrição. Vamos separar essas colunas em outro arquivo
    Vict_Sex = df["Vict Sex"]
    Vict_Age = df["Vict Age"]

    type_vict = pd.DataFrame({'Vict Sex': Vict_Sex, 'Vict Age': Vict_Age})
    type_vict = type_vict.sort_values(by="Vict Sex", ascending=False)

    masculino = type_vict[type_vict['Vict Sex'] == 'M']
    feminino = type_vict[type_vict['Vict Sex'] == 'F']
    nao_declarado = type_vict[type_vict['Vict Sex'] == 'X']
    
    # Configurar a figura e os subplots
    fig, axs = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

    # Histograma para sexo masculino
    axs[0].hist(masculino['Vict Age'], bins=10, color='blue', alpha=0.7)
    axs[0].set_title('Distribuição de Idade - Masculino')
    axs[0].set_ylabel('Frequência')

    # Histograma para sexo feminino
    axs[1].hist(feminino['Vict Age'], bins=10, color='pink', alpha=0.7)
    axs[1].set_title('Distribuição de Idade - Feminino')
    axs[1].set_ylabel('Frequência')

    # Histograma para sexo não declarado
    axs[2].hist(nao_declarado['Vict Age'], bins=10, color='gray', alpha=0.7)
    axs[2].set_title('Distribuição de Idade - Não Declarado')
    axs[2].set_xlabel('Idade')
    axs[2].set_ylabel('Frequência')

    # Ajustar espaçamento entre os subplots
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()

def observar_tempo_crimes(df):
    # Converter as colunas de data e horário para o tipo datetime
    # Data de ocorrencia = DATE OCC
    # Horario de ocorrencia = TIME OCC
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')
    try:
        df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H%M').dt.time
    except ValueError:
        df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4)
        df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H%M').dt.time

    # Agrupar os dados por data e contar as ocorrências
    ocorrencias_por_data = df.groupby('DATE OCC').size()

    # Criar um DataFrame com as datas e o número de ocorrências
    df_ocorrencias = pd.DataFrame({'DATE OCC': ocorrencias_por_data.index, 'TIME OCC': ocorrencias_por_data.values})

    # Ordenar o DataFrame pela coluna de data_ocorrencia
    df_ocorrencias = df_ocorrencias.sort_values('DATE OCC')

    # Plotar o gráfico de linha
    plt.plot(df_ocorrencias['DATE OCC'], df_ocorrencias['TIME OCC'])
    plt.xlabel('Data de Ocorrência')
    plt.ylabel('Número de Ocorrências')
    plt.title('Ocorrências ao longo do tempo')

    # Rotacionar os rótulos do eixo x para melhor visualização
    plt.xticks(rotation=45)

    # Exibir o gráfico
    plt.show()

def oberservar_crimes_local(df):
    # Criar um mapa usando a biblioteca folium
    crime_map = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=12)

    # Adicionar marcadores para cada ponto de latitude e longitude
    for _, row in df.iterrows():
        folium.Marker(location=[row['LAT'], row['LON']]).add_to(crime_map)
    crime_map
    crime_map.save('crime_map.html')
    print("Abrindo o mapa em seu navegador...")
    webbrowser.open('crime_map.html')


def ML_tipo_crime(df):
    print("empty")
    pass

def ML_qual_sera_vitima(df):
    print("Aplicando o one-hot encoding na coluna 'Vict Sex' [M,F,X]")
    one_hot_encoded = pd.get_dummies(df['Vict Sex'], prefix='Vict Sex')
    # Concatenar os dados originais com as colunas one-hot encoding
    data_encoded = pd.concat([df, one_hot_encoded], axis=1)
    # Excluir a coluna original 'Vict Sex'
    data_encoded.drop('Vict Sex', axis=1, inplace=True)
    # Converter as colunas de data e horário para o tipo datetime

    # Remover amostras com valores ausentes
    data_encoded = data_encoded.dropna()

    # Separando as features (variáveis independentes) e o target (variável dependente)
    X = data_encoded.drop(['Vict Sex_F', "DR_NO", 'DATE OCC', 'Date Rptd', "AREA NAME",'Rpt Dist No', 'Part 1-2', 'Crm Cd Desc', 'Mocodes', 
                        'Vict Descent', 'Premis Desc','Weapon Desc', 'Status', 'Status Desc', 'Crm Cd 1', 
                        'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'LOCATION', 'Cross Street', 'Vict Sex_-', 'Vict Sex_H', 'Vict Sex_M'],  axis=1) 
    y = data_encoded['Vict Sex_F']
    print("Queremos verificar se: dado as condições de um crime (arma, local, etc), qual será o sexo da vítima? (M, F, X - não declarado)")

    # Separar o conjunto de treinamento e validação
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instanciar o modelo de regressão linear
    model = LinearRegression()

    # Treinar o modelo usando o conjunto de treinamento
    model.fit(X_train, y_train)

    # Fazer previsões no conjunto de validação
    y_pred = model.predict(X_val)

    # Avaliar o desempenho do modelo
    score = model.score(X_val, y_val)
    print('Score do modelo:', score)
    if score > 0.5:
        print("O modelo está bom!")
    else:
        print("O modelo está ruim! Possíveis problemas: Não-linearidade, multicolinearidade, problemas de dados, etc. ")
    print('Coeficientes do modelo:', model.coef_)

def tabelas_cod(df):
    # Separando a tabela de codigo por Premis
    id_premis= df["Premis Cd"]
    desc_premis = df["Premis Desc"]
    cod_premis = pd.DataFrame({'Premis_Id': id_premis, 'Premis_Desc': desc_premis})
    cod_premis = cod_premis.drop_duplicates() # Remover duplicatas
    cod_premis = cod_premis.sort_values(by="Premis_Id", ascending=False) # Ordenar por código
    cod_premis.to_csv('cod_premis.csv', index=False) # Salvar em um novo arquivo

    # Separando a tabela de codigo por Arma
    id_arma= df["Weapon Used Cd"]
    desc_arma = df["Weapon Desc"]
    cod_arma = pd.DataFrame({'Arma_Id': id_arma, 'Arma_Desc': desc_arma})
    cod_arma = cod_arma.drop_duplicates() # Remover duplicatas
    cod_arma = cod_arma.sort_values(by="Arma_Id", ascending=False) # Ordenar por código
    cod_arma.to_csv('cod_arma.csv', index=False) # Salvar em um novo arquivo

    # Separando a tabela de codigo por Status
    id_status= df["Status"]
    desc_status = df["Status Desc"]
    cod_status = pd.DataFrame({'Status_Id': id_status, 'Status_Desc': desc_status})
    cod_status = cod_status.drop_duplicates() # Remover duplicatas
    cod_status = cod_status.sort_values(by="Status_Id", ascending=False) # Ordenar por código
    cod_status.to_csv('cod_status.csv', index=False) # Salvar em um novo arquivo
    
def ML_onde_ocorrera(df):
    print("empty")
    pass

def parte_i():
    print("Parte I: Data Acquisition")
    print("Los Angeles Crime Dataset (2020 -- Present)")

def menu_part2(crimes):
#------------------------------------------------ PARTE II
    op = 1
    while (op in range(0,6)):
        print("Parte II: Data Knowing")
        print("Para realizar uma avaliação rápida do dataset, escolha um número (0-5):\n1 - Ver as primeiras linhas")
        print("2 - Ver o número de linhas e colunas do DataFrame\n3 - informações sobre as colunas e seus tipos de dados\n4 - estatísticas descritivas para as colunas numéricas")
        print("5 - Continuar\n0 - Sair do codigo.")

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
        elif op<0 or op>6:
            print("Opção inválida")
            op = 1
            limpar_tela()
        elif op == 5:
            limpar_tela()
            print("---Verificando as colunas---")
            colunas = crimes.columns
            print('Colunas: ', colunas)
            # Verificando crimes por area
            break
        elif op == 0:
            print("Obrigado por usar este código. Saindo do código...")
            exit()

def menu_part3(crimes):
#------------------------------------------------ PARTE III
    op2 = 1
    while (op2 in range(0,7)):
        print("Parte III: Data Exploration")
        print("Para realizar a exploração o dataset, escolha um número (0-5):\n1 - Observar a frequencia de crimes por area")
        print("2 - Observar a frequencia de crimes por tipo\n3 - Observar a frequencia do perfil das vítimas\n4 - Ver relação de tempo dos crimes")
        print("5 - Observar mapa dos crimes [Muito pesado, preferivel nao executar]\n6 - Continuar\n0 - Sair do codigo.")
        
        try:
            op2 = int(input("Digite o número: "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")

        if op2 == 1:
            observar_crimes_area(crimes) 
            print("Observamos que a maior parte dos crimes em LA ocorrem no Centro da Cidade.")
            print("Observamos que a menor parte dos crimes em LA ocorrem no bairro Footnill.")
            limpar_tela()

        elif op2 == 2:
            observar_crimes_tipo(crimes)
            print("Observamos que a maior parte dos crimes em LA são de roubo.")
            print("Observamos que a menor parte dos crimes em LA são de homicídio.")
            limpar_tela()
        elif op2 == 3:
            observar_crimes_vitima(crimes)
            print("Observamos que a maior parte das vítimas são homens.")
            print("Observamos que a faixa étaria masculina mais atingida é de 20 a 30 anos.")
            print("Observamos que a faixa étaria feminina mais atingida é de 20 a 30 anos.")
            print("Observamos que a faixa étaria não declarada mais atingida é a proxima de 0 anos.")
            limpar_tela()
        elif op2 == 4:
            observar_tempo_crimes(crimes)
            print("Observamos que a maior parte dos crimes em LA ocorrem no período da tarde.")
            print("Observamos que a menor parte dos crimes em LA ocorrem no período da madrugada.")
            limpar_tela()
        elif op2 == 5:
            oberservar_crimes_local(crimes)
            limpar_tela()
        elif op2<0 or op2>6:
            print("Opção inválida")
            op2 = 1
            limpar_tela()
        elif op2 == 0:
            print("Obrigado por usar este código. Saindo do código...")
            exit()
        elif op2 == 6:
            print("Continuando...")
            limpar_tela()
            break

def menu_part4(crimes):
    op2 = 1
    while (op2 in range(0,5)):
        print("Parte IV: MACHINE LEARNING")
        print("Para aplicar conceitos de IA no dataset, escolha um número (0-4):\n1 - Predição do Tipo de Crime")
        print("2 - Predição do tipo de Vítima\n3 - Predição do local de ocorrência")
        print("4 - Continuar\n0 - Sair do codigo.")
        
        try:
            op2 = int(input("Digite o número: "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")

        if op2 == 1:
            ML_tipo_crime(crimes)
            limpar_tela()

        elif op2 == 2:
            ML_qual_sera_vitima(crimes)
            limpar_tela()
        elif op2 == 3:
            ML_onde_ocorrera(crimes)
            limpar_tela()
        elif op2<0 or op2>4:
            print("Opção inválida")
            op2 = 1
            limpar_tela()
        elif op2 == 0:
            print("Obrigado por usar este código. Saindo do código...")
            exit()
        elif op2 == 4:
            print("Continuando...")
            limpar_tela()
            break
    pass

if __name__ == '__main__':
#------------------------------------------------ PARTE I
    os.system('cls' if os.name == 'nt' else 'clear')
    parte_i()
    print("\nAbrindo o DataFrame...")
    crimes = pd.read_csv('Crime_Data_from_2020_to_Present.csv') #abrir o CSV
    print("DataFrame aberto com sucesso!\n\n")
    tabelas_cod(crimes) # Criar tabelas de codigo
# -------------------------Menu principal
    op = 1
    while (op in range(0,6)):
        print("Menu principal:")
        print("1 - Apresentação sequencial do trabalho:")
        print("2 - Parte I: Data Acquisition")
        print("3 - Parte II: Data Knowing")
        print("4 - Parte III: Data Exploration")
        print("5 - Parte IV: Machine Learning")
        print("0 - Sair do codigo.")
        try:
            op = int(input("Digite o número: "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")
        if op == 1:
            limpar_tela()
            menu_part2(crimes)
            menu_part3(crimes)
            menu_part4(crimes)
            limpar_tela()
        if op == 2:
            limpar_tela()
            parte_i()
            limpar_tela()    
        if op == 3:
            limpar_tela()
            menu_part2(crimes)
            limpar_tela()
        if op == 4:
            limpar_tela()
            menu_part3(crimes)
            limpar_tela()
        if op == 5:
            limpar_tela()
            menu_part4(crimes)
            limpar_tela()
        if op == 0:
            print("Obrigado por usar este código. Saindo do código...")
            exit()
        elif op<0 or op>5:
            print("Opção inválida")
            op = 1
            limpar_tela()
    

    # Verificando valores nulos
    # print(crimes.isnull().sum())