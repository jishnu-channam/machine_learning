from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation

def main():
    try:
        pipeline = Pipeline() 
        pipeline.run_pipeline()
        # # data_validation_config = Configuration().get_data_transformation_config()
        # # print(data_validation_config)
        # schema_file_path = r"/Users/jishnuch/machine_learning/config/schema.yaml"
        # file_path = r"/Users/jishnuch/machine_learning/housing/artifact/data_ingestion/2024-03-22_08-15-03/ingested_data/train/housing.csv"
         
        # df = DataTransformation.load_data(file_path, schema_file_path)
        # print(df.columns)
        # print(df.dtypes)
        
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()

