from setuptools import setup

import pickapic

setup(
    name='pickapic',
    version=pickapic.__version__,
    url='https://github.com/andrey-nakin/pickapic/',
    license='Apache License Version 2.0',
    author='Andrey Nakin',
    author_email='andrey.nakin@gmail.com',
    description='A command line tool that downloads a random photo from a public image hosting',
    packages=['pickapic'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python'
    ],
    scripts=['pickapic/__main__.py']
)
