import importlib
import os
import unittest


class TestImport(unittest.TestCase):
    def test_import_core(self):
        from simple_animl.core import Field, XmlModel

        _ = Field, XmlModel

    def test_import_all_models(self):
        import simple_animl

        module_dir = os.path.dirname(os.path.abspath(simple_animl.__file__))
        models_dir = os.path.join(module_dir, "models")

        for file_name in os.listdir(models_dir):
            if not file_name.endswith(".py") or file_name == "__init__.py":
                continue
            with self.subTest(file_name=file_name):
                module_name = file_name[:-3]
                module_path = f"simple_animl.models.{module_name}"

                try:
                    importlib.import_module(module_path)
                except ImportError as e:
                    self.fail(f"Failed to import module {module_path}: {e}")
