#!/usr/bin/env python

""" Prototipo del rotulator
Tiene que hacer 2 cosas:
1. Crear dataframe en formato CSV a partir de archivo yaml
2. Crear rotulos en excel a partir de archivo CSV"""

import os
import sys
import yaml
import argparse
import itertools
import random
import labelsCreator


def read_yaml(filepath):
    # Read experiment info from yaml file
    with open(filepath, "r") as f:
        exp_design = yaml.safe_load(f)
    return exp_design


def create_df(exp_design, options):
    """A partir de la definición del experimento en el archivo YAML
    combina los tratamientos, los multiplica por la cantidad de replicas,
    crea los IDs y bloques (si es necesario) y devuelve una lista
    de filas en formato CSV"""

    treatments = exp_design['treatments']
    replicates = exp_design['replicates']
    blocks = exp_design['blocks']
    
    # --- Combinación de niveles ---
    factors = []
    levels = []
    for factor in treatments:
        factors.append(factor)
        levels_of_factor = []
        for level in treatments[factor]:
            levels_of_factor.append(level)
        levels.append(levels_of_factor)

    combinations = list(itertools.product(*levels))
    replicated_combinations = combinations*replicates

    ids = [i for i in range(1,len(replicated_combinations) + 1)]

    # Opcion -r: random ids
    if options.r:
        random.shuffle(ids)        

    comm_sep_factors = ','.join(factors)
    comm_sep_combinations = [','.join(i) for i in replicated_combinations]

    rows = []
    if blocks == True:
        blocks_list = []
        for i in range(1,replicates + 1):
            for b in range(0, len(combinations)):
                blocks_list.append(f'bloque_{i}')

        header = f'id,bloque,{comm_sep_factors}'
        for i,b,c in zip(ids, blocks_list, comm_sep_combinations):
            rows.append(f'{i},{b},{c}')
    else:
        header = f'id,{comm_sep_factors}'
        for i,c in zip(ids, comm_sep_combinations):
            rows.append(f'{i},{c}')

    df_lines = [header]
    df_lines.extend(rows)
    df_lines = [f'{l}\n' for l in df_lines] # Agrego newline al final de cada fila
    return df_lines



def create_rotulos(csv_file):
    exp_name = os.path.basename(csv_file)
    dest_name = labelsCreator.create_labels(csv_file, exp_name)
    print(f'Se creó {dest_name}')



def main():
    parser = argparse.ArgumentParser(prog = 'rotulator',
                                     description = 'Crea un dataframe en formato CSV a partir de un archivo YAML donde se definen los tratamientos, replicas y si se utilizan o no bloques',
                                     epilog = 'fd - 2023')
    parser.add_argument('-r', action='store_true', default=False,
                        help='Random: ordena los IDs al azar')
    parser.add_argument('yaml_input')
    options = parser.parse_args()    

    yaml_file = options.yaml_input
    exp_design = read_yaml(yaml_file)
    df_lines = create_df(exp_design, options)

    sys.stdout.writelines(df_lines)


if __name__ == "__main__":
    main()

