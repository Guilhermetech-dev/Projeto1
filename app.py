import streamlit as st
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
def salvar_dados(dados):
    with open(ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

alunos = carregar_dados()

st.set_page_config(page_title="Painel de Alunos", layout="centered")
st.title("🎓 Painel de Controle de Alunos")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Aluno", "Listar Alunos", "Buscar Aluno", "Atualizar Pagamento", "📈 Inadimplência", "📤 Exportar para Excel"])

if menu == "Cadastrar Aluno":
    st.subheader("📥 Cadastro de Aluno")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    email = st.text_input("Email")
    curso = st.text_input("Curso")
    matricula = st.text_input("Matrícula")
    valor = st.number_input("Valor da Mensalidade (R$)", min_value=0.0, step=50.0)

    if st.button("Salvar"):
        aluno = {
            'nome': nome,
            'cpf': cpf,
            'email': email,
            'curso': curso,
            'matricula': matricula,
            'mensalidade': {
                'valor': valor,
                'status': 'Em aberto'
            }
        }
        alunos.append(aluno)
        salvar_dados(alunos)
        st.success("✅ Aluno cadastrado com sucesso!")

elif menu == "Listar Alunos":
    st.subheader("📋 Lista de Alunos Cadastrados")
    for aluno in alunos:
        st.write(f"**{aluno['matricula']}** - {aluno['nome']} ({aluno['curso']}) - Mensalidade: {aluno['mensalidade']['status']}")

elif menu == "Buscar Aluno":
    st.subheader("🔎 Buscar Aluno por Matrícula")
    busca = st.text_input("Digite a matrícula")

    if st.button("Buscar"):
        resultado = next((a for a in alunos if a['matricula'] == busca), None)
        if resultado:
            st.write(f"**Nome:** {resultado['nome']}")
            st.write(f"**Curso:** {resultado['curso']}")
            st.write(f"**Email:** {resultado['email']}")
            st.write(f"**Valor da mensalidade:** R${resultado['mensalidade']['valor']}")
            st.write(f"**Status de pagamento:** {resultado['mensalidade']['status']}")
        else:
            st.warning("Aluno não encontrado.")

elif menu == "Atualizar Pagamento":
    st.subheader("💰 Atualizar Status de Pagamento")
    matricula = st.text_input("Digite a matrícula do aluno")

    if st.button("Atualizar para 'Pago'"):
        for aluno in alunos:
            if aluno['matricula'] == matricula:
                aluno['mensalidade']['status'] = 'Pago'
                salvar_dados(alunos)
                st.success("💵 Status atualizado para 'Pago'")
                break
        else:
            st.warning("Aluno não encontrado.")
            
elif menu == "📈 Inadimplência":
    st.subheader("📊 Gráfico de Inadimplência")

    status_count = {"Pago": 0, "Em aberto": 0}
    for aluno in alunos:
        status = aluno['mensalidade']['status']
        if status in status_count:
            status_count[status] += 1

    # Se não houver dados, mostra aviso
    if sum(status_count.values()) == 0:
        st.info("Ainda não há dados de mensalidades para exibir.")
    else:
        import plotly.express as px

        fig = px.pie(
            names=list(status_count.keys()),
            values=list(status_count.values()),
            title="Distribuição de Pagamentos",
            color_discrete_sequence=["red", "green"]
        )
        st.plotly_chart(fig)

elif menu == "📤 Exportar para Excel":
    st.subheader("📄 Exportar Dados dos Alunos")

    if alunos:
        import pandas as pd
        from io import BytesIO

        df = pd.DataFrame(alunos)
        # A coluna "mensalidade" é um dicionário — expandimos em colunas separadas
        mensalidade_df = pd.json_normalize(df['mensalidade'])
        df = df.drop(columns=["mensalidade"])
        df = pd.concat([df, mensalidade_df], axis=1)

        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar Excel",
            data=buffer,
            file_name="alunos_exportados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Nenhum aluno cadastrado ainda.")

