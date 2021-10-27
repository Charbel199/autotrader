from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "An automated trading software"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='AutoTrader',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/Charbel199/AutoTrader2',
    license='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Charbel Bou Maorun',
    author_email='charbel-boumaroun@outlook.com',
    description=DESCRIPTION
)
