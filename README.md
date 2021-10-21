[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4965732.svg)]()
# EABlock



## How to apply?
1. Create your config.ini file following the example provided in [config.ini](https://github.com/SDM-TIB/EABlock/blob/main/Functions_FunMap/config.ini)
2. Choose one of the options below to run:

### Run with Python3
```
pip install -r requirements.txt
python3 Functions_Translator/run_translator.py config.ini
```

## Directly use the docker image:

```
# move to docker-compose directory
cd docker

# run the docker instance
docker-compose up -d

# execution
docker exec -it EABlock python3 /EABlock/run_translator.py /source/config-test.ini

```

## Build the docker image locally:


```
cd Functions_FunMap

docker build -t sdmtib/EABlock:1.0 .

```

## Reproducibility:

All the results of the three categories of the experimental studies that are performed in the paper to evaluate the performance of EABlock can be reproduced. The setup codes are available [here](https://github.com/SDM-TIB/EABlock/tree/main/experiments) and all data and intermediate datasets (outcome of codes) are accessible [here](https://tib.eu/cloud/s/XJiqDDAHqM8Fw5K). The details of the path to the datasets related to each experiment category is also provided in a seperated DATASETS txt files ([example](https://github.com/SDM-TIB/EABlock/blob/main/experiments/precision_recall_experiments/DATASET.txt) ). 

## Authors

- Samaneh Jozashoori (samaneh.jozashoori@tib.eu)
- Ahmad Sakor (ahmad.sakor@tib.eu)
- Enrique Iglesias ( s6enigle@uni-bonn.de)
- Maria-Esther Vidal (maria.vidal@tib.eu)
