 # (un)Nest Corpus

The standard process we use deals with only a single folder.
In some cases, we want to process more than one folder as a single pass.
Multi folder processing usually happens when we are provided a file structure containing grouped documents.
This process intends to convert (unnest) a hierarchical folder structure to a single folder, run some other step (i.e., tokenization), then convert back (nest) to the hierarchy.

## Run the script

These scripts need to be run in a modified manner compared to the [general form](../README.md#scripts).
There is another parameter called `control` that is needed to preserve the reverse operation.
Please update step 4 in the [general form](../README.md#scripts) to be:

* Run `python unnest-corpus.py -in d:/corpus_in -out d:/corpus_out -ctrl d:/control.csv`.
* Run `python nest-corpus.py -in d:/corpus_in -out d:/corpus_out -ctrl d:/control.csv`.

## Academic Boilerplate

This script should not be considered as a real transformation in terms of academic papers.
Instead, it should be thought of as an accessibility step.
The processing done by this step should be considered in the same manner as specifying the path on disk.
If a boilerplate is _required_ consider the following:

> All documents, including documents inside of nested folders, were processed as a single pass.
