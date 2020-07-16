from argparse import ArgumentParser
import codecs
import pathlib
import progressbar as pb
import utils as u
from typeguard import typechecked

# Iterates over all the documents in a corpus creating a new collection of sentence tokenized documents
@typechecked
def re_encode_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.is_folder_readable(path_in)
    u.is_folder_writable(path_out)
    i = 1
    widgets = [ 'Re-Encoding File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if file_name.is_file() and file_name.suffix.lower() == '.txt':
                bar.update(i)
                i = i + 1
                sentences = __read_document(file_name)
                file_out = path_out.joinpath(file_name.name)
                __write_document(file_out, sentences)

# read the document with `codecs`
@typechecked
def __read_document(document_name: pathlib.Path) -> list:
    document_name = str(document_name)
    with codecs.open(document_name, 'r', encoding = 'utf-8') as document:
        lines = document.readlines()
    return lines

# write the document with `pathlib`
@typechecked
def __write_document(document_name: pathlib.Path, lines: list) -> None:
    with document_name.open('w', encoding = 'utf-8') as document:
        for line in lines:
            document.write(f'{line.strip()}\n')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the source documents',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the re-encoded documents',
        default = 'd:/corpus_out')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    re_encode_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
