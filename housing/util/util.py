import yaml 
from housing.exception import HousingException
import os
import sys
import numpy as np
import dill 
import pandas as pd
from housing.constant import *



def read_yaml_file(file_path:str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary
    """
    try: 
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e, sys) from e
    
def save_numpy_array_data(file_path:str, array : np.array):
    """
    Saves a numpy array as a file
    file_path : str : File path to save the numpy array
    array : np.array : Numpy array to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            np.save(f, array)

    except Exception as e:
        raise HousingException(e, sys) from e

def load_numpy_array_data(file_path:str) -> np.array:
    """
    Loads a numpy array from a file
    file_path : str : File path to load the numpy array
    return : np.array : Numpy array loaded from the file
    """
    try:
        with open(file_path, "rb") as f:
            return np.load(f)
    except Exception as e:
        raise HousingException(e, sys) from e
    
def save_object(file_path:str, obj):
    """
    Saves a model as a file
    file_path : str : File path to save the model
    obj : object : Any sort of object
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            dill.dump(obj, f)

    except Exception as e:
        raise HousingException(e, sys) from e

def load_object(file_path:str):
    """
    Loads a model from a file
    file_path : str : File path to load the model
    return : object : Model loaded from the file
    """
    try:
        with open(file_path, "rb") as f:
            return dill.load(f)
    except Exception as e:
        raise HousingException(e, sys) from e
    
def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame: 
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEYS]
        dataframe = pd.read_csv(file_path)
        error_message = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])

            else:
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema."
        if len(error_message) > 0:
            raise Exception(error_message)
        return dataframe
        
    except Exception as e:
        raise HousingException(e, sys) from e