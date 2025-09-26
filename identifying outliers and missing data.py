
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.covariance import EmpiricalCovariance, MinCovDet
import scipy as sy


# chamando os arquivos
planilha1 = pd.read_csv("C:\\Users\\gabri\\Downloads\\vendas_linha_petshop_2019.csv", sep=";", encoding="latin1", decimal= ',')
planilha2 = pd.read_csv("C:\\Users\\gabri\\Downloads\\vendas_linha_petshop_2020.csv", sep=";", encoding="latin1", decimal= ',')
planilha3 = pd.read_csv("C:\\Users\\gabri\\Downloads\\vendas_linha_petshop_2021.csv", sep=";", encoding="latin1", decimal= ',')
planilha4 = pd.read_csv("C:\\Users\\gabri\\Downloads\\vendas_linha_petshop_2022.csv", sep=";", encoding="latin1", decimal= ',')

dados = pd.concat([planilha1, planilha2, planilha3, planilha4], ignore_index= True)

# vendo as informações dos CSVs
print(dados.info())

# procurando valores outliers
#pd.set_option("display.max_columns", None) # mostra todas as colunas
dados['outliers'] = scale(dados['cod_pedido'])
print(dados.sort_values('outliers', ascending= False))

dados[['valor','valor_total_bruto']].boxplot()
#plt.show()

dados.plot.scatter(x = 'valor',y = 'valor_total_bruto')
#plt.show()

#desvio padrão comum
print(
dados.groupby('valor').agg(
    desvio_medio = pd.NamedAgg(column='valor_total_bruto', aggfunc='std')
).reset_index()
)

#intervalo interquartil (IQR)
print(
    dados.groupby('valor')['valor_total_bruto'].apply(
        lambda x: x.quantile([0.05,0.25,0.5,0.75,0.95])
    ).to_frame()
    .reset_index().rename(columns={'level_1':'percentil'}
    )
)

#MAD
def mad(x):
    return np.median(np.abs(x - np.median(x)))

mad_por_valor = dados.groupby("valor").agg(
    mad_valor_total_bruto=pd.NamedAgg(column="valor_total_bruto", aggfunc=mad)
).reset_index()

print(mad_por_valor)
