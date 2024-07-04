import yaml
from typing import Dict

from wodnesdaeg_nlp.pipeline import PipelineExecutor
import wodnesdaeg_nlp.consts.model_trainer as model_consts

from wodnesdaeg_web.model_inference_server.model_inference_server_base import ModelInferenceServerBase


class ModelInferenceServerPipelineExecutor(ModelInferenceServerBase):

    CONFIG_TEMPLATE_ROOT = "config/wodnesdaeg_nlp_config_templates"
    TASK_TO_TEMPLATE_FNAME_MAP = {
        model_consts.LEMMATIZATION: "lemmatizer_model_inference.yaml"
    }

    def __init__(self, api_config_yaml: str, model_inference_path: str):

        super().__init__(api_config_yaml)
        self._load_and_update_config(model_inference_path=model_inference_path)
        self.pipeline = PipelineExecutor(preloaded_config=self.pipeline_config)

    def __call__(self, *args, **kwargs):
        self.pipeline()

    def _load_and_update_config(self, model_inference_path: str):
        task = model_consts.LEMMATIZATION
        with open(f"{self.CONFIG_TEMPLATE_ROOT}/{self.TASK_TO_TEMPLATE_FNAME_MAP[task]}", "r") as _y:
            self.pipeline_config = yaml.safe_load(_y)

        lang, fname = model_inference_path.split("/")[-2:]
        self.model_inference_fname = fname

        if task == model_consts.LEMMATIZATION:
            pos_tagger_model_path = self.api_config["model_paths"][model_consts.POS_TAGGING][lang]
            lemmatizer_model_path = self.api_config["model_paths"][model_consts.LEMMATIZATION][lang]
            fill_paths_dict = {
                "pos_tagger_model_path": pos_tagger_model_path,
                "lemmatizer_model_path": lemmatizer_model_path
            }
        else:
            raise ValueError(f"Cannot load pipeline config for task \"{task}\"")

        fill_paths_dict["inference_file_path"] = model_inference_path
        fill_paths_dict["output_file_path"] = model_inference_path.replace(self.INPUT, self.OUTPUT).replace(".tsv", ".json")
        self._update_config(fill_paths_dict)

    def _update_config(self, fill_paths_dict: Dict[str, str]):
        for fill_path_name, fill_path_value in fill_paths_dict.items():
            fill_path = self.pipeline_config["fill_paths"][fill_path_name]
            current_position = self.pipeline_config
            fill_path = fill_path.split(".")
            for i, path_component in enumerate(fill_path):
                if path_component.isdigit():
                    path_component = int(path_component)
                if i < len(fill_path) - 1:
                    current_position = current_position[path_component]
                else:
                    if current_position[path_component] == "<to_fill>":
                        current_position[path_component] = fill_path_value
                    else:
                        raise ValueError(f"Invalid filler template value found at \"{fill_path}\"")
