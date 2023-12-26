import os
import sys
from flask import Flask
from flask import request, make_response, jsonify
from flask_cors import CORS
import io
import csv

app = Flask(__name__, static_folder='', template_folder='')
CORS(app)

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# Page generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
from PageGenerator import PageGenerator

generator = PageGenerator()

@app.route('/', methods=['GET'])
def index():
  return 'Flask server is running :)'

@app.route('/set_title', methods=['POST'])
def set_title():
  arguments = request.get_json()
  generator.set_title(title=arguments['title'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_subtitle', methods=['POST'])
def set_subtitle():
  filebuffer = request.files.get('csvfile')
  if filebuffer is None:
    return jsonify(message='ファイルを選択してください'), 400
  elif 'text/csv' != filebuffer.mimetype:
    return jsonify(message='CSVファイル以外は受け付けません'), 415

  filecontent = filebuffer.stream.read().decode('SHIFT-JIS')
  csvreader = csv.reader(filecontent.splitlines(), delimiter=',')
  generator.set_subtitle(csvreader=csvreader)
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_n_summary_texts', methods=['POST'])
def set_n_summary_texts():
  arguments = request.get_json()
  generator.set_n_summary_texts(n_summary_texts=arguments['n_summary_texts'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_system_character', methods=['POST'])
def set_system_character():
  arguments = request.get_json()
  generator.set_system_character(text=arguments['text'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_subtitle_texts', methods=['GET'])
def set_subtitle_texts():
  generator.set_subtitle_texts()
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_function_tool', methods=['GET'])
def set_function_tool():
  generator.set_function_tool()
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/get_llm_payload', methods=['GET'])
def get_llm_payload():
  payload = generator.get_llm_payload()
  response = {'result': True, 'payload': payload}

  return make_response(jsonify(response))

@app.route('/execute', methods=['GET'])
def execute():
  generator.execute()
  response = {'result': True}

  return make_response(jsonify(response))

if __name__ == '__main__':
  app.debug = True
  app.run(host='127.0.0.1', port=5432)