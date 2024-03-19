from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", 
                                 ["dataset_download_url", "tgz_download_dir", "raw_data_dir", 
                                  "ingested_train_dir", "ingested_test_dir"])

# 1 - Download url 
# 2 - Download folder (compressed file)
# 3 - Extracted folder (extracted file) 
# 4 - Train dataset folder 
# 5 - Test dataset folder 


   DataValidationConfig = namedtuple("DataValidationConfig", 
                                  ["schema_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["add_bedrooms_per_room",
                                                                   "transformed_train_dir", 
                                                                   "transformed_test_dir",
                                                                   "preprocesssed_object_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["training_model_file_path", "base_accuracy"])

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path", "time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])

