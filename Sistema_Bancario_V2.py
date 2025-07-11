def menu():
    menu = """
    ================== MENU =================
    [d]  - Depositar
    [s]  - Saque
    [e]  - Extrato
    [nc] - Nova Conta
    [lc] - Listar Contas
    [nu] - Novo Usuário
    [lu] - Listar Usuários
    [q]  - Sair
    =========================================
    """
    return menu


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito de R$: \t {valor:.2f}\n"
        print(f"=> Depósito no valor de R$ {valor:.2f} efetuado com sucesso")
    else:
        print("## O valor para realizar o depósito deve ser maior que zero. Operação não realizada.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    saldo_insuficiente = valor > saldo
    limite_excedido = valor > limite
    limite_saque = numero_saques >= limite_saques

    if saldo_insuficiente:
        print("## Operação não realizada. Saldo da conta insuficiente.")
    elif limite_excedido:
        print("## Operação não realizada. Limite de saque diário excedido.")
    elif limite_saque:
        print("## Operação não realizada. Quantidade de saques excedida.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque de R$: \t\t {valor:.2f}\n"
        numero_saques += 1
        print(f"=> Saque no valor de R$ {valor:.2f} efetuado com sucesso")
    else:
        print("## Operação não realizada. Valor informado inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n=================== EXTRATO ===================\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ \t\t {saldo:.2f}\n")
    print("====================== FIM ====================\n")


def validar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
   
    cpf = input("Digite o CPF do usuário (somente números): ")
    usuario_existente = validar_usuario(cpf, usuarios)

    if usuario_existente:
        print("## Usuário já cadastrado.")
        return usuarios

    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ")
    endereco = input("Digite o endereço do usuário: ")

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    print(f"=> Usuário {nome} cadastrado com sucesso!")
    print("-------------------------------------------------------------------------")

    return usuarios
    
def listar_usuarios(usuarios):
    if not usuarios:
        print("## Não há usuários cadastrados.")
        return

  
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("---------------------------------------------------")


def nova_conta(usuarios, contas, numero_conta_atual, agencia):
   
    cpf = input("Digite o CPF do usuário (somente números): ")
    usuario = validar_usuario(cpf, usuarios)

    if not usuario:
        print("## Usuário não encontrado. Cadastre o usuário primeiro.")
        return contas, numero_conta_atual

    numero_conta_atual += 1
    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta_atual,
        "usuario": usuario
    })

    print(f"=> Conta criada com sucesso! Número da conta: {numero_conta_atual} para o usuário {usuario['nome']}")
    return contas, numero_conta_atual


def listar_contas(contas):
    if not contas:
        print("## Não há contas cadastradas.")
        return

   
    for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("---------------------------------------------------")


def iniciar_sistema():
    print("\n\n Bem-vindo ao Sistema Bancário!")

    # Variáveis principais (sem globais)
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    limite_saques = 3
    usuarios = []
    contas = []
    numero_conta_atual = 0
    agencia= "0001"

    while True:
        print(menu())
        opcao = input("Digite a opção desejada: ").lower()

        if opcao == "d":
            print("\n============ DEPÓSITO ================\n")
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            print("\n==============SAQUE ================\n")
            valor = float(input("Digite o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=limite_saques
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            print("\n============== CADASTRO DE USUÁRIO ================\n")
            usuarios = criar_usuario(usuarios)

        elif opcao == "lu":
            print("\n============== LISTA DE USUÁRIOS ================\n")
            listar_usuarios(usuarios)

        elif opcao == "nc":
            print("\n============== NOVA CONTA ================\n")
            contas, numero_conta_atual = nova_conta(usuarios, contas, numero_conta_atual, agencia)

        elif opcao == "lc":
            print("\n============== LISTA DE CONTAS ================\n")
            listar_contas(contas)

        elif opcao == "q":
            print(" Saindo do sistema... Até mais!")
            break

        else:
            print(" Opção inválida. Tente novamente.")


# Iniciar o sistema
iniciar_sistema()


# def menu():
#     menu = """
#     ================== MENU =================
#     [d]  - Depositar
#     [s]  - Saque
#     [e]  - Extrato
#     [nc] - Nova Conta
#     [lc] - Listar Contas
#     [nu] - Novo Usuário
#     [lu] - Listar Usuários
#     [q]  - Sair
#     =========================================
#     """
#     return menu

# def depositar(saldo, valor, extrato, /):
#     if valor > 0:
#         saldo += valor
#         extrato += f"Depósito de R$: \t {valor:.2f}\n"   
#         print(f"=> Depósito no valor de R$ {valor:.2f} efetuado com sucesso")
#     else:
#         print("## O valor para realizar o depósito deve ser maior que zero. Operação não realizada.")
#     return saldo, extrato

# def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
#     saldo_insuficiente = valor > saldo
#     limite_excedido = valor > limite
#     limite_saque = numero_saques >= limite_saques
    
#     if saldo_insuficiente:
#         print("## Operação não realizada. Saldo da conta insuficiente")
#     elif limite_excedido:
#         print("## Operação não realizada. Limite de saque diário excedido")
#     elif limite_saque:
#         print("## Operação não realizada. Quantidade de saques excedida")
#     elif valor > 0:
#         saldo -= valor
#         extrato += f"Saque de R$: \t\t {valor:.2f}\n"
#         numero_saques += 1
#         print(f"=> Saque no valor de R$ {valor:.2f} efetuado com sucesso")
#     else:
#         print("## Operação não realizada. Valor informado inválido")
    
#     return saldo, extrato, numero_saques

# def exibir_extrato(saldo, /, *, extrato):
#     print("\n=================== EXTRATO ===================\n")
#     print("Não foram realizadas movimentações." if not extrato else extrato)
#     print(f"\nSaldo: R$ \t\t {saldo:.2f}\n")
#     print("======================FIM======================\n")

# def validar_usuario(cpf, usuarios):
#     for usuario in usuarios:
#         if usuario['cpf'] == cpf:
#             return usuario
#     return None

# def criar_usuario(usuarios):
#     cpf = input("Digite o CPF do usuário (somente números): ")
#     usuario_existente = validar_usuario(cpf, usuarios)

#     if usuario_existente:
#         print("## Usuário já cadastrado.")
#         return

#     nome = input("Digite o nome do usuário: ")
#     data_nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ")
#     endereco = input("Digite o endereço do usuário: ")

#     usuarios.append({
#         "nome": nome,
#         "cpf": cpf,
#         "data_nascimento": data_nascimento,
#         "endereco": endereco
#     })

#     print(f"Usuário {nome} cadastrado com sucesso!")
#     return usuarios

# def listar_usuarios(usuarios):

#     if not usuarios:
#         print("Não há usuários cadastrados.")
#     for usuario in usuarios:
#         print(f"Nome: {usuario['nome']}")
#         print(f"CPF: {usuario['cpf']}")
#         print(f"Data de Nascimento: {usuario['data_nascimento']}")
#         print(f"Endereço: {usuario['endereco']}")
#         print("-------------------------------------------------------------------------")

# def nova_conta(usuarios, contas, AGENCIA, conta):
  
#     cpf = input("Digite o CPF do usuário (somente números): ")
#     usuario_existente = validar_usuario(cpf, usuarios)

#     if not usuario_existente:
#         print("## Usuário não encontrado. Cadastre o usuário primeiro.")
#         return
    
#     conta +=1
#     numero_conta = conta
#     contas.append({
#         "agencia": AGENCIA,
#         "numero_conta": numero_conta,
#         "usuario": usuario_existente
#     })

#     print(f"Conta criada com sucesso! Número da conta: {numero_conta} para o usuário {usuario_existente['nome']}")

# def listar_contas(contas):
 
#     if not contas:
#         print("Não há contas cadastradas.")
#         return
    
#     for conta in contas:
#         print(f"Agência: {conta['agencia']}")
#         print(f"Número da Conta: {conta['numero_conta']}")
#         print(f"Titular: {conta['usuario']['nome']}")
#         print("-------------------------------------------------------------------------")
    
# def iniciar_sistema():
#     print("\n\nBem-vindo ao Sistema Bancário!")
#     saldo = 0
#     limite = 500
#     extrato = ""
#     numero_saques = 0
#     limite_saques = 3
#     usuarios = []
#     contas = []
#     conta = 0
#     AGENCIA = "0001"

#     while True:
#         print(menu())
#         opcao = input("Digite a opção desejada: ")

#         if opcao == "d":
#             print("\n============DEPÓSITO ================\n")
#             valor = float(input("Digite o valor do depósito: "))
#             saldo, extrato = depositar(saldo, valor, extrato)
         
#         elif opcao == "s":
#             print("\n==============SAQUE ================\n")
#             valor = float(input("Digite o valor do saque: "))
#             saldo, extrato, numero_saques = sacar(
#                 saldo=saldo, 
#                 valor=valor, 
#                 extrato=extrato, 
#                 limite=limite, 
#                 numero_saques=numero_saques, 
#                 limite_saques=limite_saques
#                 )
           
#         elif opcao == "e":
#             print("Operação de Extrato selecionada.\n")
#             exibir_extrato(saldo, extrato = extrato)

#         elif opcao == "nu":
#             print("\n==============CADASTRO DE USUÁRIO================\n")
#             usuario = criar_usuario(usuarios)
           
#         elif opcao == "lu":
#             print("\n==============LISTA DE USUÁRIOS================\n")
#             listar_usuarios(usuarios)
           
#         elif opcao == "nc":
#             print("\n============== NOVA CONTA================\n")
#             nova_conta(usuarios)        

#         elif opcao == "lc":
#             print("\n==============LISTA DE CONTAS================\n")
#             listar_contas(contas)
            
#         elif opcao == "q":
#             print("Saindo do sistema...")
#             break

#         else:
#             print("Opção não existente. Escolha uma opção válida.")

# iniciar_sistema()