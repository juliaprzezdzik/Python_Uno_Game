from setuptools import setup, find_packages

setup(
name = "uno_game",
version ='0.1.0',

packages=find_packages(include=["src", "src.*"]))
# install_requires=[
#     'pandas',
#     'numpy',
#     'pygame',
#     'torch',
#     'tensordict',
#     'scipy',
#     ],
)