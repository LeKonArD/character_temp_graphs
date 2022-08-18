import pandas as pd
import numpy as np
import re

def most_common(lst):
    return max(set(lst), key=lst.count)

def oppose(x):
    
    if x == "Fem":
        return "Masc"
    if x == "Masc":
        return "Fem"

def speeches(x):

    if "yes" in list(x):
        return "yes"
    else:
        return "no"
    
def rename_coref(x):
    
    if x == "[]":
        return np.nan
    
    if "," in x:
        return np.nan
    
    else:
        return int(re.sub("\[|\]|\,|\s","",x))   

def rename_ner(x):
    
    if x != x:
        return np.nan
    else:
        return re.sub("\[|\]|\'","",x)



def load_data_from_tsv(path):
    
    krit = ['word.SoMaJoTokenizer',
       'sentence.SoMaJoTokenizer',
       'paragraph_id.SoMaJoTokenizer',
       'section_id.SoMaJoTokenizer',
       'scene_id.SoMaJoTokenizer', 
       'pos.RNNTagger',
       'upos.RNNTagger', 
       'morph.ParzuParser',
       'lemma.RNNLemmatizer', 
       'head.ParzuParser', 
       'deprel.ParzuParser',
       'speech_direct.RedewiedergabeTagger',
       'speech_indirect.RedewiedergabeTagger',
       'speech_reported.RedewiedergabeTagger',
       'speech_freeIndirect.RedewiedergabeTagger',
       'coref_clusters.CorefIncrementalTagger',
       'ner.FLERTNERTagger']
    
    colnames=  ['token',
                'sent',
                'para',
                'chapter',
                'scene', 
                'pos',
                'upos', 
                'morph',
                'lemma', 
                'head', 
                'deprel',
                'sd',
                'si',
                'sr',
                'sf',
                'coref',
                'ner']
    
    data = pd.read_csv(path, sep="\t")
    data = data.loc[:,krit]
    data.columns = colnames
    data["anys"] = data.loc[:,["sd","si","sr","sf"]].apply(lambda x: speeches(x), axis=1)
    data.coref = data.coref.apply(lambda x: rename_coref(x))
    data.ner = data.ner.apply(lambda x: rename_ner(x))
    return data

def load_data_from_perseg_tsv(path):
    
    krit = ['word.SoMaJoTokenizer',
       'sentence.SoMaJoTokenizer',
       'pos.RNNTagger',
       'upos.RNNTagger', 
       'morph.ParzuParser',
       'lemma.RNNLemmatizer', 
       'head.ParzuParser', 
       'deprel.ParzuParser',
       'speech_direct.RedewiedergabeTagger',
       'speech_indirect.RedewiedergabeTagger',
       'speech_reported.RedewiedergabeTagger',
       'speech_freeIndirect.RedewiedergabeTagger',
       'coref_clusters.CorefIncrementalTagger',
       'ner.FLERTNERTagger']
    
    colnames=  ['token',
                'sent',
                'pos',
                'upos', 
                'morph',
                'lemma', 
                'head', 
                'deprel',
                'sd',
                'si',
                'sr',
                'sf',
                'coref',
                'ner']
    
    data = pd.read_csv(path, sep="\t")
    data = data.loc[:,krit]
    data.columns = colnames
    data["anys"] = data.loc[:,["sd","si","sr","sf"]].apply(lambda x: speeches(x), axis=1)
    data.coref = data.coref.apply(lambda x: rename_coref(x))
    data.ner = data.ner.apply(lambda x: rename_ner(x))
    return data