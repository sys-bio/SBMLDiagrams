from setuptools import setup, find_packages
import os.path
import sys
import codecs

with open("README.md", "r") as fh:
    long_description = fh.read()

# The following two methods were copied from
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            print (line)
            delim = '"' if '"' in line else "'"
            print ('delim = ', delim)
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='SBMLDiagrams',
    packages=['SBMLDiagrams'],
    version=get_version('SBMLDiagrams/_version.py'),
    description='Visualize, edit and write SBML files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jin Xu, Jessie Jiang, Herbert M. Sauro',
    author_email='jxu2019@uw.edu',
    url='https://github.com/sys-bio/SBMLDiagrams',
    license='MIT License',
    install_requires=[
        'coverage',
        'pip>20',
        'numpy',
        'pandas',
        'python-libsbml',
        'simplesbml',
        'skia-python',
        'Ipython',
        'Pillow',
        'setuptools',
        'openpyxl',
        'opencv-python',
        'networkx',
        'matplotlib'
    ],

    #scripts=[''],# The name of your scipt, and also the command you'll be using for calling it
    include_package_data=True,
    classifiers=[
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 3.8',
       'Programming Language :: Python :: 3.9',
       'Programming Language :: Python :: 3.10',
       'Programming Language :: Python :: 3.11',
       'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
