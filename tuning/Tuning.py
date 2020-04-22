from readability import Readability
import pathlib
import progressbar as pb

class Tuning:
    def __init__(self, path_in: pathlib.WindowsPath):
        if not path_in.exists():
            raise FileNotFoundError(str(path_in))
        self.path_in = path_in
    def tune(self, path_out: pathlib.WindowsPath) -> None:
        if not path_out.exists():
            path_out.mkdir(parents = True)

