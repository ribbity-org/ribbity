from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

CLASSIFIERS = [
    "Environment :: Console",
    "Environment :: MacOS X",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

setup(
    name="ribbity",
    description="convert github issues into a mkdocs site",
    url="https://github.com/ctb/ribbity",
    author="C. Titus Brown",
    author_email="titus@idyll.org",
    license="BSD 3-clause",
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    entry_points={"console_scripts": ["ribbity  = ribbity.__main__:main"]},
    include_package_data=True,
    package_data={"ribbity": []},
    setup_requires=[
        "setuptools>=38.6.0",
        "setuptools_scm",
        "setuptools_scm_git_archive",
    ],
    use_scm_version={"write_to": "ribbity/version.py"},
    install_requires=["click",
                      "pygithub",
                      "mkdocs",
                      "tomli",
                      "jinja2",
                      "pyyaml",
                      "pytest"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
