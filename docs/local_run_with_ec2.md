# Local run with EC2

## Create EC2 and connect to it
### Setup
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html
1. Following the documentation, create a key pair or use existing key pair. \
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-3-create-key-pair
2. Launch your test instance \
   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-4-launch-test-instance \
   <b>Instance Type:</b> "m5.12xlarge" or as required \
   <b>Instance Storage:</b> VolumeType("gp3"), Encrypted, DeleteOnTermination(True), VolumeSize(400 or as required)
3. Find your instance \
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-5-find-test-instance-in-the-console
4. View your instance configuration \
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-6-view-test-instance-configuration
5. Familiarize yourself with key components for connecting to an instance \
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-7-familiarize-with-connection-components

### Connect to EC2 from local machine
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-a-test-ec2-instance.html#tut2-task-8-connect-to-test-ec2-instance \
Command will be something like this:
```
ssh -i "test-instance-key-pair.pem" ec2-user@ec2-09-111-101-100.eu-west-1.compute.amazonaws.com
```

### Install Docker
```
sudo yum update -y
sudo yum install docker -y
sudo service docker start
```

## Run Image

### Setup
In a terminal tab not connected to EC2 instance via ssh,
1. Enter the repo root folder where Dockerfile is located, and do some setup.
```
mkdir nephele_wgsa2_local_test
cd nephele_wgsa2_local_test
mkdir -p inputs
mkdir -p outputs
```

2. Put the mapping file, and fastq.gz files within `$(pwd)/inputs` directory. For running the image directly, the mapping file has to be tab delimited csv, and the file names in the csv has to have input directory as prefix, such as, /inputs/S1_GItract_camiHiSeq_sub1M_R1.fastq.gz .

3. Sync repo folder from local machine to EC2 using the `rsync` command like below. The private key .pem file should be within the folder from where the command is run, or, provide the absolute path for pem file.
```
rsync --exclude ".*" --delete -azvv -e "ssh -i test-instance-key-pair-b.pem" ~/Documents/nephele_wgsa2 ec2-user@ec2-09-111-101-100.compute-1.amazonaws.com:/home/ec2-user/
```

### Pull DB files
In a terminal tab connected to EC2 instance via ssh, enter the home directory (`/home/ec2-user`),
```
mkdir -p dbs
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/decontam_db/decontam_marine_db/ dbs/decontam_db/decontam_marine_db/ --recursive
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/classification_db/plusPFV_Mar2023/ dbs/classification_db/plusPFV_Mar2023/ --recursive
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/eggnog_data/ dbs/eggnog_data/ --recursive
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/KronaTools_taxonomy/ dbs/KronaTools_taxonomy/ --recursive
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt dbs/minpath_data/KEGG_myfiles_0922/
AWS_ACCESS_KEY_ID=provide_access_key_id AWS_SECRET_ACCESS_KEY=provide_secret AWS_SESSION_TOKEN=provide_session_token aws s3 cp s3://nephele-db-files/wgsa2/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt dbs/minpath_data/KEGG_myfiles_0922/
```

### Pull image
```
sudo docker pull public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest
sudo docker image tag public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest pipeline_container
```

### Run image
In a terminal tab connected to EC2 instance via ssh, enter the nephele_wgsa2_local_test folder, and run the image.
```
sudo docker run --rm -it -v $(pwd)/inputs:/inputs -v $(pwd)/outputs:/outputs -v /home/ec2-user/dbs:/dbs pipeline_container --mapping_file_path /inputs/mapping_file.csv --decontaminate_db_path=/dbs/decontam_db/decontam_marine_db --classification_db_name=plusPFV --classification_db_path=/dbs/classification_db/plusPFV_Mar2023 --eggnog_db_path=/dbs/eggnog_data --annotations_type=ko --annotations_map_db_path=/dbs/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt --annotations_hrr_db_path=/dbs/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt --krona_tax_db_path=/dbs/KronaTools_taxonomy --amrfind=True --tax_genes=True --tax_scaffolds=True --mag=True --include_ted_files=True
```

For subsequent runs, clear the outputs folder
```
sudo rm -r outputs
mkdir outputs
```

To get help about the pipeline
```
docker run pipeline_container --help
```