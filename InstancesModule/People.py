from datetime import datetime
from . import Profiles as profiles
#import Profiles as profiles
#import pandas as pd
#Cada pessoa terá um ID,Login, Senha, Nome, Idade, CPF, data de nascimento e por último, perfil.


def createPeople(profileAccess):

  print("Você entrou no cadastro de novos usuários.")
  name = input("Qual o nome a ser cadastrado?\n")
  age = input("Qual a idadedo usuário?\n")
  cpf = input("Qual o CPF do usuário?\n")
  while True:
    try:
      birthDate = input("Qual a data de nascimento do usuário?Eu estou esperando um formato 31/12/2020\n")
      bday = datetime.strptime(birthDate, "%d/%m/%Y")
      break
    except:
      print("Não entendi isso. Me ajuda colocando no formato dd/mm/aaaa?\n")

  
  login = input("Qual o username a ser cadastrado?\n")
  password = input("Qual a senha a ser cadastrada?\n")
  perfil = profileAccess
  print(profileAccess)
  




  