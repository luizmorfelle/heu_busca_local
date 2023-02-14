import random
import time
from functools import reduce
import pandas as pd
# m = número de máquinas {10, 20, 50}
# n = qtde tarefas = m^r
# i = tempo de cada tarefa entre 1 e 100
# r = valor randomizado de tarefas {1.5,2.0}

to_export = []


def main(versaoDoArquivo):
    posibilidades_maquina = [10, 20, 50]
    possibilidades_r = [1.5, 2]

    for m in posibilidades_maquina:
        for r in possibilidades_r:
            qtde_tarefas = int(m ** r)
            tarefas = [random.randint(1, 100) for i in range(qtde_tarefas)]
            maquinas = [[] for i in range(m)]
            maquinas[0] = tarefas
            count = 1
            start = time.time()
            while make_move(maquinas):
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
                "%Perturbacao": "null",
                "Makespan": get_makespan(maquinas,indiceMakespan),
                "tempo": end - start
            })

    print(to_export)
    df = pd.DataFrame(to_export, columns=['iteracoes', 'maquinas', 'nTarefas', 'r', '%Perturbacao', 'Makespan', 'tempo'])
    print(df)
    df.to_csv('Primeira_Melhora' + str(versaoDoArquivo) + '.csv', encoding='utf-8', index=False)

def make_move(maquinas):
    maquina_to_remove = get_next_machine(maquinas)
    tarefa_to_move = maquina_to_remove.pop()

    for i in range(len(maquinas)):
        maquina_destino = maquinas[i]

        if maquinas.index(maquina_to_remove) == i:
            continue
        if (get_makespan(maquinas, i) + tarefa_to_move) < get_makespan(maquinas, maquinas.index(
                maquina_to_remove)) + tarefa_to_move:
            maquina_destino.append(tarefa_to_move)
            return True
    maquina_to_remove.append(tarefa_to_move)
    return False


def get_next_machine(maquinas):
    return max(maquinas, key=lambda it: get_makespan(maquinas, maquinas.index(it)))


def print_machines(maquinas):
    for i in range(len(maquinas)):
        print("Máquina: ", i + 1, " - Makespan: ", get_makespan(maquinas, i))
        print(maquinas[i])
        print()
    print("-------------------------")


def get_makespan(maquinas, i):
    return reduce(lambda a, b: a + b, maquinas[i], 0)
