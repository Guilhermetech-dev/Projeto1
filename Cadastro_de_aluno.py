import json
import os

ARQUIVO = "alunos.json"

# Carrega os alunos salvos no arquivo
def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    return []

# Salva os dados no arquivo
def salvar_dados():
    with open(ARQUIVO, 'w') as f:
        json.dump(alunos, f, indent=4)

alunos = carregar_dados()

def cadastrar_aluno():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    curso = input("Curso: ")
    matricula = input("Matrícula: ")
    valor_mensalidade = float(input("Valor da mensalidade: "))

    aluno = {
        'nome': nome,
        'cpf': cpf,
        'email': email,
        'curso': curso,
        'matricula': matricula,
        'mensalidade': {
            'valor': valor_mensalidade,
            'status': 'Em aberto'
        }
    }

    alunos.append(aluno)
    salvar_dados()
    print("\nAluno cadastrado com sucesso!\n")

def listar_alunos():
    for aluno in alunos:
        print(f"{aluno['matricula']} - {aluno['nome']} ({aluno['curso']}) - {aluno['mensalidade']['status']}")

def buscar_aluno():
    matricula = input("Digite a matrícula do aluno: ")
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            print(f"\nNome: {aluno['nome']}\nCurso: {aluno['curso']}\nMensalidade: R${aluno['mensalidade']['valor']} - {aluno['mensalidade']['status']}\n")
            return
    print("Aluno não encontrado.")

def atualizar_pagamento():
    matricula = input("Digite a matrícula do aluno: ")
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            aluno['mensalidade']['status'] = 'Pago'
            salvar_dados()
            print("Status de pagamento atualizado para 'Pago'.")
            return
    print("Aluno não encontrado.")

def menu():
    while True:
        print("\n1. Cadastrar aluno\n2. Listar alunos\n3. Buscar aluno\n4. Atualizar pagamento\n5. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            buscar_aluno()
        elif opcao == '4':
            atualizar_pagamento()
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

menu()

