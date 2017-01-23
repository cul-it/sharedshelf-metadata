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

The response of the above should look like this:

```bash
$ virtualenv venv
Using base prefix '/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5'
New python executable in venv/bin/python3.5
Also creating executable in venv/bin/python
Installing setuptools, pip, wheel...done.
```

You should only have to do the above once, whereas the follow should be redone when you run the scripts or need to capture updates.

### Activate the Python Virtual Environment & Install Script Requirements

Python virtual environments enable you to isolate the Python options (version used, libraries used, version of libraries used) to a particular working area or project. This is helpful if you don't want to change any global settings on your computer - which often, you don't.

Each time you want to run the scripts, you'll want to first activate/start up your virtual environment. Within the top level of the sharedshelf-metadata directory on your computer, run the following:

```bash
$ source venv/bin/activate
```
Depending on your shell / command line client, you will see something indicating your working in the 'venv' virtual environment now:

```bash
(venv) $
```

Install all the Python scripts library requirements to this virtual environment. Note: you should only ever have to run this command once when you start and then whenever there are updates to the scripts:

```bash
(venv) $ pip install -r requirements.txt
Requirement already satisfied: requests==2.12.5 in ./venv/lib/python3.5/site-packages (from -r requirements.txt (line 1))
```
The response will tell you either if something was installed or if it was already installed.

### Harvest the data from the SharedShelf API

With your virtual environment running, you're ready to go.

You only need to run the harvest script as often as you want the most recent data. It can take a while and can take up considerable space on your local machine, so consider re-writing the same file with the most recent data (instead of saving multiple data dumps).

From the top-level of the sharedshelf-metadata directory on your computer, run:

```bash
(venv) $ python scripts/artstorharvest.py -e cmh329@cornell.edu -p yourPassword -o data/output.json
```

Fill this is with your email, your SharedShelf password, and the place where you'd like to store the data dump locally (here, it is "data/output.json"). The response should be like the following:

```bash
(venv) $ python scripts/artstorharvest.py -e cmh329@cornell.edu -p yourPassword -o data/output.json
Writing records to data/output.json from SharedShelf.
Retrieving project Obama Visual Iconography
Retrieving project Political Americana
Retrieving project Vicos
Retrieving project Billie Jean Isbell
...
```

What this script does is first query for all the unique collections in our SharedShelf instance, then iterate over each collection to grab the data. The data grabbed for each collection describes each digital object therein and, where possible, matches the collection-specific metadata field code to the metadata field text name. Where there isn't a text name for the metadata field in the collection, the field code is returned.

This can take up to 10 minutes to run. Wait until it is complete before moving to analysis.

### Analyze Your Local SharedShelf API Data dump

The most basic analysis to run is an analysis report for all metadata fields in your data dump and how often records with those fields appears. To do this, with your virtual environment activated and in the top level of the sharedshelf-metadata directory on your computer:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json
```

The script should then alert you that it is iterating through the records with this output:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json
1000 records processed
2000 records processed
3000 records processed
4000 records processed
5000 records processed
6000 records processed
7000 records processed
...
ARTstor Earliest Date: |===                      |  42093/296363 |  14%
           ARTstor Id: |                         |   7334/296363 |   2%
  ARTstor Latest Date: |===                      |  42093/296363 |  14%
       Accession Date: |                         |   6254/296363 |   2%
     Accession Number: |========                 |  95043/296363 |  32%
   Accession Sequence: |                         |    907/296363 |   0%
     Acquisition Date: |                         |   5780/296363 |   1%
    Acquisition Notes: |                         |   5780/296363 |   1%
               Active: |=====                    |  67611/296363 |  22%
Additional Imaging Notes: |                         |     81/296363 |   0%
     Additional Notes: |=                        |  14926/296363 |   5%
Additional Physical Form: |                         |   3443/296363 |   1%
Adler Notes (transcribed): |                         |   2432/296363 |   0%
 Administrative Notes: |                         |   3446/296363 |   1%
Agent_Display.display_value: |==                       |  30871/296363 |  10%
  Agent_Display.links: |==                       |  30871/296363 |  10%
      Alternate Title: |                         |   3149/296363 |   1%
      Analog Creators: |                         |    189/296363 |   0%
                Angle: |                         |   2234/296363 |   0%
       Appraisal Date: |                         |    114/296363 |   0%
       Appraisal Firm: |                         |    247/296363 |   0%
       Appraisal Note: |                         |      9/296363 |   0%
             Approval: |                         |   7620/296363 |   2%
Architect Culture (nationality): |                         |    147/296363 |   0%
       Architect Date: |                         |    184/296363 |   0%
Architect Earliest Date: |                         |    147/296363 |   0%
Architect Latest Date: |                         |    147/296363 |   0%
Architect.display_value: |                         |    233/296363 |   0%
      Architect.links: |                         |    233/296363 |   0%
      ...
```

What this analysis report offers each field (as mapped to a text label where it exists in that collection's API assets response), then a visual and numberic indicator of how many records have this field in the whole dataset.