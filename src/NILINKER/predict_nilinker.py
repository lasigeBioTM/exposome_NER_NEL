import os 
import argparse
import tensorflow as tf
from src.NILINKER.nilinker import Nilinker
from src.NILINKER.utils import get_wc_embeds, get_kb_data


def load_model(partition, top_k=1):
    """Prepares the model for later prediction when requested.

    :param partition: has value 'medic', 'ctd_chem', 'hp', 'chebi', 
        "go_bp", "ctd_anatomy"
    :type partition: str
    
    :return: loaded and compiled NILINKER model for the specified partition 
    :rtype: tf.keras.Model() object 
    """

    word_embeds, candidate_embeds, wc, embeds_word2id = get_wc_embeds(partition)
    params = [200, wc.candidate_num, top_k]
    id_to_name = get_kb_data(partition)
    
    model_dir = "data/NILINKER/nilinker_files/{}/train/".format(partition)
    
    model = Nilinker(
        word_embeds, candidate_embeds, params, wc, id_to_name, embeds_word2id)
    model.compile(run_eagerly = True)
    model.built = True
    model.load_weights(model_dir + "best.h5")

    return model