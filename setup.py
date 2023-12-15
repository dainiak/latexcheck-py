from setuptools import setup, find_packages

setup(
    name='latexcheck',
    version='1.2.5',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': ['latexcheck=latexcheck:main']
    },
    install_requires=[
        'texsoup>=0.3.1'
    ],
    python_requires='>=3.8',
    author='Alex Dainiak',
    author_email='dainiak@gmail.com',
    description='LaTeX linter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/dainiak/latexcheck-py/',
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)