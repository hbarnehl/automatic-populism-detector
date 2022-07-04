import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
import spacy
import re
import pandas as pd


def file_folder(file):
    """Input is a directory in the form of a string. The output are the name of the file and the name of the parent directory."""
    folder = re.search(r"([A-Z]){2}", os.path.dirname(file)).group(0)
    filename = re.sub(r"\.\w+","", os.path.basename(file))
    return folder, filename

def save(name, filename, target):
    '''This function takes as input either a dataframe or a string.
    It then saves the files in their corresponding folders depending on the class.'''
    if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
    if isinstance(name, str):
        textfile = re.sub("\n"," ", name).lower()
        with open(target+f"{filename}.txt", mode='w') as f:
            f.write(textfile)
    elif isinstance(name, pd.core.frame.DataFrame):
        name.to_csv(target+f"{filename}.csv")
    else:
        print('Please enter either a text or a dataframe as the first argument.')
        print(f"Your argument is {type(name)}.")
        
def clean(feature):
    '''This function takes a input a list of strings on which it performs a number of pre-processing operations.
    These are the removal of punctuation, email addresses, stopwords, roman and arabic numerals as well as double spaces.'''
    roman = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii"]
    
    #remove punctuation
    feature=["".join([x for x in par if x not in punctuation]) for par in feature]  
    
    # remove roman letter numbers
    feature=[" ".join([w for w in par.split() if w not in roman]) for par in feature]
    
    # remove all email addresses (from https://stackoverflow.com/a/201378)
    feature=[re.sub(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])","", par) for par in feature]
    
    # remove numbers
    feature=[re.sub(r"\d+","", par) for par in feature]
    
    # remove double spaces by splitting the strings into words and joining these words again
    feature=[" ".join(par.split()) for par in feature]
    
    # remove stopwords
    nl_stopwords = set(stopwords.words('dutch')) # I use the default Dutch stopwords
    feature = [" ".join([w for w in article.split() if w not in nl_stopwords]) for article in feature]
    
    return feature

def nl_lemmatise(x):
    '''This function takes a list of Dutch strings as input and returns a list of lemmatized string.'''
    nlp = spacy.load('nl_core_news_lg')
    doclist = list(nlp.pipe(x))
    docs=[]
    for i, doc in enumerate(doclist):
        docs.append(' '.join([listitem.lemma_ for listitem in doc]))
    return docs

def classification_report (y_test, y_pred):
    '''This function takes as input a list of labels and a list of predicted labels belonging to the same features.
    Its output is a report on a number of validity criteria.'''
    print(f"{metrics.classification_report(y_test, y_pred)}")
   