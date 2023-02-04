import csv
# import docx
# from docx import Document

# Read the .csv file
# filepath = 'outputs/exp1.csv'

PR_ROWS = 56
PR_COLS = 40

def get_longest_string(csv_list):
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
    rotulos = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rotulos = [row for row in reader]

    separador = "\t"

    # Get longest names to format the output
    longest_factor_name, longest_lvl_name = get_longest_string(rotulos)
    longest_row = longest_lvl_name + longest_factor_name + 2 # 2 espacios: uno entre factor/nivel y otro entre rotulos contiguos

    if longest_row < PR_COLS:
        print_columns = 3
    else:
        print_columns = 2

    # Chequear si entran en 3 columnas o si hay que hacerlo en 2
    # TODO

    # Iterar sobre cada fila y armar sus rotulos
    rotulos_list = []
    printed_rows = 0
    rows_per_rotulo = len(rotulos[0].keys())
    while len(rotulos) > 0:
        # Obtengo lista de 3 rotulos
        for i in range(0,print_columns):
            if len(rotulos) != 0:
                rotulos_list.append(rotulos.pop(0))
            
        # Armo lista de strings vacios: uno por cada fila de rotulo
        strlist = ["" for i in range(0,rows_per_rotulo)]
        
        # Para los 3 rotulos armo el string de cada linea
        col_n = 0
        for rotulo in rotulos_list:
            line_number = 0
            if col_n == 0:
                separador = ""
            else:
                separador = " "

            for key,value in rotulo.items():
                # rotulo_str = f'{key:<{longest_factor_name}},{value:>{longest_lvl_name}},'
                rotulo_str = f'{separador}{key},{value},'
                strlist[line_number] = strlist[line_number] + rotulo_str
                # strlist[line_number] = strlist[line_number] + separador + rotulo_str
                line_number += 1
            rotulos_list.remove(rotulo)
            col_n += 1


        for n in strlist:
            print(n)
            printed_rows += 1
        print()


