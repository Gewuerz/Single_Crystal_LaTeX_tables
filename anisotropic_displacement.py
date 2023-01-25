# ----------------------------------------------------------------------------------------------------------------------
# anisotropic_displacement.py
#
# Creates the anisotropic displacement parameter table
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
from uncertainties import *


def make_anisotropic_displacement_table(cif_file, filename_table):
    lines_cif = cif_file.readlines()

    table_data = []
    atomic_parameters = False

    for line in lines_cif:
        if " _jana_atom_site_ADP_C_label" in line:
            break
        if atomic_parameters:
            table_data.append(line)
        if " _atom_site_aniso_U_23" in line:
            atomic_parameters = True

    table_data = table_data[:-2]

    with open(filename_table, "a") as table_object:
        table_object.write(r"\begin{tabular}{lcS[table-format = -3(2)]S[table-format = -3(2)]S[table-format = -3(2)]"
                           r"S[table-format = -3(2)]S[table-format = -3(2)]S[table-format = -3(2)]"
                           r"S[table-format = -3(2)]}  "
                           + "\n"
                             r"\toprule" + "\n"
                                           r"Atom	&\textit{\textit{Wyckoff}-Lage}	& $U_{11}$	& $U_{22}$	& $U_{33}$	& $U_{12}$	"
                                           r" & $U_{13}$ & $U_{23}$	& $U_{\text{eq}}$ \\" + "\n"
                                                                                               r"\midrule" + "\n")

        for element in table_data:
            element = element.lstrip(" ")
            row_data = element.split(" ")
            if row_data[2] == "0":
                u11 = ufloat_fromstr("0")
            else:
                u11 = ufloat_fromstr(row_data[2]) * 10000.0

            if row_data[3] == "0":
                u22 = ufloat_fromstr("0")
            else:
                u22 = ufloat_fromstr(row_data[3]) * 10000.0

            if row_data[4] == "0":
                u33 = ufloat_fromstr("0")
            else:
                u33 = ufloat_fromstr(row_data[4]) * 10000.0

            if row_data[5] == "0":
                u12 = ufloat_fromstr("0")
            else:
                u12 = ufloat_fromstr(row_data[5]) * 10000.0

            if row_data[6] == "0":
                u13 = ufloat_fromstr("0")
            else:
                u13 = ufloat_fromstr(row_data[6]) * 10000.0

            if row_data[7].strip("\n") == "0":
                u23 = ufloat_fromstr("0")
            else:
                u23 = ufloat_fromstr(row_data[7].strip("\n")) * 10000.0

            # Make sure that std_dev smaller than 1 are correctly handled
            u11 = ufloat_fromstr("{:.0fS}".format(u11))
            if u11.std_dev < 1:
                u11.std_dev = 1
            u22 = ufloat_fromstr("{:.0fS}".format(u22))
            if u22.std_dev < 1:
                u22.std_dev = 1
            u33 = ufloat_fromstr("{:.0fS}".format(u33))
            if u33.std_dev < 1:
                u33.std_dev = 1
            u12 = ufloat_fromstr("{:.0fS}".format(u12))
            if u12.std_dev < 1:
                u12.std_dev = 1
            u13 = ufloat_fromstr("{:.0fS}".format(u13))
            if u13.std_dev < 1:
                u13.std_dev = 1
            u23 = ufloat_fromstr("{:.0fS}".format(u23))
            if u23.std_dev < 1:
                u23.std_dev = 1

            print(row_data)
            table_object.write(row_data[0] + " &   & " + "{:.0fS}".format(u11) + " & " + "{:.0fS}".format(u22) + " & "
                               + "{0:.0fS}".format(u33) + " & " + "{:.0fS}".format(u12) + " & " + "{:.0fS}".format(u13)
                               + " & " + "{:.0fS}".format(u23) + r" \\" + "\n")

        table_object.write(r"\bottomrule" + "\n"
                                            r"\end{tabular}")
    message = "Your table has been created."
    return message
