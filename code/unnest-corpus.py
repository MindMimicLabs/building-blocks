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
def unnest_corpus(path_in: pathlib.Path, path_out: pathlib.Path, control: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Unnesting Corpus # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with control.open('w', encoding = 'utf-8', newline='') as control:
            writer = csv.writer(control, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['filename', 'relitive path'])
            for file_name in path_in.rglob("*"):
                if u.is_corpus_document(file_name):
                    bar.update(i)
                    i = i + 1                    
                    dest_path = path_out.joinpath(f'{str(uuid.uuid4())}{file_name.suffix}')
                    shutil.copy(file_name, dest_path)
                    relative_path = file_name.relative_to(path_in)
                    writer.writerow([dest_path.name, str(relative_path)])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the nested documents',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the unnested documents',
        default = 'd:/corpus_out')
    parser.add_argument(
        '-ctrl', '--control',
        help = 'Control file to allow the re-nesting of documents',
        default = 'd:/control.csv')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    print(f'control file: {args.control}')
    unnest_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out), pathlib.Path(args.control))
