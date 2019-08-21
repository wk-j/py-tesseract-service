from flask import Flask
from flask import request
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import sys
import os

app = Flask(__name__)


def set_prefix():
    prefix = os.path.dirname(os.path.abspath(__file__)) + "/tessdata"
    os.environ["TESSDATA_PREFIX"] = prefix


@app.route('/ocr', methods=['POST'])
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
