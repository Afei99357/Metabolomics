# Author: Eric Liao
# April 2020

#!/usr/bin/env python3
"""This is used for convert xml file from hmdb.ca/downloads to csv file"""

import xml.etree.ElementTree as ET
import csv
import argparse

def convert_xml_2_csv(xml_filename, csv_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()

    #open a file for writing
    metabolites_data = open(csv_filename, 'w')

    #create the csv writer object
    csv_writer = csv.writer(metabolites_data)
    data_head = []

    count = 0

    for member in root.findall('{http://www.hmdb.ca}metabolite'):
        metabolites = []
        # create header for csv file
        if count == 0:
            accession = member.find('{http://www.hmdb.ca}accession').tag.split('}', 1)[1]
            data_head.append(accession)
            name = member.find('{http://www.hmdb.ca}name').tag.split('}', 1)[1]
            data_head.append(name)
            synonyms = member.find('{http://www.hmdb.ca}synonyms').tag.split('}', 1)[1]
            data_head.append(synonyms)
            chemical_formula = member.find('{http://www.hmdb.ca}chemical_formula').tag.split('}', 1)[1]
            data_head.append(chemical_formula)
            average_molecular_weight = member.find('{http://www.hmdb.ca}average_molecular_weight').tag.split('}', 1)[1]
            data_head.append(average_molecular_weight)
            monisotopic_molecular_weight = member.find('{http://www.hmdb.ca}monisotopic_molecular_weight').tag.split('}', 1)[1]
            data_head.append(monisotopic_molecular_weight)
            iupac_name = member.find('{http://www.hmdb.ca}iupac_name').tag.split('}', 1)[1]
            data_head.append(iupac_name)
            traditional_iupac = member.find('{http://www.hmdb.ca}traditional_iupac').tag.split('}', 1)[1]
            data_head.append(traditional_iupac)
            cas_registry_number = member.find('{http://www.hmdb.ca}cas_registry_number').tag.split('}', 1)[1]
            data_head.append(cas_registry_number)
            smiles = member.find('{http://www.hmdb.ca}smiles').tag.split('}', 1)[1]
            data_head.append(smiles)
            inchi = member.find('{http://www.hmdb.ca}inchi').tag.split('}', 1)[1]
            data_head.append(inchi)
            inchikey = member.find('{http://www.hmdb.ca}inchikey').tag.split('}', 1)[1]
            data_head.append(inchikey)

            csv_writer.writerow(data_head)
            count = count + 1

        # adding row value to csv file
        accession = member.find('{http://www.hmdb.ca}accession').text
        if accession is not None:
            # metabolites.append(accession.encode('utf-8'))
            metabolites.append(accession)
        else:
            accession = 'Nah'
            metabolites.append(accession)

        name = member.find('{http://www.hmdb.ca}name').text
        if name is not None:
            # metabolites.append(name.encode('utf-8'))
            metabolites.append(name)
        else:
            name = 'Nah'
            metabolites.append(name)

        number_of_synonym = len(member.find('{http://www.hmdb.ca}synonyms'))
        synonym_list = []
        if number_of_synonym > 0:
            for i in range(number_of_synonym):
                synonym_list.append(member.find('{http://www.hmdb.ca}synonyms')[i].text)
            synonyms_str = '|'.join(synonym_list)
            metabolites.append(synonyms_str)
        else:
            synonyms_str = 'Nah'
            metabolites.append(synonyms_str)

        chemical_formula = member.find('{http://www.hmdb.ca}chemical_formula').text
        if chemical_formula is not None:
            # metabolites.append(chemical_formula.encode('utf-8'))
            metabolites.append(chemical_formula)
        else:
            chemical_formula = 'Nah'
            metabolites.append(chemical_formula)

        average_molecular_weight = member.find('{http://www.hmdb.ca}average_molecular_weight').text
        if average_molecular_weight is not None:
            # metabolites.append(average_molecular_weight.encode('utf-8'))
            metabolites.append(average_molecular_weight)
        else:
            average_molecular_weight = 'Nah'
            metabolites.append(average_molecular_weight)

        monisotopic_molecular_weight = member.find('{http://www.hmdb.ca}monisotopic_molecular_weight').text
        if monisotopic_molecular_weight is not None:
            # metabolites.append(monisotopic_molecular_weight.encode('utf-8'))
            metabolites.append(monisotopic_molecular_weight)
        else:
            monisotopic_molecular_weight = 'Nah'
            metabolites.append(monisotopic_molecular_weight)

        iupac_name = member.find('{http://www.hmdb.ca}iupac_name').text
        if iupac_name is not None:
            # metabolites.append(iupac_name.encode('utf-8'))
            metabolites.append(iupac_name)
        else:
            iupac_name = 'Nah'
            metabolites.append(iupac_name)

        traditional_iupac = member.find('{http://www.hmdb.ca}traditional_iupac').text
        if traditional_iupac is not None:
            # metabolites.append(traditional_iupac.encode('utf-8'))
            metabolites.append(traditional_iupac)
        else:
            metabolites.append(traditional_iupac)

        cas_registry_number = member.find('{http://www.hmdb.ca}cas_registry_number').text
        if cas_registry_number is not None:
            # metabolites.append(cas_registry_number.encode('utf-8'))
            metabolites.append(cas_registry_number)
        else:
            cas_registry_number = 'Nah'
            metabolites.append(cas_registry_number)

        smiles = member.find('{http://www.hmdb.ca}smiles').text
        if smiles is not None:
            # metabolites.append(smiles.encode('utf-8'))
            metabolites.append(smiles)
        else:
            smiles = "Nah"
            metabolites.append(smiles)

        inchi = member.find('{http://www.hmdb.ca}inchi').text
        if inchi is not None:
            # metabolites.append(inchi.encode('utf-8'))
            metabolites.append(inchi)
        else:
            inchi = "Nah"
            metabolites.append(inchi)

        inchikey = member.find('{http://www.hmdb.ca}inchikey').text
        if inchikey is not None:
            # metabolites.append(inchikey.encode('utf-8'))
            metabolites.append(inchikey)
        else:
            inchikey = "Nah"
            metabolites.append(inchikey)

        csv_writer.writerow(metabolites)

    metabolites_data.close()

def main():
    parser = argparse.ArgumentParser(description="Reads factors for each sample and writes them into CSV file")
    parser.add_argument('--input_xml', help='xml file fetched from http://www.hmdb.ca', required=True)
    parser.add_argument('--output_csv', help='Output CSV file', required=True)
    args = parser.parse_args()

    xml_filename = args.input_xml
    csv_filename = args.output_csv

    convert_xml_2_csv(xml_filename, csv_filename)


if __name__ == '__main__':
    main()