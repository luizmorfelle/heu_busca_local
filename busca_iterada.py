import random
import time
from functools import reduce
import pandas as pd
to_export = []

def main(versaoDoArquivo):
    posibilidades_maquina = [10, 20, 50]
    possibilidades_r = [1.5, 2]
    intensidades_perturbacao = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    for m in posibilidades_maquina:
        for r in possibilidades_r:
            for per in intensidades_perturbacao:
                qtde_tarefas = int(m ** r)
                tarefas = [random.randint(1, 100) for i in range(qtde_tarefas)]
                maquinas = [[] for i in range(m)]
                maquinas[0] = tarefas
                count = 1
                start = time.time()
                sem_melhora = 0
                while sem_melhora < 1000:
                    while make_move(maquinas):
                        count += 1
                    move_random_tasks(maquinas,per)
                    sem_melhora += 1
                    count += 1

                end = time.time()
                print_machines(maquinas)

                maquinaComMaiorMakespan = get_next_machine(maquinas)
                indiceMakespan = maquinas.index(maquinaComMaiorMakespan)
                to_export.append({
                    "iteracoes": count,
                    "maquinas": m,
                    "nTarefas": qtde_tarefas,
                    "r": r,
                    "%Perturbacao": per,
                    "Makespan": get_makespan(maquinas,indiceMakespan),
                    "tempo": end - start
                })
    print(to_export)
    df = pd.DataFrame(to_export, columns=['iteracoes', 'maquinas', 'nTarefas', 'r', '%Perturbacao', 'Makespan','tempo'])
    print(df)
    df.to_csv('Busca_Iterada' + str(versaoDoArquivo) + '.csv', encoding='utf-8', index=False)
def move_random_tasks(maquinas, per):
    maquina_to_remove = get_next_machine(maquinas)
    tarefas_sorteadas = random.sample(maquina_to_remove, int(len(maquina_to_remove) * per))
    for tarefa_to_move in tarefas_sorteadas:
        for i in range(len(maquinas)):
            maquina_destino = maquinas[i]
            if maquinas.index(maquina_to_remove) == i:
                continue
            if (get_makespan(maquinas, i) + tarefa_to_move) < get_makespan(maquinas, maquinas.index(maquina_to_remove)):
                maquina_to_remove.remove(tarefa_to_move)
                maquina_destino.append(tarefa_to_move)
                break

def make_move(maquinas):
    maquina_to_remove = get_next_machine(maquinas)
    tarefa_to_move = maquina_to_remove.pop()

    for i in range(len(maquinas)):
        maquina_destino = maquinas[i]

        if maquinas.index(maquina_to_remove) == i:
            continue
        if (get_makespan(maquinas, i) + tarefa_to_move) < get_makespan(maquinas, maquinas.index(maquina_to_remove)) + tarefa_to_move:
            maquina_destino.append(tarefa_to_move)
            return True
    maquina_to_remove.append(tarefa_to_move)
    return False

def get_next_machine(maquinas):
    return max(maquinas, key=lambda it: get_makespan(maquinas, maquinas.index(it)))


def print_machines(maquinas):
    for i in range(len(maquinas)):
        print("Maquina: ", i + 1, " - Makespan: ", get_makespan(maquinas, i))
        print(maquinas[i])
        print()
    print("-------------------------")


def get_makespan(maquinas, i):
    return reduce(lambda a, b: a + b, maquinas[i], 0)
