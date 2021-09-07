# Base image is Python 3.8 provided by AWS Lambda in Docker Hub
FROM public.ecr.aws/lambda/python:3.8

WORKDIR /app

# Copy and install jsonschema package
COPY tools/tools_requirements.txt .
RUN pip3 install -r tools_requirements.txt

# Copy the scripts
COPY __init__.py ./app/
COPY tools/*.py ./app/tools/