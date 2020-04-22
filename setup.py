from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name = 'tune-corpus',
    version = '0.0.1',
    description = 'xxx',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/MindMimicLabs/tune-corpus',
    author = '@markanewman, @jkorn81',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Linguists',
        'Topic :: Language Processing',
        'License :: MIT',
        'Programming Language :: Python :: 3'
    ],
    keywords = 'language-processing',
    packages = find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5, <4',
    install_requires = requirements,
    project_urls = {
        'Bug Reports': 'https://github.com/MindMimicLabs/tune-corpus/issues',
        'Source': 'https://github.com/MindMimicLabs/tune-corpus',
    }
)