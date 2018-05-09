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
Get pip: See this link: http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/ (scroll down to Install Pip section).

Clone this repository (https://github.com/cul-it/sharedshelf-metadata.git) where you would like to keep it (for example, I keep it in a directory called 'Projects'), then in your shell / command line tool, change into the directory for this repository, then create a virtualenv with the Python version you prefer:

```bash
$ git clone --recursive https://github.com/cul-it/sharedshelf-metadata.git
 ( output should show materials being copied/cloned to your local computer )
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

You only need to run the harvest script as often as you want the most recent data. It can take a while and can take up considerable space on your local machine, so consider re-writing the same file with the most recent data (instead of saving multiple data dumps). You'll also want to make sure you grab the latest code changes each time before starting.

From the top-level of the sharedshelf-metadata directory on your computer, run:

```bash
(venv) $ git submodule update --recursive --remote
(venv) $ python metadataQA/harvest/harvestSharedShelf.py -e cmh329@cornell.edu -p yourPassword -o data/output.json
```

Fill this is with your email, your SharedShelf password, and the place where you'd like to store the data dump locally (here, it is "data/output.json"). The response should be like the following:

```bash
(venv) $ python metadataQA/harvest/harvestSharedShelf.py -e cmh329@cornell.edu -p yourPassword -o data/output.json
Writing records to data/output.json from SharedShelf.
Retrieving project Obama Visual Iconography
Retrieving project Political Americana
Retrieving project Vicos
Retrieving project Billie Jean Isbell
...
```

What this script does is first query for all the unique collections in our SharedShelf instance, then iterate over each collection to grab the data. The data grabbed for each collection describes each digital object therein and, where possible, matches the collection-specific metadata field code to the metadata field text name. Where there isn't a text name for the metadata field in the collection, the field code is returned.

This can take up to 10 minutes to run. Wait until it is complete before moving to analysis.

### Analyze Your Local SharedShelf API Data - Overall View

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

### Analyze Your Local SharedShelf API Data - Field Specific

Another analysis (or set of analyses) you can run on this SharedShelf data is to see field-specific queries. These come in the follow structures:

#### Return all values of a certain field

Use the field names as they appear in the above output (including Field.Subfield structures as they appear):

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -e 'Architect Date'
1896-1966
1895-1960
1925-1996
1919-2013
1930-
1905-1981
1936-
1920-2005
1891-1957
1940-2012
1940-2012
1940-2012
1895-1960
1940-2012
1880-1938
...
```

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -e 'Work Type.links'
AAT-300046159
AAT-300005768
AAT-300047806
AAT-300128359
AAT-300006902
AAT-300008059
AAT-300007466
AAT-300007423
AAT-300047090
AAT-300053622
AAT-300033618
AAT-300128359
AAT-300060417
AAT-300128359
AAT-300041365
AAT-300053242
AAT-300041349
AAT-300128343
AAT-300033618
...
```

#### Return all unique values / values with counts / values with a certain value from a certain field

We can add a bit of bash after our query to limit the response to only unique values ...

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -e 'Image_Title' | uniq
Detail, trapezoidal shaped grid holding marble panels, corner of facade
Statue of George IV, intersection of Hanover and George St., looking east to St. Andrew\'s Square; Royal Society of Edinburgh at right
Painted plaster wall (colors: tan)
Landscaped grounds by the firm of Hanna Olin, Ltd. (name changed in 1996 to Olin Partnership); exterior view of fiberglass panels
Detail, figures in the clouds representing angels and the Holy Spirit
Marble carriageway carved with imperial motifs, detail, clouds
Altar-like fountain, front view
Courtyard building, detail of roof
Model on site showing the 2010-2011 expansion project
Detail, figure of Jean de Fiennes, the youngest burgher
Site plan of Zhongshan Park, photographed on site
Carved and painted niches of the wall west of the central pillar
View of a typical entry
...
```

Or to get unique values with a count of how many times they appear in our dataset:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -e 'Location.display_value' | sort | uniq -c
119
  1
  1   Akureyri
  1   Egypt,  Holmes,  Mississippi,  United States
  1   Florence,  Lauderdale,  Alabama,  United States
  1   Florida,  United States
  1   Iceland
  1  Alexandria Bay
  2  Alexandria, Alexandria, Virginia, United States
  1  Anniston, Calhoun, Alabama, United States
  1  Arkansas, United States
  1  Arlington, Middlesex, Massachusetts, United States
  1  Asheville, Buncombe, North Carolina, United States
  4  Aubervilliers, Seine-Saint-Denis, Île-de-France, France
  1  Bobigny, Seine-Saint-Denis, Île-de-France, France
  1  Boscawen, Merrimack, New Hampshire, United States
 15  Boston, Suffolk, Massachusetts, United States
  1  Bristol, Bristol, Virginia, United States
  1  Brookline, Norfolk, Massachusetts, United States
 15  Brooklyn, New York, New York, United States
  1  Bucine, Arezzo, Tuscany, Italy
  1  Camaiore, Lucca, Tuscany, Italy
 15  Cambridge, Middlesex, Massachusetts, United States
  1  Carteret, Middlesex, New Jersey, United States
  1  Chattanooga, Hamilton, Tennessee, United States
 35  Chicago, Cook, Illinois, United States
...
```

Or to get only those uniq values that have a certain value in the field output:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -e 'Measurements' | sort | uniq -c | grep "in."
2 width: 8.75 in; height: 9 in
4 width: 9 in; height: 11 in
8 width: 9 in; height: 11.5 in
2 width: 9 in; height: 11.75 in
2 width: 9 in; height: 12 in
2 width: 9 in; height: 12.5 in
4 width: 9 in; height: 13 in
42 width: 9 in; height: 5.5 in
2 width: 9 in; height: 5.75 in
2 width: 9 in; height: 9 in
2 width: 9 in; height: 9.25 in
...
```

#### Return all unique values / values with counts / values with a certain value with the record's SharedShelf ID

You can add the -i flag to any of the above queries to not just return a field's values, but to return the SharedShelf record id that the value comes from. The SharedShelf record identifiers returned are a concatenation of: CollectionID_RecordID:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -i -e 'Language' | sort
139_637452	Japanese|Dutch
139_637467	Japanese|Dutch
139_637481	Japanese|Dutch
139_637496	Japanese|Dutch
139_637512	Japanese|Dutch
139_637528	Japanese|Dutch
139_637543	Japanese|Dutch
139_637558	Japanese|Dutch
139_637573	Japanese|Dutch
139_637589	Japanese|Dutch
139_637604	Japanese|Dutch
139_637620	Japanese|Dutch
139_637636	Japanese|Dutch
139_637650	Japanese|Dutch
139_637665	Japanese|Dutch
...
```

Or you can add the -p flag to any of the above queries to return a 'True' or 'False' to indicate if the field is present in a record (with the -i flag used to tell us the record ID):

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -i -p -e 'ID Number'
1150_11239776 True
1150_11224502 True
139_629781 True
1150_11255159 True
1150_11259822 True
1150_11272656 True
695_12465715 True
695_12442738 True
98_319902 True
174_4045808 True
153_356182 True
209_770438 True
1150_11246218 True
1098_12810323 True
185_1316799 True
695_12439301 True
1150_11270923 True
...
```

Or combine all of the above for many different types of queries on the metadata. For example, show me the record identifiers for all records that do not have an ID Number field:

```bash
(venv) $ python scripts/artstor_analysis.py data/output.json -i -p -e 'ID Number' | grep 'False'
1098_12812420 False
1150_11221580 False
452_3385578 False
1150_11245562 False
185_1326334 False
185_1322972 False
2849_16824114 False
452_1974872 False
1168_11313474 False
893_13518077 False
185_1319586 False
185_1323006 False
922_10637225 False
1150_11259136 False
1150_11243404 False
746_8787381 False
695_12464694 False
1098_12815018 False
...
```

Note, there will probably be some errors that arise as one goes through all the query possibilities - just let Christina know and she'll try to update these scripts.
