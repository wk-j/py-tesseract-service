from flask import Flask
from flask import request
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import sys

port = "5000" if len(sys.argv) > 0 else sys.argv[1]
app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def postJsonHandler():
    content = request.get_json()
    response = requests.get(content['url'])
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(img, lang='Thai')
    textre = text.replace(" ", "")
    return textre


app.run(debug=True, host='0.0.0.0', port=port)
