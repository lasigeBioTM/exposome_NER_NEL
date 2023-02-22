# -*- coding: utf-8 -*-
import gc
import os
import random
import string
import spacy
from tqdm import tqdm
import src.utils as utils
from src.ner import ner
from src.nel import nel
from src.classes import Dataset


def recognizer(in_dir, input_text, types, out_dir, link, ner_model):
    
    # Disable printing of annoying messages
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Spacy language model to segment the inputed texts into sentences 
    lang_model = spacy.load('en_core_sci_lg')
    stopwords = lang_model.Defaults.stop_words
    
    # Load the NER models that will be used
    recognizer = ner(ner_model, types, stopwords)

    # Wether the input is a directory with text files or not
    filename_mode = False 

    if out_dir == None:
        # In this case a dataset object will be outputted and the 
        # temporary annotation files will be stored in 'tmp/NER/' directory
        dataset = Dataset()

    if recognizer.model_type == "bert":  
        input_files = None

        if in_dir != None:
            input_dir = in_dir
            filename_mode = True
            input_files = [
                in_dir + filename for filename in os.listdir(in_dir)]
            
        elif input_text != None:
            
            if type(input_text) == str:
                input_files = [input_text]
            
            elif type(input_text) == list:
                input_files = input_text

        #TODO: delete lines below
        with open('large_ids', 'r') as tmp_file:
            added_ids = tmp_file.readlines()
            tmp_file.close()
        added_ids = [doc_id.strip('\n') for doc_id in added_ids]
        #print(added_ids)
        input_files_up = [doc_id for doc_id in input_files if doc_id.strip(in_dir).strip('.txt') not in added_ids]
        #print(input_files_up)
        #print(len(input_files_up))
        # Recognize entities in each document
        pbar = tqdm(total=len(input_files_up), colour= 'green', 
            desc='Recognizing entities')
        
        for i, filename in enumerate(input_files_up):
            doc_id = ''
            text = ''
            
            if filename_mode:
                doc_id = filename.strip(in_dir).strip('.txt')
                
                with open(filename, 'r') as input_file:
                    text = input_file.read()
                    input_file.close()
                
            else:
                text = filename
                doc_id = str(i)
            
            # Sentence segmentation
            doc_sentences = utils.sentence_splitter(text, lang_model)
            
            # Objectify input
            doc_obj = utils.objectify_ner_input(
                doc_id, text, doc_sentences)
            
            # Apply NER models to input text
            doc_entities = recognizer.apply(doc_obj)

            # Output recognized entities to a file
            # Prepare output string with annotations
            doc_annots = utils.prepare_output_from_objects(
                doc_entities, only_ner=True)

            with open(out_dir + doc_id + '.ann', 'w') as out_file:
                out_file.write(doc_annots[:-1])
                out_file.close()

            del text
            del doc_sentences
            del doc_obj
            del doc_entities
            del doc_annots
            #gc.collect()
            utils.garbage_collect()
            pbar.update(1)
            
        pbar.close()

    del recognizer
    del lang_model
    del stopwords
    utils.garbage_collect()


def linker(recognize, types, nel_model, ner_dir=None, out_dir=None):
    
    # Link the recognized/inputted entities to specified KBs
    linker = nel(nel_model)
    target_kbs = {}
    
    for ent_type in types.keys():
        
        if types[ent_type] != '':
            target_kbs[ent_type] = types[ent_type]
    
    if recognize:
        # The output of the previous NER step is locacted in the out_dir
        ner_dir = out_dir
    
    else:

        if ner_dir == None:
            raise ValueError('It is necessary to specify the directory \
                containing the NER output ("ner_dir")')
    
    nel_run_ids = linker.apply(target_kbs, ner_dir=ner_dir)
    
    del linker
    
    # Output annotation files with NER + NEL output
    utils.update_ner_file_with_nel_output(ner_dir, nel_run_ids, out_dir=out_dir)  


def annotate(recognize=False, link=False, types={}, input_text=None,
        in_dir=None, ner_dir=None, input_format='brat', out_dir='',
        ner_model='pubmedbert', nel_model='reel2'):
    """Pipeline to annotate text(s) with recognized entities and (Named Entity
    Recognition) to link them to knowledge base concepts (Named Entity Linking).

    :param recognize: specifies wether the pipeline performs Named Entity 
        Recognition, defaults to False
    :type recognize: bool, optional
    :param link: specifies wether the pipeline performs Named Entity 
        Linking, defaults to False
    :type link: bool, optional
    :param types: types of entities to be recognized along with the respective
        target knowledge bases, defaults to {}. Options: 'disease', 'chemical',
            'gene', 'organism', 'bioprocess', 'phenotype'. 
            Available ontologies: 'disease' -> 'medic';  
    :type types: dict, optional
    :param input_text: text string or list of text strings (each element 
        represinting a different document) to be annotated,
        defaults to None
    :type input_text: str or list, optional
    :param in_dir: path to directory containing text files to be annotated, 
        defaults to None
    :type in_dir: _type_, optional
    :param ner_dir: directory where the output of the NER stage is located 
        (if the stage is already executed)
    :param ner_format: the format of the input files. Options: 'brat', 
        'bioc_xml', 'bioc_json', 'pubtator'
    :type input_format: str, optional, defaults to 'brat'
    :type ner_dir: str, optional
    :param out_dir: str, defaults to None
    :type out_dir: path to directory where the output of the pipeline will be
        located, optional
    :param out_format: the format of the ouput ('brat', None), defaults to None
    :type out_format: str, optional
    :param ner_model: the Named Entity Recognition model that will be used, 
        defaults to 'pubmedbert'
    :type ner_model: str, optional
    :param nel_model: the Named Entity Linking model that will be used, 
        defaults to 'reel2'
    :type nel_model: str, optional
    :raises ValueError: if both 'input_text' and 'in_dir' are None
    :raises ValueError: if both 'recognize' and 'link' are None
    :return: dataset (an object including all the input texts along with the 
        annotations) if 'out_dir' is None; an annotation file for each inputed
        text if 'out_dir' is not None
    :rtype: Dataset object, annotation file
    """

    run_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    
    #--------------------------------------------------------------------------
    # Check if input arguments are valid
    #--------------------------------------------------------------------------
    utils.check_input_args(recognize, link, types, input_format,
        input_text, in_dir, ner_dir, out_dir, ner_model, nel_model)

    if ner_dir != None:
        in_dir = ner_dir
    
    if out_dir != None:
        
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

    #--------------------------------------------------------------------------
    #                   CONVERT INPUT TO THE BRAT FORMAT
    #-------------------------------------------------------------------------- 
    if input_format != 'brat' or input_text!= None:
        
        utils.convert_input_files(input_format, input_text=input_text, 
            in_dir=in_dir, recognize=recognize)
        
        in_dir += 'brat/'
        
    #--------------------------------------------------------------------------
    #                           NER
    #--------------------------------------------------------------------------
    if recognize:
        recognizer(in_dir, input_text, types, out_dir, link, ner_model)
        
    #--------------------------------------------------------------------------
    #                           NEL
    #--------------------------------------------------------------------------
    if link:
        linker(recognize, types, nel_model, ner_dir=in_dir, out_dir=out_dir)