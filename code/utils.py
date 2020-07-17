import pathlib
from typeguard import typechecked

# makes sure our parameters are good
@typechecked
def assert_folder_is_readable(folder: pathlib.Path) -> None:
    if not folder.exists():
        raise FileNotFoundError(str(folder))
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))
@typechecked
def assert_folder_is_writable(folder: pathlib.Path) -> None:
    if not folder.exists():
        folder.mkdir(parents = True)
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))

@typechecked
def is_corpus_document(file_path: pathlib.Path) -> bool:
    result = \
        file_path.is_file() and \
        file_path.suffix.lower() == '.txt' and \
        not file_path.stem.startswith('_')
    return result