import binascii
import json
import os
from pathlib import Path

import pandas as pd
from notion.block import CollectionViewPageBlock
from notion_as_db.configured_notion import Notion


class Alfred(Notion):
    def __init__(self):
        super().__init__()

    def create_collection4snippet(self, collection_name: str, page_block):
        tmp_schema = {
            "title": {"name": "name", "type": "title"},
            "snippet": {"name": "snippet", "type": "text"},
            "pattern": {"name": "pattern", "type": "text"}

        }
        tmp_child_page = page_block.children.add_new(CollectionViewPageBlock)
        tmp_child_page.collection = self.get_collection(
            self.create_record('collection', parent=tmp_child_page, schema=tmp_schema)
        )
        tmp_child_page.title = collection_name
        tmp_child_page.views.add_new(view_type="table")
        return tmp_child_page.collection

    def get_list_from_snippet_path(self, input_path: Path):
        tmp_json_list = list(input_path.glob("*.json"))
        tmp_list = list(json.loads(x.read_text())["alfredsnippet"] for x in tmp_json_list)
        return tmp_list

    def convert2json(self, input_list: list, save_dir_path: Path):
        df = pd.DataFrame(input_list, columns=["name", "keyword", "content"])
        for row in df.itertuples():
            uid = binascii.b2a_hex(os.urandom(15))
            uid = uid.decode("ascii")
            output = json.dumps(
                {"alfredsnippet": {"snippet": row.content, "uid": uid, "name": row.name, "keyword": row.keyword}},
                sort_keys=False, indent=4, separators=(',', ': '))
            output_file_path = save_dir_path / Path(row.name + " [" + uid + "].json")
            output_file_path.write_text(output)
