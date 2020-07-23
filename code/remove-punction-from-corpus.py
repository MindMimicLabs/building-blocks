import pathlib
import string
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus, transforming them by applying `__remove_punction_from_document()`
@typechecked
def remove_punction_from_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Cleaning Corpus # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __remove_punction_from_document(file_name)
                file_out = path_out.joinpath(f'{file_name.stem}.txt')
                with file_out.open('w', encoding = 'utf-8') as file_out:
                    for sentence in sentences:
                        file_out.write(f'{sentence}\n')

# Transforms a single document by removing punction
@typechecked
def __remove_punction_from_document(document_name: pathlib.Path) -> list:
    with document_name.open('r', encoding = 'utf-8') as document:
        lines = document.readlines()
    result = []
    for line in lines:
        line = line.strip()
        chars = [c for c in line if c not in string.punctuation]
        line = ''.join(chars)
        result.append(line)
    return result

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the source corpus',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the transformed corpus',
        default = 'd:/corpus_out')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    remove_punction_from_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
