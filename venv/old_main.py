# Convert the file to be used to UTF-8 and into a .txt file
# while True:
#     try:
#         crystal_file = input("Enter the name of your .cif-file (with file extension).\n"
#                              "Disclaimer: The tables generated with this program use the package siunitx. \n"
#                              "Enter q to quit: ")
#         if crystal_file == "q":
#             break
#         correct_file_encoding(crystal_file, "cif_Datei_konvertiert.txt", "ISO-8859-1")
#         crystal_file_utf = "cif_Datei_konvertiert.txt"
#         break
#     except FileNotFoundError:
#         print("The file you entered does not exist.")
# Dialogue to choose which table is supposed to be created
# while True:
#     table_decision = input("What kind of table do you wanna create??\n"
#                            "For a single crystal data file enter 1.\n"
#                            "For Atomic parameters enter 2.\n"
#                            "For isotropic parameters enter 3.\n"
#                            "Enter q to quit.")
#     if table_decision == "1":
#         # the single crystal data table needs additional information from the .sum and .lxr file
#         filename_lxr = input("Please enter the name of your .lxr-file (with file extension): ")
#         filename_sum = input("Please enter the name of your.sum-file (with file extension): ")
#         filename_table = input("Please name your .tex-file: ")
#         try:
#             correct_file_encoding(filename_lxr, "lxr_Datei_konvertiert.txt", "ISO-8859-1")
#             correct_file_encoding(filename_sum, "sum_Datei_konvertiert.txt", "ISO-8859-1")
#         except FileNotFoundError:
#             print("Your lxr-file or sum-file do not exist.")
#         try:
#             make_single_crystal_data_table("cif_Datei_konvertiert.txt", "lxr_Datei_konvertiert.txt",
#                                            "sum_Datei_konvertiert.txt", filename_table)
#         except FileNotFoundError:
#             print("One or more of the files you selected do not exist. Check if they have been converted to "
#                   ".txt documents.")
#     elif table_decision == "2":
#         filename_table = input("Please name your .tex-file: ")
#         make_atomic_parameters_table("cif_Datei_konvertiert.txt", filename_table)
#     elif table_decision == "3":
#         filename_table = input("Please name your .tex-file: ")
#         make_anisotropic_displacement_table("cif_Datei_konvertiert.txt", filename_table)
#     # elif table_decision == "4":
#     #     print("4")
#     elif table_decision == "q":
#         break
#     else:
#         print("Please enter a number between 1 and 4.")