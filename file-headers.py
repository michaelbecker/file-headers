#!/usr/bin/python3
import os
import re
import sys
import argparse


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
    """Return a function that searches for filename extensions.
    """
    def is_file_match(filename):
        match = re.search("." + extension + "$", filename)
        if match:
            return True
        else:
            return False

    return is_file_match


def make_filename_match(base_name):
    """Return a function that searches for a filename.
    """
    def is_file_match(filename):
        match = re.search(base_name + "$", filename)
        if match:
            return True
        else:
            return False

    return is_file_match


def read_file(filename):
    """Read a text file and return the contents as 
    a list of lines
    """
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    return lines


def write_file(filename, lines):
    """Write a list of lines into a text file.
    """
    f = open(filename, "w")
    for l in lines:
        f.write(l)
    f.close()


def strip_header(lines, find_header_start, find_header_end, find_shebang = False):
    """Remove the header lines from a list of file lines.
    """
    search_for_header = True
    in_header = False
    new_lines = []

    for l in lines:
        
        # Run once, if ever. But if it's here we need to
        # look before we look for a header.
        if find_shebang:
            find_shebang = False
            # Using match is "like" using regex "^#!"
            match = re.match("#!", l)
            if match:
                new_lines.append(l)
                continue

        # Condition: The header has to start on the first line 
        # (or the second if there's a shebang line present).
        if search_for_header:
            search_for_header = False
            if find_header_start(l):
                in_header = True

        if not in_header:
            new_lines.append(l)

        if in_header:
            if find_header_end(l):
                in_header = False

    return new_lines


def insert_new_header(file_lines, new_header, find_shebang = False):

    new_lines = []

    if find_shebang:
        find_shebang = False
        # Using match is "like" using regex "^#!"
        match = re.match("#!", file_lines[0])
        if match:
            new_lines.append(file_lines[0])
            new_lines = new_lines + new_header
            new_lines = file_lines[1:]
        else:
            new_lines = new_header + file_lines
    else:
        new_lines = new_header + file_lines

    return new_lines


def print_lines(line):
    for l in lines:
        l = l.rstrip()
        print(l,)


def update_all_cpp_files(start_dir, new_header):

    def find_header_start(line):
        match = re.search("/\*", line)
        if match:
            return True
        else:
            return False

    def find_header_end(line):
        match = re.search("\*/", line)
        if match:
            return True
        else:
            return False

    file_list = find_all_files(start_dir, make_file_extension_match("cpp"))
    for f in file_list:
        lines = read_file(f)
        lines = strip_header(lines, find_header_start, find_header_end)
        lines = insert_new_header(lines, new_header)
        write_file(f, lines)


def update_all_c_files(start_dir, new_header):

    def find_header_start(line):
        match = re.search("/\*", line)
        if match:
            return True
        else:
            return False

    def find_header_end(line):
        match = re.search("\*/", line)
        if match:
            return True
        else:
            return False

    file_list = find_all_files(start_dir, make_file_extension_match("c"))
    for f in file_list:
        lines = read_file(f)
        lines = strip_header(lines, find_header_start, find_header_end)
        lines = insert_new_header(lines, new_header)
        write_file(f, lines)


def update_all_h_files(start_dir, new_header):

    def find_header_start(line):
        match = re.search("/\*", line)
        if match:
            return True
        else:
            return False

    def find_header_end(line):
        match = re.search("\*/", line)
        if match:
            return True
        else:
            return False

    file_list = find_all_files(start_dir, make_file_extension_match("h"))
    for f in file_list:
        lines = read_file(f)
        lines = strip_header(lines, find_header_start, find_header_end)
        lines = insert_new_header(lines, new_header)
        write_file(f, lines)


def update_all_makefiles(start_dir, new_header):

    def find_header_start(line):
        match = re.match("##", line)
        if match:
            return True
        else:
            return False

    def find_header_end(line):
        match = re.match("##", line)
        if match:
            return True
        else:
            return False

    file_list = find_all_files(start_dir, make_filename_match("makefile"))
    for f in file_list:
        lines = read_file(f)
        lines = strip_header(lines, find_header_start, find_header_end)
        lines = insert_new_header(lines, new_header)
        write_file(f, lines)


parser = argparse.ArgumentParser()
parser.add_argument("start_dir", help="Directory to start scaning in.")
parser.add_argument("header_file", help="File containing the new header.")
parser.add_argument("file_type", help="Files of type to be updated.")
args = parser.parse_args()

header_lines = read_file(args.header_file)

if (args.file_type == "cpp"):
    update_all_cpp_files(args.start_dir, header_lines)

elif (args.file_type == "c"):
    update_all_c_files(args.start_dir, header_lines)

elif (args.file_type == "h"):
    update_all_h_files(args.start_dir, header_lines)

elif (args.file_type == "makefile"):

    update_all_makefiles(args.start_dir, header_lines)

else:
    print("Unsupported file type")
    sys.exit(0)


