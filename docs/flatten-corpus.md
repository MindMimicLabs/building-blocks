# Flatten Corpus

Transforms all the documents in the corpus by removing line breaks.
This will create a single long line for the entire file and is useful as a prior step to [padding](./pad-corpus.md).

## Run the script

The script is run in accordance with the [general form](../README.md#scripts)

## Academic boilerplate

Below is the suggested text to add to the Methods and Materials section of your paper when using this building block.
The references can be found [here](./references.bib)

> Each document in the corpus underwent several pre-processing steps.
> They were transformed under the following conditions:
>
> 1. Documents were flattened to remove newlines
>
> The above transformation's results are exemplified in (figure xxx).
> The transformation script can be found in the companion repository ^[http://www.github.com/{user}/{repo}].
