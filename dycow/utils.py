from dycow import search, traceback, stdout


def grep(content: str, pattern: str) -> list:
    """
    A dump grep method on a content lol

    """
    return [index if search(pattern, line) else None for index, line in enumerate(content.split("\n"))]


def get_trace():
    print("[x] Exception in code:")
    print("-" * 60)
    traceback.print_exc(file=stdout)
    print("-" * 60)


def loop_bodies(k: int, url_path: str, lines: list):
    """
    We loop lines here to extract :
    - query params
    - command to execute
    - response to return
    """
    res = "request sent."
    command, body_params, query_params = [], [], []
    # There are some query params
    if "?" in url_path:
        for p in url_path.split("?")[1].split("&"):
            query_params.append(p)

    for j in range(k, len(lines)):
        if len(lines[j]) <= 2:
            break

        if "var:" in lines[j]:
            body_params = lines[j].split("var:")[1].replace("\n", "").replace(" ", "").split(",")

        if "cmd:" in lines[j]:
            command.append(lines[j].split("cmd:")[1].lstrip().rstrip())

        if "res:" in lines[j]:
            res = lines[j].split("res:")[1].lstrip().rstrip()

    return query_params, body_params, command, res


def parse_conf_file(conf_file: str) -> list:
    """
    We parse the content of the configuration file
    """
    with open(conf_file, "r") as fil:
        conf_content = fil.read()
        lines = conf_content.split("\n")

        reqs = []
        try:
            for i in range(0, len(lines)):
                if i in grep(conf_content, "GET") or i in grep(conf_content, "POST"):
                    url_path = lines[i].split(" ")[2].replace("\n", "")

                    (query_params, body_params, command, res) = loop_bodies(i, url_path, lines)

                    reqs.append({"type": lines[i].split(" ")[1].replace("\n", ""), "url_path": url_path,
                                 "query_params": query_params, "body_params": body_params, "command": command,
                                 "res": res})
        except Exception as es:
            print("[x] There is an error with your configuration file !")
            print("[x] Please check the documentation !")
            get_trace()
            exit()

        return reqs
