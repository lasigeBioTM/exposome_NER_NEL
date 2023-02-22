# -*- coding: utf-8 -*-
import json
from src.utils import parse_bioc_json_file
from tqdm import tqdm


def ouput_json_dict(output, out_filename):
    
    output_json = json.dumps(output, indent=4)
        
    with open(out_filename, 'w') as outfile:
        outfile.write(output_json)
        outfile.close


def parse_litcovid():
    filename = 'data/corpora/litcovid2BioCJSON'

    # Open LARGE LITCOVID FILE WITH ALL THE ARTICLES

    invalid = 0

    with open(filename, 'r') as in_data:
        lines = in_data.readlines()
        
        for i, line in enumerate(lines):
            
            if 3 <= i:
                line = line[1:].strip(' ').rstrip()
                try:
                    doc = json.loads(line)
                    #print(doc['id'])
                    #if doc['id'] == '36374805':
                    #    print(doc)
                    #for passage in doc['passages']:
                    #    print(passage['infons'].keys())

                except:
                    invalid += 1

        in_data.close()


def add_entities_2_dict(entities, annot_dict):

    for entity_text in entities:
        entity_text = entity_text.lower()
        
        if entity_text in annot_dict:
            annot_dict[entity_text] += 1

        else:
            annot_dict[entity_text] = 1

    return annot_dict


def calculate_probabilites(total, annot_dict):

    for entity in annot_dict.keys():
        annot_dict[entity] = annot_dict[entity] / total
    
    return annot_dict


def parse_pubtator_annotations():

    data_dir = 'data/overlapping_entities/'
    filename = data_dir + 'bioconcepts2pubtatorcentral'
    #filename = data_dir + 'chemical2pubtatorcentral.sample'
        
    chem_dict = {}
    cell_line_dict = {}
    gene_dict = {}
    disease_dict = {}
    mutation_dict = {}
    species_dict = {}

    # Open the annotation file
    with open(filename, 'r') as in_file:
        lines = in_file.readlines()
        pbar = tqdm(total=len(lines))
        
        # Get frequency of each annotation
        for i, line in enumerate(lines):
            line_data = line.split('\t')
            kb_id = line_data[2]
            ent_type = line_data[1]
            entities = line_data[3].split('|')
            
            if ent_type == 'Chemical':
                add_entities_2_dict(entities, chem_dict)

            elif ent_type == 'CellLine':
                add_entities_2_dict(entities, cell_line_dict)

            elif ent_type == 'Gene':
                add_entities_2_dict(entities, gene_dict)

            elif ent_type == 'Disease':
                add_entities_2_dict(entities, disease_dict)

            elif ent_type == 'Mutation':
                add_entities_2_dict(entities, mutation_dict)

            elif ent_type == 'Species':
                add_entities_2_dict(entities, species_dict)

            pbar.update(1)
        
        in_file.close()
        pbar.close()

        total = len(chem_dict.keys()) + len(cell_line_dict.keys()) \
            + len(gene_dict.keys()) + len(disease_dict.keys()) \
            + len(mutation_dict.keys()) + len(species_dict.keys())

        chem_dict = calculate_probabilites(total, chem_dict)
        cell_line_dict = calculate_probabilites(total, cell_line_dict)
        gene_dict = calculate_probabilites(total, gene_dict)
        disease_dict = calculate_probabilites(total, disease_dict)
        species_dict = calculate_probabilites(total, species_dict)
        mutation_dict = calculate_probabilites(total, mutation_dict)

        ouput_json_dict(chem_dict, data_dir + 'chemical.json')
        ouput_json_dict(cell_line_dict, data_dir + 'cell_line.json')
        ouput_json_dict(gene_dict, data_dir + 'gene.json')
        ouput_json_dict(disease_dict, data_dir + 'disease.json')
        ouput_json_dict(species_dict, data_dir + 'species.json')
        ouput_json_dict(mutation_dict, data_dir + 'mutation.json')


parse_pubtator_annotations()
