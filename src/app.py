from flask import Flask, request, jsonify

from src.classifier import classify_file
app = Flask(__name__)

# Run the app
# (2) install dependencies (for Windows): 
#     python -m venv venv - first time only 
#     .\venv\Scripts\activate
#     pip install -r requirements.txt

# (3) run server 
#     python -m src.app

# (4) run using curl 
#     -> use seperate terminal after starting server
#     pdf: curl -X POST -F 'file=@files\bank_statement_1.pdf' http://127.0.0.1:5000/classify_file  
#     img: curl -X POST -F 'file=@files\drivers_license_1.jpg' http://127.0.0.1:5000/classify_file  



ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'csv', 'jpg', 'png', 'tif'}

# Labels from which the classifier makes a prediction
document_types = ['bank statement', 'invoice', 'drivers license']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    file_class = classify_file(file, document_types)
    return jsonify({"file_class": file_class}), 200

if __name__ == '__main__':
    app.run(debug=True)

