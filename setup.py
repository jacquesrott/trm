from setuptools import setup, find_packages


with open('README.md') as f:
    description = f.read()

setup(
    name='trm',
    version='0.1',
    description='Markdown import export in trello',
    long_description=description,
    author='Jacques Rott',
    author_email='jacques.rott@gmail.com',
    maintainer='Jacques Rott',
    maintainer_email='jacques.rott@gmail.com',
    packages=find_packages(),
    install_requires=[
        'py-trello',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'trm = trm.cli.main:main'
        ]
    }
)
