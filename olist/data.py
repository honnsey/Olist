import os
import pandas as pd

class Olist():
    def get_data(self):
        '''
        return contents of the olist dataset in dictionary format.
        '''

        # Specify path to csv files
        relative_path = "data-challenges/04-Decision-Science/data/csv"
        parent_path = os.path.dirname(os.getcwd())
        csv_path = os.path.join(parent_path, relative_path)

        # Extract file names from directory
        file_names = os.listdir(path = csv_path)
        file_names.remove( '.gitkeep')

        # Create key names from file name, remove "olist, dataset and .csv"
        key_names = [name.replace("olist_","") for name in file_names]
        key_names = [name.replace("_dataset","") for name in key_names]
        key_names = [name.replace(".csv","") for name in key_names]

        # store data in dictionary
        data = {key_name : pd.read_csv(os.path.join(csv_path, file_name))
                for key_name, file_name in zip(key_names,file_names)}


        return data

if __name__ == '__main__':
    print(Olist().get_data())
