import csv
import pathlib
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus recording all tokens, then iterates again to produce vectorized files
@typechecked
def vectorize_corpus(path_in: pathlib.Path, path_out: pathlib.Path, path_control: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Collecting Tokens # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    tokens = dict()
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                __append_tokens(tokens, file_name)
    token_map = __map_tokens(tokens)
    __save_token_file(tokens, token_map, path_control)
    i = 1
    widgets = [ 'Vectorising Files # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                vector = __vectorise_document(file_name, token_map)
                u.write_document(path_out, file_name, vector)

@typechecked
def __append_tokens(tokens: dict, document_name: pathlib.Path) -> None:
    lines = u.read_document(document_name)
    for line in lines:
        for token in line.split():
            cnt = tokens.get(token, 0)
            tokens[token] = cnt + 1

@typechecked
def __map_tokens(tokens: dict) -> dict:
    result = dict()
    i = 1
    sort_tokens = sorted(tokens.items(), key = lambda x: x[1], reverse = True)
    for item in sort_tokens:
        result[item[0]] = i
        i = i + 1
    return result

@typechecked
def __save_token_file(tokens: dict, token_map: dict, path: pathlib.Path) -> None:
    with path.open('w', encoding = 'utf-8', newline = '') as path:
        writer = csv.writer(path, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
        writer.writerow(['token', 'value', 'frequency'])
        sort_tokens = sorted(tokens.items(), key = lambda x: x[1], reverse = True)
        for item in sort_tokens:
            key = item[0]
            writer.writerow([key, token_map[key], tokens[key]])

@typechecked
def __vectorise_document(document_name: pathlib.Path, token_map: dict) -> list:
    lines = u.read_document(document_name)
    vectors = []
    for line in lines:
        tokens = line.split()
        tokens = [token_map[token] for token in tokens]
        tokens = [str(token) for token in tokens]
        vector = ' '.join(tokens)
        vectors.append(vector)
    return vectors

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
        '-ctrl', '--control',
        help = 'Control file to allow the re-nesting of documents',
        default = 'd:/control.csv')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    print(f'control file: {args.control}')
    vectorize_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out), pathlib.Path(args.control))