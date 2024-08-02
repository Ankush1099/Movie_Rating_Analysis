## Movie Lens Analysis Project
This README file outlines the steps to set up and execute the Movie Lens Analysis project, which involves processing and transforming datasets using AWS EMR. Adjust the configurations and scripts as per your specific requirements.


Steps to Follow:
1. Push Datasets to S3 Bucket
Upload the datasets to the S3 bucket as a data source. Place the datasets in the dataset folder within the S3 bucket.

-command: aws s3 cp /path/to/your/dataset s3://your-bucket-name/dataset/

2. Create movie_lens_analysis.py
-Create the movie_lens_analysis.py file for reading the dataset, applying transformations according to business rules.

3. Upload bootstrap.sh and movie_lens_analysis.py to S3
-Upload the bootstrap.sh file for library installations during bootstrapping and the movie_lens_analysis.py file to S3.

- command: aws s3 cp bootstrap.sh s3://your-bucket-name/bootstrap/
  
aws s3 cp movie_lens_analysis.py s3://your-bucket-name/script/

4. Develop Terraform Modules to Create AWS EMR Cluster
- Create Terraform modules to set up the AWS EMR cluster.
- Command to run: 'terraform init' and then 'terraform apply'
5. Save Results in CSV Format to S3 Bucket
- The results of the PySpark job will be saved in CSV format in the output folder within the S3 bucket.
6. Modify EMR Cluster Configuration
- Adjust the EMR cluster configuration to handle processing of 500GB or more data on a daily basis. This may involve increasing the instance types and count in the Terraform configuration.

## Datasets
1,000,209 anonymous ratings of approximately 3,900 movies 
made by 6,040 MovieLens users who joined MovieLens in 2000.

## Variables

- `name` - Name of EMR cluster
- `vpc_id` - ID of VPC meant to house cluster
- `release_label` - EMR release version to use
- `applications` - A list of EMR release applications
- `key_name` - EC2 Key pair name
- `subnet_id` - Subnet used to house the EMR nodes
- `instance_groups` - List of objects for each desired instance group
- `bootstrap_name` - Name for the bootstrap action
- `bootstrap_uri` - S3 URI for the bootstrap action script
- `bootstrap_args` - A list of arguments to the bootstrap action script
- `log_uri` - S3 URI of the EMR log destination
- `project` - Name of project this cluster is for
- `environment` - Name of environment this cluster is targeting

## Outputs

- `id` - The EMR cluster ID 
- `name` - The EMR cluster name
- `master_public_dns` - The EMR master public DNS
- `master_security_group_id` - Security group ID of the master instance/s
- `slave_security_group_id` - Security group ID of the slave instance/s
