import random
from dataclasses import dataclass
from copy import deepcopy

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex"]
HORARIOS = ["08:00", "09:00", "10:00", "11:00"]


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
    Aula("1A", "Português", "Bruno", "Sala 101"),
    Aula("1A", "História", "Carla", "Sala 101"),
    Aula("1A", "Biologia", "Diego", "101"),
    Aula("1A", "Geografia", "Helena", "Sala 101"),
    Aula("1A", "Inglês", "Elisa", "Sala 101"),
    Aula("1A", "Espanhol", "Fernanda", "Sala 101"),
    Aula("1A", "Artes", "Noeli", "Sala 101"),
    Aula("1A", "Filosofia", "Marcio", "Sala 101"),
    Aula("1A", "Sociologia", "Mafalda", "Sala 101"),
    Aula("1A", "Redação", "Relampago Marquinhos", "Sala 101"),

    Aula("1B", "Matemática", "Ana", "Sala 102"),
    Aula("1B", "Português", "Bruno", "Sala 102"),
    Aula("1B", "História", "Carla", "Sala 102"),
    Aula("1B", "Biologia", "Diego", "Sala 202"),
    Aula("1B", "Geografia", "Helena", "Sala 102"),
    Aula("1B", "Inglês", "Elisa", "Sala 102"),
    Aula("1B", "Espanhol", "Fernanda", "Sala 102"),
    Aula("1B", "Artes", "Noeli", "Sala 102"),
    Aula("1B", "Filosofia", "Marcio", "Sala 102"),
    Aula("1B", "Sociologia", "Mafalda", "Sala 102"),
    Aula("1B", "Redação", "Relampago Marquinhos", "Sala 102"),

    Aula("2A", "Matemática", "Ana", "Sala 103"),
    Aula("2A", "Português", "Bruno", "Sala 103"),
    Aula("2A", "História", "Carla", "Sala 103"),
    Aula("2A", "Biologia", "Diego", "Sala 103"),
    Aula("2A", "Geografia", "Helena", "Sala 103"),
    Aula("2A", "Inglês", "Elisa", "Sala 103"),
    Aula("2A", "Espanhol", "Fernanda", "Sala 103"),
    Aula("2A", "Artes", "Noeli", "Sala 103"),
    Aula("2A", "Filosofia", "Marcio", "Sala 103"),
    Aula("2A", "Sociologia", "Mafalda", "Sala 103"),
    Aula("2A", "Redação", "Relampago Marquinhos", "Sala 103"),

    Aula("2B", "Matemática", "Ana", "Sala 104"),
    Aula("2B", "Português", "Bruno", "Sala 104"),
    Aula("2B", "História", "Carla", "Sala 104"),
    Aula("2B", "Biologia", "Diego", "104"),
    Aula("2B", "Geografia", "Helena", "Sala 104"),
    Aula("2B", "Inglês", "Elisa", "Sala 104"),
    Aula("2B", "Espanhol", "Fernanda", "Sala 104"),
    Aula("2B", "Artes", "Noeli", "Sala 104"),
    Aula("2B", "Filosofia", "Marcio", "Sala 104"),
    Aula("2B", "Sociologia", "Mafalda", "Sala 104"),
    Aula("2B", "Redação", "Relampago Marquinhos", "Sala 104"),

    Aula("3A", "Matemática", "Ana", "Sala 105"),
    Aula("3A", "Português", "Bruno", "Sala 105"),
    Aula("3A", "História", "Carla", "Sala 105"),
    Aula("3A", "Biologia", "Diego", "Sala 105"),
    Aula("3A", "Geografia", "Helena", "Sala 105"),
    Aula("3A", "Inglês", "Elisa", "Sala 105"),
    Aula("3A", "Espanhol", "Fernanda", "Sala 105"),
    Aula("3A", "Artes", "Noeli", "Sala 105"),
    Aula("3A", "Filosofia", "Marcio", "Sala 105"),
    Aula("3A", "Sociologia", "Mafalda", "Sala 105"),
    Aula("3A", "Redação", "Relampago Marquinhos", "Sala 105"),
    
]

SLOTS = [(dia, horario) for dia in range(len(DIAS)) for horario in range(len(HORARIOS))]

POPULACAO = 50
GERACOES = 100
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

##            if aula_a.turma == aula_b.turma:
##                total += 1

            if aula_a.professor == aula_b.professor:
                total += 1

##            if aula_a.sala == aula_b.sala:
##                total += 1

    return total


def fitness(individuo):
    """
    Quanto menos conflitos, maior o fitness.
    A solução perfeita possui fitness 1.0.
    """
    return  conflitos(individuo)


def selecao_torneio(populacao):
    """Escolhe o melhor entre indivíduos aleatórios."""
    candidatos = random.sample(populacao, TORNEIO)
    return max(candidatos, key=fitness)


def crossover(pai1, pai2):
    """Crossover de ponto único."""
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
    populacao.sort(key=fitness)
    melhor = populacao[0]
    ##nova.append(deepcopy(melhor))
    nova=populacao[:10]

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
        key=lambda i: (individuo[i][0], individuo[i][1], AULAS[i].turma),
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

    melhor_global = min(populacao, key=fitness)
    historico = []
    geracao_final = 0

    for geracao in range(1, GERACOES + 1):
##        print(' '.join([f'{f}' for f in sorted([fitness(p) for p in populacao])]))
        populacao = gerar_nova_populacao(populacao)

        melhor = min(populacao, key=fitness)
        melhor_conflitos = conflitos(melhor)

        historico.append(melhor_conflitos)
        geracao_final = geracao

        if fitness(melhor) < fitness(melhor_global):
            melhor_global = deepcopy(melhor)

        if melhor_conflitos == 0:
            break

    return melhor_global, historico, geracao_final


if __name__ == "__main__":
    random.seed()  # resultados variam a cada execução
    executar()
