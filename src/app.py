#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.helpers import make_response
from flask_api import status
import pandas as pd
from io import BytesIO

XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

from flask import has_request_context, request
from flask.logging import default_handler
import logging

LOGFILE_NAME = "INFO.log"

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler(LOGFILE_NAME))

app = Flask("Excel_Web-App")

#class RequestFormatter(logging.Formatter):
#    def format(self, record):
#        if has_request_context():
#            record.url = request.url
#            record.remote_addr = request.remote_addr
#        else:
#            record.url = None
#            record.remote_addr = None
#
#        return super().format(record)
#
#formatter = RequestFormatter(
#    '[%(asctime)s] %(remote_addr)s requested %(url)s '
#    '%(levelname)s in %(module)s: %(message)s'
#)

#default_handler.setFormatter(formatter)
#default_handler.setLevel(logging.DEBUG)
#
#app.logger.setLevel(logging.DEBUG)
#log_handler = logging.FileHandler(LOGFILE_NAME)
#log_handler.setLevel(logging.DEBUG)
#app.logger.addHandler(log_handler)


#app.logger.debug('DEBUG')
#app.logger.info('INFO')
#app.logger.warning('WARNING')
#app.logger.error('ERROR')
#app.logger.critical('CRITICAL')
#logging.basicConfig(level=logging.INFO)

	

@app.route("/", methods=["GET"])
def form():
    #app.logger.info('called hello world')

    if request.method == "GET" and "code" in request.args:
        code = request.args.get('code')
        df = make_data(code)
        towrite = BytesIO()
        df.to_excel(towrite)
        towrite.seek(0)
        response = make_response()
        response.data = towrite.read()

        download_filename = "sample.xlsx"
        response.headers['Content-Disposition'] = 'attachment; filename=' + download_filename

        response.mimetype = XLSX_MIMETYPE
        return response

    return "Bad request. Input correct code.", status.HTTP_400_BAD_REQUEST


def make_data(code: str) -> pd.DataFrame:
    df = pd.DataFrame([[1, 2]], columns=[code, code])
    return df

if __name__ == "__main__":
    app.run(debug=False)