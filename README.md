# Building Blocks

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)

Below is a list of the corpus tools we use at Mind Mimic Labs.
They are intended to be building blocks for both general research in our lab as well as publication boilerplate.
Each tool should be considered stand-alone and includes both code (`~/code`) and documentation (`~/docs`).
There is a combined `requirements.txt` file for all the tools found in the root of the repo.
The documentation will include both instructions as to what the code is for, how to run it, and what publication boilerplate to put in the Methods and Materials section.

## Scripts

Unless otherwise noted, all scripts follow the same execution path.

1. Open a command prompt
2. Change into the `~/code` folder.
3. Run `python {{scriptname}}.py -in d:/corpus_in -out d:/corpus_out`.
   You should change the input and output paths as desired.

The list of current scripts is below.
In general, you want to first run [documents-to-corpus](./documents-to-corpus), then other scripts.
Individual papers/projects/repos will instruct on the exact order in their `README.md`'s **Tabula Rasa** section.

**Data Pre-Processing**

1. [remove-stop-words](./docs/remove-stopwords-from-corpus.md)
2. [lowercase-corpus](./docs/lowercase-corpus.md)
3. [stem-corpus](./docs/stem-corpus.md)
4. [remove-whitespace-from-corpus](./docs/remove-whitespace-from-corpus.md)
5. [remove-punction-from-corpus](./docs/remove-punction-from-corpus.md)
6. [remove-numbers-from-corpus](./docs/remove-numbers-from-corpus.md)

**Formatting**

1. [documents-to-corpus](./docs/documents-to-corpus.md)
2. [flatten-corpus](./docs/flatten-corpus.md)
3. [re-encode-corpus](./docs/re-encode-corpus.md)

**Deep Learning**

1. [vectorize-corpus](./docs/vectorize-corpus.md)
2. [normalize-corpus-by-padding](./docs/normalize-corpus-by-padding.md)
3. [normalize-corpus-by-truncation](./docs/normalize-corpus-by-truncation.md)
4. [normalize-corpus-by-windowing](./docs/normalize-corpus-by-windowing.md)
5. [normalize-corpus-by-zipfs-law](./docs/normalize-corpus-by-zipfs-law.md)

**Misc**

1. [corpus-to-reading-level](./docs/corpus-to-reading-level.md)
2. [(un)nest-corpus](./docs/unnest-corpus.md)
