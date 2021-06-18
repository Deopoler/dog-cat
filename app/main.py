from flask import Flask, jsonify, request

from app.utils import get_predict, preprogress

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".")[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    if (request.method == "POST"):
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})

        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        try:
            img_bytes = file.read()
            tensor = preprogress(img_bytes)
            pred = get_predict(tensor)
            return jsonify({'cat': pred[0][0], 'dog': pred[0][1]})

        except:
            return jsonify({'error': 'error during prediction'})
