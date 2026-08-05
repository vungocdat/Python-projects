import shutil
import sys


def read_file(provided_file):
    with open(provided_file, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
        return lines

def create_copy(source_file, provided_list):
    file_extension = source_file.split('.')[-1]
    for name in provided_list:
        mac_txt = f'{name}.{file_extension}'
        #mac_txt = f'{name.lower()}.{file_extension}'  # in case lower case is needed
        shutil.copyfile(source_file, mac_txt)


if len(sys.argv) != 3:      # main.py + source + file = 3
    print("Wrong number of provided arguments!\n")
    print("Usage:")
    print("python main.py <source_file> <name_list_file>")
else:
    template = sys.argv[1]
    target_file = sys.argv[2]
    list_of_strings = read_file(target_file)
    create_copy(template, list_of_strings)
    print("Finished.")
