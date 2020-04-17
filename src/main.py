from pathlib import Path
import sys
import os
import uuid
import json
import shutil

import fire

__file__ = sys.argv[0]

TRANSLATION_PATH = Path(__file__).parent / "translation"
DEFAULT_ADDON_GEN_LOCATION = str(Path(__file__).parent.resolve())


class AddonGenerator:
    def __init__(self, addon_name, author_name, generating_location):
        self.addon_name = addon_name
        self.author_name = author_name
        self.generating_location = generating_location

    def manifest_str(self) -> tuple:
        """
        return (manifest of behavior pack), (manifest of resource pack)
        """
        rp_header_uuid = uuid.uuid4()
        rp_modules_uuid = uuid.uuid4()
        rp_manifest_json = (
            '{\n',
            '    "format_version": 2,\n',
            '    "header": {\n',
            f'        "description": "Created by {self.author_name}",\n',
            f'        "name": "{self.addon_name} resource Pack",\n',
            f'        "uuid": "{rp_header_uuid}",\n',
            f'        "version": [ 0, 0, 1 ],\n',
            f'        "min_engine_version": [ 1, 14, 0 ]\n'
            '    },\n'
            '    "modules": [\n'
            '        {\n'
            f'            "description": "{self.addon_name} resource pack",\n',
            '            "type": "resources",\n'
            f'            "uuid": "{rp_modules_uuid}",\n',
            f'            "version": [ 0, 0, 1 ]\n',
            '        }\n'
            '    ]\n'
            '}\n'
        )
        bp_header_uuid = uuid.uuid4()
        bp_modules_uuid = uuid.uuid4()
        bp_manifest_json = (
            '{\n',
            '    "format_version": 2,\n',
            '    "header": {\n',
            f'        "description": "Created by {self.author_name}",\n',
            f'        "name": "{self.addon_name} behavior pack",\n',
            f'        "uuid": "{bp_header_uuid}",\n',
            f'        "version": [ 0, 0, 1 ],\n',
            f'        "min_engine_version": [ 1, 14, 0 ]\n'
            '    },\n'
            '    "modules": [\n'
            '        {\n'
            f'            "description": "{self.addon_name} behavior pack",\n',
            '            "type": "data",\n'
            f'            "uuid": "{bp_modules_uuid}",\n',
            f'            "version": [ 0, 0, 1 ]\n',
            '        }\n'
            '    ]\n'
            '}\n'
        )
        return rp_manifest_json, bp_manifest_json

    def generate_behavior_pack(self):
        behavior_pack_path = Path(self.generating_location) \
            / self.addon_name / \
            f"{self.addon_name}BP"
        shutil.copytree(
            Path(__file__).parent / "addon_template" / "templateBP",
            behavior_pack_path)
        manifest_path = behavior_pack_path / "manifest.json"
        manifest_path.touch()
        with manifest_path.open("w") as file:
            for text in self.manifest_str()[0]:
                file.write(text)

    def generate_resource_pack(self):
        resource_pack_path = Path(self.generating_location) \
            / self.addon_name / \
            f"{self.addon_name}RP"
        shutil.copytree(
            Path(__file__).parent / "addon_template" / "templateRP",
            resource_pack_path)

        manifest_path = resource_pack_path / "manifest.json"
        manifest_path.touch()
        with manifest_path.open("w") as file:
            for text in self.manifest_str()[1]:
                file.write(text)

    def generate(self):
        addon_path = Path(self.generating_location) / self.addon_name
        addon_path.mkdir()
        self.generate_behavior_pack()
        self.generate_resource_pack()


def load_config() -> dict:
    with open(str(Path(__file__).parent / "config.json"),
              encoding="utf-8_sig") as f:
        config = json.load(f)
    return config


def load_translation() -> dict:
    tl = {}
    with open(str(TRANSLATION_PATH / "jp.json"), "r",
              encoding="utf-8_sig") as f:
        tl["japanese"] = json.load(f)
    with open(str(TRANSLATION_PATH / "en.json"), "r",
              encoding="utf-8_sig") as f:
        tl["english"] = json.load(f)
    return tl


def navigate(addon_name="", author_name="",
             generating_location=""):
    """Usage: adgemin [--addon_name --author_name --generating_location]
    here is CUI program
    """
    config = load_config()
    LANG = config["language"]
    tl = load_translation()
    if config["generating_location"]:
        if not (os.path.exists(config["generating_location"]) and
                os.path.isdir(config["generating_location"])):
            print(tl[LANG]["conf_err"])
            print(tl[LANG]["conf_err_how_to_solve"])
            print("{} {}".format(tl[LANG]["conf_err_gen_location"],
                                 config["generating_location"]))
            input(tl[LANG]["exit"])
            return
        else:
            generating_location = config["generating_location"]
    print(tl[LANG]["title"])
    print(tl[LANG]["credit"])
    if not addon_name:
        while True:
            addon_name = input(tl[LANG]["input_addon_name"])
            if addon_name:
                break
    if not author_name:
        while True:
            author_name = input(tl[LANG]["input_author_name"])
            if author_name:
                break
    if not generating_location:
        while True:
            print(tl[LANG]["input_location"])
            print(tl[LANG]["if_you_enter_nothing"])
            inputed = input(
                f"'{DEFAULT_ADDON_GEN_LOCATION}'> ")
            if not inputed:
                generating_location = DEFAULT_ADDON_GEN_LOCATION
                break
            else:
                if os.path.exists(inputed):
                    if os.path.isdir(inputed):
                        generating_location = inputed
                        break
                    else:
                        print(tl[LANG]["location_not_dir"])
                else:
                    print(tl[LANG]["directory_not_exists"])
    AddonGenerator(addon_name, author_name, Path(
        generating_location)).generate()
    print("---")
    print(f"{tl[LANG]['result_addon_name']} {addon_name}")
    print(f"{tl[LANG]['result_author_name']} {author_name}")
    print("---")
    print(
        f"↑ {tl[LANG]['successfully']}'{generating_location}'")
    input(tl[LANG]["exit"])


def main():
    fire.Fire(navigate)


if __name__ == "__main__":
    main()
