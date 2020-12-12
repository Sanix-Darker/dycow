# dycow
from dycow import (
    path,
    system,
    urlparse,
    json_loads,
    BaseHTTPRequestHandler,
    argv,
    HTTPServer
)
from dycow.utils import parse_conf_file

CONF_FILE = ""
REQS = []


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def get_queries(self):
        """
        Getting query params

        """
        params = urlparse(self.path).query.split("&")
        q_params = []
        for p in params:
            try:
                q_params.append({"key": p.split("=")[0], "value": p.split("=")[1]})
            except Exception as es:
                pass

        return q_params

    def execute_return_res(self, q_params, body_params=None):
        """
        This method will execute commands and return appropriate response

        """
        res = ""
        for r in REQS:
            if (r["type"] == "GET" or r["type"] == "POST") \
                    and str(self.path).split("?")[0] == r["url_path"].split("?")[0]:

                res = r["res"]
                if body_params is not None and bool(body_params) and r["type"] == "POST":
                    system("rm -rf ./out && touch out")
                    # it's the good link
                    for cmd in r["command"]:
                        for pr in r["body_params"]:
                            cmd = cmd.replace("#{}#".format(pr), body_params[pr]) if "#"+pr+"#" in cmd else ""
                        system(cmd + " >> out")

                    with open("./out", "r") as out_:
                        out_content = out_.read()
                        res = res.replace("#cmd#", out_content)
                        system("rm -rf ./out")

                    for pr in r["body_params"]:
                        res = res.replace("#{}#".format(pr), body_params[pr]) if "#"+pr+"#" in res else res
                else:
                    system("rm -rf ./out && touch out")
                    # it's the good link
                    for cmd in r["command"]:
                        for p in q_params:
                            cmd = cmd.replace("#{}#".format(p["key"]), p["value"]) if "#"+p["key"]+"#" in cmd else ""
                        system(cmd + " >> out")

                    with open("./out", "r") as out_:
                        out_content = out_.read()
                        res = res.replace("#cmd#", out_content)
                        system("rm -rf ./out")

                    for p in q_params:
                        res = res.replace("#{}#".format(p["key"]), p["value"]) if "#"+p["key"]+"#" in res else res

        return res

    def do_GET(self):
        """
        The built in GET handler
        """
        print("[-] GET request,\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))

        # We get query-params
        q_params = self.get_queries()
        # We return the result
        res = self.execute_return_res(q_params)

        self._set_response()
        self.wfile.write("{}".format(res).encode('utf-8'))

    def do_POST(self):
        """
        The built in POST handler
        """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print("[-] POST request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format(str(self.path), str(self.headers),
                                                                            post_data.decode('utf-8')))
        # We get query params
        q_params = self.get_queries()
        # We get body params
        body_params = json_loads(post_data.decode('utf-8'))
        # We return the return response
        res = self.execute_return_res(q_params, body_params)

        self._set_response()
        self.wfile.write("{}".format(res).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    """
    The runner function
    """
    httpd = server_class(('', port), handler_class)
    print('[-] Starting dycow, port<{}>, conf-file<{}>...\n'.format(port, CONF_FILE))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print('[x] Stopping dycow...\n')
    print("- " * 30)


def help_center():
    print("[x] Help center !\n[x] Run : dw <port> <conf-file> \n"
          "[x] Documentation online https://github.com/sanix-darker/dycow")


if __name__ == '__main__':

    if len(argv) == 3:
        CONF_FILE = argv[2]
        # We check if a config file have been provide
        if path.exists(CONF_FILE):
            # We check if the port is a numeric value
            if argv[1].isnumeric():
                print("- " * 30)
                # We parse and get requests as dict from the configuration file
                REQS = parse_conf_file(CONF_FILE)
                # We start the server
                run(port=int(argv[1]))
            else:
                print("[x] Port Error !\n[x] Run : dw <port> <conf-file> \n"
                      "[x] Documentation online https://github.com/sanix-darker/dycow")
        else:
            print("[x] Error !\n[x] This file '{}' doesn't exist !".format(CONF_FILE))
    elif len(argv) <= 2:
        help_center()
    else:
        print("[x] Error !\n[x] Run : dw <port> <conf-file> \n"
              "[x] Documentation online https://github.com/sanix-darker/dycow")
