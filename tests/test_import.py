import importlib.util
import os
import unittest


class TestImport(unittest.TestCase):
    def test_import_core(self):
        from animl2.core import Field, XmlModel

        _ = Field, XmlModel

    def test_import_all_models(self):
        """Test importing of all *.py files in the models directory."""

        path = importlib.util.find_spec("animl2").submodule_search_locations[0]
        models_dir = os.path.join(path, "models")

        for file_name in os.listdir(models_dir):
            if not file_name.endswith(".py") or file_name == "__init__.py":
                continue
            with self.subTest(file_name=file_name):
                module_name = file_name[:-3]
                module_path = f"animl2.models.{module_name}"

                try:
                    importlib.import_module(module_path)
                except ImportError as e:
                    self.fail(f"Failed to import module {module_path}: {e}")
