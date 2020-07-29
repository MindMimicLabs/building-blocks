import pathlib
import string
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus, transforming them by applying `__cleanup_whitespace_in_document()`
@typechecked
def remove_whitespace_from_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Cleaning Corpus # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __cleanup_whitespace_in_document(file_name)
                file_out = path_out.joinpath(f'{file_name.stem}.txt')
                with file_out.open('w', encoding = 'utf-8') as file_out:
                    for sentence in sentences:
                        file_out.write(f'{sentence}\n')

# Transforms a single document by
# * removing blank lines
# * converting all whitespace charactors into a single space
# * reducing multipul spaces into a single space
@typechecked
def __cleanup_whitespace_in_document(document_name: pathlib.Path) -> list:
    with document_name.open('r', encoding = 'utf-8') as document:
        lines = document.readlines()
    result = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            chars = [__reduce_whitespace(c) for c in line]
            line = ''.join(chars)
            words = [token for token in line.split(' ')]
            words = [word for word in words if len(word) > 0]
            sentence = ' '.join(words)
            result.append(sentence)
    return result

# Reduce all whitespace to spaces
@typechecked
def __reduce_whitespace(c: str) -> str:
    if c in string.whitespace:
        return ' '
    else:
        return c

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
    remove_whitespace_from_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
