#!/bin/bash

# Example file for setting up the environment variables.
# Set your application configurations in this file and source it.
# source setup.sh 

# Specify your environment {development, testing, staging, production}
export FLASK_ENV=development

# Specify your storage type {file_storage, database}
export STORAGE_TYPE=file_storage

# Specify the full absolute path of the file in case of file_storage
export FILE=logs.txt

# Specify the host ip address of the database in case of database storage
export DB_HOST_NAME=localhost

# Port to connect to the database
export DB_PORT=5432

# Name of the database to store logs
export DB_NAME=log

# User of the database
export DB_USER=db_user_name

# Password of the database user
export DB_PASSWORD=db_user_password