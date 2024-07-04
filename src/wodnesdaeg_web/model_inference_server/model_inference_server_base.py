from wodnesdaeg_web.util.api_config_reader import ApiConfigReader


class ModelInferenceServerBase:

    API_INPUT_OUTPUT_ROOT = "api_input_output_root"
    INPUT = "input"
    OUTPUT = "output"
    IO_DIRS = {INPUT, OUTPUT}

    LANG = "lang"
    TASK = "task"
    INPUT_STR = "input_str"

    def __init__(self, api_config_yaml: str):
        self.api_config_yaml = api_config_yaml
        self._read_api_config_yaml(api_config_yaml=api_config_yaml)

    def _read_api_config_yaml(self, api_config_yaml: str):
        self.api_config = ApiConfigReader.read_config(
            api_config_yaml=api_config_yaml
        )
