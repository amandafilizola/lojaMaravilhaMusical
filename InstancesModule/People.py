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
    database = pd.read_excel('database.xlsx', 'pessoas')
    max_value = database['id'].max()
    id = max_value+1

  #UM LINDO DICIONÁRIO QUE SERIA O OBJETO PESSOA!
  personDict = {'id':id, 'login':[login], 'senha':[password], 'nome':[name], 'idade': [age], 'data nascimento':[bday], 'perfil':[profileAccess]}
  frame = pd.DataFrame(personDict)

  #escrever no excel
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode=excelWriteMode) as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
    frame.to_excel(writer, sheet_name='pessoas',startrow=writer.sheets['pessoas'].max_row, header=headerMode, index=False)
  writer.save()
  print('Seu cadastro agora será analisado pela nossa equipe! Basta esperar o aceite de seu cadastro!\n')
  log.log(name, 'se cadastrando pela primeira vez')

def DbInit():
  personDict = {'id':1, 'login':['admin'], 'senha':['admin'], 'nome':['admin'], 'idade': [0], 'data nascimento':[0], 'perfil':[profiles.Profiles.Manager]}
  frame = pd.DataFrame(personDict)
  #escrever no excel
  with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='w') as writer:
    #OLHA AQUI UM LIST COMPREHENSION!!
    frame.to_excel(writer, sheet_name='pessoas',header=True, index=False)
  writer.save()
  log.log('Admin', 'inicializando o banco de dados')

def login():
  if(os.path.exists('database.xlsx')):
    tryLogin = input("login?\n")
    tryPassword = input("senha?\n")

    database = pd.ExcelFile('database.xlsx')
    usersList = database.parse('pessoas')  # read a specific sheet to DataFrame
    loggedUser = usersList.loc[(usersList['login'] == tryLogin) & (usersList['senha']== tryPassword)]
    if(len(loggedUser)==1):
      nome = loggedUser.iloc[0]['nome']
      print('Login realizado, bem vindo {}!'.format(nome))
      log.log(nome, 'logou no sistema')
      return loggedUser
    else:
      print('Não encontrei seus dados no nosso cadastro. Talvez voce tenha errado a senha?\n')
      return ''

def listPendingProfiles(loggedUser):
  if(os.path.exists('database.xlsx')):
    database = pd.ExcelFile('database.xlsx')
    usersList = database.parse('pessoas')  # read a specific sheet to DataFrame
    listPendingUsers = usersList.loc[usersList['perfil'] == profiles.Profiles.Pending]
    if(len(listPendingUsers)>0):
      approve = True
      while approve:
        database = pd.ExcelFile('database.xlsx')
        usersList = database.parse('pessoas')  # read a specific sheet to DataFrame
        listPendingUsers = usersList.loc[usersList['perfil'] == profiles.Profiles.Pending]
        print('\n===========================================================================\n')
        print(listPendingUsers)
        print('\n===========================================================================\n')
        approve = questionUntilReturnsInteger("voce deseja aprovar algum cadastro?\n1.Sim\n2.Não\n")
        if(approve == 1):
          approveUserId = questionUntilReturnsInteger("qual o id da pessoa, de acordo com a tabela, que você deseja atualizar?")
          newProfile = questionUntilReturnsInteger("Esta pessoa deverá receber que tipo de perfil de cadastro?\n1.Cliente\n2.Funcionário\n3.Gerente\n")
          profileArray = ['cliente', 'funcionário', 'gerente']
          print("certo, iremos colocá-lo como {}\n\n".format(profileArray[newProfile-1]))
          if(newProfile==1):
            usersList.loc[usersList['id']==approveUserId,'perfil'] = profiles.Profiles.Client
          elif(newProfile==2):
            usersList.loc[usersList['id']==approveUserId,'perfil'] = profiles.Profiles.Employee
          elif(newProfile==3):
            usersList.loc[usersList['id']==approveUserId,'perfil'] = profiles.Profiles.Manager

          with pd.ExcelWriter('database.xlsx', engine='openpyxl', mode='a') as writer:
            workbook = writer.book
            try:
              workbook.remove(workbook['pessoas'])
            except:
                print("Worksheet does not exist")
            finally:
              usersList.to_excel(writer, sheet_name='pessoas',header=True, index=False)
            writer.save()
          log.log(loggedUser.loc[0].nome, 'aprovando o usuário {} para o perfil {}'.format(usersList.loc[usersList['id']==approveUserId].nome.iloc[0],profileArray[newProfile-1]))

        else:
          approve = False
    else:
      print('Não temos cadastros pendentes!')


#função para rejeitar as entradas do usuário caso digite errado.
def questionUntilReturnsInteger(string):
  while True:
    try:
      result = int(input(string))
      break
    except:
      print("Não entendi isso. Você digitou apenas o número?\n")
  return result