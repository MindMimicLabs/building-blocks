import pathlib
import string
import time
import progressbar as pb
import statistics as stat
import utils as u
from argparse import ArgumentParser
from collections import namedtuple
from readability import Readability
from readability.exceptions import ReadabilityException
from typeguard import typechecked

sentenceplus = namedtuple('sentenceplus', 'text grade_level')

# Iterates over all the documents in a corpus creating a new collection of documents on a per grade level basis.
@typechecked
def corpus_to_reading_level(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    u.assert_folder_is_readable(path_in)
    u.assert_folder_is_writable(path_out)
    start = time.time()
    __clean_grade_level_files(path_out)
    doc_cnt = 0
    for file_name in path_in.iterdir():
        if u.is_corpus_document(file_name):
            print(file_name.stem)
            sentences = __document_to_sentences(file_name)
            __save_new_documents(path_out, sentences)
            doc_cnt = doc_cnt + 1
    seconds = time.time() - start
    if(doc_cnt > 0):
        print(f'Processed (seconds/document): {int(seconds):,}/{doc_cnt:,} = {int(seconds/doc_cnt):,} spd')
    else:
        print(f'No text documents found in {path_in}')

# clean out any previous run
@typechecked
def __clean_grade_level_files(path_out: pathlib.Path) -> None:
    print('Clearing prior grade level files ... ', end = '', flush = True)
    for file_name in path_out.iterdir():
        if file_name.is_file() and file_name.stem.startswith('grade_level.') and file_name.suffix.lower() == '.txt':
            file_name.unlink()
    print('Done')

# breaks a single document into sentences with each sentence haveing been evaluated for grade level
@typechecked
def __document_to_sentences(document_name: pathlib.Path) -> list:
    lines = u.read_document(document_name)
    sentences = lines
    sentences = [sentence.strip() for sentence in sentences]
    sentences = [sentence for sentence in sentences if len(sentence) > 0]
    widgets = ['Calculating grade level: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
    with pb.ProgressBar(widgets = widgets, max_value = len(sentences)) as bar:
        for i in range(0, len(sentences)):
            bar.update(i)
            sentence = sentences[i]
            grade_level = __calculate_sentences_median_grade_level(sentence)
            sentences[i] = sentenceplus(sentence, grade_level)
    return sentences

# calculate a single `grade_level` based on the 8 known measures
# median is chosen over mean because the 8 measures are known to be not normally distributed
@typechecked
def __calculate_sentences_median_grade_level(line: str) -> int:
    line = __fluff_line(line)
    r = Readability(line)
    grade_levels = [
        __ari(r),
        __coleman_liau(r),
        __dale_chall(r),
        __flesch_kincaid(r),
        __gunning_fog(r),    
        __linsear_write(r),        
        __smog(r),
        __spache(r)]
    grade_levels = [min(17, max(0, x)) for x in grade_levels if x != None]
    if len(grade_levels) == 0:
        return None
    grade_level = stat.median(grade_levels)
    return round(grade_level)

# smog requires 30 sentences
# flesch_kincaid requires 100 words.
# repeat everything till you have enough text
@typechecked
def __fluff_line(line: str) -> str:
    words = line.split()
    words = words * max(30, int(200/len(words)) + 1)        
    line = ' '.join(words)
    return line

# at the low and high end, `grade_level` offen does not make sense
@typechecked
def __ari(r: Readability) -> float:
    try:
        lvls = r.ari().grade_levels        
        if 'college_graduate' in lvls:
            return 17
        elif 'college' in lvls:
            return 13
        elif 'K' in lvls:
            return 0
        else:
            return stat.mean([float(lvl) for lvl in lvls])
    except ReadabilityException:
        return None
@typechecked
def __coleman_liau(r: Readability) -> float:
    try:
        lvl = r.coleman_liau().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
@typechecked
def __dale_chall(r: Readability) -> float:
    try:
        lvls = r.dale_chall().grade_levels        
        if 'college_graduate' in lvls:
            return 17
        elif 'college' in lvls:
            return 13
        else:
            return stat.mean([float(lvl) for lvl in lvls])
    except ReadabilityException:
        return None
@typechecked
def __flesch_kincaid(r: Readability) -> float:
    try:
        lvl = r.flesch_kincaid().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
@typechecked
def __gunning_fog(r: Readability) -> float:
    try:
        lvl = r.gunning_fog().grade_level
        if lvl == 'college_graduate':
            return 17
        elif lvl == 'college':
            return 13
        elif lvl == 'na':
            return 0
        else:
            return float(lvl)
    except ReadabilityException:
        return None
@typechecked
def __linsear_write(r: Readability) -> float:
    try:
        lvl = r.linsear_write().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
@typechecked
def __smog(r: Readability) -> float:
    try:
        lvl = r.smog(all_sentences = True).grade_level
        return float(lvl)
    except ReadabilityException:
        return None
@typechecked
def __spache(r: Readability) -> float:
    try:
        lvl = r.spache().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
  
# saves the sentences to grade level aproate files
@typechecked
def __save_new_documents(path_out: pathlib.Path, sentences: list) -> None:
    grade_levels = list(set(sentence.grade_level for sentence in sentences))
    widgets = ['Saving by grade level: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
    with pb.ProgressBar(widgets = widgets, max_value = len(grade_levels)) as bar:
        gl_i = 0
        for grade_level in grade_levels:
            bar.update(gl_i)
            file_out = path_out.joinpath(f'grade_level.{grade_level}.txt')
            with file_out.open('a', encoding = 'utf-8') as file_out:
                for sentence in sentences:
                    if sentence.grade_level == grade_level:
                        file_out.write(f'{sentence.text}\n')
            gl_i = gl_i + 1

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
    corpus_to_reading_level(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
