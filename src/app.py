from flask import Flask
from flask import request
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import sys
import os
from github import Github
import markdown
from lxml import etree
from functools import reduce

app = Flask(__name__)
token = os.environ['GITHUB_TOKEN']


def set_prefix():
    prefix = os.path.dirname(os.path.abspath(__file__)) + "/tessdata"
    os.environ["TESSDATA_PREFIX"] = prefix


def get_links(body):
    body = body.replace("![", "[")
    doc = etree.fromstring(markdown.markdown(body))
    return [link for link in doc.xpath('//a') if "user-images" in link.get("href")]


def update_issue(repo, issue, body):
    links = get_links(body)
    github = Github(token)
    github_repo = github.get_repo(repo)
    github_repo.get_issue(int(issue)).edit(body=body)


def ocr_url(url):
    response = requests.get(url + "?access_token=" + token)
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(
        img, lang='Thai',  config='-c preserve_interword_spaces=1,tessedit_create_hocr=1')
    return text


def create_detail(texts):
    title, text = texts
    return f"<details><summary>{title}</summary>\n\n```java\n{text}\n```\n\n</details>"


@app.route("/ocr-issue", methods=["POST"])
def github():
    content = request.get_json()
    project = content["repository"]["name"]
    action = content["action"]
    title = content["issue"]["title"]
    body = content["issue"]["body"]
    number = content["issue"]["number"]
    org = content["organization"]["login"]

    links = get_links(body)
    ocr_text = [(link.text, ocr_url(link.get("href"))) for link in links]
    details = [create_detail(x) for x in ocr_text]
    new_body = body + '\n' + "\n".join(details)
    update_issue(f"{org}/{project}", number, new_body)

    return new_body


@app.route('/ocr-url', methods=['POST'])
def postJsonHandler():
    content = request.get_json()
    response = requests.get(content['url'])
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(
        img, lang='Thai', output_type=pytesseract.Output.STRING, config='-c preserve_interword_spaces=1,tessedit_create_hocr=1')
    textre = text.replace(" ", "")
    return textre


if __name__ == "__main__":
    set_prefix()

    port = "5000" if len(sys.argv) < 2 else sys.argv[1]
    app.run(debug=True, host='0.0.0.0', port=port)
