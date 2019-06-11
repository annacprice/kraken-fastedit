#!/usr/bin/env python3

import sys
import os
import requests
import re
import argparse

#-----------------------------------------------------------------------------------
def get_taxid(taxon):

    response = requests.get("https://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/scientific-name/{0}".format(taxon))

    if response.status_code == 200:
        data = response.json()
        taxid = data[0]["taxId"]
        print("Success! Taxon information has been retrieved from the ENA.")
        print("Tax ID of " + taxon + " is:")
        print(taxid)
    else:
        print("ERROR: Taxon not found. Do you want to input the taxonomic ID manually? [y/n]")
        taxid = taxid_manual(answer=None)

    return taxid
#-----------------------------------------------------------------------------------
def taxid_manual(answer=None):

    yes = ("yes", "y", "ye")
    no = ("no", "n")

    while answer not in (yes, no):
        answer = input().lower()
        if answer in yes:
            answer = yes
            print("Please enter the taxonomic ID:")
            taxid = input()
        elif answer in no:
            print("Program aborted.")
            exit()
        else:
            print("Please enter yes or no:")

    return taxid
#-----------------------------------------------------------------------------------
def edit_fasta(infasta, outfasta, taxon, **kwargs):

    taxid = get_taxid(taxon)


    for fasta in os.listdir(infasta):
        fileExtension = fasta.split(".")[-1]
        if fileExtension == "fasta":
            fastFile = infasta + fasta
            with open(fastFile) as file:
                 print("Editing " + fastFile + " and saving to " + outfasta + taxid + "_" + fasta)
                 fastData = file.read()
                 fastEdit = re.sub(r"(>.+)",r"\1|kraken:taxid|{0}".format(taxid), fastData)
                 fastFileN = outfasta + taxid + "_" + fasta
                 fastFileN = open(fastFileN, "w")
                 fastFileN.write(fastEdit)

    print("Done.")
#-----------------------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser()
    parser.set_defaults(method=edit_fasta)
    parser.add_argument("-i", "--input-dir", dest="infasta", required=True, 
                    help="Path to the input fasta files")
    parser.add_argument("-o", "--output-dir", dest="outfasta", required=True,
                    help="Path for the output fasta files")
    parser.add_argument("-t", "--taxon-name", dest="taxon", required=True,
                    help="Name of the taxon")

    args = parser.parse_args()
    args.method(**vars(args))


if __name__ == "__main__":
    main()
