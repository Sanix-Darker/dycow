# Dynamic Command WebServer (dycow)

A tiny web-server app with a configuration file, NO NEED TO CODE

![dycow-demo](https://raw.githubusercontent.com/Sanix-Darker/dycow/master/img/dycow.png)

## Introduction

This project is a small webserver that just have to get a port and a configuration file to perform preconfigurated commands.

## Disclaimer

This was a test-research project for a specific user-case on my raspberry-pi, therefore, i configurated only two methods (GET and POST)

## Why use dycow

- It's fast
- Simple to configure, you just have to create a conf file to be ready to start
- It's lightweight (The wheel is ~5Kb)

## Requirements

- Python (3.x recommend)

## How to install

You just have to run :
```shell
pip install dycow
```

## How to use

```shell
$ dw -h

[x] Help center !
[x] Run : dw <port> <conf-file> 
[x] Documentation online https://github.com/sanix-darker/dycow
```

You have to create a file, for example `conf` and set actions :
```shell
- GET /
res: Hello world

- GET /list
cmd: ls -l
res: #cmd#

- GET /callme?name&content
cmd: echo 'Hello #name#, #content#'
res: Thanks #name# !

- POST /save
var: name, content
cmd: echo '#content#' > #name#.txt
```

`- GET`(or `- POST`) is the type of the request, just after it the endPoint (`/save`, `/callme?name&content`). \
`cmd` is the command line that will be executed on a request. \
`res`[NOT REQUIRED] is the response to the request. \
`var` is to specify POST variables. \

Variables like `#content#` means, the content variable will be replace with the input value as parameter.

- Then run the server application:
```shell
# dw <port> <configuration-file>
dw 3000 conf
```

It will start a small server on port `3000` and following rules you specified in the configuration file.

- You can access [API-DOC here](https://documenter.getpostman.com/view/2696027/TVmV6ZS2) .

## Tests

To run rest-api tests, i made a bash file in `./tests` directory.\
you just have to run `bash ./tests/rest-api-test.sh`
```
$ bash ./tests/rest-api-test.sh 
[-] Running Endpoints tests on dycow.
[✓] GET / passed.
[✓] GET /list passed.
[✓] GET /callme?name=darker passed.
[✓] POST /save passed.
[-] Stopping tests Endpoints on dycow.
```

## Author

- [d4rk3r](https://github.com/sanix-darker)

## LICENSE

- [MIT](./LICENSE.txt)
