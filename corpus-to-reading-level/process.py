from argparse import ArgumentParser
from collections import namedtuple
from readability import Readability
from readability.exceptions import ReadabilityException
import pathlib
import progressbar as pb
import statistics as stat
import string
import time

sentenceplus = namedtuple('sentenceplus', 'text grade_level')

# Iterates over all the documents in a corpus creating a new collection of documents on a per grade level basis.
def corpus_to_reading_level(path_in: pathlib.Path, path_out: pathlib.Path) -> None:
    __is_folder_readable(path_in)
    __is_folder_writable(path_out)
    start = time.time()
    __clean_grade_level_files(path_out)
    doc_cnt = 0
    for file_name in path_in.iterdir():
        if file_name.is_file() and file_name.suffix.lower() == '.txt':
            print(file_name.stem)
            sentences = __document_to_sentences(file_name)
            __save_new_documents(path_out, sentences)
            doc_cnt = doc_cnt + 1
    seconds = time.time() - start
    if(doc_cnt > 0):
        print(f'Processed (seconds/document): {int(seconds):,}/{doc_cnt:,} = {int(seconds/doc_cnt):,} spd')
    else:
        print(f'No text documents found in {path_in}')

# makes sure our parameters are good
def __is_folder_readable(folder: pathlib.Path) -> None:
    if not folder.exists():
        raise FileNotFoundError(str(folder))
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))
def __is_folder_writable(folder: pathlib.Path) -> None:
    if not folder.exists():
        folder.mkdir(parents = True)
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))

# clean out any previous run
def __clean_grade_level_files(path_out: pathlib.Path) -> None:
    print('Clearing prior grade level files ... ', end = '', flush = True)
    for file_name in path_out.iterdir():
        if file_name.is_file() and file_name.stem.startswith('grade_level.') and file_name.suffix.lower() == '.txt':
            file_name.unlink()
    print('Done')

# breaks a single document into sentences with each sentence haveing been evaluated for grade level
def __document_to_sentences(document_name: pathlib.Path) -> list:
    with document_name.open('r', encoding = 'utf-8') as document:
        sentences = document.readlines()
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
def __fluff_line(line: str) -> str:
    words = line.split()
    words = words * max(30, int(200/len(words)) + 1)        
    line = ' '.join(words)
    return line

# at the low and high end, `grade_level` offen does not make sense
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
def __coleman_liau(r: Readability) -> float:
    try:
        lvl = r.coleman_liau().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
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
def __flesch_kincaid(r: Readability) -> float:
    try:
        lvl = r.flesch_kincaid().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
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
def __linsear_write(r: Readability) -> float:
    try:
        lvl = r.linsear_write().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
def __smog(r: Readability) -> float:
    try:
        lvl = r.smog(all_sentences = True).grade_level
        return float(lvl)
    except ReadabilityException:
        return None
def __spache(r: Readability) -> float:
    try:
        lvl = r.spache().grade_level
        return float(lvl)
    except ReadabilityException:
        return None
  
# saves the sentences to grade level aproate files
def __save_new_documents(path_out: pathlib.Path, sentences: list) -> None:
    min_grade_level = min(sentence.grade_level for sentence in sentences)
    max_grade_level = max(sentence.grade_level for sentence in sentences)
    widgets = ['Saving by grade level: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
    with pb.ProgressBar(widgets = widgets, max_value = max_grade_level + 1 - min_grade_level) as bar:
        for grade_level in range(min_grade_level, max_grade_level + 1):
            bar.update(grade_level - min_grade_level)
            file_out = path_out.joinpath(f'grade_level.{grade_level}.txt')
            with file_out.open('a', encoding = 'utf-8') as file_out:
                for sentence in sentences:
                    if sentence.grade_level == grade_level:
                        file_out.write(f'{sentence.text}\n')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the source corpus',
        default = 'd:/corpus_in')
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder containing the by grade level corpus',
        default = 'd:/corpus_out')
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.folder_out}')
    corpus_to_reading_level(pathlib.Path(args.folder_in), pathlib.Path(args.folder_out))
