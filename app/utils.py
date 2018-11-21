import magic, base64, hmac, hashlib, time
from app import app, jsonrpc
# from app import s3_client
from config import Config


def get_mime_type(url):
    with open(url, 'w') as file:
        return magic.from_buffer(file.read(), mime=True)


# def generate_key(key, message):
#     key = bytes(key, 'UTF-8')
#     message = bytes(message, 'UTF-8')
#
#     digester = hmac.new(key, message, hashlib.sha1)
#     signature = digester.digest()
#     return base64.b64encode(signature)
#
#
# @jsonrpc.method('api.upload_file')
# @app.route('/api/file/<string:filename>')
# def upload_file(b64content, filename):
#     s3_client.put_object(Bucket=Config.S3_BUCKET_NAME, Key=filename, Body=b64content)
#
#
# @jsonrpc.method('api.download_file')
# def download_file(filename):
#     response = s3_client.get_object(Bucket=Config.S3_BUCKET_NAME, Key=filename)
#     content = response.get('Body').read().decode('UTF-8')
#     return content
#
#
# def get_file(filename):
#     response = s3_client.get_object(Bucket=Config.S3_BUCKET_NAME, Key=filename)
#
#     now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
#     string_to_sign = "GET\n\n\n\nx-amz-date:{}\n/{}/{}".format(now, Config.S3_BUCKET_NAME, filename)
#     signature = generate_key(Config.S3_SECRET_ACCESS_KEY, string_to_sign).decode("UTF-8")
#
#     response.headers["Authorization"] = "AWS {}:{}".format(Config.S3_ACCESS_KEY_ID, signature)
#     response.headers["X-Amz-Date"] = now
#     response.headers["Date"] = now
#     response.headers["Host"] = "{}.hb.bizmrg.com".format(Config.S3_BUCKET_NAME)
#     response.headers["X-Accel-Redirect"] = "/s3/{}".format(filename)
#
#     return response