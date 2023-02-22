# -*- coding: utf-8 -*-
import orjson as json
import os
import networkx as nx
import sys
from kb import KnowledgeBase


def generate_dicts_4_kb(kb=None, mode='reel', terms_filename=None, 
        edges_filename=None, kb_filename=None, input_format=None):
    
    out_dir = 'data/kbs/dicts/{}/'.format(kb)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    kb_obj = KnowledgeBase(kb, mode, terms_filename=terms_filename, 
        edges_filename=edges_filename, input_format=input_format)
    
    #print(kb_obj.name_to_id)
    #print(kb_obj.graph.nodes)
    
    if mode == 'reel':
        name_to_id = json.dumps(kb_obj.name_to_id)
        
        with open(out_dir + '/name_to_id.json', 'wb') as outfile:
            outfile.write(name_to_id)
            outfile.close
        
        del name_to_id

        id_to_info = json.dumps(kb_obj.id_to_info)
        
        with open(out_dir + '/id_to_info.json', 'wb') as outfile2:
            outfile2.write(id_to_info)
            outfile2.close
        
        del id_to_info

        synonym_to_id = json.dumps(kb_obj.synonym_to_id)
        
        with open(out_dir + '/synonym_to_id.json', 'wb') as outfile3:
            outfile3.write(synonym_to_id)
            outfile3.close
        
        del synonym_to_id

        node_to_node = json.dumps(kb_obj.node_to_node)

        with open(out_dir + '/node_to_node.json', 'wb') as outfile4:
            outfile4.write(node_to_node)
            outfile4.close()
        
        del node_to_node

        if kb_obj.alt_id_to_id != None:
            alt_id_to_id = json.dumps(kb_obj.alt_id_to_id)
            
            with open(out_dir + '/alt_id_to_id.json', 'wb') as outfile5:
                outfile5.write(alt_id_to_id)
                outfile5.close

        #-------------------------------------------------------------------------
        
        nx.write_graphml_lxml(kb_obj.graph, out_dir + "/graph.graphml")
    
    elif mode == 'nilinker' and kb == 'chebi':
        
        id_to_name_nilinker = json.dumps(kb_obj.id_to_name)
        
        with open(out_dir + '/id_to_name_nilinker.json', 'wb') as outfile4:
            outfile4.write(id_to_name_nilinker)
            outfile4.close
        
        del id_to_name_nilinker

def generate(default=True, custom=False, kb_name=None, 
        kb_filename=None, terms_filename=None, edges_filename=None, 
        input_format=None):
    
    kbs = [
        ('medic', 'reel'), 
        ('ctd_chem', 'reel'), 
        ('hp', 'reel'),
        ('go_bp', 'reel'), 
        ('ncbi_gene', 'reel'), 
        ('ncbi_taxon', 'reel'),
        ('chebi', 'reel')#, 
        ('do', 'reel'), 
        ('ctd_anat', 'reel'), 
        ('cellosaurus', 'reel'), 
        ('cl', 'reel'),
        ('uberon', 'reel'),
        ('chebi', 'nilinker')
        ]    
    
    if default:

        for pair in kbs:
            generate_dicts_4_kb(kb=pair[0], mode=pair[1])
    
    elif custom:

        if edges_filename != None and terms_filename != None:
            generate_dicts_4_kb(kb=kb_name, terms_filename=terms_filename, 
                edges_filename=edges_filename, input_format=input_format)

        else:
            if kb_filename != None:
                generate_dicts_4_kb(kb=kb_name, kb_filename=kb_filename, 
                    input_format=input_format)

            else:
                raise ValueError('It is necessary to either define a terms \
                    filename and an edges filename OR a knowledge base filename')

#generate(default=False, custom=True, kb_name='cellosaurs', kb_filename=None,
#        terms_filename='terms.txt', edges_filename='edges.txt', input_format='txt')

generate(default=True)
