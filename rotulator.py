#!/usr/bin/env python3

import os
import sys
import yaml
import argparse
import itertools
import random
import csv


template = """
# Config file del experimento.
# En este archivo YAML se define el diseño experimental: 
# los factores, sus niveles, el numero de réplicas y si se utilizan o no bloques.
#
# Hay 3 parametros:
#
# 1. Tratamientos
#   Se describe cada factor y sus niveles como en este ejemplo.
#   Notese que los factores estan identados y que sus niveles tienen un nivel mas de identación.
#
#   tratamientos:
#     factor1:
#       - nivel1
#       - nivel2
#       - nivel3
#     factor2:
#       - nivel1
#       - nivel2
#     etc...
#
# 2. Replicas
#   El número de replicas.
#
# 3. Bloques
#   True si se usan bloques.
#   False si no se usan bloques.
#

treatments:
  endofito:
    - e+
    - e-
  corte_raices:
    - control
    - con_corte
  diloboderus:
    - h+
    - h-

replicates: 8

blocks: True
"""

def read_yaml(filepath):
    # Read experiment info from yaml file
    with open(filepath, "r") as f:
        exp_design = yaml.safe_load(f)
    return exp_design


def create_df(exp_design, options, random_ids):
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
    if random_ids:
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


def get_longest_string(csv_list):
    """Funcion accesoria de create_labels.
    Buscar las palabras mas largas: el factor y el nivel mas largo posible"""
    longest_factor_name = 0
    longest_lvl_name = 0
    for i in csv_list:
        for key,value in i.items():
            if len(key) > longest_factor_name:
                longest_factor_name = len(key)
            if len(value) > longest_lvl_name:
                longest_lvl_name = len(value)

    return longest_factor_name, longest_lvl_name


def create_labels(csv_file):
    A4_COLS = 80                # Un word con letra tamaño 12 banca 80 caracteres. Habria que sacar cuentas con espacios y demas

    rotulos = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rotulos = [row for row in reader]

    separador = "\t"
    
    # Get longest names to format the output
    longest_factor_name, longest_lvl_name = get_longest_string(rotulos)
    longest_row = longest_lvl_name + longest_factor_name + 2 # 2 espacios: uno entre factor/nivel y otro entre rotulos contiguos

    if longest_row < A4_COLS:
        print_columns = 3
    else:
        print_columns = 2

    # 
    # TODO!!! Chequear si entran en 3 columnas o si hay que hacerlo en 2
    # 

    # Iterar sobre cada fila y armar sus rotulos
    rotulos_list = []
    printed_rows = 0
    rows_per_rotulo = len(rotulos[0].keys()) # Keys porque es un diccionario

    while len(rotulos) > 0:
        # Obtengo lista de 3 rotulos
        for i in range(0,print_columns):
            if len(rotulos) != 0:
                rotulos_list.append(rotulos.pop(0))

        # Armo lista de strings vacios: uno por cada fila de rotulo
        strlist = ["" for i in range(0,rows_per_rotulo)]
        
        # Para los 3 rotulos armo el string de cada linea
        col_n = 0
        for i in range(0,3):
            if len(rotulos_list) == 0: # Chequear que aun haya elementos. Puede ser que el numero de unidades exp no sea multiplo de 3
                break
            rotulo = rotulos_list.pop(0)
            line_number = 0
            if col_n == 0:      # Si es la primera columna de rotulos no tiene que dejar espacio
                separador = ""
            else:
                separador = "  "

            for key,value in rotulo.items():
                rotulo_str = f'{key:<{longest_factor_name}},{value:>{longest_lvl_name}},'
                # rotulo_str = f'{separador}{key},{value},'
                # strlist[line_number] = strlist[line_number] + rotulo_str
                strlist[line_number] = strlist[line_number] + separador + rotulo_str
                line_number += 1
            col_n += 1

        for i in strlist:
            sys.stdout.write(i + "\n")
            printed_rows += 1
        sys.stdout.write("\n")


def main():
    parser = argparse.ArgumentParser(prog = 'rotulator',
                                     description = '(1) Crea un dataframe en formato CSV a partir de un archivo YAML donde se define el experimento (2) Crea rotulos para cada ID de un dataframe')

    parser.add_argument('-t', '--template', action='store_true', default=False,
                        help='crea una plantilla YAML para cargar el diseño de un experimento.')
    parser.add_argument('-r', '--random', action='store_true', default=False,
                        help='Opcion para usar con -d. Ordena IDs al azar.') 
    parser.add_argument('-d', '--dataframe', action='store', dest="yaml_file", metavar="template",
                        help="Create dataframe. Crea un CSV a partir del archivo YAML pasado como argumento")
    parser.add_argument('-l', '--labels', action='store', dest="csv_file", metavar="dataframe",
                        help="Create labels: arma rotulos para macetas a partir de un archivo CSV")


    options = parser.parse_args()    

    # --new-template
    if options.template:
        with open("template.yaml", "w") as f:
            f.write(template)
        sys.stdout.write("Se creo template.\n")

    # --template-to-dataframe
    elif options.yaml_file is not None:
        exp_design = read_yaml(options.yaml_file)
        df_lines = create_df(exp_design, options, options.random)
        sys.stdout.writelines(df_lines)
        
    # --dataframe-to-labels
    elif options.csv_file is not None:
        create_labels(options.csv_file)

    else:
        parser.print_help()

    exit(0)


if __name__ == "__main__":
    main()

