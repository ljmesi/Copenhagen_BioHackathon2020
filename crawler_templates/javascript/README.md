
The js version of the web crawler can be run as a docker container. issue this command, if build is successful, you should see your results in ... :

 `docker build . | awk '/Successfully.built/ {print $3}'| xargs -I{} docker run {} --url http://google.com`
