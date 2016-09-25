# file-headers
This is a utility I wrote to update file headers to a standard file header for all files of a specific type within a directory and all subdirectories.

## Usage:
```
usage: file-headers.py [-h] [--dir DIR] header_file file_type

positional arguments:
  header_file  File containing the new header.
  file_type    [c|h|cpp|hpp|makefile] File type to be updated.

optional arguments:
  -h, --help   show this help message and exit
  --dir DIR    Directory to start scaning in. Default is current directory.
```

