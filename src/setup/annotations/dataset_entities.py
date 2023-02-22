# This module builds dictionaries containing entities that appear in the 
# traiining datasets used to train the NER model. The entities are associated
# with the respective KB identifier. For example the entity 'woman' is associated
# with the identifier 'Taxonomy ID: 9606' ('Homo spaiens').
# The generated dicts are concatenated with the synonym_to_id dict of the target
# KB

import json
import os
import sys
sys.path.append('./')


def get_annotations_from_pubtator(filename, ent_types):

    pubtator_annots = {}

    with open(filename, 'r') as ann_file:
        annotations = ann_file.readlines()
        ann_file.close()

        for line in annotations:

            line_data = line.split('\t')

            if len(line_data) == 6:

                if line_data[4] in ent_types:

                    kb_id = line_data[5].strip('\n')

                    if kb_id != '-1' and kb_id[:4] != 'OMIM':
                        pubtator_annots[line_data[3]] = 'MESH_' + kb_id

        
    return pubtator_annots


def get_annotations_from_brat(filename, ent_type):

    brat_annots = {}

    with open(filename, 'r') as ann_file:
        annotations = ann_file.readlines()
        #doc_id = filename.strip('.ann').strip('.a1')
        entity_tmp = ''
        found_entity = False
        kb_id = ''

        for line in annotations:

            if found_entity and line[0] == 'N':
                #print(line)
                kb_id = line.split('\t')[1].split(' ')[2].replace('MeSH:', 'MESH_')
                #print(line.split('\t'))
                brat_annots[entity_tmp] = kb_id
                found_entity = False
                #print(line)
            
            else:
                line_data = line.split('\t')
                ann_type = line_data[1].split(' ')[0]
                ann_text = line_data[2].strip('\n')
                
                if ann_type == ent_type:
                    #print(ann_type)
                    #print(line)
                    entity_tmp = ann_text
                    found_entity = True
                else:
                    found_entity = False

        ann_file.close()

    found_entity = False

    return brat_annots 


def get_annotations_from_craft(filename):

    craft_annots = {}

    with open(filename, 'r') as ann_file:
        annotations = ann_file.readlines()

        for line in annotations:
            line_data = line.split('\t')
            kb_id = line_data[1].split(' ')[0].replace(':', '_')
            text = line_data[2].strip('\n')
            
            if text not in craft_annots:
                #print(text, kb_id)
                craft_annots[text] = kb_id

        ann_file.close()
    
    return craft_annots


def build_annotations_dict(corpora_dir, out_dir, kb):

    entity_2_kb_id = {}

    # ------------------------------------------------------------------------
    #                       Import useful data from corpora
    # ------------------------------------------------------------------------
    
    #-------------------------- NCBI TAXON -----------------------------------
    if kb == 'ncbi_taxon':

        # CRAFT-NCBITaxon
        corpora_dir += 'CRAFT-4.0.1/concept-annotation/NCBITaxon/NCBITaxon/brat/'
        craft_files = os.listdir(corpora_dir)

        for filename in craft_files:

            if filename[-3:] == 'ann':
                file_annots = get_annotations_from_craft(corpora_dir + filename)
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        # Manully add some common entities
        entity_2_kb_id['woman'] = 'NCBITaxon_9606'
        entity_2_kb_id['women'] = 'NCBITaxon_9606'
        entity_2_kb_id['man'] = 'NCBITaxon_9606'
        entity_2_kb_id['men'] = 'NCBITaxon_9606'
        entity_2_kb_id['girl'] = 'NCBITaxon_9606'
        entity_2_kb_id['boy'] = 'NCBITaxon_9606'
        entity_2_kb_id['patient'] = 'NCBITaxon_9606'
        entity_2_kb_id['patients'] = 'NCBITaxon_9606'
        entity_2_kb_id['child'] = 'NCBITaxon_9606'
        entity_2_kb_id['children'] = 'NCBITaxon_9606'
        entity_2_kb_id['person'] = 'NCBITaxon_9606'
        entity_2_kb_id['people'] = 'NCBITaxon_9606'
        entity_2_kb_id['human'] = 'NCBITaxon_9606'
        entity_2_kb_id['humans'] = 'NCBITaxon_9606'
        entity_2_kb_id['individual'] = 'NCBITaxon_9606'
        entity_2_kb_id['mother'] = 'NCBITaxon_9606'
        entity_2_kb_id['father'] = 'NCBITaxon_9606'
        #print(entity_2_kb_id)
    #-------------------------- DISEASE -----------------------------------
    elif kb == 'medic':
        
        # BC5CDR - train and dev sets
        file_annots = get_annotations_from_pubtator(
            corpora_dir + 'CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.PubTator.txt',
            ['Disease']
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        file_annots = get_annotations_from_pubtator(
            corpora_dir + 'CDR_Data/CDR.Corpus.v010516/CDR_DevelopmentSet.PubTator.txt',
            ['Disease']
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        # NCBI Disease: all
        file_annots = get_annotations_from_pubtator(
            'data/NCBI_Disease/NCBItrainset_corpus.txt',
            ['DiseaseClass', 'SpecificDisease', 'Modifier']
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        file_annots = get_annotations_from_pubtator(
            'data/NCBI_Disease/NCBIdevelopset_corpus.txt',
            ['DiseaseClass', 'SpecificDisease', 'Modifier']
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        file_annots = get_annotations_from_pubtator(
            'data/NCBI_Disease/NCBItestset_corpus.txt',
            ['DiseaseClass', 'SpecificDisease', 'Modifier']
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

    #-------------------------- Chemical -----------------------------------
    elif kb == 'ctd_chem':
    
        # PHAEDRA
        phaedra_dir = corpora_dir + 'PHAEDRA_corpus/all/'
        phaedra_files = os.listdir(phaedra_dir)

        for filename in phaedra_files:

            if filename[-2:] == 'a1':
                file_annots = get_annotations_from_brat(phaedra_dir + filename, 'Pharmacological_substance')
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        # BC5CDR - train and dev sets
        file_annots = get_annotations_from_pubtator(
            corpora_dir + 'CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.PubTator.txt',
            'Chemical'
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        file_annots = get_annotations_from_pubtator(
            corpora_dir + 'CDR_Data/CDR.Corpus.v010516/CDR_DevelopmentSet.PubTator.txt',
            'Chemical'
        )
        entity_2_kb_id = {**entity_2_kb_id, **file_annots}

        #NLMChem
        nlmchem_dir = corpora_dir + 'chemical/NLMChem/chem_brat_identifiers/'
        nlmchem_dir_files = os.listdir(nlmchem_dir)

        for filename in nlmchem_dir_files:

            if filename[-3:] == 'ann':
                file_annots = get_annotations_from_brat(nlmchem_dir + filename, 'Chemical')
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}

    elif kb == 'chebi':

        # CRAFT-NCBITaxon
        corpora_dir += 'CRAFT-4.0.1/concept-annotation/CHEBI/CHEBI/brat/'
        craft_files = os.listdir(corpora_dir)

        for filename in craft_files:

            if filename[-3:] == 'ann':
                file_annots = get_annotations_from_craft(corpora_dir + filename)
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}

    elif kb == 'go_bp':

        # CRAFT-GO-BP
        corpora_dir += 'CRAFT-4.0.1/concept-annotation/GO_BP/GO_BP/brat/'
        craft_files = os.listdir(corpora_dir)

        for filename in craft_files:

            if filename[-3:] == 'ann':
                file_annots = get_annotations_from_craft(corpora_dir + filename)
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}

    elif kb == 'ncbi_gene':
        
        # CRAFT-PR
        corpora_dir += 'CRAFT-4.0.1/concept-annotation/PR/PR/brat/'
        craft_files = os.listdir(corpora_dir)

        for filename in craft_files:

            if filename[-3:] == 'ann':
                file_annots = get_annotations_from_craft(corpora_dir + filename)
                entity_2_kb_id = {**entity_2_kb_id, **file_annots}


    # ------------------------------------------------------------------------
    # Filter out the annotations that have an exact match in the target KB
    # ------------------------------------------------------------------------

    with open('../../data/kbs/dicts/{}/name_to_id.json'.format(kb), 'r') as dictfile1:
        name_to_id = json.load(dictfile1)
        dictfile1.close()
    
    with open('../../data/kbs/dicts/{}/synonym_to_id.json'.format(kb), 'r') as dictfile2:
        synonym_to_id = json.load(dictfile2)
        dictfile2.close()

    alt_id_to_id = {}

    if os.path.exists('../../data/kbs/dicts/{}/alt_id_to_id.json'):
        with open('../../data/kbs/dicts/{}/alt_id_to_id.json'.format(kb), 'r') as dictfile3:
            alt_id_to_id = json.load(dictfile3)
            dictfile3.close()
        
    with open('../../data/kbs/dicts/{}/id_to_name.json'.format(kb), 'r') as dictfile4:
        id_to_name = json.load(dictfile4)
        dictfile4.close()

    to_delete = []

    for entity in entity_2_kb_id.keys():

        if entity in name_to_id or entity in synonym_to_id:
            to_delete.append(entity) 

        kb_id = entity_2_kb_id[entity]
        
        if kb_id in alt_id_to_id.keys():
            kb_id = alt_id_to_id[kb_id]
            entity_2_kb_id[entity] = kb_id
       
        if kb_id not in id_to_name.keys() and kb != 'ncbi_taxon':
            to_delete.append(entity)
            
    
    to_delete_up = [entity for entity in set(to_delete)]
    
    for entity in to_delete_up:
        del entity_2_kb_id[entity]

    # ------------------------------------------------------------------------
    #                           Output the dictionary
    # ------------------------------------------------------------------------
    
    #output = json.dumps(entity_2_kb_id, indent=4, ensure_ascii=False)
    
    #with open(out_filename, 'w') as out_file:
    #    out_file.write(output)
    #    out_file.close()

    # ------------------------------------------------------------------------
    #     Concatenate the generated dict with the respective synonym_to_id
    # ------------------------------------------------------------------------

    synonyms_filepath = '../../data/kbs/dicts/{}/synonym_to_id.json'.format(kb)
    
    with open(synonyms_filepath, 'r') as synonyms_file:
        synonym_to_id = json.load(synonyms_file)
        synonyms_file.close()
    print(entity_2_kb_id)
    output_dict = {**synonym_to_id, **entity_2_kb_id}
    
    output = json.dumps(output_dict, indent=4, ensure_ascii=False)
    out_filename = out_dir + 'synonym_to_id_full.json'

    with open(out_filename, 'w') as out_file:
        out_file.write(output)
        out_file.close()


def generate_annotation_dict(kb):

    corpora_dir = '../NER_training/data/corpora/'
    out_dir = '../../data/kbs/dicts/{}/'.format(kb)

    build_annotations_dict(corpora_dir, out_dir, kb)