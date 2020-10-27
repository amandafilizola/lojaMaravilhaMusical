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

def listInstruments(loggedUser, showMode, logMode):
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
  if(logMode == True):
    log.log(loggedUser.loc[row].nome, 'listou todos os instrumentos')

def buyInstrument(loggedUser, showMode, logMode):
  listInstruments(loggedUser, showMode, logMode)
  whichInstrument = people.questionUntilReturnsInteger('Qual o id do instrumento que deseja comprar?\n')
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')
  if(pd.isnull(instrumentsList.loc[instrumentsList['id'] == whichInstrument].vendedor.iloc[0])):
    usersList = database.parse('pessoas')  # read a specific sheet to DataFrame
    listEmployees = usersList.loc[usersList['perfil'] == profiles.Profiles.Employee]

    print('\n===========================================================================\n')
    print(listEmployees)
    print('\n===========================================================================\n')

    whichSeller = people.questionUntilReturnsInteger('Qual o id do vendedor que o atendeu?\n')
    buyApproved = people.questionUntilReturnsInteger('O instrumento é um(a) {} e custa {}. Você realizará esta compra com {}?\n1.Sim\n2.Não\n'.format(
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
      print('Aw, uma pena que não vais levar desta vez! Sempre estaremos de portas abertas para sua vontade musical! Volte sempre!\n')
  else:
    print('Ops, parece que já vendemos este item! Quer olhar algo mais?\n')

def showStock(loggedUser):
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame

  instrumentTypes = set(instrumentsList.loc[:,'tipo'].values)
  filteredArray = instrumentsList[instrumentsList['vendedor'].isnull()]
  print('________________')
  for instrumentType in instrumentTypes:
    print('| {} -->  {}    '.format(instrumentType,len(filteredArray[filteredArray.loc[:,'tipo']==instrumentType])))
  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'consultou o estoque de instrumentos')

def createInstrument(loggedUser):
  print("Você entrou no cadastro de novos instrumentos.")
  typeOfInstrument = input("Qual o tipo do instrumento a ser cadastrado?\n")
  price = people.questionUntilReturnsInteger("Qual o preço do instrumento?\n")

  #ler excel para pegar o ultimo id de instrumento gerado
  if(not os.path.exists('database.xlsx')):
    id=1
    excelWriteMode = 'w'
    headerMode = True
  else:
    excelWriteMode = 'a'
    headerMode = False
    database = pd.read_excel('database.xlsx', 'instrumentos')
    max_value = database['id'].max()
    id = max_value+1

  #UM LINDO DICIONÁRIO QUE SERIA O OBJETO INSTRUMENTO NOVO!
  instrumentsDict = {
    'id':id,
    'tipo':[typeOfInstrument],
    'vendido a':'',
    'vendedor':'',
    'data da venda': '',
    'preco':[price]
    }
  frame = pd.DataFrame(instrumentsDict)

  #escrever no excel
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode=excelWriteMode) as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
    frame.to_excel(writer, sheet_name='instrumentos',startrow=writer.sheets['instrumentos'].max_row, header=headerMode, index=False)
  writer.save()
  row = loggedUser.index[0]
  employeeName = loggedUser.loc[row].nome

  log.log(employeeName, 'Cadastrou um(a) {} pelo preço de {} reais'.format(
    typeOfInstrument,
    price,
  ))

def updateInstrument(loggedUser):
  print("Você entrou na atualização de instrumentos.")
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')
  listInstruments(loggedUser, False, False)

  whichInstrument = people.questionUntilReturnsInteger('Qual id do instrumento que você deseja atualizar?\n')

  #salvando antigas informações para logar a mudança em detalhes
  oldType = instrumentsList.loc[instrumentsList['id'] == whichInstrument].tipo.iloc[0]
  oldPrice = instrumentsList.loc[instrumentsList['id'] == whichInstrument].preco.iloc[0]

  if(pd.isnull(instrumentsList.loc[instrumentsList['id'] == whichInstrument].vendedor.iloc[0])):
    updateType = people.questionUntilReturnsInteger('Você deseja atualizar que características do instrumento?\n1.Tipo\n2.Preço\n3.Tipo e preço\n')

    if(updateType == 1):
      newType = input('Qual o novo tipo do instrumento?\n')
      instrumentsList.loc[instrumentsList['id'] == whichInstrument,'tipo'] = newType

    elif(updateType == 2):
      newPrice = people.questionUntilReturnsInteger('Qual o novo preço do instrumento?\n')
      instrumentsList.loc[instrumentsList['id'] == whichInstrument,'preco'] = newPrice

    elif(updateType == 3):
      newType = input('Qual o novo tipo do instrumento?\n')
      newPrice = people.questionUntilReturnsInteger('Qual o novo preço do instrumento?\n')
      instrumentsList.loc[instrumentsList['id'] == whichInstrument,'tipo'] = newType
      instrumentsList.loc[instrumentsList['id'] == whichInstrument,'preco'] = newPrice

    updateApproved = people.questionUntilReturnsInteger('O instrumento é um(a) {} e custa {}. Você confirma esta modificação?\n1.Sim\n2.Não\n'.format(
    instrumentsList.loc[instrumentsList['id'] == whichInstrument].tipo.iloc[0],
    instrumentsList.loc[instrumentsList['id'] == whichInstrument].preco.iloc[0]
    ))
    if(updateApproved == 1):
      with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
        workbook = writer.book
        try:
          workbook.remove(workbook['instrumentos'])
        except:
            print("Worksheet does not exist")
        finally:
          instrumentsList.to_excel(writer, sheet_name='instrumentos',header=True, index=False)
        writer.save()

      row = loggedUser.index[0]
      if(updateType == 1):
        log.log(loggedUser.loc[row].nome, 'atualizou o tipo do instrumento {} de "{}" para "{}"'.format(whichInstrument,oldType,newType))

      elif(updateType == 2):
        log.log(loggedUser.loc[row].nome, 'atualizou o preço do instrumento {} de "{}" para "{}"'.format(whichInstrument,oldPrice,newPrice))

      elif(updateType == 3):
        log.log(loggedUser.loc[row].nome, 'atualizou o tipo do instrumento {} de "{}" para "{}" e o preço de "{}" para "{}"'.format(whichInstrument,oldType,newType, oldPrice, newPrice))
  else:
    print('Ops, parece que já vendemos este item! Quer editar algo mais?\n')

def deleteInstrument(loggedUser):
  print("Você entrou na deleção de instrumentos.")
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')
  listInstruments(loggedUser, False, False)


  whichInstrument = people.questionUntilReturnsInteger('Qual id do instrumento que você deseja deletar?\n')
  #checar se o id está na lista
  if(len(instrumentsList[instrumentsList['id'] == whichInstrument])>0):
    print(instrumentsList[instrumentsList['id'] == whichInstrument])
    deleteApproved = people.questionUntilReturnsInteger('Você confirma esta deleção?\n1.Sim\n2.Não\n')
    if(deleteApproved == 1):
      filteredInstrumentlist = instrumentsList[instrumentsList['id'] != whichInstrument]
      with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
        workbook = writer.book
        try:
          workbook.remove(workbook['instrumentos'])
        except:
          print("Worksheet does not exist")
        finally:
          filteredInstrumentlist.to_excel(writer, sheet_name='instrumentos',header=True, index=False)
        writer.save()
      row = loggedUser.index[0]
      log.log(loggedUser.loc[row].nome, 'deletou o instrumento {} do tipo {} e preço {}'.format(
      whichInstrument,
      instrumentsList.loc[instrumentsList['id'] == whichInstrument].tipo.iloc[0],
      instrumentsList.loc[instrumentsList['id'] == whichInstrument].preco.iloc[0]
      ))
    else:
      print('Certo, nada foi deletado não!\n')
  else:
    print('Não temos esse instrumento no nosso cadastro!\n')

def searchForInstrument(loggedUser):
  print("Você entrou na busca por instrumentos.")
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')
  searchTerm = input('Procuras por que tipo de instrumento?')
  searchResults = instrumentsList[instrumentsList['tipo'].str.contains(searchTerm)]
  print(searchResults)
  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'buscou na base de dados o termo "{}" e teve {} resultados'.format(
  searchTerm,
  len(searchResults)
  ))

def listSales(loggedUser):
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame

  filteredInstrumentlist = instrumentsList[instrumentsList['vendedor'].notnull()]
  quantity = len(filteredInstrumentlist)

  print('\n===========================================================================\n')
  print(filteredInstrumentlist)
  print('\n===========================================================================\n')
  print('{} vendas ocorreram.'.format(quantity))

  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'listou todas as vendas no banco de dados')

def listSalesInTimeRange(loggedUser):
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame

  print('você entrou na listagem de vendas por período de tempo')
  while True:
    try:

      dateInput = input("Qual o período de tempo inicial? Eu estou esperando um formato 31/12/2020\n")
      initial = dt.datetime.strptime(dateInput, "%d/%m/%Y")
      break
    except KeyboardInterrupt:
      exit()
    except:
      print("Não entendi isso. Me ajuda colocando no formato dd/mm/aaaa?\n")

  while True:
    try:
      dateInput = input("Qual o período de tempo final? Eu estou esperando um formato 31/12/2020\n")
      final = dt.datetime.strptime(dateInput, "%d/%m/%Y")
      break
    except KeyboardInterrupt:
      exit()
    except:
      print("Não entendi isso. Me ajuda colocando no formato dd/mm/aaaa?\n")

  filteredInstrumentlist = instrumentsList[(instrumentsList['vendedor'].notnull()) & (pd.to_datetime(instrumentsList['data da venda']) > initial) & (pd.to_datetime(instrumentsList['data da venda']) < final) ]
  quantity = len(filteredInstrumentlist)

  print('\n===========================================================================\n')
  print(filteredInstrumentlist)
  print('\n===========================================================================\n')
  print('{} vendas ocorreram.'.format(quantity))

  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'listou todas as vendas no banco de dados de {} até {}'.format(initial, final))

def listSalesInTimeAndAgeRange(loggedUser):
  database = pd.ExcelFile('database.xlsx')
  instrumentsList = database.parse('instrumentos')  # read a specific sheet to DataFrame
  usersList = database.parse('pessoas')

  print('você entrou na listagem de vendas por período de tempo e por idade')
  while True:
    try:

      dateInput = input("Qual o período de tempo inicial? Eu estou esperando um formato 31/12/2020\n")
      initial = dt.datetime.strptime(dateInput, "%d/%m/%Y").date()
      break
    except KeyboardInterrupt:
      exit()
    except:
      print("Não entendi isso. Me ajuda colocando no formato dd/mm/aaaa?\n")

  while True:
    try:
      dateInput = input("Qual o período de tempo final? Eu estou esperando um formato 31/12/2020\n")
      final = dt.datetime.strptime(dateInput, "%d/%m/%Y").date()
      break
    except KeyboardInterrupt:
      exit()
    except:
      print("Não entendi isso. Me ajuda colocando no formato dd/mm/aaaa?\n")


  minimum = people.questionUntilReturnsInteger('Qual a idade mínima a ser pesquisada?')
  maximum = people.questionUntilReturnsInteger('Qual a idade máxima a ser pesquisada?')

  listPeopleInRange = usersList.loc[(usersList['idade'] >= minimum) & (usersList['idade'] <= maximum)]
  quantity = len(listPeopleInRange)
  filteredInstrumentlist = instrumentsList[(instrumentsList['vendedor'].notnull()) & (pd.to_datetime(instrumentsList['data da venda']) > initial) & (pd.to_datetime(instrumentsList['data da venda']) < final) & (instrumentsList['vendido a'].isin(listPeopleInRange['nome']))]
  quantity = len(filteredInstrumentlist)

  print('\n===========================================================================\n')
  print(filteredInstrumentlist)
  print('\n===========================================================================\n')
  print('{} vendas ocorreram no período de {} a {}.'.format(quantity, initial, final))

  row = loggedUser.index[0]
  log.log(loggedUser.loc[row].nome, 'listou todas as vendas no banco de dados de {} até {} com usuários de {} aos {} anos de idade'.format(initial, final, minimum, maximum))