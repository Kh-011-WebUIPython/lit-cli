# LitVCS
The project “LIT” is a version control system. Project tracks all changes in local files and compares these files with files stored on the remote server. Basically “LIT” can be used as source code management, but you can store any files you want.

## Goal
* The main goal is to create a new version control system with command line interface and web-based user interface.
* Another goals of the new system:
* Store the history of documents;
* Track files’ changes;
* Availability to get remote access to the files;
* Teams can work on one project;
* User-friendly interface;
* Simple to understand and work with LIT;
* Easy to start using if you have no previous experience with VCS.

## Installation

### PyPI
To install LitVCS, run this command in your terminal:
```sh
$ pip install litvcs
```
This is the preferred method to install LitVCS, as it will always install the most recent stable release.

### Source files
In case you downloaded or cloned the source code from [GitHub] or your own fork, you can run the following to install cameo for development:

```sh
$ git clone https://github.com/Kh-011-WebUIPython/lit-cli
$ cd lit-cli
$ pip install --editable .
```
**Note**: _Don't forget about 'sudo'!_

## Basic Usage
Available command list:
```sh
$ lit -h
usage: lit [-h] {add,commit,diff,init,log,rm,status} ...

LIT version control system

positional arguments:
  {add,commit,diff,init,log,rm,status}
    add                 adds files to staging area
    commit              commits files from staging area to repository
    diff                shows difference between two files
    init                initializes repository in the current directory
    log                 shows lit log
    rm                  removes files from staging area
    status              shows repository state

optional arguments:
  -h, --help            show this help message and exit
```


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Kh-011-WebUIPython/lit-cli/blob/master/LICENSE) file for details

Copyright (c) 2017 - SoftServe Academy

[GitHub]: <https://github.com/Kh-011-WebUIPython/lit-cli>