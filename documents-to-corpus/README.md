# Documents to Corpus

A collection of documents is a corpus in name only.
Unstructured data is just like its continuous cousin in that it needs cleaned and prepared before it becomes useful.

The difference in this script and others in this collection is that each corpus will have its own nuanced data cleaning process.
As such, this script should serve _only_ as a baseline for what _can_ be done.
In some cases this is a simple find/replace on all files before running the code as-is.
Other times extensive evaluation is needed.
As an example, academic works have a whole different set of abbreviations when compared to general English.
These differences produce a bad tokenization when not accounted for in the process.
In the case where extensive evaluation is undertaken, it is appropriate to copy/paste this code to the new project and make modifications there.

## Run the script

The script is run in accordance with the [general form](../#scripts)

## Academic Boilerplate

Below is the suggested text to add to the Methods and Materials section of your paper when using this building block.
The references can be found [here](./references.bib)

> After the corpus was collected and converted to plain text, it was tokenized using the NLTK's ^[http://www.nltk.org] implementation of the Punkt sentence tokenizer [@kiss2006unsupervised] followed by the Penn Treebank word tokenizer [@marcus1993building].
> Punkt was chosen as it has proven viable in several other works [@hiippala2016semi;@avramidis2011evaluate;@yao2014information;@nothman2013learning;@marrese2014novel].
> Laboreiro et al. note that while the Penn Treebank may have some issues, it is still the de-facto standard [@laboreiro2010tokenizing].
