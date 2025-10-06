SETUP_PY = """
from setuptools import setup, find_packages

setup(
    name="optimization_algorithms",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.4.0',
        'pandas>=1.3.0',
        'seaborn>=0.11.0',
        'tqdm>=4.62.0',
    ],
    author="Tmimi Ines ",
    description="Comparaison d'algorithmes d'optimisation métaheuristiques",
    python_requires='>=3.8',
)
"""