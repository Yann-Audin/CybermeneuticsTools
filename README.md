# CybermeneuticsTools

v1.0

## What is CybermeneuticsTools?

CybermeneuticsTools is a Python software designed to transform textual data into a network of hypertexts with index cards for the names entities in a given corpus. 

It aims to facilitate the humanistic inquiry into interconnected texts.

## How-tos

### How to install

There are two ways to use the Cybermeneutics Tools software:

1. **Cloning the repository**
2. **Downloading the file "cybermeneutics.py"**

To call the software, you will need to have Python 3 installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

### How to run the software

Once you have Python installed, you can run the software by executing the following command in your terminal or command prompt:

```bash
python cybermeneutics.py
```

Alternatively, you can use a Python IDE like PyCharm or Visual Studio Code to run the script.

**Before running the software, you might want to change its parameters too better suit your needs. Running Cybermeneutics on a large corpus may take a few hours depending on the strenght of your processor, the chosen model and the lenght of the texts.**

The software will download the necessary libraries and SpaCy models, and create a folder architecture before stopping with a prompt:

```
You can now add your files to the data folder.
When ready, press 'y' and then enter to continue. You can at any time stop this script by pressing 'ctrl + c'.
```

Before pressing 'y', first add the ```.md``` or ```.txt``` files you want to study in the ```/data``` folder. If these files are logically ordered in folders, you should copy that architecture in the data folder as it will be replicated in the viewer. 

#### How to use a virtual environment

To create a virtual environment, you can use the following commands:

```bash
python -m venv myenv
```

This will create a new directory called `myenv` in your current directory. To activate the virtual environment, use the following command:

```bash
source myenv/bin/activate  # On Linux/macOS
```
Or on Windows, use:

```bash
myenv\Scripts\activate  # On Windows
```

A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus several additional packages. It allows you to manage dependencies for different projects separately.

### How to change the parameters

The parameters of the CybermeneuticsTools software can be modified in the ```Cybermeneutics.py``` file by changing the values of the variables in the ```main()``` function at the end of the file.

List of parameters:

- ```sample```: True or False. If True, the software will generate a sample file with an example of yaml metadata and a short text. (Default is True);
- ```path```: The path is the name of the new folder that will be created during the initialization of the softare. This folder will receive the data that the user wants to transform into hypertexts, the entity dictionary and the viewer-ready files. (Default is "Cybermeneutics");
- ```model_name```: The name of the SpaCy model to be used for named entity recogntion. (Default is ```en_core_web_sm``` which has a precision of $0.84$.)
- ```min_sources```: The minimum number of sources in which an entity must appear to be included in the index cards. (Default is 2);
- ```min_count```: The minimum number of times an entity must appear in the corpus to be included in the index cards. (Default is 10).

#### Custom list 

When you initialize the program, an empty file named ```list.txt``` is created. Terms saved in this list will be treated as entities, and index cards will be created for the terms. To use a custom list, enter one word per line in the file, and save the file before processing the files.

#### Chosing the right SpaCy model

The SpaCy library offers multiple pre-trined models for different languages and computational power. Choosing the right model can significantly affect the precision and speed of the software. For instance, the ```en_core_web_sm``` model is a small English model optimized for speed on regular CPUs while the ```en_core_web_trf``` model is larger, more accurate, but requires a GPU for optimal performance as it uses the transformer architecture.

The name of the model can be changed in the parameters of the software. You can find the list of available models in English here: [SpaCy English models](https://spacy.io/models/en), in French here: [SpaCy French models](https://spacy.io/models/fr), and in other languages here: [Spacy models](https://spacy.io/models). 

### How to view the files

To visualize the files as hypertexts, the ```/viewer``` folder should be opened using either Zettlr or Obsidian. Zettlr is an open source software for markdown note taking. Obsidian is not open source, but it is free to use on local files and is better at handling large amount of files and folders. 

### How to contribute

The two mains way to contribute to Cybermeneutics is to suggest new features, and contribute code. The main way to do so is to contact me directly or use issues (see next section). 

### How to report bugs

You can help me by reporting any issue you encounter, either by contacting me directly, or by opening an issue on github. Note that my mailing box is, has been so far, and is likely to always be a *hot mess*. Github has a [tutorial on how to create an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue) which explains it better than I would and I am more likely to answer an issue than an email. 

### Limits of the tool

Cybermeneutics is mostly limited by the main package it uses: SpaCy models are not perfect and they are not adequate for every type of text. Older texts, poetry and plays might have low precision in terms of named entity recognition. I would suggest modifying the source code so that it re-formats your data in the named entity recognition process to avoid line changes which are known to confuse SpaCy models. 

### How to cite

If you use this code, please cite it as follows: 

- Audin, Yann. (2025). CybermeneuticsTools: A python script for augmented reading. Retrieved from https://github.com/Yann-Audin/CybermeneuticsTools

```bibtex
@misc{cybermeneutics,
  author = {Yann Audin},
  title = {CybermeneuticsTools: A python script for augmented reading},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Yann-Audin/CybermeneuticsTools}
}
```

I will write (and hopefully publish) an article on these tools in (hopefully) the next year to present its use, theory and a case study. 

## License

Find here the fairly short [MIT License](LICENSE) license under which this tool is published.

## Contact

You can contact me at [yann.audin@umontreal.ca](mailto:yann.audin@umontreal.ca), although I might be more reactive to issues opened on the github.

## Acknowledgements

The author acknowledges the direct financial support from the following institutions:

- Conseil de recherche en sciences humaines du Canada (CRSH);
- Fond de recherche du Québec (FRQ).

The author is grateful for the support received from the following institutions:

- Chaire de recherche du Canada sur les écritures numériques;
- Centre de recherche interuniversitaire sur les humanités numériques (CRIHN);
- Université de Montréal.

## Note on the use of AI

Cybermeneutics was coded on VS Code with limited use of AI tools, specifically for code completion (VS Code Copilot) and debugging (Claude Sonnet 4). The core logic and design of the software were developed by the author. 
