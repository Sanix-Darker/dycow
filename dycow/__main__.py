# dycow
from dycow import (
    VERSION,
    BaseHTTPRequestHandler,
    HTTPServer,
    argv,
    json_loads,
    path,
    system,
    urlparse,
)
from dycow.utils import cmd_output_to_res, parse_conf_file

CONF_FILE = ""
REQS = []


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def get_queries(self):
        """
        Getting query params
        """
        q_params = []
        for p in urlparse(self.path).query.split("&"):
            try:
                q_params.append({"key": p.split("=")[0], "value": p.split("=")[1]})
            except Exception:
                pass

        return q_params

    def execute_return_res(self, q_params: list, body_params=None):
        """
        This method will execute commands and return appropriate response

        """
        res = ""
        for r in REQS:
            if (r["type"] == "GET" or r["type"] == "POST") and str(self.path).split(
                "?"
            )[0] == r["url_path"].split("?")[0]:

                res = r["res"]
                # To create / empty the file
                open("./out", "w").close()
                if (
                    body_params is not None
                    and bool(body_params)
                    and r["type"] == "POST"
                ):
                    # it's the good link
                    for cmd in r["command"]:
                        for pr in r["body_params"]:
                            cmd = (
                                cmd.replace("#{}#".format(pr), body_params[pr])
                                if "#" + pr + "#" in cmd
                                else ""
                            )
                        system(cmd + " >> out")

                    res = cmd_output_to_res(res)

                    for p in r["body_params"]:
                        res = (
                            res.replace("#{}#".format(p), body_params[p])
                            if "#" + p + "#" in res
                            else res
                        )
                else:
                    # it's the good link
                    for cmd in r["command"]:
                        for p in q_params:
                            cmd = (
                                cmd.replace("#{}#".format(p["key"]), p["value"])
                                if "#" + p["key"] + "#" in cmd
                                else ""
                            )
                        system(cmd + " >> out")

                    res = cmd_output_to_res(res)

                    for p in q_params:
                        res = (
                            res.replace("#{}#".format(p["key"]), p["value"])
                            if "#" + p["key"] + "#" in res
                            else res
                        )

        return res

    def do_GET(self):
        """
        The built in GET handler
        """
        self._set_response()
        self.wfile.write(
            "{}".format(self.execute_return_res(self.get_queries())).encode("utf-8")
        )

    def do_POST(self):
        """
        The built in POST handler
        """
        self._set_response()
        self.wfile.write(
            "{}".format(
                self.execute_return_res(
                    self.get_queries(),
                    json_loads(
                        self.rfile.read(int(self.headers["Content-Length"])).decode(
                            "utf-8"
                        )
                    ),
                )
            ).encode("utf-8")
        )


def run(server_class=HTTPServer, handler_class=S, port=8080):
    """
    The runner function
    """
    print("- " * 30)
    httpd = server_class(("", port), handler_class)
    print(
        "[-] Starting dycow instance...\n[-] On port<{}>, conf<{}>...\n".format(
            port, CONF_FILE
        )
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print("[x] Stopping dycow...\n")
    print("- " * 30)


def help_center():
    print(
        "[-] dycow v"
        + VERSION
        + ".\n[-] Help center !\n[x] Run : dw <port> <conf-file> \n"
        "[x] Documentation online https://github.com/sanix-darker/dycow"
    )


if __name__ == "__main__":
    if len(argv) == 3:
        CONF_FILE = argv[2]
        # We check if a config file have been provide
        if path.exists(CONF_FILE):
            # We check if the port is a numeric value
            if argv[1].isnumeric():
                # We parse and get requests as dict from the configuration file
                REQS = parse_conf_file(CONF_FILE)
                # We start the server
                run(port=int(argv[1]))
            else:
                help_center()
        else:
            print("[x] Error !\n[x] This file '{}' doesn't exist !".format(CONF_FILE))
            help_center()
    else:
        help_center()
