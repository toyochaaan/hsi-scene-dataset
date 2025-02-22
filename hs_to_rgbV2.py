import os
import glob
import sys
import cv2
import numpy as np
from tqdm import tqdm

def make_folder(folder_name):
    """
    指定したフォルダが存在しない場合、新規作成する。

    Args:
        folder_name (str): 作成するフォルダのパス。

    Returns:
        None
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def hyprawread(file_path, width, height, spectral_dim):
    """
    ハイパースペクトルデータをバイナリファイルから読み込み、3次元配列として返す。

    Args:
        file_path (str): 読み込むファイルのパス。
        width (int): 画像の幅 (ピクセル単位)。
        height (int): 画像の高さ (ピクセル単位)。
        spectral_dim (int): スペクトルの次元数 (バンド数)。

    Returns:
        numpy.ndarray: (height, width, spectral_dim) の形状を持つ画像データ。
    """
    with open(file_path, 'rb') as file:
        img_data = np.fromfile(file, np.uint16)
    img_data = np.reshape(img_data, (height, spectral_dim, width))
    img_data = np.transpose(img_data, (0, 2, 1))  # 転置して正しい順序に戻す
    return img_data

def extract_rgb(img_data):
    """
    ハイパースペクトルデータからRGB画像を生成する。

    - 赤 (R) バンド: 54~70番のバンドの平均値
    - 緑 (G) バンド: 30~40番のバンドの平均値
    - 青 (B) バンド: 20~30番のバンドの平均値
    - 各バンドは 0-255 の範囲に正規化される。

    Args:
        img_data (numpy.ndarray): (height, width, spectral_dim) の形状を持つ画像データ。

    Returns:
        numpy.ndarray: OpenCV形式のBGR画像 (uint8)。
    """
    red_band = np.mean(img_data[:, :, 54:70], axis=2)
    green_band = np.mean(img_data[:, :, 30:40], axis=2)
    blue_band = np.mean(img_data[:, :, 20:30], axis=2)

    red_band = 255 * red_band / np.max(red_band)
    green_band = 255 * green_band / np.max(green_band)
    blue_band = 255 * blue_band / np.max(blue_band)

    rgb_image = np.dstack((red_band, green_band, blue_band)).astype(np.uint8)
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    return rgb_image

def process_hyperspectral_images(input_dir, output_dir, width, height, spectral_dim):
    """
    指定したディレクトリ内の .nh9 ファイルを処理し、RGB画像として保存する。

    - 入力フォルダ内の全 .nh9 ファイルをスキャン。
    - 各ファイルを RGB に変換し、指定した出力フォルダに保存。

    Args:
        input_dir (str): .nh9 ファイルを含むフォルダのパス。
        output_dir (str): 変換後の画像を保存するフォルダのパス。
        width (int): 画像の幅。
        height (int): 画像の高さ。
        spectral_dim (int): スペクトルの次元数。

    Returns:
        None
    """
    files = glob.glob(os.path.join(input_dir, "*.nh9"))
    
    if not files:
        print(f"No .nh9 files found in {input_dir}")
        return

    print(f"Found {len(files)} .nh9 files in {input_dir}")

    for file_path in tqdm(files, desc=f"Processing files in {input_dir}"):
        img_data = hyprawread(file_path, width, height, spectral_dim)
        rgb_image = extract_rgb(img_data)

        base_name = os.path.basename(file_path)
        output_name = f"rgb-{os.path.splitext(base_name)[0]}.jpg"
        output_path = os.path.join(output_dir, output_name)

        make_folder(output_dir)
        cv2.imwrite(output_path, rgb_image)
        print(f"Image saved: {output_path}")

def process_hyperspectral_images_in_location_folders(date_folder, output_dir, width, height, spectral_dim):
    """
    日付フォルダ内の各場所フォルダを探索し、ハイパースペクトル画像を処理する。

    - 各場所フォルダを処理し、RGB画像を「RGB-日付フォルダ/場所フォルダ」に保存。

    Args:
        date_folder (str): 日付フォルダのパス。
        output_dir (str): 変換後の画像を保存するフォルダの親ディレクトリ。
        width (int): 画像の幅。
        height (int): 画像の高さ。
        spectral_dim (int): スペクトルの次元数。

    Returns:
        None
    """
    location_folders = [os.path.join(date_folder, d) for d in os.listdir(date_folder) if os.path.isdir(os.path.join(date_folder, d))]

    for location_folder in location_folders:
        print(f"Processing location folder: {location_folder}")

        location_subdir = os.path.basename(location_folder)
        output_location_dir = os.path.join(output_dir, location_subdir)

        process_hyperspectral_images(location_folder, output_location_dir, width, height, spectral_dim)

if __name__ == "__main__":
    """
    コマンドライン引数から日付フォルダのパスを取得し、RGB画像を生成する。

    - コマンドライン引数が指定されていない場合はエラーメッセージを出して終了。
    - 「RGB-日付フォルダ」の出力ディレクトリを作成。
    - 指定された日付フォルダ内の場所フォルダごとに処理を実行。
    """
    if len(sys.argv) > 1:
        date_folder = sys.argv[1]
    else:
        print("Please provide the date folder path.")
        sys.exit()

    folder_name = os.path.basename(os.path.normpath(date_folder))
    output_directory = os.path.join(os.getcwd(), f"RGB-{folder_name}")

    make_folder(output_directory)

    width, height, spectral_dim = 2048, 1080, 151

    print(f"Starting to process hyperspectral images in {date_folder}")
    process_hyperspectral_images_in_location_folders(date_folder, output_directory, width, height, spectral_dim)
    print("Processing complete.")
