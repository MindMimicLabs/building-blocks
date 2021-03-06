from argparse import ArgumentParser
import codecs
import pathlib
import progressbar as pb
import utils as u
from typeguard import typechecked

# Iterates over all the documents in a corpus creating a new collection of sentence tokenized documents
@typechecked
def re_encode_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Formatting Document # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __read_document(file_name)
                u.write_document(path_out, file_name, sentences)

# read the document with `codecs`
@typechecked
def __read_document(document_name: pathlib.Path) -> list:
    document_name = str(document_name)
    with codecs.open(document_name, 'r', encoding = 'utf-8') as document:
        lines = document.readlines()
    return lines

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the source documents',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the transformed corpus',
        default = 'd:/corpus_out')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    re_encode_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
