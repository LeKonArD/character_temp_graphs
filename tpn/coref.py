import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None 

def most_common(lst):
    return max(set(lst), key=lst.count)

def oppose(x):
    
    if x == "Fem":
        return "Masc"
    if x == "Masc":
        return "Fem"
    
def get_namedict(data):
    
    nameframe = data[(~data.coref.isna()) & (~data.ner.isna())].loc[:,["lemma","coref"]]
    nameframe["lemma"] = [x.lower() for x in nameframe.lemma]

    coref_ids = set(nameframe.coref.astype(int))
    nameframe["c"] = 1
    nameframe = nameframe.groupby(["coref","lemma"]).count()

    namedict = {}
    for coref_id in coref_ids:

        name = nameframe.loc[coref_id,:].sort_values("c").index[-1]
        namedict[coref_id] = name
        
    return namedict


def name_mapper(x, namedict):

    
    try:
        return namedict[x]
    except KeyError:
        return np.nan
    
    
def map_names(data, namedict):
    
    data["named_coref"] = data["coref"].apply(lambda x: name_mapper(x, namedict))

    return data


def correct_coref(data, full_namelist):

    entrys = data[(~data.coref.isna()) & (data.ner == "PER")]
    corrections = []

    for index, row in entrys.iterrows():

        if row["lemma"].lower() != row["named_coref"].lower():
            if row["lemma"].lower() in full_namelist:
                corrections.append([index, row["lemma"].lower()])
            else:
                continue
                
    for ind, name in corrections:
        
        data.loc[ind,"named_coref"] = name
    
    return data

def prop_gen(x):
    
    try:
        return  x.split("|")[2]
    except:
        return ""

def update_genderdict(data, personal, gender_dict):
    
    pers = [x for x in personal if x not in gender_dict.keys()]
    
    for cor in pers:

        mentions = list(data[(data.named_coref == cor) & (data.pos.isin(["PPER","PPOSAT"]))].morph)
        gender = [x.split("|")[2] for x in list(mentions)]
        gender = [x for x in gender if x in ["Masc","Fem"]]
        
        try:
            gender_dict[cor] = most_common(gender)
        except ValueError:
            pass
        
    return gender_dict

def correct_gender(data, gender_dict):
    
    candidates = data[(data.named_coref.isin(gender_dict.keys())) & (data.pos.isin(["PPER","PPOSAT"]))]

    mistakes = []
    for index, row in candidates.iterrows():

        gen = gender_dict[row["named_coref"]]
        info = row["morph"].split("|")

        if "Masc" not in info and "Fem" not in info:
            continue

        if gen not in info:

            mistakes.append([index, oppose(gen)])

    lookup = data[(~data.named_coref.isna()) & (data.ner == "PER")]
    inds = np.array(lookup.index)
    corrections = []

    for mis in mistakes:

        lookup["offset"] = np.abs(inds-mis[0])


        for index, row in lookup.iterrows():
            try:
                
                if gender_dict[row["named_coref"]] == mis[1]:
                    corrections.append([mis[0], row["named_coref"]])
                    break
            except KeyError:
                # named entities without gender ;()
                pass
                
    for c in corrections:

        data.loc[c[0], "named_coref"] = c[1]
        
    return data
