import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads as json_loads
from os import path, system
from re import search
from sys import argv, stdout
from urllib.parse import urlparse

from dycow.settings import VERSION
