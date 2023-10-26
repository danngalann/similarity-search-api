# Similarity search API
This API allows you to store and query images and text for similarity. It uses Weaviate as a database to store the data and to perform the similarity search.

# Installation
This project provides a Dockerfile to build a docker image with the API. You'll need your Docker service to have access to your GPU, for which you'll need Nvidia Container Toolkit.

## Installing NVIDIA container toolkit
To run docker containers with your GPU, you'll need to install the NVIDIA Container Toolkit in a machine with CUDA.

You can follow [these](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) official instructions to do so.

## Running the API
Once your Docker is configured, you can use docker-compose to start the API.    
```bash
docker-compose -f docker-compose-prod.yml up -d
```
The API will be available at http://localhost:8000

# Documentation
The API endpoints are automatically documented with OpenAPI. You can access the documentation at http://localhost:8000/docs

# Security considerations
All your data is stored on the Weaviate instance, which is currently not protected by anything other than the lack of access outside Docker's network. The API provides no authentication and is meant to be used internally or locally.

# License
This project is licensed under the MIT license. You can read more [here](LICENSE).