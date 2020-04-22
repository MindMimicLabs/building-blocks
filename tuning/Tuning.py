from readability import Readability
from readability.exceptions import ReadabilityException
import pathlib
import progressbar as pb
import statistics as stat
import string
import time

class Tuning:
    def __init__(self, path_in: pathlib.Path):
        if not path_in.exists():
            raise FileNotFoundError(str(path_in))
        if not path_in.is_dir():
            raise NotADirectoryError(str(path_in))
        self.path_in = path_in
    
    def tune_corpus(self, path_out: pathlib.Path) -> None:
        """
        Iterates over all the documents in a corpus creating a new collection of documents on a per grade level basis.
        """
        if not path_out.exists():
            path_out.mkdir(parents = True)
        elif not path_out.is_dir():
            raise NotADirectoryError(str(path_out))
        start = time.time()
        self.__clean_grade_level_files(path_out)
        doc_cnt = 0
        for file_name in self.path_in.iterdir():
            if file_name.is_file() and file_name.suffix.lower() == '.txt':
                self.__tune_document(path_out, file_name)
                doc_cnt = doc_cnt + 1
        seconds = time.time() - start
        print(f'Processed (documents/sec): {doc_cnt:,}/{int(seconds):,} = {int(doc_cnt/seconds):,} dps')

    # clean out any previous run
    def __clean_grade_level_files(self, path_out: pathlib.Path) -> None:
        print('Clearing prior grade level files ... ', end = '', flush = True)
        for file_name in path_out.iterdir():
            if file_name.is_file() and file_name.stem.startswith('grade_level.') and file_name.suffix.lower() == '.txt':
                file_name.unlink()
        print('Done')

    # tunes a single document
    def __tune_document(self, path_out: pathlib.Path, document_name: pathlib.Path) -> None:
        with document_name.open('r', encoding = 'utf-8') as document:
            lines = document.readlines()
        pb_i = 0
        widgets = [document_name.stem, ': ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
        with pb.ProgressBar(widgets = widgets, max_value = len(lines)) as bar:
            for line in lines:
                bar.update(pb_i)
                line = line.strip()
                if len(line) > 0:
                    grade_level = self.__median_grade_level_by_line(line)
                    self.__save_line_to_grade_level(path_out, line, grade_level)
                pb_i = pb_i + 1

    # calculate a single `grade_level` based on the 8 known measures
    # median is chosen over mean because the 8 measures are known to be not normally distributed
    def __median_grade_level_by_line(self, line: str) -> int:
        line = self.__fluff_line(line)
        r = Readability(line)
        grade_levels = [
            self.__ari(r),
            self.__coleman_liau(r),
            self.__dale_chall(r),
            self.__flesch_kincaid(r),
            self.__gunning_fog(r),    
            self.__linsear_write(r),        
            self.__smog(r),
            self.__spache(r)]
        grade_levels = [min(17, max(0, x)) for x in grade_levels if x != None]
        if len(grade_levels) == 0:
            return None
        grade_level = stat.median(grade_levels)
        return round(grade_level)

    # at the low and high end, `grade_level` offen does not make sense
    def __ari(self, r: Readability) -> float:
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
    def __coleman_liau(self, r: Readability) -> float:
        try:
            lvl = r.coleman_liau().grade_level
            return float(lvl)
        except ReadabilityException:
            return None
    def __dale_chall(self, r: Readability) -> float:
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
    def __flesch_kincaid(self, r: Readability) -> float:
        try:
            lvl = r.flesch_kincaid().grade_level
            return float(lvl)
        except ReadabilityException:
            return None
    def __gunning_fog(self, r: Readability) -> float:
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
    def __linsear_write(self, r: Readability) -> float:
        try:
            lvl = r.linsear_write().grade_level
            return float(lvl)
        except ReadabilityException:
            return None
    def __smog(self, r: Readability) -> float:
        try:
            lvl = r.smog(all_sentences = True).grade_level
            return float(lvl)
        except ReadabilityException:
            return None
    def __spache(self, r: Readability) -> float:
        try:
            lvl = r.spache().grade_level
            return float(lvl)
        except ReadabilityException:
            return None

    # smog requires 30 sentences
    # flesch_kincaid requires 100 words.
    # repeat everything till you have enough text
    def __fluff_line(self, line: str) -> str:
        words = line.split()
        words = words * max(30, int(200/len(words)) + 1)        
        line = ' '.join(words)
        return line
    
    # saves the line to a file based on grade_level
    def __save_line_to_grade_level(self, path_out: pathlib.Path, line: str, grade_level: int) -> None:
        file_out = path_out.joinpath(f'grade_level.{grade_level}.txt')
        with file_out.open('a', encoding = 'utf-8') as file:
            file.write(f'{line}\n')

if __name__ == '__main__':
    path_in = pathlib.Path('d:/corpus_in')
    path_out = pathlib.Path('d:/corpus_out')
    Tuning(path_in).tune_corpus(path_out)
