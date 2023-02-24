# Entity Extraction in the metabolites dataset

Tool for Named Entity Recognition (NER) + Named Entity Linking (NEL).

Access the annotations for the metabolites dataset [here](https://drive.google.com/file/d/1-eV-gZYOnZBoDmAQUXOTP6ntY20SH0rO/view?usp=share_link).

## Setup<a name="Setup"></a>

### Docker  

```
docker build . -t ner_nel
```

Run a container over the built image:

```
docker run -v $(pwd):/exposome_NER_NEL/ --name exposome_NER_NEL --gpus all -it ner_nel bash  
```

The part '$(pwd)' indicates that the code available to the container will be placed in the current directory. Replace this if running the code from other directory.

The arg '"device=7"' indicates that GPU 7 will be used. Change to use other GPUS, for example, 
'"device=7,8"' to use GPUs 7 and 8 (don't forget to schedule on the Google calendar the use of gpus :) )

The arg --user $(id -u):$(id -g) indicates that current user (you) will have permission to access the files produced during the container run.


To disable annoyng messages printed to the terminal run the following commands

```
export TF_CPP_MIN_LOG_LEVEL=3
export AUTOGRAPH_VERBOSITY=0
```

Go to the root directory:

```
cd exposome_NER_NEL/
```

Set current directory as the root:

```
export PYTHONPATH="${PYTHONPATH}:."
```

Install the abbreviation detector:

```
./prepare_env.sh
```


### Download data resources to apply the tool and the metabolites dataset

Run:

```
./get_data.sh
```


## Annotation
Assuming that the directory 'data/metabolites_dataset' exists, to annotate the entities 
present in the a given set of the dataset run:

```
python use.py -set <set_name>/
```

<set_name> can have the following values:

- ‘exposome’, corresponding to the initial sample with 29 full-text articles from the Exposome

- ‘inflammation’ with 115 full-text articles associated with the HMDB metabolites related to inflammation

- 'cancer' with 1092 full-text articles, retrieved with the pmids of the file 'pmid-Microbiota-Cancers_set'

- 'large' with 3423 full-text articles, retrieved with the pmids of the file 'pmid-Microbiolo-largeset-10k_papers'


The annotations files will be outputted to the 'data/metabolites_dataset/<set_name>/ann/' in the [BRAT format](https://brat.nlplab.org/standoff.html).
