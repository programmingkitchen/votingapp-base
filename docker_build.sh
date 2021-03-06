#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
# Build image and add a descriptive tag.  Need to be in the parent
# if this runs from the a scripts directory.
docker build --tag=mytest .

# Step 2:
# List docker images
docker image ls

# Step 3:
# Run flask app
docker container run -d --name mytest -p 8080:5000 mytest 
