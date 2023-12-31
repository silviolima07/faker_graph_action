# -*- coding: utf-8 -*-

from faker import Faker                
import numpy as np
import pandas as pd
fake = Faker() 

fake = Faker('pt_BR')



def create_profile(x): 
    print("Creating profile with ", n, " lines")
    # dictionary 
    profile_data ={} 
    for i in range(0, x): 
        profile_data[i]={} 
        profile_data[i] = fake.profile(infos)

    print("done")
    return profile_data
    


def create_sales(x): 
    print("Creating sales with ", n, " lines")
  
    # dictionary 
    sales_data ={} 
    for i in range(0, x): 
        sales_data[i]={} 
        sales_data[i]['preco'] = np.random.randint(10,500)
        sales_data[i]['qtd'] = np.random.randint(1,10)
        sales_data[i]['produto'] =  chr(np.random.randint(ord('A'), ord('Z')))
        sales_data[i]['total'] = sales_data[i]['preco'] * sales_data[i]['qtd']
        sales_data[i]['forma_de_pagamento'] = np.random.choice(['boleto', 'cartao_cred', 'a vista'])
    print("done")
    return sales_data



# Total lines created
n = np.random.randint(100,200)

# Create fake profile
infos = ['job', 'company', 'address', 'sex']
profiles = create_profile(n)
df_prof = pd.DataFrame.from_dict(profiles)
df_profile = df_prof.T

# Create fake sales
sales = create_sales(n)
temp_sales = pd.DataFrame.from_dict(sales)
df_sale = temp_sales.T

df_fake = pd.concat([df_profile, df_sale], axis=1)

# Extracting and creating column UF
lista_uf=[]
for i in range(len(df_fake['address'])):
  lista_uf.append(df_fake['address'][i].split(' / ')[1])

df_fake['uf'] = lista_uf
df_fake.drop_duplicates(inplace=True)
del df_fake['address']

df_fake.rename(columns={'job':'cargo', 'company':'empresa','sex':'sexo'}, inplace=True)
df_fake['preco'] = df_fake['preco'].astype('int32')
df_fake['total'] = df_fake['total'].astype('int32')
df_fake['qtd'] = df_fake['qtd'].astype('int32')

# Teste de leitura no redshift ok
#header = ['cargo','uf']
#df_fake.to_csv("df_fake.csv", index=False, encoding='utf-8', columns = header)

df_fake.to_csv("df_fake.csv", index=False, encoding='utf-8')
print("Shape:", df_fake.shape)
print("Columns:", df_fake.columns)
print("Type:", df_fake.info())
print(df_fake[['cargo', 'empresa']])
print(df_fake[['produto', 'preco', 'total']])
