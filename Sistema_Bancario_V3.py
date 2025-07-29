from abc import ABC, abstractmethod
from datetime import datetime

def menu():
    menu = """
    ================== MENU =================
    [1] - Novo Cliente
    [2] - Listar Clientes
    [3] - Nova Conta
    [4] - Listar Contas
    [5] - Depositar
    [6] - Sacar
    [7] - Extrato
    [8] - Sair
    =========================================
    """
    return menu

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.conta = []

    def realizar_transacao(self, conta, transacao):
       transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.conta.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, endereco, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class PessoaJuridica(Cliente):
    def __init__(self, razao_social, cnpj, endereco):
        super().__init__(endereco)
        self.razao_social = razao_social
        self.cnpj = cnpj

class Conta:
    def __init__(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero
        self._agencia = "0001"
        self._saldo = 0.0
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, cliente, numero):  
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):    
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        saldo_excedido = valor > saldo
        if saldo_excedido:
            print("\n Saldo insuficiente para realizar o saque solicitado. \n")
        elif valor > 0:
            self._saldo -= valor
            print(f"\n Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("\n Operação não realizada.Valor de saque inválido. \n")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n Depósito de {valor} realizado com sucesso. \n")
        else:
            print("\n Operação não realizada. Valor de depósito inválido. \n")
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite_saque=500, quantidade_saques=3):
        super().__init__(cliente, numero)
        self.limite_saque = limite_saque
        self.quantidade_saques = quantidade_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)])
        excede_limite = valor > self.limite_saque
        excede_saques = numero_saques >= self.quantidade_saques

        if excede_limite:
            print(f"\n Operação não realizada. O valor do saque ({valor}) excede o limite de saque ({self.limite_saque}). \n")
        elif excede_saques:
            print(f"\n Operação não realizada. O número máximo de saques ({self.quantidade_saques}) foi atingido. \n")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"Conta Corrente - Número: {self.numero}, Agência: {self.agencia}, Cliente: {self.cliente.nome if isinstance(self.cliente, PessoaFisica) else self.cliente.razao_social}, Saldo: {self.saldo:.2f}"

class ContaPoupanca(Conta):
    def __init__(self, cliente, numero, rendimento=0.05):
        super().__init__(cliente, numero)
        self.rendimento = rendimento

    def aplicar_rendimento(self):
        self._saldo += self._saldo * self.rendimento
        print(f"\n Rendimento aplicado. Novo saldo: {self.saldo:.2f} \n")
    
    def __str__(self):
        return f"Conta Poupança - Número: {self.numero}, Agência: {self.agencia}, Cliente: {self.cliente.nome if isinstance(self.cliente, PessoaFisica) else self.cliente.razao_social}, Saldo: {self.saldo:.2f}"

class Historico:   
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
        
class Transacao(ABC):   
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass    

class Saque(Transacao):
    def __init__(self, valor, descricao="Saque realizado", data= None):
        self._valor = valor
        self._descricao = descricao
        self._data = data
        if data is None:
            self._data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._data = data

    @property
    def valor(self):
        return self._valor
    
    @property
    def descricao(self):
        return self._descricao

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor, descricao="Depósito realizado",data= None):
        self._valor = valor
        self._descricao = descricao
        if data is None:
            self._data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._data = data

    @property
    def valor(self):
        return self._valor
    
    @property
    def descricao(self):
        return self._descricao

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def depositar(clientes):
    cpf = input("Digite o CPF do cliente (somente números): ")
    cliente = validar_usuario(cpf, clientes)
    if not cliente:
        print("\n## Cliente não encontrado.\n ")
        return
    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(cliente):
    if not cliente.conta:
        print("\n## Cliente não possui conta cadastrada.\n")
        return None
    if len(cliente.conta) > 1:
        print("\n## Cliente possui mais de uma conta. Selecione a conta desejada.")
        for i, conta in enumerate(cliente.conta, start=1):
            print(f"{i}. {conta}")
        escolha = int(input("Digite o número da conta: ")) - 1
        return cliente.conta[escolha] if 0 <= escolha < len(cliente.conta) else None
    return cliente.conta[0]

def sacar(clientes):
    cpf = input("Digite o CPF do usuário (somente números): ")
    cliente = validar_usuario(cpf, clientes)
    if not cliente:
        print("\n## Cliente não encontrado.\n ")
        return
    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Digite o CPF do usuário (somente números): ")
    cliente = validar_usuario(cpf, clientes)
    if not cliente:
        print("\n## Usuário não encontrado.\n ")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=================== EXTRATO ===================\n")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação realizada."
    else:
        for transacao in transacoes:
            extrato += f"Tipo: {transacao.__class__.__name__}, Valor: {transacao.valor:.2f}, Data: {transacao.data}, Descrição: {transacao.descricao}\n"
    print(extrato)
    print(f"Saldo atual:  R$ {conta.saldo:.2f}")

    print("====================== FIM ====================\n")

def validar_usuario(cpf, usuarios):
    cliente_validado = [cliente for cliente in usuarios if cliente.cpf == cpf]
    return cliente_validado[0] if cliente_validado  else None

def criar_clientes(clientes):
    tipo_cliente = input("Digite o tipo de cliente ( 1 para Física ou 2 para Jurídica): ")
    cpf = input("Digite o CPF do usuário (somente números): ")
    cliente = validar_usuario(cpf, clientes)

    if tipo_cliente.lower() == '1':
        nome = input("Digite o nome do usuário: ")
        data_nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ")
        endereco = input("Digite o endereço do usuário: ")
        cliente = PessoaFisica(nome=nome, cpf=cpf, endereco=endereco, data_nascimento=data_nascimento)

    elif tipo_cliente.lower() == '2':
        razao_social = input("Digite a razão social da empresa: ")
        cnpj = input("Digite o CNPJ da empresa (somente números): ")
        endereco = input("Digite o endereço da empresa: ")
        cliente = PessoaJuridica(razao_social=razao_social, cnpj=cnpj, endereco=endereco)
    else:
        print("## Tipo de cliente inválido. Por favor, escolha entre Física ou Jurídica.")
        return None
    
    clientes.append(cliente)
    print(f"\n=> Cliente {nome} cadastrado com sucesso!")
    print("-------------------------------------------------------------------------")

def listar_clientes(clientes):
    if not clientes:
        print("## Não há usuários cadastrados.")
        return

  
    for cliente in clientes:
        print(f"Nome: {cliente.nome}")
        print(f"CPF: {cliente.cpf}")
        print(f"Data de Nascimento: {cliente.data_nascimento}")
        print(f"Endereço: {cliente.endereco}")
        print("---------------------------------------------------")

def criar_conta(clientes, contas, numero):
   
    cpf = input("Digite o CPF do usuário (somente números): ")
    cliente = validar_usuario(cpf, clientes)
    if not cliente:
        print("## Cliente não encontrado. Não foi possivel a abertura da conta.")
        return 
    conta = ContaCorrente.criar_conta(cliente=cliente, numero=numero)
    contas.append(conta)
    cliente.conta.append(conta)
    print(f"\n=> Conta criada com sucesso! Número da conta: {numero}, para o cliente: {cliente.nome if isinstance(cliente, PessoaFisica) else cliente.razao_social}")
    for conta in contas:
        print(str(conta)) 
        print("=" *100)
  
def listar_contas(contas):
     if not contas:
        print("Nenhuma conta cadastrada.")
        return
     for conta in contas:
        print("=" * 100)
        print(str(conta))

def main():
    clientes = []
    contas = []
    
    while True:
        print(menu())
        opcao = input("Escolha uma opção:  ").lower()
        print("\n")
        if opcao == '1':
            criar_clientes(clientes)
        elif opcao == '2':
            listar_clientes(clientes)
        elif opcao == '3':
            numero = len(contas) + 1
            criar_conta(clientes, contas, numero) 
        elif opcao == '4':
            listar_contas(contas)      
        elif opcao == '5':
            depositar(clientes)
        elif opcao == '6':
            sacar(clientes)
        elif opcao == '7':
            exibir_extrato(clientes)     
        elif opcao == '8':
            print("Saindo do sistema...")
            break

main()