 # Vectorize Corpus

A corpus is composed of a collection document.
A document is composed of a collection of words.
Deep Learning networks typically deal with _integers_, not words.
Vectorizing a corpus is the process of collecting all the words in all the documents and assigning a _unique_ integer to represent the word.
Word order is maintained as part of vectorization.

## Run the script

These scripts need to be run in a modified manner compared to the [general form](../README.md#scripts).
There is another parameter called `control` that is needed to preserve the reverse operation.
The `control` file can also be used for filtering or vectorising addtional documents later.
Please update step 4 in the [general form](../README.md#scripts) to be:

* Run `python vectorize-corpus.py -in d:/corpus_in -out d:/corpus_out -ctrl d:/control.csv`.

## Academic Boilerplate

This script should not be considered as a real transformation in terms of academic papers.
Instead, it should be thought of as an accessibility step.
The processing done by this step should be considered in the same manner as specifying the path on disk.
If a boilerplate is _required_ consider the following:

> After preprocessing, documents were vectorized.
