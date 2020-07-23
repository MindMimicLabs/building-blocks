# Re-Encode Corpus

The standard process we use to read in a `.txt` file uses `pathlib`'s `Path.open('r', encoding = 'utf-8')` function.
Under some blue-moon conditions, this will just break and we have never really figured out why.
It seems like using `codecs`'s `open('{filename}', 'r', encoding = 'utf-8')` allows for the file to be read in.
We can then write it out using `pathlib.Path.open(...)` which fixes the problem.

## Run the script

The script is run in accordance with the [general form](../README.md#scripts)

## Academic boilerplate

This script should not be considered as a real transformation in terms of academic papers.
Instead, it should be thought of as an accessibility step.
The processing done by this step should be considered in the same manner as specifying the path on disk.
If a boilerplate is _required_ consider the following:

> After acquiring the source documents, each document was encoded into the UTF-8 format ^[https://tools.ietf.org/html/rfc3629].
