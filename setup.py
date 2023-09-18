"""setup file for giganttic """

from setuptools import setup

setup(
    name='giganttic',
    version='0.1.0',
    description='A python gantt chart package, mostly using pandas and matplotlib patches',
    url='https://github.com/adlhancock/giganttic',
    author='David Hancock',
    author_email='adlhancock@gmail.com',
    license='MIT',
    packages=['giganttic'],
    install_requires=['matplotlib',
                      'pandas',
                      'openpyxl',
                      'xml2dict',
                      'tkinter',
                      'numpy',
                      ],
    )
