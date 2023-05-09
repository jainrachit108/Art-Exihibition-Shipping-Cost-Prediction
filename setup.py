from setuptools import find_packages,setup

REQUIREMENT_FILE = 'requirements.txt'
HYPHEN_E_DOT = '-e .'

def get_requirements():
    with open(REQUIREMENT_FILE, 'rb') as req_file:
        requirement_list = req_file.readlines()

    requirement_list = [requirement.replace('\n','')  for requirement in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
        
    return requirement_list

setup(
    name= 'Shipping Cost Prediction',
    version="0.0.1",
    author= 'Rachit',
    author_email='jainrachit124@gmail.com',
    package = find_packages(),
    install_requires = get_requirements()
)
    
