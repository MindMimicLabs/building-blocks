# Normalize Corpus by Truncation

Deep Learning networks typically need a fixed shape for their inputs.
This script truncates all documents above a given length `xxx`.
This script is intended to be run _after_ [vectorization](./vectorize-corpus.md)

## Run the script

These scripts need to be run in a modified manner compared to the [general form](../README.md#scripts).
There is another parameter called `length` that is needed to provide a consistent input shape.
Please update step 4 in the [general form](../README.md#scripts) to be:

* Run `python normalize-corpus-by-padding.py -in d:/corpus_in -out d:/corpus_out -l 2000`.

## Academic Boilerplate

Below is the suggested text to add to the Methods and Materials section of your paper when using this building block.
The references can be found [here](./references.bib)

> Each document was normalized to provide a consistent input shape to the deep learning network.
> The below normalization steps were undertaken:
>
> 1. Documents above length `xxx` were truncated.
>
> The normalization script can be found in the companion repository ^[http://www.github.com/{user}/{repo}].
