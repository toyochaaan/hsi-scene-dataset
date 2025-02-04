import os
import glob
import sys
import cv2
import numpy as np
from tqdm import tqdm

# フォルダが存在しない場合、新規作成
def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# ハイパースペクトルデータを読み込み、画像データを生成
def hyprawread(file_path, width, height, spectral_dim):
    with open(file_path, 'rb') as file:
        img_data = np.fromfile(file, np.uint16)
    img_data = np.reshape(img_data, (height, spectral_dim, width))
    img_data = np.transpose(img_data, (0, 2, 1))  # 転置して元の順序に戻す
    return img_data

# ハイパースペクトルデータからRGB画像を抽出
def extract_rgb(img_data):
    red_band = np.mean(img_data[:, :, 54:70], axis=2)
    green_band = np.mean(img_data[:, :, 30:40], axis=2)
    blue_band = np.mean(img_data[:, :, 20:30], axis=2)

    # 0-255の範囲に正規化
    red_band = 255 * red_band / np.max(red_band)
    green_band = 255 * green_band / np.max(green_band)
    blue_band = 255 * blue_band / np.max(blue_band)

    # RGB画像として結合
    rgb_image = np.dstack((red_band, green_band, blue_band)).astype(np.uint8)
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    return rgb_image

# ハイパースペクトル画像を処理し、指定されたディレクトリに保存
def process_hyperspectral_images(input_dir, output_dir, width, height, spectral_dim):
    # 場所フォルダ内の .nh9 ファイルをリスト化
    files = glob.glob(os.path.join(input_dir, "*.nh9"))
    
    if not files:
        print(f"No .nh9 files found in {input_dir}")
        return  # .nh9ファイルがなければスキップ

    print(f"Found {len(files)} .nh9 files in {input_dir}")

    # 各ファイルをRGBに変換して保存
    for file_path in tqdm(files, desc=f"Processing files in {input_dir}"):
        img_data = hyprawread(file_path, width, height, spectral_dim)
        rgb_image = extract_rgb(img_data)

        # 出力ファイル名の設定
        base_name = os.path.basename(file_path)
        output_name = f"rgb-{os.path.splitext(base_name)[0]}.jpg"

        # 出力先のディレクトリを作成
        output_path = os.path.join(output_dir, output_name)
        make_folder(output_dir)

        # 画像を保存
        cv2.imwrite(output_path, rgb_image)
        print(f"Image saved: {output_path}")

# 場所フォルダを処理する関数
def process_hyperspectral_images_in_location_folders(date_folder, output_dir, width, height, spectral_dim):
    # 日付フォルダ内の場所フォルダを探索
    location_folders = [os.path.join(date_folder, d) for d in os.listdir(date_folder) if os.path.isdir(os.path.join(date_folder, d))]

    for location_folder in location_folders:
        print(f"Processing location folder: {location_folder}")

        # 出力先のディレクトリは「RGB-日付フォルダ/場所フォルダ」の構造を維持
        location_subdir = os.path.basename(location_folder)
        output_location_dir = os.path.join(output_dir, location_subdir)

        # 場所フォルダ内の .nh9 ファイルを処理
        process_hyperspectral_images(location_folder, output_location_dir, width, height, spectral_dim)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_folder = sys.argv[1]
    else:
        print("Please provide the date folder path.")
        sys.exit()

    # 日付フォルダ名を取得して出力ディレクトリ名を作成
    folder_name = os.path.basename(os.path.normpath(date_folder))
    output_directory = os.path.join(os.getcwd(), f"RGB-{folder_name}")

    # 出力ディレクトリ作成
    make_folder(output_directory)

    width, height, spectral_dim = 2048, 1080, 151

    print(f"Starting to process hyperspectral images in {date_folder}")

    # 日付フォルダ内の場所フォルダを処理
    process_hyperspectral_images_in_location_folders(date_folder, output_directory, width, height, spectral_dim)

    print("Processing complete.")
