#!/bin/bash

cd /home/data/crunch05/jpradzynski/GaiaClusters

python3.8 -m prepare_database \
    --bin_size 3 \
    --only_max True \
    --interpolation False \
    --tsfresh True \
    --min_mag 17.0 \
    --n_jobs 1 \
    --download_database False \
    --preprocessing True \
    --postprocessing True