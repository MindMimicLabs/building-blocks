import pathlib
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from collections import namedtuple
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer
from typeguard import typechecked

sent_tokenize = PunktSentenceTokenizer()
word_tokenize = TreebankWordTokenizer()

# Iterates over all the documents in a corpus, transforming them by applying `__tokenize_document()`
@typechecked
def documents_to_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    widgets = [ 'Converting File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __tokenize_document(file_name)
                file_out = path_out.joinpath(f'{file_name.stem}.txt')
                with file_out.open('w', encoding = 'utf-8') as file_out:
                    for sentence in sentences:
                        file_out.write(f'{sentence}\n')

# Transforms a single document by applying Punkt then PENN Treebank to each sentences
@typechecked
def __tokenize_document(document_name: pathlib.Path) -> list:
    with document_name.open('r') as document:
        lines = document.readlines()
    result = []
    for line in lines:
        sentences = sent_tokenize.tokenize(line.strip())
        for i in range(0, len(sentences)):
            sentence = sentences[i]
            words = word_tokenize.tokenize(sentence)
            sentences[i] = ' '.join(words)
        result.extend(sentences)
    return result

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
    documents_to_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
