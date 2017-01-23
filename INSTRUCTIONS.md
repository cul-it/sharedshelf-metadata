# Instructions for Running Analysis Scripts

## Overview

Basically, the analysis scripts here run by first harvesting a full data dump of Artstor data, across collections, from the SharedShelf API. This is stored locally. Then, the analyses occur by running the analysis scripts (with some options available for type of analysis) on that data dump. This generates reports across all collections unless explicitly set in the analysis options.

To speed up this process, we're working on a hosted version of these analysis scripts that copies the data dumps to a database that is then queried (in place of pulling full json data onto your local system).

## Workflow

### Check Python, Pip, VirtualEnv Installation/Versions

This script was built with Python 3.5, but should work for Python >=2.7 or >=3.3.

Check Python is installed and what version(s) are available.

```bash
$ python --version
```
Should return something like:

```bash
$ Python 3.5.1
```
Clone this repository (https://github.com/cul-it/sharedshelf-metadata.git) where you would like to keep it (for example, I keep it in a directory called 'Projects'), then in your shell / command line tool, change into the directory for this repository, then create a virtualenv with the Python version you prefer:

```bash
$ cd ~/Projects/sharedshelf-metadata
$ virtualenv venv
```
If you want to specific a particular Python version that is not the default, use the following command instead:

```bash
$ cd ~/Projects/sharedshelf-metadata
$ virtualenv -p /usr/local/bin/python venv
```
Where '/usr/local/bin/python' points to the response of 'which python' or 'which python3', etc.

You should only have to do the above once, whereas the follow should be redone when you run the scripts or need to capture updates.

### Activate the Python Virtual Environment (if using)

Python virtual environments enable you to isolate the Python options (version used, libraries used, version of libraries used) to a particular working area or project. This is helpful if you don't want to change any global settings on your computer - which often, you don't.

```bash

```

### Harvest the data from the SharedShelf API

You only need to run this as often as you want the most recent data. It can take a while and can take up considerable space on your local machine, so consider re-writing the same file with the most recent data (instead of saving multiple data dumps).

```bash

```