from re import search
from sys import argv, stdout
from os import path, system
from json import loads as json_loads

from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from dycow.settings import VERSION

import traceback
