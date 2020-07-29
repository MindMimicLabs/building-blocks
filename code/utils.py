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

@typechecked
def write_document(path_out: pathlib.Path, file_name:  pathlib.Path, lines: list) -> None:
    file_out = path_out.joinpath(file_name.name)
    with file_out.open('w', encoding = 'utf-8') as file_out:
        for line in lines:
            file_out.write(f'{line}\n')

@typechecked
def read_document(document_name:  pathlib.Path) -> list:
    with document_name.open('r') as document:
        lines = document.readlines()
    lines = [line.rstrip('\n') for line in lines]
    return lines
