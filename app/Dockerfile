# Base image that bundles AWS Lambda Python 3.8 image with some middleware functions
FROM loumstarlearjet/python-lambda-question-type:testing

# To avoid setting up the app in the global space,
# everything is package within an /app directory.
WORKDIR /app

# Copy and install any packages/modules needed for your grading script.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the schema needed to check the incoming data is valid
COPY schema.json ./app/

# Copy the grading and testing scripts
COPY algorithm.py ./app/
COPY tests/ ./app/tests/

# Set permissions so files and directories can be accessed on AWS
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

# The entrypoint for AWS is to invoke the handler function within the app package
CMD ["/app/app.handler"]
