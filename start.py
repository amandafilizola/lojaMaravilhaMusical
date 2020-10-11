#from InstancesModule.People import * as people
import InstancesModule.People as people
import InstancesModule.Instruments as instruments
import InstancesModule.Profiles as profiles
from os import path
import subprocess

#checar arquivos da base de dados, se não existir, rodar função de criação
if(not path.exists('database.xlsx')):
  print('DB init method...')
  people.DbInit()
  instruments.DbInit()

loginOption = people.questionUntilReturnsInteger('Olá, bem-vindo a Loja Maravilha Musical! Você pode:\n1.Realizar login.\n2.Se cadastrar no sistema\n3.Sair do sistema\n')

if(loginOption == 1): 
  loggedUser = people.login()
  print('Basta digitar a opção desejada!')
  row = loggedUser.index[0]

  #CASO SEJA UM CLIENTE
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Client):
    clientActionOption = people.questionUntilReturnsInteger('1.Listar itens à venda.\n2.Comprar item à venda\n3.Sair do sistema\n')
    if(clientActionOption == 1):
      instruments.listInstruments(loggedUser, False, True)
    if(clientActionOption == 2):
      instruments.buyInstrument(loggedUser, False, False)
    if(clientActionOption == 3):
      people.logout()




  #CASO SEJA UM FUNCIONÁRIO
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Employee):
    employeeActionOption = people.questionUntilReturnsInteger('1.Listar itens.\n2.Comprar item à venda\n3.Mostrar estoque atual\n4.Cadastrar novo instrumento\n5.Atualizar instrumento\n6.Deletar instrumento\n7.Buscar por instrumento\n8.Busca por usuário\n9.Criar novo usuário\n')
    if(employeeActionOption == 1):
      instruments.listInstruments(loggedUser, True, True)
    if(employeeActionOption == 2):
      instruments.buyInstrument(loggedUser, True, False)
    if(employeeActionOption == 3):
      instruments.showStock(loggedUser)
    if(employeeActionOption == 4):
      instruments.createInstrument(loggedUser)
    if(employeeActionOption == 5):
      instruments.updateInstrument(loggedUser)
    if(employeeActionOption == 6):
      instruments.deleteInstrument(loggedUser)
    if(employeeActionOption == 7):
      instruments.searchForInstrument(loggedUser)
    if(employeeActionOption == 8):
      people.searchForUsers(loggedUser)
    if(employeeActionOption == 9):
      people.createPeople(profiles.Profiles.Pending, loggedUser)


  #CASO SEJA UM GERENTE
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Manager):
    managerActionOption = people.questionUntilReturnsInteger('1.Aceitar um perfil pendente\n')
    if(managerActionOption == 1):
      people.listPendingProfiles(loggedUser)





elif(loginOption == 2): #para se cadastrar no sistema como cliente independente
  people.createPeople(profiles.Profiles.Pending,loggedUser = None)

elif(loginOption == 3): # para sair do sistema
  people.logout()


