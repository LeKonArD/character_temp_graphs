
def get_scenes(data):
    
    sc = -1
    scenes = []
    deletions = []
    
    for index, row in data.iterrows():
        
        if row["token"] == "Szene":
            sc+=1
            deletions.append(index)
            continue
            
        else:
            
            scenes.append(sc)
    
    data = data.drop(deletions)
    data["scene"] = scenes
    
    return data


def postprocess_scenes(data, threshold):
    """
    merges small scenes to longer ones
 
    """
    sc = 0
    scenes = []
    buffer = ""
    i = 0
    for index, row in data.iterrows():
        
        
        
        if buffer != row["scene"] and i > threshold:
            i = 0
            sc+=1
            
            
        scenes.append(sc)
        i+=1
        
        buffer = row["scene"]
        
    data["long_scenes"] = scenes
    
    return data