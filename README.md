# Gerador de horários escolares

Este projeto usa um algoritmo genético para montar uma grade semanal para as
turmas cadastradas em `main.py`. A interface é feita com Streamlit e apresenta
a grade, a quantidade de conflitos, o fitness e a evolução do algoritmo.

## Como executar

Instale as dependências, caso ainda não estejam disponíveis:

```bash
python -m pip install streamlit pandas
```

Na pasta do projeto, inicie a interface:

```bash
streamlit run interface.py
```

Clique em **Gerar Grade** para executar o algoritmo e exibir os resultados.
Cada execução pode produzir uma grade diferente, pois a população inicial e
as mutações são aleatórias.

## Como a grade é representada

Cada aula cadastrada é um gene do indivíduo. O gene guarda o dia e o horário
da aula; turma, disciplina, professor e sala são os dados associados a esse
gene.

Atualmente, o cadastro contém 5 turmas com 15 aulas cada (75 aulas no total).
Há 5 dias (`Seg` a `Sex`) e 4 horários (`08:00`, `09:00`, `10:00` e `11:00`),
ou seja, 20 opções de dia e horário para cada aula.

## O que é considerado conflito

Duas aulas entram em conflito quando estão no mesmo dia e horário e:

- pertencem à mesma turma; ou
- são ministradas pelo mesmo professor.

Cada par de aulas em conflito é contado. Se o mesmo par compartilhar turma e
professor, ele contribui com dois conflitos. A sala aparece na grade, mas a
ocupação simultânea de uma sala **ainda não é verificada** pelo algoritmo.

Na tabela, a coluna **Conflito** identifica cada aula envolvida:

- `⚠️ Turma 1A` indica outra aula da turma 1A no mesmo horário;
- `⚠️ Professor Ana` indica outra aula do mesmo professor no mesmo horário;
- os dois avisos podem aparecer juntos;
- `✅ Nenhum` indica que aquela aula não está envolvida em conflito.

Uma aula pode aparecer marcada por causa de outra linha da tabela. Por isso,
os avisos devem ser lidos por dia e horário, em conjunto.

## Como o algoritmo busca uma solução

1. **População inicial:** cria 50 grades aleatórias.
2. **Avaliação:** calcula os conflitos de cada grade e seu fitness:

   ```text
   fitness = 1 / (1 + conflitos)
   ```

   Menos conflitos significam um fitness maior; uma grade sem conflitos tem
   fitness `1.0`.

3. **Seleção:** escolhe 3 indivíduos aleatórios e usa o de maior fitness como
   pai.
4. **Crossover:** combina dois pais em um ponto do cromossomo. Na versão atual,
   o crossover é aplicado sempre; embora exista uma constante
   `TAXA_CROSSOVER = 0.85`, ela ainda não é usada para controlar essa etapa.
5. **Mutação:** cada aula tem 8% de chance de receber um novo dia e horário.
6. **Elitismo:** mantém os 10 melhores indivíduos da população anterior na
   seguinte.

O algoritmo encerra após encontrar uma grade com zero conflitos ou completar
250 gerações. Se não encontrar uma solução sem conflitos nesse limite, a
interface mostra a melhor grade encontrada e avisa quantos conflitos restaram.

## Como ler os resultados

- **Conflitos:** total de conflitos da melhor grade encontrada. É uma contagem
  por par de aulas e por regra violada, não necessariamente o número de linhas
  marcadas.
- **Fitness:** qualidade da melhor grade; quanto mais próximo de `1.0`, menos
  conflitos ela tem.
- **Geração:** quantidade de gerações executadas até o encerramento.
- **Evolução dos Conflitos** e **Evolução do Fitness:** acompanham o melhor
  indivíduo de cada geração registrada.

