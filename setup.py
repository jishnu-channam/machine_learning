from setuptools import setup
from typing import List
# Declaring variables for setup functions

    
PROJECT_NAME = "housing_predictor"
PROJECT_VERSION = "0.0.1"
AUTHOR = "Jishnu"
DESCRIPTION = "This is a package to predict the price of a house based on certain features."
PACKAGES = ["housing"]
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list() -> List[str]:

    """ This function reads the requirements from the requirement file and returns a list of requirements.
    Thiis function is going to return a list which contains name od libraries mentioned in requirements.txt file.
    """

    with open(REQUIREMENT_FILE_NAME) as f:
        return f.read().splitlines()

setup(
    name = PROJECT_NAME,
    version = PROJECT_VERSION,
    author = AUTHOR,
    description = DESCRIPTION,
    packages = PACKAGES,
    install_requires = get_requirements_list()
)

if __name__ == "__main__":
    print(get_requirements_list())