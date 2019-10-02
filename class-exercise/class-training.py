import os.path
import csv
from random import randint
import datetime

path = 'C:/Users/andre.toniati/Documents/TRAINEE KEYRUS2019/py-training/class-exercise/'
path_contas = path + 'contas/'
path_bancos =  path + 'bancos/'

################################################################################################################
# Functions used in class #######################################################################################
#################################################################################################################

def registro_contas_do_banco(banco):
    contas = []
    for conta in banco:
        contas.append(conta['numero'])
    return contas

def cria_id():
    conta_id = ''
    for i in range(4):
        conta_id = conta_id + str(randint(0,9))
    conta_id = conta_id + '-' + str(randint(0,9))
    return conta_id

def le_banco(path):
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf8') as f:
            all_file = csv.reader(f)
            all_file = list(all_file)
        banco = []
        for i in all_file:
            banco.append(list_to_conta(i[0].split('|')))
        return banco
    banco = []
    return banco

def list_to_conta(v):
    conta = {}
    dados_padrao = ['numero', 'titular', 'saldo', 'limite']
    for i in range(4):
        conta[dados_padrao[i]] = str(v[i])
    return conta    

def check_duplicate(contas):
    while True:
        conta_id = cria_id()
        if conta_id not in contas:
            break
    return conta_id

def add_conta_no_banco_e_registro(nome, conta):
    full_path_bancos = path_bancos + nome + '.csv'
    f = open(full_path_bancos, '+a', encoding='utf8')
    registro = "|".join(conta.values())
    f.write(registro + '\n')
    f.close()
    
    full_path_contas = path_contas + nome + '_' + conta['numero'] + '.txt'
    f = open(full_path_contas, '+w', encoding='utf8')

    date_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    header_registro =  """
BANCO: """ + nome + """
NUMERO CONTA: """ + conta['numero'] + """
TITULAR: """ + conta['titular'] + """
CLIENTE DESDE: """ + date_time + """
------------------------------------------------------------------------------------------
LIMITE : """ + conta['limite'] + """
------------------------------------------------------------------------------------------
EXTRATO
------------------------------------------------------------------------------------------ \n
""" + date_time + """ | INÍCIO \t\t\t\t\t\t\t | Saldo : """ + conta['saldo']
    f.write(header_registro + '\n')
    f.close()                  
    
def cria_conta(nome):
    full_path_bancos = path_bancos + nome + '.csv'
    banco = le_banco(full_path_bancos)
    contas = registro_contas_do_banco(banco)
    numero = check_duplicate(contas)
    titular = input('Digite o nome completo do titular:\n')
    saldo = input('Digite o saldo atual da conta\n')
    limite = input('Digite o limite de crédito da conta:\n')
    conta = {"numero": numero,\
             "titular": titular,\
             "saldo": saldo,\
             "limite": limite
            }
    key_cliente = conta['numero'].replace('-','')
    clientes[key_cliente] = Cliente(
                                    conta['numero'],
                                    conta['titular'],
                                    conta['saldo'],
                                    conta['limite'],
                                    nome
                            )
    add_conta_no_banco_e_registro(nome, conta)
    return conta


################################################################################################################
CLASSE # BANCO #################################################################################################
################################################################################################################
class Banco:
    
    def __init__(self, nome):
        self.nome = nome
        Banco.recupera_clientes(nome)
    
    def cria_banco(self, numero_pessoas):
        banco = []
        for i in range(numero_pessoas):
            banco.append(cria_conta(self.nome))
            print('\n')
            print('Conta criada com sucesso!\n')
        return banco    
    
    @staticmethod
    def recupera_clientes(nome):
        global clientes
        clientes = {}
        full_path_bancos = path_bancos + nome + '.csv'
        banco = le_banco(full_path_bancos)
        
        for cliente in banco:
            key_cliente = cliente['numero'].replace('-','')
            clientes[key_cliente] = Cliente(
                                    cliente['numero'],
                                    cliente['titular'],
                                    cliente['saldo'],
                                    cliente['limite'],
                                    nome
                            )
            
    @staticmethod
    #dada uma conta devolve o indice da lista que contem as informações dessa conta ou retorna False caso não exista
    def pega_indice_conta(banco, conta):
        for i in banco:
            if i['numero'] == conta:
                return banco.index(i)
        print('Conta não encontrada!\n')
        return False
          
    def deleta(self):
        full_path_bancos = path_bancos + self.nome + '.csv'
        banco = le_banco(full_path_bancos)
        
        with open(full_path_bancos, 'w', encoding='utf8') as f:
            conta = input('digite o número da conta a ser excluída:\n')
            indice = Banco.pega_indice_conta(banco, conta)
            full_path_contas = path_contas + self.nome + '_' + banco[indice]['numero'] + '.txt'
            if type(indice) == int:
                key_cliente = banco[indice]['numero'].replace('-','')
                del clientes[key_cliente]
                os.remove(full_path_contas)
                banco.remove(banco[indice])
                for pessoa in banco:
                    registro = "|".join(pessoa.values())
                    f.write(registro + '\n')
                print('Conta deletada com sucesso\n')
            else:
                print('Conta não consta nos registros do banco\n')
       
    
    def acrescenta(self):
        novo = cria_conta(self.nome)

#############################################################################################################
# CLASSE # CLIENTE ##########################################################################################
#############################################################################################################

class Cliente:
    def __init__(self, numero, titular, saldo, limite, nome_banco):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        self.limite = limite
        self.nome_banco = nome_banco
    
    #deposito de valor X em uma conta qualquer  
    def deposita(self):
        valor = int(input('Digite o valor do depósito:\n'))
        self.saldo = str(float(self.saldo) + valor)
        
        full_path_bancos = path_bancos + self.nome_banco + '.csv'
        f = open(full_path_bancos, 'r', encoding='utf8')
        all_file = list(csv.reader(f, delimiter ='|'))
        
        for conta in all_file:
            if conta[0] == self.numero:
                conta[2] = self.saldo
        
        f = open(full_path_bancos, '+w', encoding='utf8')
        for conta in all_file:
            registro = "|".join(conta)
            f.write(registro + '\n')  
        
        full_path_contas = path_contas + self.nome_banco + '_' + self.numero + '.txt'
        f = open(full_path_contas, '+a', encoding='utf8')
        
        date_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        registro = """
""" + date_time + """ | DEPÓSITO \t\t\t\t\t\t | Saldo : """ + self.saldo
        
        f.write(registro)
        f.close()
    
    #saca valor X de uma conta qualquer
    def saca(self):
        valor = int(input('Digite o valor do saque:\n'))
        self.saldo = str(float(self.saldo) - valor)
        
        full_path_bancos = path_bancos + self.nome_banco + '.csv'
        f = open(full_path_bancos, 'r', encoding='utf8')
        all_file = list(csv.reader(f, delimiter ='|'))
        
        for conta in all_file:
            if conta[0] == self.numero:
                conta[2] = self.saldo
        
        f = open(full_path_bancos, '+w', encoding='utf8')
        for conta in all_file:
            registro = "|".join(conta)
            f.write(registro + '\n')            
        
        full_path_contas = path_contas + self.nome_banco + '_' + self.numero + '.txt'
        f = open(full_path_contas, '+a', encoding='utf8')
        
        date_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        registro =  """
""" + date_time + """ | SAQUE \t\t\t\t\t\t\t | Saldo : """ + self.saldo
        
        f.write(registro)
        f.close()
    
    #imprime o Extrato de uma conta qualquer 
    def extrato(self):
        full_path_contas = path_contas + self.nome_banco + '_' + self.numero + '.txt'
        f = open(full_path_contas, 'r', encoding='utf8')
        for line in f:
            print(line)
    
##############################################################################################################
# MÉTODOS Banco
# .cria_banco(número_pessoas) / .acrescenta() / .deleta()
##############################################################################################################

banco1 = Banco('itau')

banco1.cria_banco(1)

##############################################################################################################
# objeto cliente é criado automaticamente ####################################################################
##############################################################################################################

# FORMA DO OBJETO cliente
# clientes[x], ONDE x É O NÚMERO DA CONTA TIRANDO O '-', POR EXEMPLO, número: 0987-2, x = 09872
#############################################################################################################
# MÉTODOS Cliente
# .deposita() / .saca() / .extrato()