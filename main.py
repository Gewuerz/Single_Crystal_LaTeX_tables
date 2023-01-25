# ----------------------------------------------------------------------------------------------------------------------
# main.py
#
# Program to create LaTeX tables from single crystal data files
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
from button_commands import *
from tkinter import *

cif_file = None
lxr_file = None
sum_file = None


def open_cif_files():
    # Use a file browser to open the .cif-file
    global cif_file
    cif_file = browse_files_cif()
    button_text = cif_file.name.split("/")[-1]
    cif_button.configure(text=button_text)
    return cif_file


def open_lxr_files():
    # Use a file browser to open the .lxr-file
    global lxr_file
    lxr_file = browse_files_lxr_sum()
    button_text = lxr_file.name.split("/")[-1]
    lxr_button.configure(text=button_text)
    return lxr_file


def open_sum_files():
    # Use a file browser to open the .sum-file
    global sum_file
    sum_file = browse_files_lxr_sum()
    button_text = sum_file.name.split("/")[-1]
    sum_button.configure(text=button_text)
    return sum_file


def make_table(cif_file, lxr_file, sum_file, message):
    # Make the selected table
    tex_table_name = entry_table.get()
    option = question_variable.get()
    message.set(table_decision(option, cif_file, lxr_file, sum_file, tex_table_name))
    return


def close_program(cif_file, lxr_file, sum_file):
    # Make sure all files are closed before exiting the program
    close_files(cif_file, lxr_file, sum_file)
    window.destroy()


# Create the window
window = Tk()
window.title("LaTeX-Einkristalltabellen")
window.configure(bg="#F1EEEE")
window.grid_columnconfigure(0, weight=1)
message = StringVar()
message.set("Noch keine Tabelle erzeugt.")
info_message = Label(window, bg="#F1EEEE", width=40, textvariable=message)
info_text_1 = Label(window, font="Calibri 14 bold", bg="#F1EEEE", text="Program zum Erstellen von TeX-Tabellen.\n")
info_text_2 = Label(window, font="Calibri", bg="#F1EEEE", justify=LEFT,
                    text="Für die Erstellung der Strukturverfeinerungsdatentabelle werden alle drei Dateien benötigt!\n"
                         "Die .cif Datei muss mit Jana oder SHELLX97 erstellt worden sein.\n"
                         "Die Wyckoff-Lagen sind in den Dateien nicht vollständig enthalten!\n"
                         "Die erstellten Tabellen benötigen das siunitx-Packet.\n"
                    )

cif_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name der .cif-Datei:")
lxr_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name der .lxr-Datei")
sum_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name .sum-Datei:")

cif_button = Button(window, text=".cif Datei öffnen", bg="#E1E6DF", width=20, command=open_cif_files)
lxr_button = Button(window, text=".lxr Datei öffnen", bg="#E1E6DF", width=20, command=open_lxr_files)
sum_button = Button(window, text=".sum Datei öffnen", bg="#E1E6DF", width=20, command=open_sum_files)

table_tex = Label(window, bg="#F1EEEE", font="Calibri", text="Name für die .tex-Datei (ohne Extension):")
entry_table = Entry(window, bg="white", width=30)

question_text = Label(window, font="Calibri", bg="#F1EEEE", text="Was für eine Tabelle soll erstellt werden?")
question_variable = IntVar()
question_variable.set(1)
r_structure_data = Radiobutton(window, bg="#F1EEEE", text="Daten der Strukturverfeinerung (.cif, .lxr, .sum)",
                               variable=question_variable, value=1)
r_atomic_positions = Radiobutton(window, bg="#F1EEEE", text="Atomlagen (.cif)", variable=question_variable, value=2)
r_displacement_parameters = Radiobutton(window, bg="#F1EEEE", text="Auslenkungsparameter (.cif)",
                                        variable=question_variable, value=3)
make_table_button = Button(window, bg="#E1E6DF", text="Tabelle erstellen", width="20",
                           command=lambda: make_table(cif_file, lxr_file, sum_file, message))
close_window = Button(window, bg="#E1E6DF", text="Schließen", width="15",
                      command=lambda: close_program(cif_file, lxr_file, sum_file))

# Assign a position to each element

info_text_1.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
info_text_2.grid(row=2, column=0, columnspan=3, sticky="W", padx=5, pady=5)
cif_text.grid(row=3, column=0, padx=5, pady=5)
cif_button.grid(row=3, column=1, sticky="W", padx=10, pady=5)

lxr_text.grid(row=4, column=0, padx=5, pady=5)
lxr_button.grid(row=4, column=1, sticky="W", padx=10, pady=5)

sum_text.grid(row=5, column=0, padx=5, pady=5)
sum_button.grid(row=5, column=1, sticky="W", padx=10, pady=5)

question_text.grid(row=6, column=0, padx=5, pady=5)
r_structure_data.grid(row=6, column=1, sticky="WS", padx=10, pady=5)
r_atomic_positions.grid(row=7, column=1, sticky="WS", padx=10, pady=5)
r_displacement_parameters.grid(row=8, column=1, sticky="WS", padx=10, pady=5)

table_tex.grid(row=9, column=0, padx=5, pady=5)

entry_table.grid(row=9, column=1, sticky="WS", padx=10, pady=5)

make_table_button.grid(row=10, column=1, sticky="WS", padx=10, pady=5)

info_message.grid(row=11, column=1, sticky="W", padx=10, pady=5)

close_window.grid(row=13, column=1, sticky="E", padx=5, pady=5)

window.mainloop()
