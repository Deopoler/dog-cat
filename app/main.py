from flask import Flask, jsonify, request

from app.utils import get_predict, preprogress

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    print(filename)
    return "." in filename and filename.rsplit(".")[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    if (request.method == "POST"):
        file = request.files.get('file')
        if file is None or file.filename == "":
            print("error: no file")
            return jsonify({'error': 'no file'})

        if not allowed_file(file.filename):
            print("error: format not supported")
            return jsonify({'error': 'format not supported'})

        try:
            img_bytes = file.read()
            tensor = preprogress(img_bytes)
            pred = get_predict(tensor)
            print("success")
            return jsonify({'cat': pred[0][0], 'dog': pred[0][1]})

        except:
            print("error: error during prediction")
            return jsonify({'error': 'error during prediction'})
