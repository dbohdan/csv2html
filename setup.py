from setuptools import setup, find_packages

from csv2html import __version__

setup(
    name='csv2html',
    version=__version__,
    description='A flexible utility to convert CSV files into HTML tables.',
    url='http://github.com/dbohdan/csv2html',
    author='dbohdan',
    author_email='dbohdan@dbohdan.com',
    license='BSD',
    packages=['csv2html'],
    data_files=[('', ['LICENSE', 'README.md'])],
    zip_safe=False,
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'csv2html = csv2html.csv2html:main',
        ],
    }
)
