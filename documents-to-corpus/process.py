from argparse import ArgumentParser
from collections import namedtuple
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from shutil import rmtree
import csv
import json
import pathlib
import progressbar as pb

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['al', 'fig', 'i.e', 'e.g'])
sent_tokenize = PunktSentenceTokenizer(punkt_param)

cite_span = namedtuple('cite_span', 'start end')
article = namedtuple('article', 'id abstract body')

def convert_folder_to_corpus(folder_in, folder_out):
    folder_in = pathlib.Path(folder_in)
    folder_out = pathlib.Path(folder_out)
    create_folder_structure(folder_out)
    errors = []
    i = 1
    widgets = [ 'Converting File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in folder_in.iterdir():
            if file_name.is_file() and file_name.suffix.lower() == '.json':
                bar.update(i)
                i = i + 1
                article = parse_json_to_article(file_name)
                if article == None:
                    errors.append(file_name.stem)
                else:
                    write_article(folder_out, article)
    write_errors(folder_out, errors)

def create_folder_structure(folder_out):
    if folder_out.exists():
        if folder_out.is_dir():
            rmtree(folder_out)
        else:
            folder_out.unlink()
    folder_out.mkdir(parents = True)
    folder_out.joinpath('./abstract').mkdir()
    folder_out.joinpath('./body').mkdir()

def parse_json_to_article(file_name):
    file_in = file_name
    with file_in.open('r', encoding = 'utf-8') as file_in:
        raw_data = json.load(file_in)
    id = raw_data['paper_id']
    abstract = extract_paragraphs(raw_data['abstract'])
    abstract = convert_to_sentences(abstract)
    body = extract_paragraphs(raw_data['body_text'])
    body = convert_to_sentences(body)
    return article(id, abstract, body) if len(abstract) > 0 and len(body) > 0 else None

def extract_paragraphs(paragraphs):
    result = [clean_paragraph(paragraph) for paragraph in paragraphs]
    return result

def clean_paragraph(paragraph):
    text = paragraph['text']
    cite_spans = paragraph['cite_spans']
    cite_spans = [cite_span(x['start'], x['end']) for x in cite_spans]
    for x in sorted(cite_spans, key = lambda x: x.end, reverse = True):
        text = text[0: x.start:] + text[x.end + 1::]
    return text

def convert_to_sentences(paragraphs):
    result = [sent_tokenize.tokenize(paragraph) for paragraph in paragraphs]
    return result

def write_article(folder_out, article):
    write_article_part(folder_out.joinpath(f'./abstract/{article.id}.txt'), article.abstract)
    write_article_part(folder_out.joinpath(f'./body/{article.id}.txt'), article.body)

def write_article_part(file_out, paragraphs):
    first = True
    with file_out.open('w', encoding = 'utf-8') as file_out:
        for paragraph in paragraphs:
            if first:
                first = False
            else:
                file_out.write('\n')
            for sentence in paragraph:
                file_out.write(sentence)
                file_out.write('\n')

def write_errors(folder_out, errors):
    errors_file = folder_out.joinpath('./error.csv')
    with errors_file.open('w', encoding = 'utf-8', newline='') as errors_file:
        writer = csv.writer(errors_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
        writer.writerow(['incomplete article'])
        for error in errors:
            writer.writerow([error])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--folder-in', help = 'Folder containing the raw JSON files', required = True)
    parser.add_argument('-out', '--folder-out', help = 'Folder containing the newly created text corpus', required = True)
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    convert_folder_to_corpus(args.folder_in, args.folder_out)
