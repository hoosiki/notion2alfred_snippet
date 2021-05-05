import shutil
from pathlib import Path

from config2.config import config

from .alfred import Alfred


def copy_config_dir_to_package_dir(dir_path: str):
    tgt_dir_path = Path(__path__[0]) / Path("config")
    if tgt_dir_path.exists():
        shutil.rmtree(str(tgt_dir_path))
    shutil.copytree(dir_path, str(tgt_dir_path), dirs_exist_ok=True)


def remove_config_dir():
    tgt_dir_path = Path(__path__[0]) / Path("config")
    if tgt_dir_path.exists():
        shutil.rmtree(str(tgt_dir_path))


def transfer_notion2alfred_snippets():
    client = Alfred()
    snippets_dict = client.get_collections_as_dict(client.block_dict["materials_reading"])["AlfredSnippets"]

    for key in snippets_dict.keys():
        saving_dir_path = Path(config.path.mac.alfred_snippets) / Path(key)
        if not saving_dir_path.exists():
            saving_dir_path.mkdir()
        else:
            for file in saving_dir_path.glob("*.json"):
                file.unlink()

    for item in snippets_dict.items():
        if item[0] == "emoji pack" and item[1].isinstance(snippets_dict["dummy"]):
            continue
        saving_dir_path = Path(config.path.mac.alfred_snippets) / Path(item[0])
        tmp_list = list((x.name, x.pattern, x.snippet) for x in item[1].get_rows())
        client.convert2json(tmp_list, saving_dir_path)
        if len(tmp_list) == 0:
            saving_dir_path.rmdir()


def transfer_alfred_snippets2notion():
    client = Alfred()
    snippet_dir_path = Path(config.path.mac.alfred_snippets)
    path_dict = dict()
    tmp_menu = client.get_collections_as_dict(client.block_dict["materials_reading"])["AlfredSnippets"][
        "dummy"].parent.parent
    for x in snippet_dir_path.glob("*"):
        path_dict[x.name] = x

    list_dict = dict()
    for key in path_dict.keys():
        list_dict[key] = client.get_list_from_snippet_path(path_dict[key])

    for key in list_dict.keys():
        tmp_collection = client.create_collection4snippet(key.lower(), tmp_menu)
        for line in list_dict[key]:
            tmp_row = tmp_collection.add_row()
            tmp_row.name = line["name"]
            tmp_row.snippet = line["snippet"]
            tmp_row.pattern = line["keyword"]
