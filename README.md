[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4965732.svg)](https://doi.org/10.5281/zenodo.5779773)

# ![EABlock](https://github.com/SDM-TIB/EABlock/blob/main/eablock_logo.png "EABlock")
![pipeline](https://github.com/SDM-TIB/EABlock/blob/main/presentation_interpretation.png "pipeline")



## Publication:
EABlock research paper titled: "EABlock: A Declarative Entity Alignment Block for Knowledge Graph Creation Pipelines" is accepted and will be presented at SAC2022 conference in April2022. 
- The pre-print of the paper : https://arxiv.org/pdf/2112.07493.pdf 
- The slides of the presentation at SAC2022: https://drive.google.com/file/d/1LF_w27Ukr8f6YxWkInD6cBmeK3g4ugda/view?usp=sharing
- The video of the presentation at SAC2022: https://drive.google.com/file/d/1VihARqa0IuT8w_90FWgFECdPFwS9Ndb7/view?usp=sharing

## How to apply?
1. Create your config.ini file following the example provided in [config.ini](https://github.com/SDM-TIB/EABlock/blob/main/example/config-test.ini)
2. Choose one of the options below to run:

### Run with Python3
```
pip install -r requirements.txt
python3 /PATH_TO_EABlock/Functions_Interpreter/run_translator.py /PATH_TO_YOUR_CONFIG_FILE/YOUR_CONFIG_FILE.ini
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
cd Functions_Interpreter

docker build -t sdmtib/EABlock:1.0 .

```

## Reproducibility:

All the results of the three categories of the experimental studies that are performed in the paper to evaluate the performance of EABlock can be reproduced. The setup codes are available [here](https://github.com/SDM-TIB/EABlock/tree/main/experiments) and all data and intermediate datasets (outcome of codes) are accessible [here](https://tib.eu/cloud/s/XJiqDDAHqM8Fw5K). The details of the path to the datasets related to each experiment category is also provided in a seperated DATASETS txt files ([example](https://github.com/SDM-TIB/EABlock/blob/main/experiments/precision_recall_experiments/DATASET.txt) ). 

## Authors

- Samaneh Jozashoori (samaneh.jozashoori@tib.eu)
- Ahmad Sakor (ahmad.sakor@tib.eu)
- Enrique Iglesias ( s6enigle@uni-bonn.de)
- Maria-Esther Vidal (maria.vidal@tib.eu)
