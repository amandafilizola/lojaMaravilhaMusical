import datetime as dt
import os, sys

def log(user, actionDescription):
  
  #pego a hora atual da ação
  now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
  print("please wait, logging activity...")
  location = os.path.abspath(os.path.dirname(sys.argv[0]))

  #abro o arquivo de logs se ele já existir, senão, o cria
  f = open(os.path.join(location,'log_maravilha_musical.txt'), 'a')

  #escrevo as informações em uma linha do txt com o formato [HORA ATUAL] USUÁRIO --> AÇÃO
  f.write('[{0}] {1} --> {2}\n'.format(now, user, actionDescription))
  f.close()

#descomente as linhas abaixo para testar
#log('Amanda', 'Criando bases de dados')
#log('joao', 'nada')

  