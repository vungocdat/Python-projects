import shutil
import sys

template = sys.argv[1]
target_file = sys.argv[2]

def read_file(provided_file):
    with open(provided_file, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
        return lines


def create_copy(source_file, provided_list):
    file_extension = source_file.split('.')[-1]
    for name in provided_list:
        mac_txt = f'{name}.{file_extension}'
        shutil.copyfile(source_file, mac_txt)

list_of_strings = read_file(target_file)
create_copy(template, list_of_strings)
print("Finished.")
