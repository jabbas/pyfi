import os
from setuptools import setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return open(path).read()


setup(
    name="pyfi",
    version='0.1.0',
    author='Grzegorz Dzięgielewski',
    author_email='jabbas@jabbas.eu',
    description=('Grabs stocks data into influxdb'),
    long_description=read('README.md'),
    license='GPL3',
    keywords='stocks influxdb finance',
    packages=['pyfi'],
    entry_points={'console_scripts': 'pyfi = pyfi.cmd:cmd'},
)
