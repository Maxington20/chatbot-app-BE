from flask import Flask, jsonify, request
from flask_cors import CORS
from helper_functions import construct_index, chatbot, add_document, delete_document, update_document_list

app  = Flask(__name__)
CORS(app)

@app.route('/api/getDocuments', methods=['GET'])
def getDocuments():
    return jsonify({'documents': update_document_list()})


@app.route('/api/addFile', methods=['GET'])
def addFile():
    print(request.args.get('document_user'), request.args.get('document_name'), request.args.get('document_content'))
    add_document(request.args.get('document_user'), request.args.get('document_name'), request.args.get('document_content'))
    return jsonify({'message': 'File added successfully'})


@app.route('/api/deleteFile', methods=['GET'])
def deleteFile():
    delete_document(request.args.get('document_user'), request.args.get('document_name'))
    return jsonify({'message': 'File deleted successfully'})


@app.route('/api/prompt', methods=['GET'])
def prompt():
    return jsonify({'message': chatbot(request.args.get('prompt'))})


if __name__ == '__main__':
    app.run(debug=True)