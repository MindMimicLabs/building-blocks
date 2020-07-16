import pathlib
from typeguard import typechecked

# makes sure our parameters are good
@typechecked
def is_folder_readable(folder: pathlib.Path) -> None:
    if not folder.exists():
        raise FileNotFoundError(str(folder))
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))
@typechecked
def is_folder_writable(folder: pathlib.Path) -> None:
    if not folder.exists():
        folder.mkdir(parents = True)
    elif not folder.is_dir():
        raise NotADirectoryError(str(folder))