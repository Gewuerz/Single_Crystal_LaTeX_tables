# ----------------------------------------------------------------------------------------------------------------------
# main.py
#
# Program to create LaTeX tables from single crystal data files
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
import webbrowser
from tkinter import *
from tkinter import ttk

from button_commands import *


class Main:
    def __init__(self):
        self.cif_file = None
        self.lxr_file = None
        self.sum_file = None
        self.save_path = ""
        self._build_gui()

    def open_all_files(self):
        filelist = browse_files_all()
        for file in filelist:
            if ".cif" in file:
                self.cif_file = open(file, "r", encoding="utf-8")
                self.cif_text.configure(text=self.cif_file.name.split("/")[-1])
            if ".lxr" in file:
                self.lxr_file = open(file, "r", encoding="windows-1254")
                self.lxr_text.configure(text=self.lxr_file.name.split("/")[-1])
            if ".sum" in file:
                self.sum_file = open(file, "r", encoding="windows-1254")
                self.sum_text.configure(text=self.sum_file.name.split("/")[-1])
        # set a default savepath
        try:
            self.save_path = self.cif_file.name + ".tex"
        except AttributeError:
            pass

        return

    def make_table(self):
        # Make the selected table
        option = self.question_variable.get()
        self.message.set(table_decision(option, self.cif_file, self.lxr_file, self.sum_file, self.save_path))
        return

    def save_table(self):
        self.save_path = select_save_path()
        self.save_table_button.configure(text=self.save_path.split("/")[-1])
        return

    def callback(self, url):
        webbrowser.open_new(url)

    def close_program(self):
        # Make sure all files are closed before exiting the program
        close_files(self.cif_file, self.lxr_file, self.sum_file)
        self.window.destroy()

    def _build_gui(self):
        # Create the window
        self.window = Tk()
        self.window.resizable(width=False, height=False)
        self.window.title("LaTeX-Einkristalltabellen")
        self.window.configure(bg="#FFFFFF")
        self.window.grid_columnconfigure(0, weight=1)

        self.message = StringVar()
        self.message.set("Noch keine Tabelle erzeugt.")
        self.info_message = Label(self.window, bg="#FFFFFF", font="Calibri", width=30, textvariable=self.message)
        self.info_text_1 = Label(self.window, font="Calibri 14 bold", bg="#FFFFFF",
                                 text="Program zum Erstellen von TeX-Tabellen.")
        self.info_text_2 = Label(self.window, font="Calibri", bg="#FFFFFF",
                                 text="Für die Erstellung der Strukturverfeinerungsdatentabelle werden alle drei Dateien benötigt!\n"
                                      "Die .cif Datei muss mit JANA oder SHELLXL erstellt worden sein.\n"
                                      "Die Wyckoff-Lagen sind in den Dateien nicht vollständig enthalten!\n"
                                      "Die erstellten Tabellen benötigen das siunitx-Packet."
                                 )

        self.cif_text = Label(self.window, font="Calibri", bg="#FFFFFF", text="Name der .cif-Datei")
        self.lxr_text = Label(self.window, font="Calibri", bg="#FFFFFF", text="Name der .lxr-Datei")
        self.sum_text = Label(self.window, font="Calibri", bg="#FFFFFF", text="Name .sum-Datei")
        self.all_text = Label(self.window, font="Calibri", bg="#FFFFFF", borderwidth=1, relief="ridge",
                              text="Es können sowohl einzelne, \n als auch alle drei Dateien \n auf einmal geöffnet werden.")

        self.all_button = Button(self.window, text="Dateien öffnen", font="Calibri 11", bg="#CCDDAA", width=20,
                                 command=self.open_all_files)

        self.separator1 = ttk.Separator(self.window, orient="horizontal")
        self.separator2 = ttk.Separator(self.window, orient="horizontal")

        self.entry_table = Entry(self.window, bg="white", width=30)

        self.question_text = Label(self.window, font="Calibri", bg="#FFFFFF",
                                   text="Was für eine Tabelle soll erstellt werden?")
        self.question_variable = IntVar()
        self.question_variable.set(1)

        self.r_structure_data = Radiobutton(self.window, bg="#FFFFFF", justify=LEFT, font="Calibri",
                                            text="Daten der Strukturverfeinerung \n (.cif, .lxr, .sum)",
                                            variable=self.question_variable, value=1)
        self.r_atomic_positions = Radiobutton(self.window, bg="#FFFFFF", font="Calibri",
                                              text="Atomlagen (.cif)", variable=self.question_variable, value=2)
        self.r_displacement_parameters = Radiobutton(self.window, bg="#FFFFFF", font="Calibri",
                                                     text="Auslenkungsparameter (.cif)",
                                                     variable=self.question_variable, value=3)

        self.save_table_button = Button(self.window, bg="#E1E6DF", font="Calibri 11", text="Tabelle speichern unter",
                                        width="20", command=self.save_table)

        self.make_table_button = Button(self.window, bg="#E1E6DF", font="Calibri 11", text="Tabelle erstellen",
                                        width="20",
                                        command=self.make_table)

        self.copyright = Label(self.window, font="Calibri", bg="#FFFFFF", text=" © 2022-2023 Judith Bönnighausen")
        self.github_link = Label(self.window, font="Calibri 12 bold", bg="#FFFFFF", fg="#034748", text="GitHub",
                                 cursor="hand2")
        self.github_link.bind("<Button-1>",
                              lambda e: self.callback("https://github.com/Gewuerz/Single_Crystal_LaTeX_tables"))
        self.close_window = Button(self.window, bg="#E1E6DF", font="Calibri 11", text="Schließen", width="15",
                                   command=self.close_program)

        # Assign a position to each element

        self.info_text_1.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        self.info_text_2.grid(row=2, column=0, columnspan=4, padx=5, pady=(5, 20))

        self.separator1.grid(row=3, columnspan=3, sticky="WE")

        self.cif_text.grid(row=4, column=1, padx=5, pady=(20, 5))

        self.lxr_text.grid(row=5, column=1, padx=5, pady=5)

        self.all_text.grid(row=4, rowspan=4, column=2, padx=15)
        self.all_button.grid(row=5, column=0)

        self.sum_text.grid(row=6, column=1, padx=5, pady=(5, 20))

        self.separator2.grid(row=7, columnspan=3, sticky="WE")

        self.question_text.grid(row=8, column=0, padx=10, pady=5)
        self.r_structure_data.grid(row=8, column=1, sticky="W", padx=10, pady=5)
        self.r_atomic_positions.grid(row=9, column=1, sticky="W", padx=10, pady=5)
        self.r_displacement_parameters.grid(row=10, column=1, sticky="W", padx=10, pady=(5, 25))

        self.save_table_button.grid(row=11, column=0, padx=10, pady=5)

        self.make_table_button.grid(row=11, column=1, padx=10, pady=5)

        self.info_message.grid(row=13, column=1, sticky="W", padx=10, pady=5)

        self.close_window.grid(row=14, column=2, sticky="E", padx=15, pady=15)

        self.copyright.grid(row=14, column=0, sticky="W", padx=5, pady=10)
        self.github_link.grid(row=14, column=0, sticky="E", padx=5, pady=10)

        self.window.mainloop()


Main()
