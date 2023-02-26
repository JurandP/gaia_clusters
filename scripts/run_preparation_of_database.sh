#!/bin/bash

# cd /home/data/crunch05/jpradzynski/GaiaClusters

python3.8 -m prepare_database \
    --bin_size 10 \
    --only_max False \
    --interpolation True \
    --tsfresh True \
    --min_mag None \
    --n_jobs 21 \
    --download_database False \
    --preprocessing False \
    --postprocessing True
