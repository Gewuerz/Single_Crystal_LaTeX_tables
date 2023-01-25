# ----------------------------------------------------------------------------------------------------------------------
# atomic_parameters.py
#
# Creates the atomic parameters table
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
def make_atomic_parameters_table(cif_file, filename_table):
    table_data = []
    atomic_parameters = False

    for line in cif_file.readlines():
        if " _atom_site_aniso_label" in line:
            break
        if atomic_parameters:
            table_data.append(line)
        if " _atom_site_disorder_group" in line:
            atomic_parameters = True

    with open(filename_table, "a") as table_object:
        table_object.write(r"\begin{tabular}{lcS[table-format = 1.5(2)]S[table-format = 1.5(2)]S[table-format = 1.5(2)]"
                           r"c}"
                           + "\n"
                             r"\toprule" + "\n"
                                           r"Atom	&\textit{\textit{Wyckoff}-Lage}	&{\textit{x}} &{\textit{y}}	&{\textit{z}} "
                                           r"& S.O.F.\\" + "\n"
                                                           r"\midrule" + "\n")

        for element in table_data:
            element = element.lstrip(" ")
            row_data = element.split(" ")
            print(row_data)
            table_object.write(
                row_data[0] + " & " + row_data[7] + "$$" + " & " + row_data[2] + " & " + row_data[3] + " & "
                + row_data[4] + " & " + row_data[8] + r" \\" + "\n")

        table_object.write(r"\bottomrule" + "\n"
                                            r"\end{tabular}")

    message = "Your table has been created."
    return message
