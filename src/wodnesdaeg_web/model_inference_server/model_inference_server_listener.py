import os
import glob
import shutil
from time import sleep

from wodnesdaeg_nlp.consts.languages import LANGUAGES

from wodnesdaeg_web.model_inference_server.model_inference_server_base import ModelInferenceServerBase
from wodnesdaeg_web.model_inference_server.model_inference_server_pipeline_executor import ModelInferenceServerPipelineExecutor


class ModelInferenceServerListener(ModelInferenceServerBase):

    def __init__(self, api_config_yaml: str):
        super().__init__(api_config_yaml)
        self._setup_io_directories()

    def _setup_io_directories(self):
        self.input_dirs = set()
        self.io_root = self.api_config[self.API_INPUT_OUTPUT_ROOT]
        if os.path.isdir(self.io_root):
            shutil.rmtree(self.io_root)
        os.mkdir(self.io_root)
        for io_dir in self.IO_DIRS:
            self.full_io_dir = f"{self.io_root}/{io_dir}"
            if not os.path.isdir(self.full_io_dir):
                os.mkdir(self.full_io_dir)
            for lang in LANGUAGES:
                lang_io_dir = f"{self.full_io_dir}/{lang}"
                if not os.path.isdir(lang_io_dir):
                    os.mkdir(lang_io_dir)
                if io_dir == self.INPUT:
                    self.input_dirs.add(lang_io_dir)

    def listen(self):
        while True:
            for input_dir in self.input_dirs:
                new_files = glob.glob(f"{input_dir}/*")
                if len(new_files) > 0:
                    print(f"{len(new_files)} found in {input_dir}")

                    for new_file in new_files:
                        pipeline_executor = ModelInferenceServerPipelineExecutor(
                            api_config_yaml=self.api_config_yaml,
                            model_inference_path=new_file
                        )
                        pipeline_executor()
                        os.remove(new_file)
            sleep(5)
