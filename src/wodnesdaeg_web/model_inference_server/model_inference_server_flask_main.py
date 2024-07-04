import os
import json
from uuid import uuid4
from time import sleep, perf_counter
from flask import Flask, request

from wodnesdaeg_web.util.api_config_reader import ApiConfigReader
from wodnesdaeg_web.model_inference_server.model_inference_server_base import ModelInferenceServerBase


app = Flask(__name__)


API_CONFIG = ApiConfigReader.read_config(
    api_config_yaml="config/api_config.yaml"
)


@app.route("/model_inference", methods=["POST"])
def get_model_inference():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        request_json = request.json
        lang = request_json[ModelInferenceServerBase.LANG]
        model_inference_fname = f"{uuid4().hex}"
        with open(f"{API_CONFIG[ModelInferenceServerBase.API_INPUT_OUTPUT_ROOT]}/{ModelInferenceServerBase.INPUT}/{lang}/{model_inference_fname}.tsv", "w") as _o:
            _o.write(f"{request_json[ModelInferenceServerBase.INPUT_STR]}\n")

        start_time = perf_counter()
        expected_output_fname = f"{API_CONFIG[ModelInferenceServerBase.API_INPUT_OUTPUT_ROOT]}/{ModelInferenceServerBase.OUTPUT}/{lang}/{model_inference_fname}.json"
        while True:
            if not os.path.isfile(expected_output_fname):
                sleep(5)
            else:
                break
        result = {
            "runtime": perf_counter() - start_time
        }
        with open(expected_output_fname, "r") as _j:
            result["inference_result"] = json.load(_j)

        return result


if __name__ == "__main__":
    app.run(debug=True)
