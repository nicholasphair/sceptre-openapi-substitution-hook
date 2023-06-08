# -*- coding: utf-8 -*-

from hook.openapi_substituter import (
    OpenApiSubstituter,
    OPENAPI_KEY,
    OPENAPI_SUBSTITUTIONS_KEY,
    OPENAPI_INPUT_PATH_KEY,
    OPENAPI_OUTPUT_PATH_KEY,
)
from pathlib import Path


class TestOpenApiSubstituer:
    hook = OpenApiSubstituter()

    def setup(self):
        self.hook.argument = {
            OPENAPI_KEY: {
                OPENAPI_SUBSTITUTIONS_KEY: {
                    "limit_max": 42,
                    "default_description": "foobar",
                }
            }
        }

    def test_substitution(self, tmp_path):
        input_path = Path(__file__).parent / "petstore.yaml"
        tmp_input_path = tmp_path / "petstore.yaml"
        tmp_input_path.write_text(input_path.read_text())
        tmp_output_path = tmp_path / "petstore_updated.yaml"

        self.hook.argument[OPENAPI_KEY][OPENAPI_INPUT_PATH_KEY] = tmp_input_path
        self.hook.argument[OPENAPI_KEY][OPENAPI_OUTPUT_PATH_KEY] = tmp_output_path
        self.hook.run()

        assert tmp_output_path.exists()
        with open(tmp_output_path, "r") as f:
            data = f.read()
        for to_sub in self.hook.argument[OPENAPI_KEY][OPENAPI_SUBSTITUTIONS_KEY].keys():
            assert to_sub not in data
