import pandas as pd
import os

def replied_list(filepath):
        
        if not os.path.isfile(filepath):
                replied_database=pd.DataFrame(columns=['id','text', 'user','time'])
                replied_database.to_csv(filepath)
        else:
                replied_database = pd.read_csv(filepath)

        return replied_database

def prefix_list(filepath):
        
    with open(filepath, "r") as f:
        prefix_list = f.read()
        prefix_list = list(filter(None, prefix_list.split("\n")))

    return prefix_list