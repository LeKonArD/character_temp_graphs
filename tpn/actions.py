import pandas as pd
import numpy as np

def get_interactions(data, personal):
    
    verb_dict = {}
    obj_dict = {}
    const_dict = {}
    
    for pers in personal:
        
        v = []
        o = []
        c = []
        
        for s in set(data.sent):
        
            chunk = data[data.sent == s].loc[:,["token","pos","head","upos",
                                                "lemma", "deprel","anys","named_coref"]]
            chunk["ind"] = list(range(1, len(chunk)+1, 1))
            chunk.index = chunk["ind"]
            
            try:
                r1 = passive_subject(chunk, pers)
            except:
                pass
            try:
                r2 = active_subject(chunk, pers)
            except:
                pass
            v += r1[0]+r2[0]
            o += r1[1]+r2[1]
            c += r1[2]+r2[2]
            
        verb_dict[pers] = v
        obj_dict[pers] = o
        const_dict[pers] = c
        
    return verb_dict, obj_dict, const_dict

def passive_subject(chunk, cor):

    verben = []
    obj = []
    const = []
    
    # 1
    anchors = chunk[(chunk["named_coref"] == cor) & (chunk.deprel.isin(["obja"])) & (chunk.anys == "no")]

    for index, head in anchors.iterrows():

        cand = chunk.loc[head["head"],:]

        if cand["upos"] == "VERB":
            verben.append(cand["lemma"])
            obj.append(head.token)
            const.append(cand["lemma"]+" "+head.token)
            
        if cand["upos"] == "AUX":
            
            derived_cand = chunk[(chunk["head"] == cand["ind"]) & (chunk["upos"] == "VERB")]
            
            for index, derived_c in derived_cand.iterrows():
            
                verben.append(derived_c.lemma)
                obj.append(head.token)
                const.append(cand["lemma"]+" "+head.token)
                               
    return verben, obj, const


def active_subject(chunk, cor):

    verben = []
    obj = []
    const = []
    
    # 1
    anchors = chunk[(chunk["named_coref"] == cor) & (chunk.deprel.isin(["pn", "subj"])) & (chunk.anys == "no")]

    for head in anchors["head"]:

        cand = chunk.loc[head,:]

        if cand["upos"] == "VERB":
            verben.append(cand["lemma"])
            objects = list(chunk[(chunk["head"] == cand["ind"]) & (chunk["deprel"] == "obja")].token)
            if len(objects) != 0:
                for o in objects:
                    obj.append(o)
                const.append(cand["lemma"]+" "+" ".join(objects))
        
        if cand["upos"] == "AUX":
            
            derived_cand = chunk[(chunk["head"] == cand["ind"]) & (chunk["upos"] == "VERB")]
  
            
            for index, derived_c in derived_cand.iterrows():
            
                verben.append(derived_c.lemma)
                objects = list(chunk[(chunk["head"] == derived_c["ind"]) & (chunk["deprel"] == "obja")].token)
                
                if len(objects) != 0:
                    for o in objects:
                        obj.append(o)
                    const.append(derived_c["lemma"]+" "+" ".join(objects))
                    
    return verben, obj, const