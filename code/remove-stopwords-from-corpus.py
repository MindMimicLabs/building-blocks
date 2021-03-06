import nltk
import pathlib
import shutil
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from typeguard import typechecked

# Iterates over all the documents in a corpus, transforming them by applying `__remove_stopwords_from_document()`
@typechecked
def remove_stopwords_from_corpus(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    i = 1
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = set(stopwords)
    widgets = [ 'Pre-Processing Document # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in path_in.iterdir():
            if u.is_corpus_document(file_name):
                bar.update(i)
                i = i + 1
                sentences = __remove_stopwords_from_document(file_name, stopwords)
                u.write_document(path_out, file_name, sentences)

# Transforms a single document by removeing all the stopwords
@typechecked
def __remove_stopwords_from_document(document_name: pathlib.Path, stopwords: set) -> list:
    lines = u.read_document(document_name)
    result = []
    for line in lines:
        words = [token for token in line.split(' ')]
        words = [word for word in words if word not in stopwords]
        sentence = ' '.join(words)
        result.append(sentence)
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
    remove_stopwords_from_corpus(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
