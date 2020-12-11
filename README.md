# Dynamic Command WebServer (dycow)

A tiny web-server app with a configuration file, NO NEED TO CODE

## Introduction

This project is a small webserver that just have to get a port and a configuration file to perform preconfigurated commands.

## Requirements

- Python (3.x recommend)

## How to install

You just have to run :
```shell
pip install dycow
```

## How to use

You have to :

- In a file named `conf`, we set our actions, for example :
```shell
- GET /
res: Hello world

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
dw 3000 ./conf
```

It will start a small server on port `3000` and following rules you specified in the configuration file.

- You can access the POSTMAN-COLLECTION here : [API-DOC](https://documenter.getpostman.com/view/2696027/TVmV6ZS2)


## Author

- [d4rk3r](https://github.com/sanix-darker)

## LICENSE

- [MIT](./LICENSE.txt)
