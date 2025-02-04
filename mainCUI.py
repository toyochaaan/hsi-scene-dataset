import os
import numpy as np
import h5py
from tqdm import tqdm

IGNORE_FOLDERS = ['.Spotlight-V100', '.fseventsd', 'System Volume Information', '$RECYCLE.BIN']

# NH9ファイルをnpy形式に変換する関数
def convert_nh9_to_npy(nh9_file):
    try:
        with open(nh9_file, 'rb') as file:
            data = np.fromfile(file, dtype=np.float32)
        return data
    except Exception as e:
        print(f"エラー: {nh9_file} の変換中に問題が発生しました: {e}")
        return None

# 場所フォルダ内のNH9ファイルをHDF5に圧縮保存
def process_files_in_folder(location_folder_path, date_folder_name, location_folder_name, output_root):
    try:
        # HDF5ファイル名を設定
        hdf5_filename = f"{location_folder_name}_{date_folder_name}.h5"
        hdf5_file_path = os.path.join(output_root, hdf5_filename)

        print(f"HDF5ファイル生成中: {hdf5_file_path}")

        # NH9ファイルリストを取得
        nh9_files = [f for f in os.listdir(location_folder_path) if f.endswith('.nh9')]
        if not nh9_files:
            print(f"警告: {location_folder_path} にNH9ファイルが見つかりません。")
            return

        # HDF5ファイルを作成し、各NH9ファイルをデータセットとして保存
        with h5py.File(hdf5_file_path, 'w') as hdf5_file:
            for nh9_file in tqdm(nh9_files, desc=f"Processing {location_folder_name}", unit="file"):
                nh9_path = os.path.join(location_folder_path, nh9_file)
                npy_data = convert_nh9_to_npy(nh9_path)  # NH9をNumPyデータに変換
                if npy_data is not None:
                    dataset_name = os.path.splitext(nh9_file)[0]  # データセット名としてNH9ファイル名を使用
                    hdf5_file.create_dataset(dataset_name, data=npy_data, compression="gzip")
                else:
                    print(f"エラー: {nh9_file} のデータセット作成に失敗しました。")
        print(f"完了: HDF5ファイルを生成しました -> {hdf5_file_path}")
    except Exception as e:
        print(f"エラー: {location_folder_path} の処理中に問題が発生しました: {e}")

# 指定された日付フォルダを処理
def process_date_folder(date_folder_path, output_root):
    try:
        # 日付フォルダ名を取得（例: 08022024）
        date_folder_name = os.path.basename(date_folder_path)

        # 場所フォルダの探索
        location_folders = [l for l in os.listdir(date_folder_path) if os.path.isdir(os.path.join(date_folder_path, l))]
        if not location_folders:
            print(f"警告: {date_folder_path} に場所フォルダが見つかりませんでした。")
            return

        for location_folder in location_folders:
            location_folder_path = os.path.join(date_folder_path, location_folder)
            print(f"場所フォルダを処理中: {location_folder_path}")

            # 場所フォルダ内のNH9ファイルを処理
            process_files_in_folder(location_folder_path, date_folder_name, location_folder, output_root)
    except Exception as e:
        print(f"エラー: 日付フォルダ {date_folder_path} の処理中に問題が発生しました: {e}")

if __name__ == "__main__":
    # 入力日付フォルダと出力フォルダをCUIで指定
    input_folder = input("処理する日付フォルダのパスを入力してください: ").strip()
    output_folder = input("HDF5ファイルを保存するルートフォルダのパスを入力してください: ").strip()

    if os.path.isdir(input_folder) and os.path.isdir(output_folder):
        process_date_folder(input_folder, output_folder)
    else:
        print("エラー: 有効なフォルダパスを指定してください。")
