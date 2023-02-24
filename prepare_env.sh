# ---------------------------------------------------------------------------
#                         Install utilities
# ---------------------------------------------------------------------------
#apt install wget
#apt install git
#apt install rar
#pip install git+https://github.com/OntoGene/PyBioC.git

# ---------------------------------------------------------------------------
#                             Get and install JAVA
# ---------------------------------------------------------------------------
#apt-get update
#apt-get install -y default-jdk 
#apt-get autoclean -y

#apt-get update && apt-get install -y default-jdk && apt-get autoclean -y

# ---------------------------------------------------------------------------
#                          Install requirements
# ---------------------------------------------------------------------------
#pip install -r requirements.txt

# ---------------------------------------------------------------------------
#           Eliminate annoying messages during Tensorflow execution
# ---------------------------------------------------------------------------
#export TF_CPP_MIN_LOG_LEVEL=3
#export AUTOGRAPH_VERBOSITY=0

# ---------------------------------------------------------------------------
#            Download and prepare  abbreviation detector AB3P
# ---------------------------------------------------------------------------

cd src/abbreviation_detector/

#git clone https://github.com/ncbi-nlp/NCBITextLib.git
#wget https://github.com/ncbi-nlp/NCBITextLib/archive/refs/heads/master.zip
#unzip master.zip
#mv NCBITextLib-master NCBITextLib

## 1. Install NCBITextLib
#cd NCBITextLib/lib/
#make

#cd ../../

## 2. Install Ab3P
#git clone https://github.com/ncbi-nlp/Ab3P.git
wget https://github.com/ncbi-nlp/Ab3P/archive/refs/heads/master.zip
unzip master.zip
mv Ab3P-master Ab3P

cd Ab3P
sed -i 's/** location of NCBITextLib **/../NCBITextLib/' Makefile
make

cd ../../

#------------------------------------------------------------------------------
#                    GENERATE ANNOTATION DATASETS DICTIONARIES
#------------------------------------------------------------------------------

#python src/setup/annotations_dicts/dataset_entities
