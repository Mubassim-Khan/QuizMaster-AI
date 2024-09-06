from setuptools import find_packages,setup

setup(
    name='mcqGenrator',
    version='0.0.1',
    author='Mubassim Ahmed Khan',
    install_requires=["openai","langchain","streamlit","python-dotenv","langchain-community","pypdf"],
    packages=find_packages()
)