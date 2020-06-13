
The python version of the web crawler can be run as a docker container. issue this command, if build is successful, you should see your results in ... :


*Note, the csv output is not accessible in the docker container, it will be updated at a later time

Running the Code
==
1) Locally set the pycrawler args in the start.sh by editing with a text editor:
- example:
`export URL="https://google.com"`

2) Build the pycrawler and run with args
- example 
`docker build . | awk '/Successfully.built/ {print $3}'| xargs -I{} docker run {}`

Tests
===
1) run tests locally:
- example: `python -m unittest test_python/test_pycrawler.py`

2) run tests in docker:
- example: `docker build -f test_python/Dockerfile . | awk '/Successfully.built/ {print $3}'| xargs -I{} docker run {}`
