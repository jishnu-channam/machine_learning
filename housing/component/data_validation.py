from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os, sys
import evidently
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab 

from housing.util.util import read_yaml_file
import pandas as pd
import json 


class DataValidation: 

    def __init__(self, data_validation_config: DataValidationConfig, 
                 data_ingestion_artifact: DataIngestionArtifact):
        
        try: 
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def get_train_and_test_file(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise HousingException(e, sys) from e
        

    def is_train_test_file_exists(self):
        try:

            logging.info("Checking if train and test file exists") 
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_test_file_exists = os.path.exists(test_file_path)

            is_available = is_train_file_exists and is_test_file_exists
            logging.info(f"Is train and test file exists? -> {is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path 
                message = f"Training file : {training_file} or Testing file: {testing_file} does not exist"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e, sys) from e
        

    def validate_dataset_schema(self) -> bool:

        try: 
            validation_status = False

            # Assignment validate training and testing dataset using schema file 
            logging.info("Validating training and testing dataset using schema file")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            schema_file_path = self.data_validation_config.schema_file_path
            schema = read_yaml_file(schema_file_path)
            #1. Number of columns 
            logging.info("Checking number of columns in the dataset")
            num_columns_schema = len(schema['columns'])
            num_columns_train = len(train_df.columns)
            num_columns_test = len(test_df.columns)

            num_columns_status = num_columns_schema == num_columns_train and num_columns_schema == num_columns_test

            if num_columns_test:
                logging.info("Number of columns in the dataset is as expected")

            else:
                raise Exception("Number of columns in the dataset is not as expected")
            
            #2. Check the value of ocean proximity 
            logging.info("Checking the values in ocean proximity")
            train_ocean_list = list(train_df['ocean_proximity'].unique())
            test_ocean_list = list(test_df['ocean_proximity'].unique())
            schema_ocean_list = schema['domain_value']['ocean_proximity']

            for i in train_ocean_list:
                if i in schema_ocean_list:
                    continue
                else:
                    raise Exception(f"{i} is not in the schema")
            
            for i in test_ocean_list:
                if i in schema_ocean_list:
                    continue
                else:
                    raise Exception(f"{i} is not in the schema")
            
            logging.info("Values in ocean proximity is as expected")

            #3. Check Column names 

            logging.info("Checking column names in the dataset")
            schema_columns = list(schema['columns'].keys())
            train_columns = list(train_df.columns)
            test_columns = list(test_df.columns)

            for i in train_columns:
                if i in schema_columns:
                    continue
                else:
                    raise Exception(f"{i} is not in the schema")
            
            for i in test_columns:
                if i in schema_columns:
                    continue
                else:
                    raise Exception(f"{i} is not in the schema")
            
            logging.info("Column names in the dataset is as expected")

            validation_status = True
            
            return validation_status
        except Exception as e:  
            raise HousingException(e, sys) from e
        
    def get_and_save_data_drift_report(self):
        try:
            
            profile = Profile(sections = [DataDriftProfileSection()])

            train_df, test_df = self.get_train_and_test_file()

            profile.calculate(train_df, test_df)

            report = json.loads(profile.json())
            
            report_file_path = self.data_validation_config.report_file_path

            report_dir = os.path.dirname(report_file_path)

            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, 'w') as report_file:
                json.dump(report, report_file, indent= 6)
            return report 
            
        except Exception as e: 
            raise HousingException(e, sys) from e
        

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_and_test_file()
            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path

            report_page_dir = os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(report_page_file_path)
        
        except Exception as e:
            raise HousingException(e, sys) from e 

    def is_data_drift_found(self) -> bool:

        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e, sys) from e
        

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path = self.data_validation_config.schema_file_path,
                report_file_path = self.data_validation_config.report_file_path,
                report_page_file_path = self.data_validation_config.report_page_file_path,
                is_validated = True,
                message = "Data Validation completed successfully"
            )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
        except Exception as e:
            raise HousingException(e, sys) from e