#from InstancesModule.People import * as people
import InstancesModule.People as people
import InstancesModule.Instruments as instruments
import InstancesModule.Profiles as profiles
from os import path
import subprocess

#checar arquivos da base de dados, se não existir, rodar função de criação
if(not path.exists("database.xlsx")):
  print("DB init method...")
  people.DbInit()
  instruments.DbInit()

loginOption = people.questionUntilReturnsInteger("Olá, bem-vindo a Loja Maravilha Musical! Você pode:\n1.Realizar login.\n2.Se cadastrar no sistema\n3.Sair do sistema\n")

if(loginOption == 1): 
  loggedUser = people.login()
  print("Basta digitar a opção desejada!")
  row = loggedUser.index[0]

  #CASO SEJA UM CLIENTE
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Client):
    clientActionOption = people.questionUntilReturnsInteger("1.Listar itens à venda.\n2.Comprar item à venda\n3.Sair do sistema\n")
    if(clientActionOption == 1):
      instruments.listInstruments(loggedUser, False)
    if(clientActionOption == 2):
      instruments.buyInstrument(loggedUser, False)
    if(clientActionOption == 3):
      people.logout()




  #CASO SEJA UM FUNCIONÁRIO
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Employee):
    employeeActionOption = people.questionUntilReturnsInteger("1.Listar itens.\n2.Comprar item à venda\n3.Sair do sistema\n4.Mostrar estoque atual")
    if(employeeActionOption == 1):
      instruments.listInstruments(loggedUser, True)
    if(employeeActionOption == 2):
      instruments.buyInstrument(loggedUser, True)
    # if(employeeActionOption == 3):
    #   people.logout()
    if(employeeActionOption == 4):
      instruments.showStock(loggedUser)


  #CASO SEJA UM GERENTE
  #====================================================================================
  if(loggedUser.loc[row].perfil == profiles.Profiles.Manager):
    managerActionOption = people.questionUntilReturnsInteger("1.Aceitar um perfil pendente\n")
    if(managerActionOption == 1):
      people.listPendingProfiles(loggedUser)





elif(loginOption == 2): #para se cadastrar no sistema como cliente independente
  people.createPeople(profiles.Profiles.Pending)

elif(loginOption == 3): # para sair do sistema
  people.logout()


