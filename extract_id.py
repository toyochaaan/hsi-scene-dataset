import os
import re
import json

# 入力ディレクトリと出力JSONファイル
input_directory = "/mnt/hdd1/toyo/workspace/data"  # 変更してください
output_json = "hsi_data_ids.json"

# ファイル名から日時を抽出する正規表現
pattern = re.compile(r".*_(\d{8}_\d{6})\.nh9")

# データを格納するリスト
hsi_data = []

# ファイルをスキャンして日時を抽出
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".nh9"):
            match = pattern.match(file)
            if match:
                # 日時部分を抽出
                datetime_str = match.group(1)

                # 階層構造から日時フォルダと場所フォルダを取得
                relative_path = os.path.relpath(root, input_directory)
                path_parts = relative_path.split(os.sep)
                datetime_folder = path_parts[0] if len(path_parts) > 0 else ""
                location_folder = path_parts[1] if len(path_parts) > 1 else ""

                # データを追加
                hsi_data.append({
                    "file_name": file,
                    "id": datetime_str,
                    "datetime_folder": datetime_folder,
                    "location_folder": location_folder
                })

# JSONファイルに書き出し
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(hsi_data, f, ensure_ascii=False, indent=4)

print(f"Extracted HSI data saved to {output_json}")
