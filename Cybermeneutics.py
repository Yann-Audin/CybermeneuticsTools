# Cybermeneutics is a Python script that uses the SpaCy library to transform a 
# textual corpus into a wiki-style database with hyperlinks and index cards for
# named entities as well as terms from a list. 

# MIT License
# Copyright (c) 2025 Yann Audin

# If you use this code, please cite it as follows:
# Audin, Yann. (2025). CybermeneuticsTools: A python script for augmented 
# reading. Retrieved from https://github.com/Yann-Audin/CybermeneuticsTools

"""{bibtex}
@misc{cybermeneutics,
  author = {Yann Audin},
  title = {CybermeneuticsTools: A python script for augmented reading},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Yann-Audin/CybermeneuticsTools}
}
"""

# Cybermeneutics tools uses a class named Corpus that does the following:
# 1. Initializes the file structure and downloads necessary libraries.
# 2. Reads text files from a specified directory.
# 3. Processes the text to extract named entities and terms from a word list.
# 4. Generates a dictionary of entities and their occurrences in the text.
# 5. Creates viewer files with hyperlinks to the entities and terms.
# 6. Generates index files with hyperlinks to the augmented texts.

# The script can be run directly, and it will prompt the user to add files to 
# the data folder.

# The user can specify the model name, minimum sources, and minimum count for 
# entities to be included in the viewer index files.

# Options should be set in the main function, which is called when the script 
# is run. To modify the parameters of the Corpus class, you can change the
# arguments in the main function at the bottom of the script (line 730).

class Corpus:
    def __init__(self, path, sample = True, model_name = "en_core_web_sm", 
                    min_sources = 4, min_count = 20):
        import subprocess
        import sys
        from tqdm import tqdm
        requirements = ["spacy"]

        print("""Downloading the required libraries...""")
        for req in requirements:
            # Check the the operating system and install the library accordingly
            if sys.platform.startswith("win"):
                subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            elif sys.platform.startswith("macos"):
                subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            else:
                print(f"Unsupported operating system: {sys.platform}. Please install {req} manually.")
                return
        
        print("""Importing the relevant libraries...""")
        import spacy
        import os

        print("""Downloading the model...""")
        try:     
            # Check the operating system and download the model accordingly
            if sys.platform.startswith("win"):
                subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            elif sys.platform.startswith("macos"):
                subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            else:
                print(f"Unsupported operating system: {sys.platform}. Please download the model manually.")
                return
            print("""Model downloaded successfully.""")
            print("""Loading the model...""")
            nlp = spacy.load(model_name)
        except:
            print("""Model not found, downloading the default model...""")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            nlp = spacy.load("en_core_web_sm")

        self.data_path = path + "/data"
        self.viewer_path = path + "/viewer"
        self.min_sources = min_sources
        self.min_count = min_count
        self.path = path
        self.model_name = model_name
        self.sample = sample
        self.dictionary = {}
        self.model = nlp
        self.word_list = []
        print("Initializing...")
        self.initialize()
        print("You can now add your files to the data folder.")
        print("When ready, press 'y' and then enter to continue. You can at any time stop this script by pressing 'ctrl + c'.")
        while True:
            answer = input("Are you ready to continue?")
            if answer.lower() == "y":
                break
            else:
                print("Invalid input. Please enter 'y' when you are done adding files.")
                continue
        self.process()
        self.generate()
                                  
    def initialize(self):
        if self._starting_files():
            print("File structure initialised")
        else:
            print("There was an issue with the initialisation of the file structure")
    
    def _create_file(self, path, content):
        import os
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = path.replace("\"", "")
        path = path.replace("'", "")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    def _starting_files(self):
        import os
        print("""Creating the file structure...""")
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        if not os.path.exists(self.viewer_path):
            os.mkdir(self.viewer_path)
        
        print("""Creating the readme.txt file...""")
        readme_path = self.path + "/readme.txt"
        readme_content = """
# CybermeneuticsTools

v1.0

## What is CybermeneuticsTools?

CybermeneuticsTools is a Python software designed to transform textual data into a network of hypertexts with index cards for the names entities in a given corpus. It aims to facilitate the humanistic inquiry into interconnected texts, 

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
"""
        if self._create_file(readme_path, readme_content):
            pass
        else:
            print("There was an issue with the initialisation of the file structure (readme.txt was not created).")
            return False
        
        print("""Creating the empty list file...""")
        list_path = self.path + "/list.txt"
        list_content = """

"""
        if self._create_file(list_path, ""):
            pass
        else:
            print("There was an issue with the initialisation of the file structure (list.txt was not created).")
            return False

        print("""Creating the .obsidian folder and file""")
        obs_path = self.viewer_path + "./obsidian/graph.json"
        obs_content = """{
  "collapse-filter": true,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": true,
  "colorGroups": [
    {
      "query": "path:PERSON  ",
      "color": {
        "a": 1,
        "rgb": 14701138
      }
    },
    {
      "query": "path:GPE  ",
      "color": {
        "a": 1,
        "rgb": 5431380
      }
    },
    {
      "query": "path:LOC  ",
      "color": {
        "a": 1,
        "rgb": 11657298
      }
    },
    {
      "query": "path:LIST  ",
      "color": {
        "a": 1,
        "rgb": 5396192
      }
    },
    {
      "query": "",
      "color": {
        "a": 1,
        "rgb": 5431473
      }
    }
  ],
  "collapse-display": true,
  "showArrow": false,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1,
  "lineSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.198961937716263,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 166,
  "scale": 0.20640086681036243,
  "close": false
}"""
        if self._create_file(obs_path, obs_content):
            pass
        else:
            print("There was an issue with the initialisation of the file structure (.obsidian/graph.json was not created).")
            return False

        print("""Creating the empty dictionary file...""")
        dict_path = self.path + "/dictionary.json"
        dict_content = """
        {}
        """
        if self._create_file(dict_path, dict_content):
            pass
        else:
            print("There was an issue with the initialisation of the file structure (dictionary.json was not created).")
            return False

        if self.sample:
            print("""Creating the sample file...""")
            sample_path = self.data_path + "/sample.txt"
            sample_content = """
---
title: "Novel"
author: "Yann Audin"
year: 2025
---
This is an example of a novel with named characters like Jacob Williamson and William Jacobson, who went to a place like San Diego to eat a product like Cordon Bleu. 
"""
            try:
                self._create_file(sample_path, sample_content)
            except:
                print("There was an issue with the initialisation of the file structure (sample.txt was not created).")
                return False
        
        return True

    def _create_entity_link(self, ent_type, string):
        return f"[[ENTITY/{ent_type}/{string}|{string}]]"

    def _remove_path_from_title(self, path):
        instances_of_slash = []
        for i in range(len(path)):
            if path[i] == "/":
                instances_of_slash.append(i)
        if len(instances_of_slash) > 0:
            path = path[instances_of_slash[-1] + 1:len(path)]
        return path

    def _create_file_link(self, path, title):
        # Create relative path from viewer entity files back to viewer text files
        relative_path = path.replace(self.data_path + "\\", "")
        relative_path = relative_path.replace(".txt", "")
        relative_path = relative_path.replace(".md", "")
        relative_path = relative_path.replace("\\", "/")
        title = self._remove_path_from_title(title)
        return f"[[FILES/{relative_path}|{title}]]"

    def _read_word_list(self):
        with open(self.path + "/list.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                self.word_list = [word.strip().lower() for word in content.split("\n") if word.strip()]
            else:
                self.word_list = []
        return self.word_list

    def _find_text_files(self, folder_path):
        import os
        text_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".txt") or file.endswith(".md"):
                    text_files.append(os.path.join(root, file))
        return text_files

    def _extract_yaml_and_text(self, input_string):
        """
            Extracts the yaml from a string (from the first "---" to the second "---" of the string) and returns the yaml and the text that has been stripped of the yaml.

            Args:
                input_string: The input string potentially containing YAML front matter.

            Returns:
                A tuple containing two strings: the extracted YAML (or None if not found) and the text without the YAML.
            """
        start = input_string.find("---")
        if start == -1:
            return None, input_string

        end = input_string.find("---", start + 3)
        if end == -1:
            return None, input_string

        yaml_content = input_string[start + 3 : end].strip()
        text_content = input_string[end + 3 :].strip()

        return yaml_content, text_content

    def _filter_dictionary(self, token):
        import spacy
        # Filters the dictionary to remove unwanted tokens.
        # FIXED: Don't filter out words that are in the word list - they should be processed
        if isinstance(token, spacy.tokens.Token):
            if token.is_stop:
                return False
        
        if hasattr(token, 'text'):
            text = token.text
        else:
            text = str(token)
            
        if "\n" in text:
            return False
        
        # Clean text for length check
        clean_text = text.replace("-", "").replace("'", "").replace(".", "")
        if len(clean_text) < 2:
            return False
        if clean_text in ["Mr.", "Mrs.", "Ms."]:
            return False
        return True 

    def _clean_entity_text(self, text):
        """Clean entity text by removing possessives and other unwanted suffixes"""
        # Remove possessive 's at the end
        if text.endswith("'s"):
            text = text[:-2]
        elif text.endswith("'"):
            text = text[:-1]
        return text

    def _clean_text(self, text):
        text = text.replace("-", "--")  # Em dash to double hyphen
        text = text.replace("-", "-")  # En dash to hyphen
        text = text.replace("--", " -- ") # Insure space around em-dashes and double dashes
        text = text.replace("  ", " ") # Double space to single space
        text = text.replace(".", "...")  # Ellipsis to three periods
        text = text.replace("’", "'")  # Left single quote to apostrophe
        text = text.replace("'", "'")  # Right single quote to apostrophe
        text = text.replace('“', "\"")  # Left double quote to double quote
        text = text.replace("”", "\"")
        text = text.replace("`", "'")  # Backticks to apostrophe
        return text

    def _is_word_in_list(self, word):
        """Check if a word (in various forms) is in the word list"""
        word_lower = word.lower()
        # Check direct match
        if word_lower in self.word_list:
            return True
        # Check without possessives
        clean_word = self._clean_entity_text(word_lower)
        if clean_word in self.word_list:
            return True
        return False

    def _add_to_dictionary(self, key, text_file, word_type, original_text=None):
        """Helper method to add items to dictionary"""
        if key not in self.dictionary:
            self.dictionary[key] = {
                "counts": {text_file: 1},
                "type": word_type,
                "original_text": original_text or key.replace("_", " ")
            }
        else:
            if text_file not in self.dictionary[key]["counts"]:
                self.dictionary[key]["counts"][text_file] = 1
            else:
                self.dictionary[key]["counts"][text_file] += 1

    def process(self):
        from tqdm import tqdm
        import re
        print("""Processing the text files...""")
        
        # Read the word list first
        self._read_word_list()
        
        text_files = self._find_text_files(self.data_path)
        for text_file in tqdm(text_files):
            with open(text_file, "r", encoding = "utf-8") as f:
                text = f.read()
            
            text = self._clean_text(text)
            yaml, text = self._extract_yaml_and_text(text)
            
            paragraphs = text.split("\n\n")

            for paragraph in paragraphs:
                paragraph = paragraph.replace("\n", " ")
                doc = self.model(paragraph)
                for ent in doc.ents:
                    if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "FAC", "NORP", "DATE", "WORK_OF_ART", "PRODUCT"]:
                        cleaned_entity_text = self._clean_entity_text(ent.text)
                        ent_key = cleaned_entity_text.replace(" ", "_")

                        if self._filter_dictionary(ent):
                            try: 
                                self._add_to_dictionary(ent_key, text_file, ent.label_, cleaned_entity_text)
                            except Exception as e:
                                print(f"Error processing entity {ent.text}: {e}")
            # Process the word list items
            for list_word in self.word_list:
                # Create regex pattern for word boundaries
                pattern = r'\b' + re.escape(list_word) + r'\b'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                match_count = 0
                for match in matches:
                    match_count += 1
                
                # If we found matches, add to dictionary
                if match_count > 0:
                    list_key = list_word.lower().replace(" ", "_")
                    if list_key not in self.dictionary:
                        self.dictionary[list_key] = {
                            "counts": {text_file: match_count},
                            "type": "LIST",
                            "original_text": list_word
                        }
                    else:
                        if text_file not in self.dictionary[list_key]["counts"]:
                            self.dictionary[list_key]["counts"][text_file] = match_count
                        else:
                            self.dictionary[list_key]["counts"][text_file] += match_count
        
        for word in self.word_list:
            list_key = word.lower().replace(" ", "_")
            if list_key not in self.dictionary:
                self.dictionary[list_key] = {
                    "counts": {},
                    "type": "LIST",
                    "original_text": word
                }
        
        # Save dictionary as a json file
        import json
        with open(self.path + "/" + "dictionary.json", "w", encoding="utf-8") as f:
            json.dump(self.dictionary, f, indent = 4)
        
        return True

    def _term_appears_in_file(self, term, file_path):
        """Check if a term appears in the dictionary for the given file"""
        if term not in self.dictionary:
            return False
        
        file_counts = self.dictionary[term].get("counts", {})
        return file_path in file_counts

    def _strip_path(self, path):
        # Returns everything after the last "/"
        title = path.split("/")[-1]
        title = path.split("""\\""")[-1]
        # Returns everything before the last "."
        return title.split(".")[0]

    def _replace_words(self, text, word, word_type, current_file_path):
        import re
        
        # Check if this term actually appears in the current file
        if not self._term_appears_in_file(word, current_file_path):
            return text
        
        # Get the original text for display
        original_text = self.dictionary[word].get("original_text", word.replace("_", " "))
        
        # Handle both underscore and space versions
        patterns = []
        if "_" in word:
            # For underscored words, create patterns for both versions
            space_version = word.replace("_", " ")
            patterns.append((space_version, word, original_text))  # space version, link to underscore
            patterns.append((word.replace("_", " "), word, original_text))  # ensure we catch the spaced version
        else:
            patterns.append((word, word, original_text))
        
        # Also handle possessive versions
        for pattern_word, link_word, display_text in patterns[:]:  # Copy list to avoid modifying while iterating
            patterns.append((pattern_word + "'s", link_word, display_text + "'s"))  # possessive version
            patterns.append((pattern_word + "'", link_word, display_text + "'"))   # alternative possessive
        
        for pattern_word, link_word, display_text in patterns:
            # Escape special regex characters
            escaped_word = re.escape(pattern_word)
            # Create word boundary pattern
            pattern = r'\b' + escaped_word + r'\b'
            
            def replacer(match):
                matched_text = match.group(0)
                start_pos = match.start()
                end_pos = match.end()
                
                # Check if this match is inside an existing link
                # Look backwards for [[ and forwards for ]]
                text_before = text[:start_pos]
                text_after = text[end_pos:]
                
                # Find the last [[ before this position
                last_open = text_before.rfind('[[')
                # Find the first ]] after this position  
                next_close = text_after.find(']]')
                
                if last_open != -1:
                    # Check if there's a ]] between the [[ and our match
                    text_between = text[last_open:start_pos]
                    if ']]' not in text_between and next_close != -1:
                        # We're inside a link, don't replace
                        return matched_text
                
                # Create the exact path format requested
                link_path = f"ENTITY/{word_type}/{link_word}"
                return f"[[{link_path}|{matched_text}]]"
            
            text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
        
        return text

    def generate(self):
        from tqdm import tqdm
        import spacy
        print("""Generating the viewer entity files...""")
        for element in tqdm(self.dictionary):
            sources = self.dictionary[element]["counts"]
            total_count = sum(self.dictionary[element]["counts"].values())
            
            # Generate page for items that meet criteria OR are from the word list
            if (len(sources) >= self.min_sources and total_count >= self.min_count) or self.dictionary[element]["type"] == "LIST":
                entity_type = self.dictionary[element]["type"]
                path = self.viewer_path + "/ENTITY/" + entity_type + "/" + element + ".md"
                
                # Use original text with spaces if available, otherwise use the key
                display_name = self.dictionary[element].get("original_text", element.replace("_", " "))
                content = f"# {display_name}\n\n"
                
                if sources:  # Only show sources if there are any
                    content += "## Occurrences\n\n"
                    for source in self.dictionary[element]["counts"]:
                        content += f"- {self._create_file_link(source, self._strip_path(source))}: " + str(self.dictionary[element]["counts"][source])+ "\n"
                else:
                    content += "*This term was in your word list but not found in any documents.*\n"
                
                self._create_file(path, content)
        print("""Viewer entity files generated.""")
        
        print("""Generating the viewer text files...""")
        text_files = self._find_text_files(self.data_path)
        for file_path in tqdm(text_files):
            with open(file_path, "r", encoding = 'utf-8') as f:
                text = f.read()
            
            # Apply replacements for all dictionary elements that meet criteria
            for element in self.dictionary:
                sources = self.dictionary[element]["counts"]
                total_count = sum(self.dictionary[element]["counts"].values())
                
                if (len(sources) >= self.min_sources and total_count >= self.min_count) or self.dictionary[element]["type"] == "LIST":
                    word_type = self.dictionary[element]["type"]
                    # Pass current file path to check if term appears in this file
                    text = self._replace_words(text, element, word_type, file_path)

            # Create the viewer version of the file
            relative_path = file_path.replace(self.data_path, "")
            if relative_path.startswith("/"):
                relative_path = relative_path[1:]
            
            viewer_path = self.viewer_path + "/FILES/" + relative_path
            viewer_path = viewer_path.replace(".txt", ".md")
            
            self._create_file(viewer_path, text)
        
        print("""Viewer text files generated.""")


def main():
    # The main function calls the corpus class with the desired parameters.
    corpus = Corpus("Cybermeneutics_corpus", # 
                    model_name = "en_core_web_sm", # See the README.md for information on models
                    sample = True, # True or False, add a sample text to the data folder
                    min_count = 1, # How many total instances necto have an index cardessary 
                    min_sources = 1 # How many sources necessary to have an index card
                )

if __name__ == "__main__":
    main()