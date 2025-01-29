from setuptools import setup, find_packages

setup(
name = "uno_game",
version ='0.1.0',

packages=find_packages(include=["src", "src.*", "DQN", "DQN*", "QLearning", "QLearning*"]),
install_requires=[
    'pandas',
    'numpy',
    'pygame',
    'torch==2.5.1',
    'torchrl==0.6.0',
    'tensordict==0.6.1',
    'scipy',
    'matplotlib',
    ],
    python_requires='>=3.10',
)
