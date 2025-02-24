import os
import re
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from matplotlib.widgets import Slider

def parse_filename(file_name):
    """
    ファイル名からメタデータを解析する。

    Args:
        file_name (str): 解析対象のNH9ファイル名。

    Returns:
        dict: 解析されたメタデータ（scan, gain, exposure, wavelength, datetime）。
              マッチしない場合は空の辞書を返す。
    """
    pattern = r"Scan-d\(s(?P<scan>.+),g(?P<gain>\d+),(?P<exposure>[\d.]+ms),(?P<wavelength>\d+-\d+)\)_(?P<datetime>\d+_\d+)\.nh9"
    match = re.match(pattern, file_name)
    return match.groupdict() if match else {}

def select_file():
    """
    ファイル選択ダイアログを開く。

    Returns:
        str: 選択されたファイルのパス（選択されなかった場合は空文字列）。
    """
    root = Tk()
    root.withdraw()  # メインウィンドウを非表示にする
    return filedialog.askopenfilename(
        title="NH9ファイルを選択",
        filetypes=[("NH9 Files", "*.nh9"), ("All Files", "*.*")]
    )

def load_hsi_data(file_path, height, width, bands, dtype=np.uint16):
    """
    HSIデータをNH9ファイルから読み込む。

    Args:
        file_path (str): 読み込むNH9ファイルのパス。
        height (int): 画像の高さ（ピクセル）。
        width (int): 画像の幅（ピクセル）。
        bands (int): スペクトルのバンド数。
        dtype (numpy.dtype): 読み込むデータの型（デフォルトは np.uint16）。

    Returns:
        numpy.ndarray: (height, width, bands) の形状を持つ3次元配列のHSIデータ。
    """
    with open(file_path, "rb") as f:
        raw_data = np.fromfile(f, dtype, -1)
    img = np.reshape(raw_data, (height, bands, width))
    return np.transpose(img, (0, 2, 1))  # 転置して正しい順序にする

def interactive_band_viewer(hsi_data, metadata):
    """
    HSIデータをスライダーでバンドを切り替えながら可視化する。

    - 初期状態では最初のバンドを表示。
    - スライダーを動かすと異なるバンドが表示される。

    Args:
        hsi_data (numpy.ndarray): (height, width, bands) の形状を持つ3次元配列のHSIデータ。
        metadata (dict): ファイル名から取得したメタデータ。

    Returns:
        None
    """
    initial_band = 0
    max_band = hsi_data.shape[2] - 1

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.25)

    band_image = hsi_data[:, :, initial_band]
    img = ax.imshow(band_image, cmap="gray")

    title_text = f"Band {initial_band} ({350 + 5 * initial_band} nm)\n" \
                 f"scan: {metadata.get('scan', 'N/A')}, gain: {metadata.get('gain', 'N/A')}, " \
                 f"exposure: {metadata.get('exposure', 'N/A')}, wavelength: {metadata.get('wavelength', 'N/A')}"
    ax.set_title(title_text)
    plt.colorbar(img, ax=ax, label="Intensity")

    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor="lightgoldenrodyellow")
    slider = Slider(ax_slider, "Band", 0, max_band, valinit=initial_band, valstep=1)

    def update(val):
        """
        スライダーの値変更時に呼び出される更新関数。

        Args:
            val (float): スライダーの現在の値。

        Returns:
            None
        """
        band = int(slider.val)
        band_image = hsi_data[:, :, band]
        img.set_data(band_image)
        img.set_clim(vmin=band_image.min(), vmax=band_image.max())

        updated_title = f"Band {band} ({350 + 5 * band} nm)\n" \
                        f"scan: {metadata.get('scan', 'N/A')}, gain: {metadata.get('gain', 'N/A')}, " \
                        f"exposure: {metadata.get('exposure', 'N/A')}, wavelength: {metadata.get('wavelength', 'N/A')}"
        ax.set_title(updated_title)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    """
    メイン処理:
    - NH9ファイルを選択。
    - ファイル名からメタデータを解析。
    - HSIデータを読み込む。
    - インタラクティブビューアでデータを可視化。

    Raises:
        FileNotFoundError: ファイルが存在しない場合にエラーメッセージを表示して終了する。
    """
    file_path = select_file()
    if not file_path or not os.path.exists(file_path):
        print("エラー: ファイルが選択されなかったか、存在しません。")
        exit()

    print(f"選択されたファイル: {file_path}")

    metadata = parse_filename(os.path.basename(file_path))
    print("ファイルのメタデータ:", metadata)

    height, width, bands = 1080, 2048, 151  # カメラの仕様
    dtype = np.uint16  # 12ビットデータ → np.uint16 として扱う

    try:
        hsi_data = load_hsi_data(file_path, height, width, bands, dtype)
        print(f"HSIデータの形状: {hsi_data.shape}")

        interactive_band_viewer(hsi_data, metadata)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
