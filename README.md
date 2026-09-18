
# Algoritmo Genético - Horários Escolares


## 1. Problema

O objetivo é gerar uma grade de horários escolares alocando turmas, professores e salas em diferentes períodos, buscando eliminar conflitos.

Os conflitos considerados são:

- uma mesma turma em duas aulas no mesmo horário;
- um mesmo professor em duas aulas no mesmo horário;
- uma mesma sala ocupada por duas aulas no mesmo horário.

O projeto foi modelado como um problema de otimização por Algoritmo Genético.

## 2. Representação do indivíduo

Um indivíduo representa uma grade completa.

Cada gene representa uma aula e armazena:

```text
(dia, horário)
```

Exemplo:

```text
Gene 1 -> (Segunda, 08:00)
Gene 2 -> (Quarta, 10:00)
Gene 3 -> (Sexta, 14:00)
```

As informações de turma, disciplina, professor e sala pertencem à aula
correspondente ao gene.

## 3. População inicial

São criados 50 indivíduos.

Cada indivíduo recebe posições aleatórias entre os 30 horários disponíveis
(5 dias × 6 horários).

## 4. Função de fitness

O objetivo é minimizar o número de conflitos.

A função utilizada é:

```text
fitness = 1 / (1 + conflitos)
```

Quanto menor o número de conflitos, maior o fitness.

Uma solução sem conflitos possui:

```text
fitness = 1.0
```

## 5. Seleção

Foi utilizada **seleção por torneio**.

Três indivíduos são escolhidos aleatoriamente e aquele que possui maior
fitness é selecionado para reprodução.

## 6. Crossover

Foi utilizado **crossover de ponto único**.

Um ponto aleatório divide os cromossomos dos pais e os filhos recebem
partes de cada um.

Taxa utilizada:

```text
85%
```

## 7. Mutação

Na mutação, cada gene possui uma pequena probabilidade de receber um novo
horário aleatório.

Taxa utilizada:

```text
8%
```

## 8. Elitismo

O melhor indivíduo de cada geração é mantido na próxima geração.

Isso evita que uma boa solução seja perdida durante o processo evolutivo.

## 9. Critério de parada

O algoritmo termina quando:

1. encontra uma solução com zero conflitos; ou
2. atinge 500 gerações.


## Exemplo de interpretação

No início, as grades são aleatórias e normalmente apresentam vários
conflitos.

Durante as gerações, indivíduos com menos conflitos tendem a ser
selecionados para reprodução. O crossover e a mutação geram novas grades,
e o fitness permite identificar quais são melhores.

O objetivo final é chegar a:

```text
0 conflitos
```

Nesse caso, a grade encontrada atende às restrições consideradas pelo
sistema.
