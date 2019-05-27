import sys
import os
import requests
import re

#-----------------------------------------------------------------------------------
def get_taxid(taxname):

    response = requests.get("https://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/scientific-name/{0}".format(taxname))

    if response.status_code == 200:
        data = response.json()
        taxid = data[0]["taxId"]
        print("Success! Taxon information has been retrieved from the EBI.")
        print("Tax ID of " + taxname + " is:")
        print(taxid)
    else:
        question = "ERROR: Taxon not found. Do you want to input the taxonomic ID manually? [y/n]"
        print(question)
        taxid = taxid_manual(question, answer=None)

    return taxid
#-----------------------------------------------------------------------------------
def taxid_manual(question, answer=None):

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
def edit_fasta(input, output):

    taxid = get_taxid(*sys.argv[1:])

    for fasta in os.listdir(input):
        fileExtension = fasta.split(".")[-1]
        if fileExtension == "fasta":
            fastFile = input + fasta
            with open(fastFile) as file:
                 print("Editing " + fastFile + " and saving to " + output)
                 fastData = file.read()
                 fastEdit = re.sub(r">.+",r">|kraken:taxid|{0}|".format(taxid), fastData)
                 fastFileN = output + fasta
                 fastFileN = open(fastFileN, "w")
                 fastFileN.write(fastEdit)

    print("Done.")
#-----------------------------------------------------------------------------------
def main(argv):

    input = "/data/"
    output = "/data/output/"

    edit_fasta(input, output)

if __name__ == "__main__":
    main(*sys.argv[1:])
