#from InstancesModule.People import * as people
import InstancesModule.People as people
import InstancesModule.Instruments as instruments
import InstancesModule.Profiles as profiles
from os import path

#checar arquivos da base de dados
if(not path.exists("database.xlsx")):
  people.DbInit()
  instruments.DbInit()
  

print("Olá, bem-vindo a Loja Maravilha Musical! Você pode:\n1.Realizar login.\n2.Se cadastrar no sistema\n3.Sair do sistema")

while True:
  try:
    loginOption=int(input("Basta digitar a opção desejada!"))
    break
  except:
    print("Não entendi isso. Você digitou apenas o número?")


if(loginOption == 1): 
  loggedUser = people.login()

  #caso seja um cliente
  # if(loggedUser[0]['profile'] == profiles.Profiles.Client):
    



if(loginOption == 2): #para se cadastrar no sistema como cliente independente
  people.createPeople(profiles.Profiles.Pending)

if(loginOption == 3): # para sair do sistema
  print("Obrigado por escolher a Maravilha Musical! Até mais!")
  exit()


