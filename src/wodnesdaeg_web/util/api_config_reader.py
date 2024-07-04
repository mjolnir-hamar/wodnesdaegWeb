import yaml


class ApiConfigReader:

    @classmethod
    def read_config(cls, api_config_yaml: str):
        with open(api_config_yaml, "r") as _y:
            return yaml.safe_load(_y)
