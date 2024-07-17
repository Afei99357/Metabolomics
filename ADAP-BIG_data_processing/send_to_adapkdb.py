import argparse
import json
import re
import requests

from os.path import join
from typing import Dict, List
from urllib.parse import urljoin


def strip(x: str) -> str:
    return x.strip().lower()


def create_json(filename: str) -> Dict:
    meta = json.load(open(filename))

    external_id = None
    match = re.compile(".*StudyID=(ST[0-9]{6})").match(meta["url"])
    if match is not None:
        external_id = match.group(1)
    if match is None:
        if meta["study_id"] is not None:
            external_id = meta["study_id"]

    tags = []
    for key in meta["tags"]:
        values = meta["tags"][key]
        if type(values) is not list:
            values = [values]
        for value in values:
            if value is None or len(value) == 0:
                continue
            tags.append({"tagKey": strip(key), "tagValue": strip(value)})

    submission = {
        "name": meta["study_title"],
        "description": meta["study_summary"],
        "reference": meta["url"],
        "externalId": external_id,
        "tags": tags,
    }

    return submission


def check_chromatography(filenames: List[str]) -> str:

    for filename in filenames:
        for line in open(filename):
            line = line.strip()
            if line.startswith("IonMode:"):
                _, value = line.split(":", maxsplit=1)
                value = value.strip().upper()
                if value == "P":
                    return "LC_MSMS_POS"
                elif value == "N":
                    return "LC_MSMS_NEG"

    return "GAS"


def send_to_adapkdb(
    url: str, username: str, password: str, meta_filename: str, filenames: List[str]
):
    url = urljoin(url, "rest/fileupload/")
    print(url)
    submission = create_json(meta_filename)
    data = {
        "username": username,
        "password": password,
        "file-type": "MSP",
        "chromatography": check_chromatography(filenames),
        "json": json.dumps(submission),
    }
    files = [("files", open(filename)) for filename in filenames]

    print(data)
    response = requests.post(url, data=data, files=files)
    print(response)
    if not response:
        print(response.content)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sends URL request to ADAP-KDB")
    parser.add_argument("--url", help="URL to the ADAP-KDB website", required=True)
    parser.add_argument("--username", help="Name of ADAP-KDB user", required=True)
    parser.add_argument("--password", help="Password of ADAP-KDB user", required=True)
    parser.add_argument("--meta", help="File with meta information", required=True)
    parser.add_argument("files", metavar="FILE", nargs="+", help="MSP files")

    args = parser.parse_args()
    send_to_adapkdb(args.url, args.username, args.password, args.meta, args.files)
