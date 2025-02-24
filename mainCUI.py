import os
import numpy as np
import h5py
from tqdm import tqdm

IGNORE_FOLDERS = ['.Spotlight-V100', '.fseventsd', 'System Volume Information', '$RECYCLE.BIN']

def convert_nh9_to_npy(nh9_file):
    """
    NH9ファイルをNumPy配列（npy形式）に変換する。

    Args:
        nh9_file (str): 変換するNH9ファイルのパス。

    Returns:
        numpy.ndarray or None: 変換されたNumPy配列。エラーが発生した場合は None を返す。
    """
    try:
        with open(nh9_file, 'rb') as file:
            data = np.fromfile(file, dtype=np.float32)
        return data
    except Exception as e:
        print(f"エラー: {nh9_file} の変換中に問題が発生しました: {e}")
        return None

def process_files_in_folder(location_folder_path, date_folder_name, location_folder_name, output_root):
    """
    指定された場所フォルダ内のNH9ファイルをHDF5形式で圧縮保存する。

    - HDF5ファイルは、場所フォルダ名と日付フォルダ名を組み合わせたファイル名で保存される。
    - 各NH9ファイルは、HDF5内のデータセットとして保存される。

    Args:
        location_folder_path (str): NH9ファイルが含まれるフォルダのパス。
        date_folder_name (str): 日付フォルダ名（例: 08022024）。
        location_folder_name (str): 場所フォルダ名。
        output_root (str): HDF5ファイルの保存先ディレクトリ。

    Returns:
        None
    """
    try:
        hdf5_filename = f"{location_folder_name}_{date_folder_name}.h5"
        hdf5_file_path = os.path.join(output_root, hdf5_filename)

        print(f"HDF5ファイル生成中: {hdf5_file_path}")

        nh9_files = [f for f in os.listdir(location_folder_path) if f.endswith('.nh9')]
        if not nh9_files:
            print(f"警告: {location_folder_path} にNH9ファイルが見つかりません。")
            return

        with h5py.File(hdf5_file_path, 'w') as hdf5_file:
            for nh9_file in tqdm(nh9_files, desc=f"Processing {location_folder_name}", unit="file"):
                nh9_path = os.path.join(location_folder_path, nh9_file)
                npy_data = convert_nh9_to_npy(nh9_path)
                if npy_data is not None:
                    dataset_name = os.path.splitext(nh9_file)[0]
                    hdf5_file.create_dataset(dataset_name, data=npy_data, compression="gzip")
                else:
                    print(f"エラー: {nh9_file} のデータセット作成に失敗しました。")
        print(f"完了: HDF5ファイルを生成しました -> {hdf5_file_path}")
    except Exception as e:
        print(f"エラー: {location_folder_path} の処理中に問題が発生しました: {e}")

def process_date_folder(date_folder_path, output_root):
    """
    指定された日付フォルダ内の場所フォルダを探索し、NH9ファイルをHDF5に変換する。

    - 各場所フォルダごとに `process_files_in_folder` を実行する。
    - 場所フォルダが存在しない場合は警告を表示する。

    Args:
        date_folder_path (str): 日付フォルダのパス。
        output_root (str): HDF5ファイルを保存するルートフォルダ。

    Returns:
        None
    """
    try:
        date_folder_name = os.path.basename(date_folder_path)
        location_folders = [l for l in os.listdir(date_folder_path) if os.path.isdir(os.path.join(date_folder_path, l))]

        if not location_folders:
            print(f"警告: {date_folder_path} に場所フォルダが見つかりませんでした。")
            return

        for location_folder in location_folders:
            location_folder_path = os.path.join(date_folder_path, location_folder)
            print(f"場所フォルダを処理中: {location_folder_path}")
            process_files_in_folder(location_folder_path, date_folder_name, location_folder, output_root)
    except Exception as e:
        print(f"エラー: 日付フォルダ {date_folder_path} の処理中に問題が発生しました: {e}")

if __name__ == "__main__":
    """
    CUI（コマンドライン）から日付フォルダと出力フォルダのパスを取得し、HDF5変換処理を実行する。

    - ユーザーに日付フォルダと出力フォルダのパスを入力させる。
    - 有効なフォルダが指定されているかチェックし、処理を開始する。

    Raises:
        エラー: 無効なフォルダパスが指定された場合、エラーメッセージを表示して終了する。
    """
    input_folder = input("処理する日付フォルダのパスを入力してください: ").strip()
    output_folder = input("HDF5ファイルを保存するルートフォルダのパスを入力してください: ").strip()

    if os.path.isdir(input_folder) and os.path.isdir(output_folder):
        process_date_folder(input_folder, output_folder)
    else:
        print("エラー: 有効なフォルダパスを指定してください。")
