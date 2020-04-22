# Tune Corpus

![Travis Build](https://travis-ci.org/MindMimicLabs/tune-corpus.svg?branch=master)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)

Turn a single domain corpus into a collection of smaller corpuses sutable for a RNN style network to learn.
This is the implementation of some of our other work.

## Install

You can install the `tune-corpus` module either from [GitHub](https://github.org) or from a local Clone. 

```{shell}
python -m pip install git+https://github.com/MindMimicLabs/tune-corpus.git
```
```{shell}
python -m pip install ./tune-corpus
```

## Usage

You can use the `tune-corpus` module either from within your own Python module or from the command line.
I choose `d:/corpus_in` + `d:/corpus_out` as my input paths, you may want to select something different.

```{python}
from tuning import Tuning

t = Tuning(path_in)
t.tune_corpus(path_out)
```
```{shell}
python python -c "from tuning import Tuning; Tuning('d:/corpus_in').tune_corpus('d:/corpus_out')"
```
