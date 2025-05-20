################################################################################################################
# Author: ISEL-GT
# Subject: Laboratório de Informática e Computadores
# Date: 20/05/2025
#
# Description: This script is meant to be a simple way to add all project files inside the current folder
# recursively into a quartus project. It only works where there is a single .qsf file, since it will
# search for the first one it finds in the current folder.
################################################################################################################

# Built-in imports
import os

# Third-Party imports
# Local Application Imports

# Finds the first .qsf file in the current working directory
TEST_MODE = False
base_path = "../.hardware" if TEST_MODE else "."
qsf_filepath =  os.path.join(base_path, [file for file in os.listdir(base_path) if file.endswith(".qsf")][0])
found_vhd = list()

def find_vhd(path):
    """
    Recursively finds all .vhd files in the given path and adds them to the found_vhd list.
    :param path:
    :return:
    """
    for root, dirs, files in os.walk(path):

        if not dirs:
            # If the directory is not the one where the .qsf file is, we can assume that we are at the bottom of the tree

            for file in files:
                filepath = os.path.join(root, file).replace("\\", "/")[2:]
                if file.endswith(".vhd"): found_vhd.append(filepath)

        for directory in dirs:
            find_vhd(os.path.join(root, directory))


def add_files_to_qsf():
    """
    Adds all the files in the found_vhd list to the .qsf file, rewriting the currently set global assignments.
    :return:
    """
    lines = []

    # Finds the first "set_global_assignment -name VHDL_FILE" line in the .qsf file
    # and rewrites the file without anything after it
    with open(qsf_filepath, "r") as qsf_file:
        lines = qsf_file.readlines()
        for i, line in enumerate(lines):
            if line.startswith("set_global_assignment -name VHDL_FILE"):
                lines = lines[:i]
                break

    # Writes the lines back to the file
    with open(qsf_filepath, "w") as qsf_file:
        qsf_file.writelines(lines)


    # Opens the .qsf file and adds all the files to it
    with open(qsf_filepath, "a") as qsf_file:
        for file in found_vhd:
            qsf_file.write(f"set_global_assignment -name VHDL_FILE {file}\n")
            print(f"Added {file} to {qsf_filepath}")

if __name__ == "__main__":
    find_vhd(base_path)
    add_files_to_qsf()
    print(found_vhd)

