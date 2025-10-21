import json
from json import JSONDecodeError
from typing import Optional

from facefusion.filesystem import is_file
from facefusion.types import Content


def read_json(json_path : str) -> Optional[Content]:
    if is_file(json_path):
        try:
            # --- 这是我们修改的核心部分 ---
            with open(json_path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except JSONDecodeError:
            pass
    return None


def write_json(json_path : str, content : Content) -> bool:
    # --- 为了代码的健壮性，写入时也明确指定UTF-8 ---
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(content, json_file, indent = 4, ensure_ascii=False)
    return is_file(json_path)
