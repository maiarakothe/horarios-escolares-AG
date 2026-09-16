import random
from dataclasses import dataclass
from copy import deepcopy

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex"]
HORARIOS = ["08:00", "09:00", "10:00", "13:00", "14:00", "15:00"]


@dataclass(frozen=True)
class Aula:
    turma: str
    disciplina: str
    professor: str
    sala: str


# Cada posição do cromossomo representa uma aula.
# O gene guarda o dia e o horário em que aquela aula foi colocada.
# (30 aulas para 30 slots disponíveis)
AULAS = [
    Aula("1A", "Matemática", "Ana", "Sala 101"),
    Aula("1A", "Português", "Bruno", "Sala 102"),
    Aula("1A", "História", "Carla", "Sala 103"),
    Aula("1A", "Biologia", "Diego", "Lab 1"),
    Aula("1A", "Geografia", "Helena", "Sala 101"),
    Aula("1A", "Inglês", "Elisa", "Sala 102"),

    Aula("1B", "Matemática", "Ana", "Sala 102"),
    Aula("1B", "Português", "Elisa", "Sala 101"),
    Aula("1B", "História", "Carla", "Sala 104"),
    Aula("1B", "Biologia", "Fabio", "Lab 1"),
    Aula("1B", "Geografia", "Helena", "Sala 102"),
    Aula("1B", "Inglês", "Bruno", "Sala 103"),

    Aula("2A", "Matemática", "Gustavo", "Sala 103"),
    Aula("2A", "Português", "Bruno", "Sala 104"),
    Aula("2A", "História", "Helena", "Sala 101"),
    Aula("2A", "Biologia", "Diego", "Lab 1"),
    Aula("2A", "Geografia", "Carla", "Sala 103"),
    Aula("2A", "Inglês", "Ana", "Sala 104"),

    Aula("2B", "Matemática", "Gustavo", "Sala 104"),
    Aula("2B", "Português", "Elisa", "Sala 103"),
    Aula("2B", "História", "Ana", "Sala 102"),
    Aula("2B", "Biologia", "Fabio", "Lab 2"),
    Aula("2B", "Geografia", "Bruno", "Sala 101"),
    Aula("2B", "Inglês", "Carla", "Sala 102"),

    Aula("3A", "Matemática", "Ana", "Sala 101"),
    Aula("3A", "Português", "Bruno", "Sala 102"),
    Aula("3A", "História", "Diego", "Sala 103"),
    Aula("3A", "Biologia", "Helena", "Lab 1"),
    Aula("3A", "Geografia", "Fabio", "Sala 104"),
    Aula("3A", "Inglês", "Gustavo", "Sala 101"),
]

SLOTS = [(dia, horario) for dia in range(len(DIAS))
         for horario in range(len(HORARIOS))]

POPULACAO = 50
GERACOES = 500
TAXA_CROSSOVER = 0.85
TAXA_MUTACAO = 0.08
TORNEIO = 3


def criar_individuo():
    """Cria uma grade aleatória. Cada gene recebe um slot (dia, horário)."""
    return [random.choice(SLOTS) for _ in AULAS]


def conflitos(individuo):
    """
    Conflitos considerados:
    1. mesma turma no mesmo horário;
    2. mesmo professor no mesmo horário;
    3. mesma sala no mesmo horário.
    """
    total = 0

    for i in range(len(AULAS)):
        for j in range(i + 1, len(AULAS)):
            if individuo[i] != individuo[j]:
                continue

            aula_a = AULAS[i]
            aula_b = AULAS[j]

            if aula_a.turma == aula_b.turma:
                total += 1

            if aula_a.professor == aula_b.professor:
                total += 1

            if aula_a.sala == aula_b.sala:
                total += 1

    return total


def fitness(individuo):
    """
    Quanto menos conflitos, maior o fitness.
    A solução perfeita possui fitness 1.0.
    """
    return 1 / (1 + conflitos(individuo))


def selecao_torneio(populacao):
    """Escolhe o melhor entre indivíduos aleatórios."""
    candidatos = random.sample(populacao, TORNEIO)
    return max(candidatos, key=fitness)


def crossover(pai1, pai2):
    """Crossover de ponto único."""
    if random.random() > TAXA_CROSSOVER:
        return deepcopy(pai1), deepcopy(pai2)

    ponto = random.randint(1, len(AULAS) - 1)

    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]

    return filho1, filho2


def mutacao(individuo):
    """Altera alguns genes aleatoriamente."""
    filho = deepcopy(individuo)

    for i in range(len(filho)):
        if random.random() < TAXA_MUTACAO:
            filho[i] = random.choice(SLOTS)

    return filho


def gerar_nova_populacao(populacao):
    nova = []

    # Elitismo: mantém a melhor solução da geração anterior.
    melhor = max(populacao, key=fitness)
    nova.append(deepcopy(melhor))

    while len(nova) < POPULACAO:
        pai1 = selecao_torneio(populacao)
        pai2 = selecao_torneio(populacao)

        filho1, filho2 = crossover(pai1, pai2)

        nova.append(mutacao(filho1))

        if len(nova) < POPULACAO:
            nova.append(mutacao(filho2))

    return nova


def imprimir_grade(individuo):
    print("\n" + "=" * 75)
    print("MELHOR GRADE ENCONTRADA")
    print("=" * 75)

    ordenado = sorted(
        range(len(AULAS)),
        key=lambda i: (individuo[i][0], individuo[i][1], AULAS[i].turma)
    )

    atual = None

    for i in ordenado:
        dia, hora = individuo[i]
        chave = (dia, hora)

        if chave != atual:
            print(f"\n{DIAS[dia]} - {HORARIOS[hora]}")
            print("-" * 75)
            atual = chave

        aula = AULAS[i]
        print(
            f"Turma: {aula.turma:<3} | "
            f"{aula.disciplina:<12} | "
            f"Prof.: {aula.professor:<7} | "
            f"Sala: {aula.sala}"
        )


def executar():
    populacao = [criar_individuo() for _ in range(POPULACAO)]

    melhor_global = max(populacao, key=fitness)
    historico = []
    geracao_final = 0

    for geracao in range(1, GERACOES + 1):
        populacao = gerar_nova_populacao(populacao)

        melhor = max(populacao, key=fitness)
        melhor_conflitos = conflitos(melhor)

        historico.append(melhor_conflitos)
        geracao_final = geracao

        if fitness(melhor) > fitness(melhor_global):
            melhor_global = deepcopy(melhor)

        if melhor_conflitos == 0:
            break

    return melhor_global, historico, geracao_final


if __name__ == "__main__":
    random.seed()  # resultados variam a cada execução
    executar()
