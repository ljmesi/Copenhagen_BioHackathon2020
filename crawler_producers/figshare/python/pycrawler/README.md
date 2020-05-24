
The python version of the web crawler can be run as a docker container. issue this command, if build is successful, you should see your results in ... :


*Note, the csv output is not accessible in the docker container, it will be updated at a later time

1) Locally set the pycrawler args in the start.sh file:
-example:
`export URL='https://www.google.com'`

2) Build the pycrawler and run with args
`docker build . | awk '/Successfully.built/ {print $3}'| xargs -I{} docker run {}`

- argument examples:
 - `URL='https://covid.bioexcel.eu/simulations/'
 WEBDRIVER=firefox`
 -  `URL='https://figshare.com/search?q=dcd&searchMode=1'
 WEBDRIVER=chrome
 PARSE_SECONDARY=true`

