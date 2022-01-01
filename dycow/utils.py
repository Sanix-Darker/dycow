"""
utils.py
some common functions utils
"""
from dycow import search, stdout, traceback


def grep(content: str, pattern: str) -> list:
    """
    A dump grep method on a content lol

    """
    return [
        index if search(pattern, line) else None
        for index, line in enumerate(content.split("\n"))
    ]


def get_trace():
    print("[x] Exception in code:")
    print("-" * 60)
    traceback.print_exc(file=stdout)
    print("-" * 60)


def loop_bodies(k: int, url_path: str, lines: list) -> dict:
    """
    We loop lines here to extract :
    - query params
    - command to execute
    - response to return
    """

    extracted_params = {
        "command": [],
        "body_params": [],
        "query_params": [],
        "res": "request sent.",
    }
    # There are some query params
    if "?" in url_path:
        for p in url_path.split("?")[1].split("&"):
            extracted_params["query_params"].append(p)

    for j in range(k, len(lines)):
        if len(lines[j]) <= 2:
            break

        if "var:" in lines[j]:
            extracted_params["body_params"] = (
                lines[j].split("var:")[1].replace("\n", "").replace(" ", "").split(",")
            )

        if "cmd:" in lines[j]:
            extracted_params["command"].append(
                lines[j].split("cmd:")[1].lstrip().rstrip()
            )

        if "res:" in lines[j]:
            extracted_params["res"] = lines[j].split("res:")[1].lstrip().rstrip()

    return extracted_params


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

                    extracted_params = loop_bodies(i, url_path, lines)

                    reqs.append(
                        {
                            "type": lines[i].split(" ")[1].replace("\n", ""),
                            "url_path": url_path,
                            "query_params": extracted_params["query_params"],
                            "body_params": extracted_params["body_params"],
                            "command": extracted_params["command"],
                            "res": extracted_params["res"],
                        }
                    )
        except Exception as es:
            print("[x] There is an error with your configuration file !")
            print("[x] Please check the documentation !")
            get_trace()
            exit()

        return reqs


def cmd_output_to_res(res) -> str:
    with open("./out", "r") as out_:
        return res.replace("#cmd#", out_.read())
