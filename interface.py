import streamlit as st
import pandas as pd


from main import (
    executar,
    AULAS,
    DIAS,
    HORARIOS,
    conflitos,
    detalhar_conflitos,
    fitness,
)

st.set_page_config(page_title="Gerador de Horários", page_icon="📅", layout="wide")


st.title("📅 Gerador de Horários")
st.write("Sistema de geração automática de horários utilizando " "Algoritmo Genético.")

# BOTÃO

if st.button("🚀 Gerar Grade", width="stretch"):

    with st.spinner("Executando algoritmo genético..."):

        melhor_grade, historico, geracao, geracao_fitness = executar()

    st.session_state["melhor_grade"] = melhor_grade
    st.session_state["historico"] = historico
    st.session_state["geracao"] = geracao
    st.session_state["geracao_fitness"] = geracao_fitness


# MOSTRAR RESULTADO

if "melhor_grade" in st.session_state:

    melhor_grade = st.session_state["melhor_grade"]
    historico = st.session_state["historico"]
    geracao = st.session_state["geracao"]
    geracao_fitness = st.session_state["geracao_fitness"]

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
    detalhes_conflitos = detalhar_conflitos(melhor_grade)

    for i, aula in enumerate(AULAS):

        dia, horario = melhor_grade[i]
        conflitos_aula = detalhes_conflitos[i]

        dados.append(
            {
                "Dia": DIAS[dia],
                "Horário": HORARIOS[horario],
                "Turma": aula.turma,
                "Disciplina": aula.disciplina,
                "Professor": aula.professor,
                "Sala": aula.sala,
                "Conflito": (
                    f"⚠️ {', '.join(conflitos_aula)}" if conflitos_aula else "✅ Nenhum"
                ),
            }
        )

    df = pd.DataFrame(dados)

    df["Dia"] = pd.Categorical(df["Dia"], categories=DIAS, ordered=True)

    df = df.sort_values(["Dia", "Horário", "Turma"])

    st.dataframe(df, width="stretch", hide_index=True)

    # EVOLUÇÃO

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📉 Evolução dos Conflitos")

        grafico_conflitos = pd.DataFrame(
            {"Geração": range(1, len(historico) + 1), "Conflitos": historico}
        )

        st.line_chart(grafico_conflitos, x="Geração", y="Conflitos")

    with col2:
        st.subheader("📈 Evolução do Fitness")

        grafico_fitness = pd.DataFrame(
            {"Geração": range(1, len(geracao_fitness) + 1), "Fitness": geracao_fitness}
        )

        st.line_chart(grafico_fitness, x="Geração", y="Fitness")

    # RESULTADO

    if total_conflitos == 0:

        st.success("✅ Solução sem conflitos encontrada!")

    else:

        st.warning(f"⚠️ A solução possui {total_conflitos} conflito(s).")
