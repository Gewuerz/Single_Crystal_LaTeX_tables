# ----------------------------------------------------------------------------------------------------------------------
# main.py
#
# Program to create LaTeX tables from single crystal data files
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
from tkinter import *

from button_commands import *

cif_file = None
lxr_file = None
sum_file = None
save_path = ""

def open_all_files():
    global cif_file
    global lxr_file
    global sum_file
    global save_path
    filelist = browse_files_all()
    for file in filelist:
        if ".cif" in file:
            cif_file = open(file, "r", encoding="utf-8")
            cif_text.configure(text=cif_file.name.split("/")[-1])
            #cif_button.configure(text=cif_file.name.split("/")[-1])
        if ".lxr" in file:
            lxr_file = open(file, "r", encoding="windows-1254")
            lxr_text.configure(text=lxr_file.name.split("/")[-1])
            #lxr_button.configure(text=lxr_file.name.split("/")[-1])
        if ".sum" in file:
            sum_file = open(file, "r", encoding="windows-1254")
            sum_text.configure(text=sum_file.name.split("/")[-1])
            #sum_button.configure(text=sum_file.name.split("/")[-1])
    # set a default savepath
    save_path = cif_file.name + ".tex"
    return


def make_table(cif_file, lxr_file, sum_file, save_path, message):
    # Make the selected table
    option = question_variable.get()
    message.set(table_decision(option, cif_file, lxr_file, sum_file, save_path))
    return

def save_table():
    global save_path
    save_path = select_save_path()
    save_table_button.configure(text=save_path.split("/")[-1])
    return

def close_program(cif_file, lxr_file, sum_file):
    # Make sure all files are closed before exiting the program
    close_files(cif_file, lxr_file, sum_file)
    window.destroy()

# Create the window
window = Tk()
window.resizable(width=False, height=False)
window.title("LaTeX-Einkristalltabellen")
window.configure(bg="#F1EEEE")
window.grid_columnconfigure(0, weight=1)
message = StringVar()
message.set("Noch keine Tabelle erzeugt.")
info_message = Label(window, bg="#F1EEEE", width=30, textvariable=message)
info_text_1 = Label(window, font="Calibri 14 bold", bg="#F1EEEE", text="Program zum Erstellen von TeX-Tabellen.\n")
info_text_2 = Label(window, font="Calibri", bg="#F1EEEE",
                    text="Für die Erstellung der Strukturverfeinerungsdatentabelle werden alle drei Dateien benötigt!\n"
                         "Die .cif Datei muss mit JANA oder SHELLXL erstellt worden sein.\n"
                         "Die Wyckoff-Lagen sind in den Dateien nicht vollständig enthalten!\n"
                         "Die erstellten Tabellen benötigen das siunitx-Packet.\n"
                    )

cif_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name der .cif-Datei")
lxr_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name der .lxr-Datei")
sum_text = Label(window, font="Calibri", bg="#F1EEEE", text="Name .sum-Datei")
all_text = Label(window, font="Calibri", bg="#F1EEEE",
 text="Es können sowohl einzelne, \n als auch alle drei Dateien \n auf einmal geöffnet werden.")

all_button = Button(window, text="Dateien öffnen", bg="#C4D4C4", width=20, command=open_all_files)

table_tex = Label(window, bg="#F1EEEE", font="Calibri",
                  text="Name für die .tex-Datei (ohne Extension)")
entry_table = Entry(window, bg="white", width=30)

question_text = Label(window, font="Calibri", bg="#F1EEEE", text="Was für eine Tabelle soll erstellt werden?")
question_variable = IntVar()
question_variable.set(1)

r_structure_data = Radiobutton(window, bg="#F1EEEE", justify=LEFT,
                               text="Daten der Strukturverfeinerung \n (.cif, .lxr, .sum)",
                               variable=question_variable, value=1)
r_atomic_positions = Radiobutton(window, bg="#F1EEEE", text="Atomlagen (.cif)", variable=question_variable, value=2)
r_displacement_parameters = Radiobutton(window, bg="#F1EEEE", text="Auslenkungsparameter (.cif)",
                                        variable=question_variable, value=3)

save_table_button = Button(window, bg="#E1E6DF", text="Tabelle speichern unter", width="20",
                           command=save_table)
make_table_button = Button(window, bg="#E1E6DF", text="Tabelle erstellen", width="20",
                           command=lambda: make_table(cif_file, lxr_file, sum_file, save_path, message))
close_window = Button(window, bg="#E1E6DF", text="Schließen", width="15",
                      command=lambda: close_program(cif_file, lxr_file, sum_file))

# Assign a position to each element

info_text_1.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
info_text_2.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

cif_text.grid(row=3, column=1, padx=5, pady=5)
#cif_button.grid(row=3, column=2, sticky="W", padx=10, pady=5)

lxr_text.grid(row=4, column=1, padx=5, pady=5)
#lxr_button.grid(row=4, column=2, sticky="W", padx=10, pady=5)

all_text.grid(row=4, rowspan=2, column=0)
all_button.grid(row=3, column=0)

sum_text.grid(row=5, column=1, padx=5, pady=5)
#sum_button.grid(row=5, column=2, sticky="W", padx=10, pady=5)

question_text.grid(row=6, column=0, padx=5, pady=5)
r_structure_data.grid(row=6, column=1, sticky="W", padx=10, pady=5)
r_atomic_positions.grid(row=7, column=1, sticky="W", padx=10, pady=5)
r_displacement_parameters.grid(row=8, column=1, sticky="W", padx=10, pady=5)

table_tex.grid(row=9, column=0, padx=5, pady=5)

# entry_table.grid(row=9, column=1, sticky="W", padx=10, pady=5)

save_table_button.grid(row=9, column=1, padx=10, pady=5)

make_table_button.grid(row=10, column=1, padx=10, pady=5)

info_message.grid(row=11, column=1, sticky="W", padx=10, pady=5)

close_window.grid(row=12, column=3, sticky="E", padx=5, pady=5)

window.mainloop()
