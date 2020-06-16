# Building Blocks

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)

Below is a list of the corpus tools we use at Mind Mimic Labs.
They are intended to be building blocks for both general research in our lab as well as publication boilerplate.
Each tool is stand-alone and includes both code and documentation.
The code will have its own `requirements.txt` file.
The documentation will include both instructions as to what the code is for, how to run it, and what publication boilerplate to put in the Methods and Materials section.

## Scripts

All scripts follow the same execution path.

1. Open a command prompt
2. Change into the directory of the script
3. Get any prerequisites that may be needed by running `pip install -r requirements.txt`
4. Run `python process.py -in d:/corpus_in -out d:/corpus_out`.
   You should change the input and output paths as desired.

The list of current scripts is below.
In general, you want to run [documents-to-corpus](./documents-to-corpus) then other scripts.
The individual project will instruct on the order. 

1. [documents-to-corpus](./documents-to-corpus)
2. [corpus-to-reading-level](./corpus-to-reading-level)
