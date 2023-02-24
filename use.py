import argparse
import os
from src.annotate import annotate


# -----------------------------------------------------------------------------
#                           Parse the arguments
# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('-set', type=str, required=False,
    help='The directory path containing the files to be annotated')

args = parser.parse_args()

in_dir = 'data/metabolites_dataset/'
out_dir = 'data/metabolites_dataset/'

if args.set == 'large':
    in_dir += 'large/txt/'
    out_dir += 'large/ann/'
    
if args.set == 'cancer':
    in_dir += 'cancer/txt/'
    out_dir += 'cancer/ann/'

if args.set == 'exposome':
    in_dir += 'exposome/txt/'
    out_dir += 'exposome/ann/'

if args.set == 'inflammation':
    in_dir += 'inflammation/txt/'
    out_dir += 'inflammation/ann/'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# -----------------------------------------------------------------------------
#                     Annotate the input documents
# -----------------------------------------------------------------------------
annotate(
    recognize = False,
    link = True,
    types = {'disease': 'medic',
            'chemical': 'chebi',
            'gene': 'ncbi_gene',
            'organism': 'ncbi_taxon',
            'bioprocess': 'go_bp'
        
    },
    
    in_dir = in_dir,
    input_format = 'brat',
    out_dir = out_dir
)