import os
import re
import json

def extract_hsi_data(input_directory, output_json):
    """
    指定したディレクトリ内の .nh9 ファイルをスキャンし、ファイル名から日時を抽出して
    階層構造に基づくフォルダ情報と共にJSONファイルに保存する。

    - ファイル名から日時情報を取得（形式: YYYYMMDD_HHMMSS）
    - ファイルのディレクトリ階層から「日時フォルダ」と「場所フォルダ」を取得
    - 取得した情報をリストに格納し、JSONファイルとして保存

    Args:
        input_directory (str): NH9ファイルを含む親ディレクトリのパス。
        output_json (str): 抽出したデータを保存するJSONファイルのパス。

    Returns:
        None
    """

    pattern = re.compile(r".*_(\d{8}_\d{6})\.nh9")
    hsi_data = []

    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".nh9"):
                match = pattern.match(file)
                if match:
                    datetime_str = match.group(1)
                    relative_path = os.path.relpath(root, input_directory)
                    path_parts = relative_path.split(os.sep)

                    hsi_data.append({
                        "file_name": file,
                        "id": datetime_str,
                        "datetime_folder": path_parts[0] if len(path_parts) > 0 else "",
                        "location_folder": path_parts[1] if len(path_parts) > 1 else ""
                    })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(hsi_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted HSI data saved to {output_json}")

if __name__ == "__main__":
    extract_hsi_data("/mnt/hdd1/toyo/workspace/data", "hsi_data_ids.json")
