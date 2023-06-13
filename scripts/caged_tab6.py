# -*- coding: utf-8 -*-
"""caged_tab6

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FUNVGXuHkLHWgIpJA_biUPrgKXhdTJlN
"""

import pandas as pd
import numpy as np
import requests
import io
from bs4 import BeautifulSoup
import urllib.request
import time

import boto3
from botocore import exceptions
from botocore.exceptions import ClientError

url_caged = "http://pdet.mte.gov.br/novo-caged"
parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen(url_caged)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
url_tabela='http://pdet.mte.gov.br'
for link in soup.find_all('a', href=True):
  if "tabelas.xlsx" in link['href']:
        #print("Link:",link['href'])
        #print("Url tabela: ", url_tabela+str(link['href']))
        url_tabela = url_tabela+str(link['href'])

def excel_to_pandas2(URL, local_path, sheet, header):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header)
    return df

def excel_to_pandas(URL, local_path, sheet, header,colunas):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header, usecols= colunas)
    return df

# Tabela 6

df_tab6 = excel_to_pandas2(url_tabela,'caged_tabela6_original.xlsx', 'Tabela 6', [4,5] )
print("\nCriada tabela df_tab6\n")

#df_tab6.columns

colunas_tab6 = df_tab6.columns

meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro", "Dezembro"]

#colunas_tab6

colunas_temp = colunas_tab6.to_list()
colunas = []
for i in colunas_temp:
  temp = str(i).replace("/", "'/")
  #print("TEMP:",temp)
  
  var = temp.split(',')[0].lstrip('(').strip().replace("'",'')
  #if (temp != "Unnamed: 0_level_0', 'Unnamed: 0_level_1"):
  #print("Coluna:", var)
  colunas.append(var)

colunas = colunas[2:]

#colunas

#for i in meses:
#  print(i)

colunas_filtered = []
for i in colunas:
  #print("Coluna:",i)
  temp = i.split('/')[0]
  if temp in meses:
    colunas_filtered.append(i)

col_set = set(colunas_filtered)

col_set

colunas = col_set

#cols1 = ['Admissões', 'Desligamentos','Saldos']
#cols2 = ['Admissões', 'Desligamentos','Saldos','Variação Relativa (%)']
#for col in colunas:
#  if col == 'Janeiro/2020':
#      print("coluna:",col,"\n",df_tab6[col][:27][cols1])
#  else:
#      print("coluna:",col,"\n",df_tab6[col][:27][cols1])

lista_ativ = df_tab6['Grupamento de Atividades Econômicas e Seção CNAE 2.0'][:27].values.tolist()

atividades =[]
for var in lista_ativ:
        atividades.append(var)

#atividades

len(atividades)

from datetime import datetime
x = datetime.now().date()
data = x.strftime("%m%Y")
print("Data:", data)

# Algumas tabelas tem apenas as colunas de col1: Janeiro/2020
col1 = ['Admissões', 'Desligamentos', 'Saldos']
#col2 = ['Estoque','Admissões', 'Desligamentos', 'Saldos', 'Variação Relativa (%)']
frames = []
for i in colunas:
  try:
      print("Coluna:",i)
      temp = df_tab6[i][1:27][col1]
      mes, ano = i.split('/')
      temp['data'] = i
      temp['mes'] = mes
      temp['ano'] = ano
      temp['atividade'] = atividades[1:]
      #print(temp)
      #print("df temp:", temp)
      #print("df:",temp[i][:28])
      #print("Colunas:", temp.columns)
      #temp['variavel'] = i
      frames.append(temp)
  except:
    
    print("\nError")
    #print(temp)

df_final = pd.concat(frames)

#df_final.to_csv('df_caged_tab6_'+data+'.csv', index=False, encoding='utf-8')
df_final.to_csv('df_caged_tab6.csv', index=False, encoding='utf-8')


print("\nCriado df_caged_tab6.csv no mes/ano:", data)
