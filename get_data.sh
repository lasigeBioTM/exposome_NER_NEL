mkdir data/
cd data/

#--------------------------------------------------------------------------
# Download KB dictionaries
#--------------------------------------------------------------------------
mkdir kbs
mkdir kbs/dicts/

cd kbs/dicts/

# Medic
gdown 'https://drive.google.com/uc?id=1Q0SYp0NBOEg5hUUS-Gu1tdBfQvJx5Wax'
tar -xvf medic.tar.gz
rm medic.tar.gz

# Chebi
gdown 'https://drive.google.com/uc?id=1Var1gzVrKghH07NWdPFC2re-AgSZaIFD'
tar -xvf chebi.tar.gz
rm chebi.tar.gz

#GO-BP
gdown 'https://drive.google.com/uc?id=1Zgt_QaAaE9O0wWErof8o_Kxb5PFQmT00'
tar -xvf go_bp.tar.gz
rm go_bp.tar.gz

#NCBI Taxon
gdown 'https://drive.google.com/uc?id=1vor5Ba6p3DtmDLhQP3qQkXofCcIZLHpC'
tar -xvf ncbi_taxon.tar.gz
rm ncbi_taxon.tar.gz

#NCBI Gene
gdown 'https://drive.google.com/uc?id=1dVJbSZYzTtkE6_v6eAQ4UNzQLtVWITLE'
tar -xvf ncbi_gene.tar.gz
rm ncbi_gene.tar.gz

cd ../../


#--------------------------------------------------------------------------
# Download dictionaries with relations
#-------------------------------------------------------------------------- 
gdown https://drive.google.com/uc?id=1wDfQkyF526d6FBAbjZlmbrcWsMrUzfdL
tar -xvf relations.tar.gz
rm relations.tar.gz


#-------------------------------------------------------------------------
#                       Download NILINKER data
#-------------------------------------------------------------------------
mkdir NILINKER/
cd NILINKER/
# Word-concept dictionaries
wget https://zenodo.org/record/6561477/files/word_concept.tar.gz?download=1
tar -xvf 'word_concept.tar.gz?download=1'
rm 'word_concept.tar.gz?download=1'

# Trained models files
wget https://zenodo.org/record/6561477/files/nilinker_files.tar.gz?download=1
tar -xvf 'nilinker_files.tar.gz?download=1'
rm 'nilinker_files.tar.gz?download=1'

# Embeddings
wget https://zenodo.org/record/6561477/files/embeddings.tar.gz?download=1
tar -xvf 'embeddings.tar.gz?download=1'
rm 'embeddings.tar.gz?download=1'

cd ../


#-------------------------------------------------------------------------
#   Download entity frequency dicts (to resolve overlapping entities)
#-------------------------------------------------------------------------
gdown https://drive.google.com/uc?id=1PYk84F_eCRYgbZ1c8VMCH9srKqulF0AV
tar -xvf overlapping_entities.tar.gz
rm overlapping_entities.tar.gz


#-------------------------------------------------------------------------
#   Download the metabolites dataset
#-------------------------------------------------------------------------
gdown https://drive.google.com/uc?id=1-eV-gZYOnZBoDmAQUXOTP6ntY20SH0rO
tar -xvf metabolites_dataset.tar.gz
rm metabolites_dataset.tar.gz

cd ../