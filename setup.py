from setuptools import setup, find_packages

execfile('csv2html/__init__.py')

setup(
    name='csv2html',
    version=__version__,
    description='A flexible utility to convert CSV files into HTML tables.',
    url='http://github.com/dbohdan/csv2html',
    author='dbohdan',
    author_email='dbohdan@dbohdan.com',
    license='BSD',
    packages=find_packages(),
    data_files=[('', ['LICENSE', 'README.md'])],
    zip_safe=False,
    install_requires=[
            'argparse',
            'html',
        ],
    entry_points={
        'console_scripts': [
            'csv2html = csv2html.csv2html:main',
        ],
    }
)
