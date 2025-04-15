from io import BytesIO

import pytest
from src.app import app, allowed_file



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_success(client, mocker):
    mocker.patch('src.app.classify_file', return_value='test_class')

    data = {'file': (BytesIO(b"dummy content"), 'file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "test_class"}

def test_classifier(client):
    file_names = [['bank_statement_1.csv', 'bank_statement_1.docx', 
                   'bank_statement_1.pdf', 'bank_statement_1.xlsx', 
                   'bank_statement_2.pdf', 'bank_statement_3.pdf'], 
                  ['drivers_licence_2.jpg', 'drivers_license_1.jpg', 
                   'drivers_license_1.png', 'drivers_license_1.tif',
                   'drivers_license_3.jpg'], 
                  ['invoice_1.pdf', 'invoice_2.pdf', 'invoice_3.pdf']]
    file_types = ['bank statement', 'drivers license', 'invoice']

    for i in range(len(file_types)):
        for filename in file_names[i]:
            # cv2 and PyMuPDF only accept strings as argtype for a file, thus files/filename.ext must be provided in preprocessor
            # python.open() only accepts strings as argytpe for a file, thus files/filename.ext must be provided here
            # 'data' is a var with {"file": (file_stream, filepath)} used in preprocessor, thus must be just filename.ext
            ## Probably due to format of curl commands?
            # docx2txt and pandas accept file type argtype for a file, thus this isn't an issue for .docx, .xlsx, or .csv files
            file = open(f'files/{filename}', "rb")
            data = {"file": (BytesIO(file.read()), filename)}
            response = client.post("/classify_file", data=data, content_type="multipart/form-data")
            assert response.status_code == 200
            response_data = response.get_json()
            assert file_types[i] in response_data['file_class']





