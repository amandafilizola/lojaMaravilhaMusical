#from InstancesModule.People import * as people
import InstancesModule.People as people
import InstancesModule.Profiles as profiles
import pandas as pd

print("Olá, bem-vindo a Loja Maravilha Musical! Você pode:\n1.Realizar login.\n2.Se cadastrar no sistema\n3.Sair do sistema")

while True:
  try:
    loginOption=int(input("Basta digitar a opção desejada!"))
    break
  except:
    print("Não entendi isso. Você digitou apenas o número?")




if(loginOption == 2): #para se cadastrar no sistema como cliente independente
  people.createPeople(profiles.Profiles.Pending)



if(loginOption == 3): # para sair do sistema
  exit()


