# **FastEdit**


Edits the sequence IDs in fasta files into the format required for building custom databases with Kraken (e.g. >sequenceID|kraken:taxid|1773).


## **Requirements**

FastEdit requires python 3.x

The following python packages are prerequisites:
- requests


## **Usage**
```
usage: fastedit.py [-h] -i INFASTA -o OUTFASTA -t TAXON

optional arguments:
  -h, --help            show this help message and exit
  -i INFASTA, --input-dir INFASTA
                        Path to the input fasta files
  -o OUTFASTA, --output-dir OUTFASTA
                        Path for the output fasta files
  -t TAXON, --taxon-name TAXON
                        Name of the taxon
```


The program pulls down the taxonomic ID from the ENA. The name of the taxon must be specified through the -t flag. E.g. to modify the sequence IDs for the taxon Mycobacterium tuberculosis you would run
```
python fastedit.py -i /path/to/the/input/fasta -o /path/to/the/output/fasta -t "mycobacterium tuberculosis"
```
If the taxon isn’t found, the program will prompt you to input the taxonomic ID manually through the command line.
