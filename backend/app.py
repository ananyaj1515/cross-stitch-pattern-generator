from flask import Flask, request, jsonify
from flask_cors import CORS
from ImageProcessing import complete_pipeline
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Main app is running!'})

@app.route('/process', methods=['POST'])
def process_image():
    print("Request received!")
    try:
        print("Getting file...")
        if 'image' not in request.files:
            return jsonify({'error': 'No Image Provided'}), 400
        file = request.files['image']
        print(f"File received: {file.filename}")

        max_dim = int(request.form.get('max_dim',50))
        n_colors = int(request.form.get('n_colors', 15))
        print(f"Params: max_dim={max_dim}, n_colors={n_colors}")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = complete_pipeline(filepath, max_dim, n_colors)
        os.remove(filepath)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


if __name__== "__main__":
    app.run(debug=True, port=5000)
