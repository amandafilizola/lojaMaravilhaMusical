from datetime import datetime
from . import Profiles as profiles
import pandas as pd
import LogModule.log as log
import os, sys

#Cada pessoa terá um ID,Login, Senha, Nome, Idade, CPF, data de nascimento e por último, perfil.

def createPeople(profileAccess):

  print("Você entrou no cadastro de novos usuários.")
  name = input("Qual o nome a ser cadastrado?\n")
  age = input("Qual a idade do usuário?\n")
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

  #ler excel para pegar o ultimo id de pessoa gerado
  if(not os.path.exists('database.xlsx')):
    id=1
    excelWriteMode = 'w'
    headerMode = True
  else:
    excelWriteMode = 'a'
    headerMode = False
    database = pd.read_excel('database.xlsx')
    max_value = database['id'].max()
    id = max_value+1

  #UM LINDO DICIONÁRIO QUE SERIA O OBJETO PESSOA!
  personDict = {'id':id, 'login':[login], 'senha':[password], 'nome':[name], 'idade': [age], 'data nascimento':[bday], 'perfil':[profileAccess]}
  frame = pd.DataFrame(personDict)

  #escrever no excel
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode=excelWriteMode) as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
    frame.to_excel(writer, sheet_name='pessoas',startrow=writer.sheets['pessoas'].max_row, header=headerMode)
  writer.save()
  log.log(name, 'se cadastrando pela primeira vez')