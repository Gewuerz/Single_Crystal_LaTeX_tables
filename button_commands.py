# ----------------------------------------------------------------------------------------------------------------------
# button_commands.py
#
# Contains most button_commands, except for those that change the button text
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
import os
from tkinter import filedialog
from tkinter import messagebox

from anisotropic_displacement import make_anisotropic_displacement_table
from atomic_parameters import make_atomic_parameters_table
from single_crystal_data import make_single_crystal_data_table


def browse_files_cif():
    """Open a file browser to select the .cif file"""
    return filedialog.askopenfile(title="Datei auswählen",
                                  filetypes=[("Crystallographic Information File", ".cif")])


def browse_files_lxr_sum():
    """Open a file browser to select the .lxr or .sum file
    the .lxr and .sum files are not UTF-8 encoded and cannot be correctly opened with askopenfile()"""
    filename = filedialog.askopenfilename(title="Datei auswählen",
                                          filetypes=[("Einkristalldaten", ".lxr .sum")])
    return open(filename, "r", encoding="windows-1254")


def browse_files_all():
    """Select all three files at once. They will only be opened in the button command."""
    filelist = filedialog.askopenfilenames(title="Datei auswählen",
                                           filetypes=[("Einkristalldateien", ".cif .lxr .sum")])
    return filelist


def select_save_path():
    """Select the location and name for the file to be saved."""
    save_path = filedialog.asksaveasfilename(title="Speichern als", filetypes=[("TeX-Dateien", ".tex")],
                                             defaultextension=".tex")
    return save_path


def delete_tmp_files():
    for file in ["lxr_Datei_konvertiert.txt", "sum_Datei_konvertiert.txt"]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


def close_files(cif_file, lxr_file, sum_file):
    try:
        cif_file.close()
    except AttributeError:
        pass
    try:
        lxr_file.close()
    except AttributeError:
        pass
    try:
        sum_file.close()
    except AttributeError:
        pass


def check_file(file):
    if not file:
        return False
    else:
        return True


def correct_file_encoding(file, new_filename, encoding_to="UTF_8"):
    """A function that will make sure that the files used are utf-8"""
    with open(new_filename, "w", encoding=encoding_to) as fw:
        for line in file.readlines():
            fw.write(line[: -1] + "\r\n")


def table_decision(decision, cif_file, lxr_file, sum_file, save_path):
    """A function that creates the tables"""
    try:
        if not check_file(cif_file):
            messagebox.showerror("Fehlende Datei:", ".cif Datei noch nicht ausgewählt")
            return "Fehlende Datei"
        if save_path == "":
            messagebox.showerror("Fehlender Speicherort",
                                 "Bitte einen Namen & Speicherort für die Tabelle angeben.")
            return "Fehlender Tabellenname"

        if decision == 1:
            if not check_file(lxr_file):
                messagebox.showerror("Fehlende Datei", ".lxr Datei noch nicht ausgewählt")
                return "Fehlende Datei"
            if not check_file(sum_file):
                messagebox.showerror("Fehlende Datei", ".sum Datei noch nicht ausgewählt")
                return "Fehlende Datei"

            correct_file_encoding(lxr_file, "lxr_Datei_konvertiert.txt")
            correct_file_encoding(sum_file, "sum_Datei_konvertiert.txt")
            return make_single_crystal_data_table(cif_file, "lxr_Datei_konvertiert.txt", "sum_Datei_konvertiert.txt",
                                                  save_path)
        elif decision == 2:
            return make_atomic_parameters_table(cif_file, save_path)
        elif decision == 3:
            return make_anisotropic_displacement_table(cif_file, save_path)
    finally:
       delete_tmp_files()
