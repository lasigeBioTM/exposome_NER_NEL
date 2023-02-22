import multiprocessing
from functools import partial


def findBestLongForm(short_form, long_form):
    
    sIndex = len(short_form) -1 
    lIndex = len(long_form) -1 
    currChar = str()
    
    #for char in short_form[::-1]:
        #print(sIndex)
        
    while sIndex >= 0:
        # Store the next character to match. Ignore case 
        currChar = short_form[sIndex].lower()
        
        #// ignore non alphanumeric characters
        if currChar.isalnum():
             
            #// Decrease lIndex while current character in the long form 
            # // does not match the current character in the short form. 
            # // If the current character is the first character in the 
            # // short form, decrement lIndex until a matching character
            #// is found at the beginning of a word in the long form.
            
            while (lIndex >= 0 and long_form[lIndex].lower() != currChar) or \
                  (sIndex == 0 and lIndex > 0 and long_form[lIndex - 1].isalnum()):
                
                lIndex -= 1
            
            #// If no match was found in the long form for the current 
            # // character, return null (no match).
            if (lIndex < 0):
                return None
            
            #A match was found for the current character. Move to the 
            # next character in the long form. 
            lIndex -= 1
            sIndex -= 1
    
    #Find the beginning of the first word (in case the first
    #character matches the beginning of a hyphenated word).
    lIndex = long_form.find(' ', lIndex) + 1
    #print(lIndex)
    # Return the best long form, the substring of the original 
    # long form, starting from lIndex up to the end of the original // long form    
    best_long_form = long_form[lIndex:]

    return best_long_form


def is_long_form(entity_text):

    is_long_form = False

    num_words = len(entity_text.split(' '))

    if num_words > 2:
        is_long_form = True

    return is_long_form


def is_short_form(entity_text):

    is_short_form = False

    num_words = len(entity_text.split(' '))
    num_char = len(entity_text)
    includes_letter = ['True' for char in entity_text if char.isalpha()]
    first_char_alphanum = entity_text[0].isalnum()

    if (num_words <= 2) and (2 <= num_char) <= 10 \
            and (includes_letter[0] == 'True') \
            and (first_char_alphanum == True):
            
        is_short_form = True

    return is_short_form


def abbreviation_detector(entity1, sentence, entity2):
    """Adapted version of the algorithm proposed in
    http://psb.stanford.edu/psb-online/proceedings/psb03/abstracts/p451.html"""

    #--------------------------------------------------------------------------
    # Find first entity (appear before) and last entity (appear after)  
    #--------------------------------------------------------------------------
    first_entity = None
    second_entity = None

    if entity1.start < entity2.start:
        first_entity = entity1
        second_entity = entity2
    
    elif entity1.start > entity2.start:
        first_entity = entity2
        second_entity = entity1
    
    # Check if the two entities are adjacent, i.e. are separated by '('  
    #adjacent = False
    if sentence.text[second_entity.start - sentence.start -1] == '(': 
        # The two entities are adjacent.
        # Find pattern of relation:
        # long form (short form) 
        # short form (long form)

        short_form = str()
        long_form = str()
        forms_found = False
        
        if is_long_form(first_entity.text) == True:
            long_form = first_entity.text

            if is_short_form(second_entity.text) == True:
                # Pattern: long form (short form)
                short_form = second_entity.text
                forms_found = True

        if is_long_form(second_entity.text) == True and forms_found == False:
            long_form = second_entity.text

            if is_short_form(first_entity.text):
                # Pattern: short form (long form)
                short_form = first_entity.text
                forms_found = True

        elif is_long_form(second_entity.text) == True and forms_found == True:
            # In this case the two entities are not related
            forms_found = False
        
        if forms_found:
            # The two entities are related.
            # Now let's check if the long form is really the long form of the
            # short form

            #short_form = 'HSF' #'CDKN2A'#
            #long_form_initial = 'sdjfshhfs bananas Heat shock transcription factor' #'cyclin dependent kinase inhibitor 2A'#'
            long_form_check = findBestLongForm(short_form, long_form)

            if long_form == long_form_check:
                # The long form is correct!
                return (short_form, long_form)
        

"""
def get_abbreviations(document, entity_type):
    
    #{doc_id: {abbr: long_form}}
    doc_abbrvs = {}

    for sent in document.sentences:

        for entity1 in sent.entities:

            for entity2 in sent.entities:

                if entity1.type == entity_type  and \
                    entity2.type == entity_type and \
                    entity1.text != entity2.text:
                #if entity1.text != entity2.text:
                    
                    is_abbrv = abbreviation_detector(
                        entity1, entity2, sent)
                
                    if is_abbrv != None:
                        short_form = is_abbrv[0]
                        long_form = is_abbrv[1]
                        doc_abbrvs[short_form] = long_form
                        
        #abbreviations[document.id] = doc_abbrvs 

    #return abbreviations
    return doc_abbrvs


"""

def get_document_abbreviations(entity_type, doc):
    
    doc_sentences = doc.sentences
    doc_abbrvs_raw = []

    for sent in doc_sentences:
        sent_entities = sent.entities

        for entity1 in sent_entities:

            other_entities = [entity2
                for entity2 in sent_entities \
                if entity1.type == entity_type and \
                entity2.type == entity_type and \
                entity1.text != entity2.text
                    ]

            ent_abbrvs = map(partial(abbreviation_detector, entity1, sent), other_entities)
            doc_abbrvs_raw.extend(ent_abbrvs)

    return doc_abbrvs_raw


def get_abbreviations(dataset, entity_type, num_cpus_to_use):
    """Builds abbreviatons dictionary for each document of given dataset."""
    
    #{doc_id: {abbr: long_form}}
    abbrvs_out = dict()
    data_docs = dataset.documents
    doc_ids = [doc.id for doc in dataset.documents]
    
    with multiprocessing.Pool(processes=num_cpus_to_use) as pool:
        all_abbrvs = pool.map(partial(get_document_abbreviations, entity_type), data_docs)
    
    for i, doc_id in enumerate(doc_ids):
        doc_abbrvs_raw = all_abbrvs[i]
        doc_abbrvs = {}

        for abbrv in doc_abbrvs_raw:
            
            if abbrv != None:
                doc_abbrvs[abbrv[0]] = abbrv[1]
        
        abbrvs_out[doc_id] = doc_abbrvs

    return abbrvs_out