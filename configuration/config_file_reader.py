from os import getenv
from os.path import dirname, abspath, join, splitext, exists
import json


class ConfigReader:

    def __init__(self):
        self.config_data = None

    def read_file(self, file_name):
        file_path = self._get_file_path(file_name)
        extension = splitext(file_path)[-1].lower()

        if extension == '.json':
            try:
                self.config_data = self._read_json_file(file_path)
            except Exception as ex:
                raise Exception("Could not read file: {}, exception thrown: {}".format(file_name, str(ex)))
        else:
            try:
                self.config_data = self._read_text_file(file_path)
            except Exception as ex:
                raise Exception("Could not read file: {}, exception thrown: {}".format(file_name, str(ex)))
        return self.config_data

    @staticmethod
    def _read_text_file(file_path):
        config_data = {}
        with open(file_path, 'r') as infile:
            for line in infile:
                output_line = line.splitlines()
                output = output_line[0].strip().split(':')
                config_data[output[0]] = output[1]
        return config_data

    @staticmethod
    def _read_json_file(file_path):
        with open(file_path, 'r') as infile:
            config_data = json.load(infile)
        return config_data

    @staticmethod
    def _get_file_path(resource_file):
        directory_path = dirname(abspath(__file__))
        filepath = join(directory_path, resource_file)
        if not exists(filepath):
            config_dir = getenv('CONFIG_DIR', None)
            if config_dir is None:
                raise ValueError('Environmental variable CONFIG_DIR needs to be set to use configuration file with '
                                 'location outside the configuration folder')
            else:
                filepath = join(config_dir, resource_file)
        return filepath
