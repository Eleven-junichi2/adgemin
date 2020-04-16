from pathlib import Path
import sys
import uuid

import fire

__file__ = sys.argv[0]


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


def generate_addon(author_name, addon_name):
    addon_path = Path(__file__).parent / addon_name
    addon_path.mkdir()

    # generate behavior pack
    behavior_pack_path = addon_path / f"{addon_name}BP"
    behavior_pack_path.mkdir()

    manifest_path = behavior_pack_path / "manifest.json"
    manifest_path.touch()
    with manifest_path.open("w") as file:
        for text in generate_manifest(addon_name, author_name)[0]:
            file.write(text)

    dir_path = behavior_pack_path / "animation_controllers"
    dir_path.mkdir()

    dir_path = behavior_pack_path / "entities"
    dir_path.mkdir()

    dir_path = behavior_pack_path / "items"
    dir_path.mkdir()

    dir_path = behavior_pack_path / "loot_tables"
    dir_path.mkdir()
    entities_path = dir_path / "entities"
    entities_path.mkdir()
    gameplay_path = dir_path / "gameplay"
    gameplay_path.mkdir()
    entities_path = gameplay_path / "entites"
    entities_path.mkdir()
    fishing_path = gameplay_path / "fishing"
    fishing_path.mkdir()

    dir_path = behavior_pack_path / "recipes"
    dir_path.mkdir()

    dir_path = behavior_pack_path / "scripts"
    dir_path.mkdir()
    client_path = dir_path / "client"
    client_path.mkdir()
    server_path = dir_path / "server"
    server_path.mkdir()

    dir_path = behavior_pack_path / "spawn_rules"
    dir_path.mkdir()

    dir_path = behavior_pack_path / "trading"
    dir_path.mkdir()
    economy_trades_path = dir_path / "economy_trades"
    economy_trades_path.mkdir()

    pack_icon_path = behavior_pack_path / "pack_icon.png"
    pack_icon_path.touch()

    # generate resource pack
    resource_pack_path = addon_path / f"{addon_name}RP"
    resource_pack_path.mkdir()

    manifest_path = resource_pack_path / "manifest.json"
    manifest_path.touch()
    with manifest_path.open("w") as file:
        for text in generate_manifest(addon_name, author_name)[1]:
            file.write(text)

    dir_path = resource_pack_path / "animation_controllers"
    dir_path.mkdir()

    dir_path = resource_pack_path / "animations"
    dir_path.mkdir()

    dir_path = resource_pack_path / "attachables"
    dir_path.mkdir()

    dir_path = resource_pack_path / "entity"
    dir_path.mkdir()

    dir_path = resource_pack_path / "models"
    dir_path.mkdir()
    entity_path = dir_path / "entity"
    entity_path.mkdir()

    dir_path = resource_pack_path / "particles"
    dir_path.mkdir()

    dir_path = resource_pack_path / "render_controllers"
    dir_path.mkdir()

    dir_path = resource_pack_path / "texts"
    dir_path.mkdir()

    dir_path = resource_pack_path / "textures"
    dir_path.mkdir()

    dir_path = resource_pack_path / "ui"
    dir_path.mkdir()

    pack_icon_path = resource_pack_path / "pack_icon.png"
    pack_icon_path.touch()


def navigate():
    print("'Adgemin' minecraft addon template generator")
    print("Created by eleven-junichi2")
    author_name = input(("What's your name as author of your addon?"))
    addon_name = input(("What's your addon name?: "))
    generate_addon(author_name, addon_name)


def main():
    navigate()


if __name__ == "__main__":
    main()
