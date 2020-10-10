from datetime import datetime
import pandas as pd
import LogModule.log as log
import os, sys

def DbInit():
  vendido_a = [x for x in range(20)]
  vendedor = [x for x in range(20)]

  #UMA LAMBDA PARA SUBSTITUIR TUDO POR STRING VAZIA POR QUE NADA FOI VENDIDO AINDA
  broadcast_with_lambda = lambda x: ['' for i in x]

  vendido_a = broadcast_with_lambda(vendido_a)
  vendedor = broadcast_with_lambda(vendedor)

  instrumentsDict = {
    'id':[x for x in range(20)],
    'tipo':['violino','violino','violino','violino','violão','violão','violão','violão','teclado','teclado','teclado','teclado','violoncelo','violoncelo','violoncelo','violoncelo','flauta','flauta','flauta','flauta'],
    'vendido a':vendido_a,
    'vendedor':vendedor,
    'preco':[800,800,800,800,400,400,400,400,1400,1400,1400,1400,1200,1200,1200,1200,550,550,550,550]
    }
  frame = pd.DataFrame(instrumentsDict)
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    frame.to_excel(writer, sheet_name='instrumentos',header=True)
  writer.save()
  log.log('Instrumentos', 'inicializando o banco de dados')