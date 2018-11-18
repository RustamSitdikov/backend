#! /usr/bin/env python3

import sys
import base64
import config
from . import jsonrpc
from . import s3_session, s3_client
from jsonrpc.proxy import ServiceProxy

if __name__ == "__main__":
    if len( sys.argv ) != 2:
        print(sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]

    service = ServiceProxy('http://127.0.0.1:5000/api/')
    with open( filename, 'rb') as input_file:
        content = input_file.read()

        b64_content = base64.b64encode(content).decode("utf-8")
        print(b64_content)

        # response = service.api.upload_file(b64_content)
        # print(response)
        response = service.api.download_file(filename)


    @jsonrpc.method('print_name')
    def foo():
        return dict(name='Ivan')


    @jsonrpc.method('api.upload_file')
    def upload_file(b64_content, filename):
        content = base64.b64decode(b64_content).encode('utf-8')
        s3_client.put_object(Bucket=config.S3_BUCKET_NAME, Key=filename, Body=content)
        return b64_content


    @jsonrpc.method('api.download_file')
    def download_file(filename):
        response = s3_client.get_object(Bucket=config.S3_BUCKET_NAME, Key=filename)
        return response.get('Body')

    @jsonrpc.method('api.generate_key')
    def generate_key(key, message):
        key = bytes(key, 'utf-8')
        message = bytes(message, 'utf-8')
        return key