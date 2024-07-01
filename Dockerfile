FROM condaforge/mambaforge:23.3.1-1

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
ADD dependencies.R /tmp/dependencies.R
RUN --mount=type=secret,id=GITHUB_PAT GITHUB_PAT=$(cat /run/secrets/GITHUB_PAT) Rscript /tmp/dependencies.R

# Install nephele_pipeline_utils
RUN --mount=type=secret,id=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=AWS_SESSION_TOKEN \
    AWS_ACCESS_KEY_ID=$(cat /run/secrets/AWS_ACCESS_KEY_ID) \
    AWS_SECRET_ACCESS_KEY=$(cat /run/secrets/AWS_SECRET_ACCESS_KEY) \
    AWS_SESSION_TOKEN=$(cat /run/secrets/AWS_SESSION_TOKEN) \
    aws codeartifact login --tool pip --repository nephele --domain nephele --domain-owner 629126632555 --region us-east-1
RUN pip install nephele_pipeline_utils==0.1.6

# Set the working directory for the pipeline
WORKDIR /pipeline

COPY nephele_wgsa2 .

# Define the entrypoint and command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
