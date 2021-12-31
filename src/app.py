#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.helpers import make_response
from flask_api import status
import pandas as pd
from io import BytesIO

XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


app = Flask("Excel_Web-App")
	

@app.route("/", methods=["GET"])
def form():
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
    app.run(debug=True)