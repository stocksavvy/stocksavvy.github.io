"""
Insta485 python package configuration.

Sahil Dogra <dogras@umich.edu>
"""

from setuptools import setup

setup(
    name='predictor',
    version='0.1.0',
    packages=['predictor'],
    include_package_data=True,
    install_requires=[
        'Flask==1.1.1',
        'nodeenv==1.3.5',
        'pylint==2.4.4',
        'requests==2.22.0',
        'sh==1.12.14',
    ],
)