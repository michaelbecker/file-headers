#!/usr/bin/python3

import os
import re


def find_all_files(directory, filename_filter = None, dirname_filter = None):
    """ Return a list of all normal files in the directory
        as well as all subdirs. This performs a breath first 
        search.
    """
    original_dir = os.getcwd()
    os.chdir(directory)
    dir_list = []
    file_list = []

    for e in os.listdir(directory):

        if os.path.isfile(e):
            e = os.path.realpath(e)
            if filename_filter == None:
                file_list.append(e)
            elif filename_filter(e):
                file_list.append(e)

        elif os.path.isdir(e):
            e = os.path.realpath(e)
            if dirname_filter == None:
                dir_list.append(e)
            elif dirname_filter(e):
                dir_list.append(e)

    for d in dir_list:
        file_list = file_list + find_all_files(d, filename_filter)

    os.chdir(original_dir)

    return file_list


def make_file_extension_match(extension):

    def is_file_match(filename):
        match = re.search("." + extension + "$", filename)
        if match:
            return True
        else:
            return False

    return is_file_match


def make_filename_match(base_name):

    def is_file_match(filename):
        match = re.search(base_name + "$", filename)
        if match:
            return True
        else:
            return False

    return is_file_match


cpp_match = make_file_extension_match("cpp")
h_match = make_file_extension_match("h")
makefile_match = make_filename_match("makefile")


print("CPP match")
file_list = find_all_files(".", cpp_match)
for f in file_list:
    print (f)

print("H match")
file_list = find_all_files(".", h_match)
for f in file_list:
    print (f)

print("makefile match")
file_list = find_all_files(".", makefile_match)
for f in file_list:
    print (f)


