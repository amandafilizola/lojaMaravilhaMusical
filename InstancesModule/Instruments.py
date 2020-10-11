import datetime as dt
import pandas as pd
import LogModule.log as log
import InstancesModule.People as people
import InstancesModule.Profiles as profiles
import os, sys

def DbInit():
  vendido_a = [x for x in range(20)]
  vendedor = [x for x in range(20)]
  data_da_venda = [x for x in range(20)]

  #UMA LAMBDA PARA SUBSTITUIR TUDO POR STRING VAZIA POR QUE NADA FOI VENDIDO AINDA
  broadcast_with_lambda = lambda x: ['' for i in x]

  vendido_a = broadcast_with_lambda(vendido_a)
  vendedor = broadcast_with_lambda(vendedor)
  data_da_venda = broadcast_with_lambda(data_da_venda)

  instrumentsDict = {
    'id':[x for x in range(20)],
    'tipo':['violino','violino','violino','violino','violão','violão','violão','violão','teclado','teclado','teclado','teclado','violoncelo','violoncelo','violoncelo','violoncelo','flauta','flauta','flauta','flauta'],
    'vendido a':vendido_a,
    'vendedor':vendedor,
    'data da venda': data_da_venda,
    'preco':[800,800,800,800,400,400,400,400,1400,1400,1400,1400,1200,1200,1200,1200,550,550,550,550]
    }
  frame = pd.DataFrame(instrumentsDict)
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    frame.to_excel(writer, sheet_name='instrumentos',header=True, index=False)
  writer.save()
  log.log('Instrumentos', 'inicializou o banco de dados')


def listInstruments(loggedUser, showMode):
  #se showMode for True, itens já vendidos devem aparecer
  #se showMode for False, apenas itens disponíveis devem aparecer

  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame
  
  if(showMode == False):
    filteredInstrumentlist = instrumentsList[instrumentsList['vendedor'].isnull()]
  else:
    filteredInstrumentlist = instrumentsList
  print('\n===========================================================================\n')
  print(filteredInstrumentlist)
  print('\n===========================================================================\n')
  
  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'listou todos os instrumentos')


def buyInstrument(loggedUser, showMode):
  listInstruments(loggedUser, showMode)
  whichInstrument = people.questionUntilReturnsInteger('Qual o id do instrumento que deseja comprar?\n')
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')
  print(instrumentsList.loc[instrumentsList['id'] == whichInstrument].vendedor.iloc[0])
  if(pd.isnull(instrumentsList.loc[instrumentsList['id'] == whichInstrument].vendedor.iloc[0])):
    usersList = database.parse('pessoas')  # read a specific sheet to DataFrame
    listEmployees = usersList.loc[usersList['perfil'] == profiles.Profiles.Employee]

    print('\n===========================================================================\n')
    print(listEmployees)
    print('\n===========================================================================\n')

    whichSeller = people.questionUntilReturnsInteger('Qual o id do vendedor que o atendeu?\n')
    buyApproved = people.questionUntilReturnsInteger('O instrumento é um(a) {} e custa {}. Você realizará esta compra com {}?\n1.Sim\n2.Não'.format(
    instrumentsList.loc[instrumentsList['id'] == whichInstrument].tipo.iloc[0],
    instrumentsList.loc[instrumentsList['id'] == whichInstrument].preco.iloc[0],
    usersList.loc[usersList['id'] == whichSeller].nome.iloc[0]
    ))
    
    if(buyApproved == 1):
      sellerName = usersList.loc[usersList['id'] == whichSeller].nome.iloc[0]
      row = loggedUser.index[0]
      clientName = loggedUser.loc[row].nome
      now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

      #SETANDO AS NOVAS INFORMAÇÕES DE VENDA NAS COLUNAS
      instrumentsList.loc[instrumentsList['id']==whichInstrument,'vendido a'] = clientName
      instrumentsList.loc[instrumentsList['id']==whichInstrument,'vendedor'] = sellerName
      instrumentsList.loc[instrumentsList['id']==whichInstrument,'data da venda'] = now
        
      with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
        workbook = writer.book
        try:
          workbook.remove(workbook['instrumentos'])
        except:
            print("Worksheet does not exist")
        finally:
          instrumentsList.to_excel(writer, sheet_name='instrumentos',header=True, index=False)
        writer.save()
      log.log(clientName, 'Comprou um(a) {} pelo preço de {} reais com o vendedor {}'.format(
      instrumentsList.loc[instrumentsList['id'] == whichInstrument].tipo.iloc[0],
      instrumentsList.loc[instrumentsList['id'] == whichInstrument].preco.iloc[0],
      usersList.loc[usersList['id'] == whichSeller].nome.iloc[0]
      ))
    else:
      print('Aw, uma pena que não vais levar desta vez! Sempre estaremos de portas abertas para sua vontade musical! Volte sempre!')
  else:
    print('Ops, parece que já vendemos este item! Quer olhar algo mais?')


def showStock():
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame

  instrumentTypes = set(instrumentsList.loc[:,'tipo'].values)
  filteredArray = instrumentsList[instrumentsList['vendedor'].isnull()]
  print('________________')
  for instrumentType in instrumentTypes:
    print('| {} -->  {}    '.format(instrumentType,len(filteredArray[filteredArray.loc[:,'tipo']==instrumentType])))
  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'consultou o estoque de instrumentos')
  

    
  
  

