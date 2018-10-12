from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pdover2t',
    version='0.0.1',
    description='Computational subsea pipeline engineering.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qwilka/PDover2t',
    author='Stephen McEntee',
    author_email='stephenmce@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Natural Language :: English',
    ],
    keywords='engineering computational',
    packages=find_packages(exclude=['docs']),
    python_requires='>=3.6',
    install_requires=[
        "toml",
    ],
)
