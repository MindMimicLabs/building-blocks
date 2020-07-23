import csv
import pathlib
import shutil
import uuid
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus recording their relitive path and moving them to the root of the output folder
@typechecked
def nest_corpus(path_in: pathlib.Path, path_out: pathlib.Path, control: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Re-nesting Corpus # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with control.open('r', encoding = 'utf-8', newline='') as control:
            reader = csv.DictReader(control, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            for row in reader:
                bar.update(i)
                i = i + 1
                source_path = path_in.joinpath(row['filename'])
                dest_path = path_out.joinpath(row['relitive path'])
                pathlib.Path(dest_path.parent).mkdir(parents = True, exist_ok = True)
                shutil.copy(source_path, dest_path)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the unnested documents',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the re-nested documents',
        default = 'd:/corpus_out')
    parser.add_argument(
        '-ctrl', '--control',
        help = 'Control file to allow the re-nesting of documents',
        default = 'd:/control.csv')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    print(f'control file: {args.control}')
    nest_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out), pathlib.Path(args.control))
