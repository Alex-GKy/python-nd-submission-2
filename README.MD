# Meme generator 
This project is used to generate memes that consist of an image, a quote, and its author. 

## Overview
There are several ways to use this application: 
1. Generate a random meme from an existing set of pictures and quotes
2. Supply a link to an image, a quote, and an author to generate your own meme
3. Supply a path to an image, quote and author via the command line

## Installation
Nothing to install except the pip dependencies.

## Usage
Either start the web app via
```commandline
flask run
```
or run from the command line: 
```commandline
python meme.py 
```

For the command line, see 
```commandline
python meme.py --help
```

to get info on the arguments supported.

## Technical architecture
Entry point for the web app is app.py, for the command line it's meme.py. 
Built-in quotes are supplied in the ./_data folder, as well as pictures. 
Additional quotes can be put as pdf, word, csv, or txt - see examples on how to format them. 

A quote is represented by the QuoteModel class, and quotes and images are put together
by the MemeEngine. The make_meme method in MemeEngine returns a path to the generated file
for further processing. 

Two modules are available: 

QuoteEngine: Ingests quotes and returns QuoteModels as representation.
MemeEngine: Consumes quotes and images, generates a meme from them and puts it in specified folder. 