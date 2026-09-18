import streamlit as st
import pandas as pd

from main import executar, AULAS, DIAS, HORARIOS, conflitos, fitness

st.set_page_config(page_title="Gerador de Horários", page_icon="📅", layout="wide")


st.title("📅 Gerador de Horários")
st.write("Sistema de geração automática de horários utilizando " "Algoritmo Genético.")

# BOTÃO

if st.button("🚀 Gerar Grade", use_container_width=True):

    with st.spinner("Executando algoritmo genético..."):

        melhor_grade, historico, geracao = executar()

    st.session_state["melhor_grade"] = melhor_grade
    st.session_state["historico"] = historico
    st.session_state["geracao"] = geracao

# MOSTRAR RESULTADO

if "melhor_grade" in st.session_state:

    melhor_grade = st.session_state["melhor_grade"]
    historico = st.session_state["historico"]
    geracao = st.session_state["geracao"]

    total_conflitos = conflitos(melhor_grade)
    resultado_fitness = fitness(melhor_grade)

    # INDICADORES

    col1, col2, col3 = st.columns(3)

    col1.metric("Conflitos", total_conflitos)

    col2.metric("Fitness", f"{resultado_fitness:.4f}")

    col3.metric("Geração", geracao)

    st.divider()

    # GRADE

    st.subheader("📅 Grade de Horários")

    dados = []

    for i, aula in enumerate(AULAS):

        dia, horario = melhor_grade[i]

        dados.append(
            {
                "Dia": DIAS[dia],
                "Horário": HORARIOS[horario],
                "Turma": aula.turma,
                "Disciplina": aula.disciplina,
                "Professor": aula.professor,
                "Sala": aula.sala,
            }
        )

    df = pd.DataFrame(dados)

    df = df.sort_values(["Dia", "Horário", "Turma"])

    st.dataframe(df, use_container_width=True, hide_index=True)

    # EVOLUÇÃO

    st.subheader("📈 Evolução do Algoritmo")

    grafico = pd.DataFrame(
        {"Geração": range(1, len(historico) + 1), "Conflitos": historico}
    )

    st.line_chart(grafico, x="Geração", y="Conflitos")

    # RESULTADO

    if total_conflitos == 0:

        st.success("✅ Solução sem conflitos encontrada!")

    else:

        st.warning(f"⚠️ A solução possui {total_conflitos} conflito(s).")
