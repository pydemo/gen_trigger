#Write Python script to read and write to a file
from os.path import join, isfile
in_file = join('tmp', 'test_in.txt')
out_file = 'test_out.txt'

assert isfile(in_file)


with open(in_file, 'rb') as fh_in:
    with open(out_file, 'wb') as fh_out:
        fh_out.write(fh_in.read())