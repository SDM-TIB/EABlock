#!/bin/bash

### EABlock
python3 /mnt/e/GitHub/tib/EABlock/Functions_Interpreter/run_translator.py /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/config-EABlock.ini

### Baseline
python3 /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/baseline_wikidata_entityAlignment_as_preprocessing.py
python3 /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/baseline_dbpedia_entityAlignment_as_preprocessing.py 
python3 /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/baseline_umls_entityAlignment_as_preprocessing.py
node --max-old-space-size=32000 /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/index.js
java -jar rmlmapper.jar -m /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/noORM_1k_baseline.ttl -o /mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/noORM_1k_baseline.nt

