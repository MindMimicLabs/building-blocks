import csv
import pathlib
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus, normalizing them by applying `__normalize_document_by_truncation()`
@typechecked
def normalize_corpus_by_truncation(path_in: pathlib.Path, path_out: pathlib.Path, max_length: int) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Normalize Document # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __normalize_document_by_truncation(file_name, min_length)
                u.write_document(path_out, file_name, sentences)

# Makes sure a document has at most `max_length` tokens. If not, any token beond that limit is removed.
@typechecked
def __normalize_document_by_truncation(document_name: pathlib.Path, max_length: int) -> list:    
    lines = u.read_document(document_name)
    results = []
    for line in lines:
        tokens = line.split()
        if len(tokens) > max_length:
            tokens = tokens[0:max_length]
        max_length = max_length - len(tokens)
        if len(tokens) > 0:
            results.append(' '.join(tokens))
    return results   

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the source documents',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the vectorise documents',
        default = 'd:/corpus_out')
    parser.add_argument(
        '-l', '--max-length',
        help = 'Max length the document can take on',
        type = int,
        default = '1000')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    print(f'max length: {args.max_length}')
    normalize_corpus_by_truncation(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out), int(args.max_length))
