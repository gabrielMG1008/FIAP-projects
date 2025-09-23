import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

# chamando os arquivos
planilha1 = pd.read_csv("vendas_linha_2019.csv", sep=";", encoding="latin1", decimal= ',')
planilha2 = pd.read_csv("vendas_linha_2020.csv", sep=";", encoding="latin1", decimal= ',')
planilha3 = pd.read_csv("vendas_linha_2021.csv", sep=";", encoding="latin1", decimal= ',')
planilha4 = pd.read_csv("vendas_linha_2022.csv", sep=";", encoding="latin1", decimal= ',')

dados = pd.concat([planilha1, planilha2, planilha3, planilha4], ignore_index= True)

# vendo as informações dos CSVs
print(dados.info())

# procurando valores nulos ou missings
# contando linhas
missings_por_linha = pd.DataFrame({'cod_pedido': dados['cod_pedido'].tolist(),
                                   'n_missings': dados.isna().sum(axis=1).tolist()})
n_colunas = dados.shape[1] - 1
# verificando o resultado
print(missings_por_linha.assign(perc_missings=missings_por_linha['n_missings'] / n_colunas) \
      .sort_values('perc_missings', ascending=False) \
      .head(10))

# contando colunas
missings_por_coluna = dados.isna().sum()
missings_por_coluna = pd.DataFrame( missings_por_coluna,
                                    columns=['n']) \
                                    .reset_index() \
                                    .rename(columns={'index': 'variaveis'})
n_linhas = dados.shape[0]

# verificando o resultado
print(missings_por_coluna \
    .assign( perc_missings = missings_por_coluna["n"] / n_linhas) \
    .sort_values("n", ascending= False))


# procurando valores outliers
#pd.set_option("display.max_columns", None) # mostra todas as colunas
dados['outliers'] = scale(dados['cod_pedido'])
print(dados.sort_values('outliers', ascending= False))

dados[['lucro_liquido','valor_total_bruto']].boxplot()
plt.show()

dados.plot.scatter(x = 'lucro_liquido',y = 'valor_total_bruto')
plt.show()
