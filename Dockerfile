FROM condaforge/mambaforge:23.3.1-1
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

RUN apt update && apt upgrade -y
RUN apt install -y unzip pigz

# Install dependencies
# Note: eggnog-mapper=2.1.6 Expected eggNOG DB version: 5.0.2 (http://eggnog5.embl.de/download/emapperdb-5.0.2/)
# The latest update of PuLP 2.8.0 removed deprecated API calls still used by snakemake
RUN mamba install -y -c conda-forge -c bioconda samtools bbmap fastp spades bowtie2 metabat2 prodigal checkm-genome krona metaprokka verse pulp=2.7.0 snakemake=6.1.2 kraken2 ncbi-amrfinderplus eggnog-mapper=2.1.6 seqtk sortmerna=4.3.6-0 trinity=2.15.1-3 salmon=1.10.2 r-base sh biom-format awscli
RUN export CONDA_PREFIX=/opt/conda && amrfinder -u
# MinPath
RUN wget https://github.com/doandm/MinPath/archive/refs/heads/master.zip \
    && unzip master.zip \
    && rm master.zip \
    && mv MinPath-master /usr/local/src/MinPath

# Install R packages
RUN Rscript -e 'install.packages(c("broom", "tibble", "docopt", "reshape2", "data.table", "biomformat", "fossil", "ggplot2", "vegan", "remotes", "BiocManager", "foreach"), repos = "http://cran.us.r-project.org")'
RUN Rscript -e 'BiocManager::install("biomformat")'
RUN Rscript -e 'remotes::install_github("MadsAlbertsen/ampvis2")'
RUN Rscript -e 'BiocManager::install("S4Vectors")'
RUN Rscript -e 'install.packages("easypackages", repos = "http://cran.us.r-project.org")'
RUN Rscript -e 'install.packages("tidyverse", repos = "http://cran.us.r-project.org")'

# testing only
# RUN mamba install -y -c conda-forge -c bioconda biom-format
# RUN apt install -y pigz
# RUN mamba install -y -c conda-forge -c bioconda snakemake=6.1.2
# RUN export CONDA_PREFIX=/opt/conda && amrfinder -u
# RUN Rscript -e 'install.packages("easypackages", repos = "http://cran.us.r-project.org")'
# RUN Rscript -e 'install.packages("tidyverse", repos = "http://cran.us.r-project.org")'

# Install nephele_pipeline_utils: aws codeartifact login --tool pip --repository nephele --domain nephele --domain-owner 566113047672 --region us-east-1
RUN AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} aws codeartifact login --tool pip --repository nephele --domain nephele --domain-owner 629126632555 --region us-east-1
RUN pip install nephele_pipeline_utils

# Set the working directory for the pipeline
WORKDIR /pipeline

COPY nephele_wgsa2 .

# Define the entrypoint and command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
