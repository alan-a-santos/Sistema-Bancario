menu = """
    [d] - Depositar
    [s] - Saque
    [e] - Extrato
    [q] - Sair
"""
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques =3

while True:
    print("Escolha uma das opções disponíveis")
    opcao = input(menu)
    if  opcao == 'd':
        valor= float(input('Digite o valor do depósito: '))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito de R$ {valor:.2f}\n"
            print("Operação efetuada com sucesso")
            print("--------------------------------------------------------\n")
        else:
            print("Operação não realizada, valor informado inválido")
            print("--------------------------------------------------------\n")

    elif opcao == 's':
        if saldo ==0 and extrato=="":
            print("Olá!, Para iniciar a movimentação da conta realize o primeiro depósito!!!")
        else:
            valor = float(input('Digite o valor do saque: '))
            saldo_insulficiente = valor > saldo
            limite_excedido = valor > limite
            limite_saque = numero_saques >= limite_saques
            if saldo_insulficiente:
                print("Operação não realizada. Saldo insulficiente")
                print("--------------------------------------------------------\n")
            elif limite_excedido:
                print("Operação não realizada. Limite de saque diário excedido")
                print("--------------------------------------------------------\n")
            elif limite_saque:
                print("Operação não realizada. Quantidade de saques excedido")
                print("--------------------------------------------------------\n")
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque de R$ {valor:.2f}\n"
                numero_saques +=1
                print("Operação efetuada com sucesso")
                print("--------------------------------------------------------\n")
            else:
                print("Operação não realizada. Valor inofrmado inválido")
                print("--------------------------------------------------------\n")

    elif opcao == 'e':
        print("\n ================ EXTRTATO ===============")
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
        print("========================================\n")       
    elif opcao =="q":
        break
    else:
        print("Operação inválida, seleciona novamente a opção desejada.")
        print("--------------------------------------------------------\n")
