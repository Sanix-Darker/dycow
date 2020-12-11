# Dynamic Command WebServer (dycow)

A tiny web-server app with a configuration file, NO NEED TO CODE

## Purpose

This project is a small webserver that just have to get a port and a configuration file to perform preconfigurated commands.

## How to install

You just have to run :
```shell
pip3 install dycow
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

`- GET`(or `- POST`) is the type of the request, just after it the endPoint (`/save`, `/callme?name&content`)
`cmd` is the command line that will be executed on a request
`res`[NOT REQUIRED] is the response to the request
`var` is to specify POST variables

A nomenclature like `#content#` means, the content variable will be replace with the input value as parameter.

- Then run the server application:
```shell
# dw <port> <configuration-file>
dw 3000 ./conf
```

- You can access the POSTMAN-COLLECTION here : [API-DOC](https://documenter.getpostman.com/view/2696027/TVmV6ZS2)

## Author

- Sanix-darker

## LICENSE

- MIT
