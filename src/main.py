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


def generate_manifest(addon_name, author_name) -> tuple:
    """
    return (manifest of behavior pack), (manifest of resource pack)
    """
    rp_header_uuid = uuid.uuid4()
    rp_modules_uuid = uuid.uuid4()
    rp_manifest_json = (
        '{\n',
        '    "format_version": 2,\n',
        '    "header": {\n',
        f'        "description": "Created by {author_name}",\n',
        f'        "name": "{addon_name} resource Pack",\n',
        f'        "uuid": "{rp_header_uuid}",\n',
        f'        "version": [ 0, 0, 1 ],\n',
        f'        "min_engine_version": [ 1, 14, 0 ]\n'
        '    },\n'
        '    "modules": [\n'
        '        {\n'
        f'            "description": "{addon_name} resource pack",\n',
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
        f'        "description": "Created by {author_name}",\n',
        f'        "name": "{addon_name} behavior pack",\n',
        f'        "uuid": "{bp_header_uuid}",\n',
        f'        "version": [ 0, 0, 1 ],\n',
        f'        "min_engine_version": [ 1, 14, 0 ]\n'
        '    },\n'
        '    "modules": [\n'
        '        {\n'
        f'            "description": "{addon_name} behavior pack",\n',
        '            "type": "data",\n'
        f'            "uuid": "{bp_modules_uuid}",\n',
        f'            "version": [ 0, 0, 1 ]\n',
        '        }\n'
        '    ]\n'
        '}\n'
    )
    return rp_manifest_json, bp_manifest_json


def generate_behavior_pack(author_name, addon_name, where_to_generate: Path):
    behavior_pack_path = where_to_generate / f"{addon_name}BP"
    shutil.copytree(Path(__file__).parent / "addon_template" / "templateBP",
                    behavior_pack_path)
    manifest_path = behavior_pack_path / "manifest.json"
    manifest_path.touch()
    with manifest_path.open("w") as file:
        for text in generate_manifest(addon_name, author_name)[0]:
            file.write(text)


def generate_resource_pack(author_name, addon_name, where_to_generate: Path):
    resource_pack_path = where_to_generate / f"{addon_name}RP"
    shutil.copytree(Path(__file__).parent / "addon_template" / "templateRP",
                    resource_pack_path)

    manifest_path = resource_pack_path / "manifest.json"
    manifest_path.touch()
    with manifest_path.open("w") as file:
        for text in generate_manifest(addon_name, author_name)[1]:
            file.write(text)


def generate_addon(author_name, addon_name, generating_location):
    addon_path = Path(generating_location) / addon_name
    addon_path.mkdir()
    generate_behavior_pack(author_name, addon_name, addon_path)
    generate_resource_pack(author_name, addon_name, addon_path)


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
    """Usage: adgemin [--addon_name --author_name --generating_location]"""
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
    generate_addon(author_name, addon_name, generating_location)
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
