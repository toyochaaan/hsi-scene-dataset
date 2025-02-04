import os
import re
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from matplotlib.widgets import Slider

# ファイル名解析用関数
def parse_filename(file_name):
    """
    ファイル名からメタデータを解析。
    """
    pattern = r"Scan-d\(s(?P<scan>.+),g(?P<gain>\d+),(?P<exposure>[\d.]+ms),(?P<wavelength>\d+-\d+)\)_(?P<datetime>\d+_\d+)\.nh9"
    match = re.match(pattern, file_name)
    if match:
        return match.groupdict()
    return {}

# ファイル選択ダイアログ
def select_file():
    """
    ファイル選択ダイアログを開く。
    """
    root = Tk()
    root.withdraw()  # メインウィンドウを非表示に
    file_path = filedialog.askopenfilename(
        title="NH9ファイルを選択",
        filetypes=[("NH9 Files", "*.nh9"), ("All Files", "*.*")]
    )
    return file_path

# HSIデータ読み込み関数
def load_hsi_data(file_path, height, width, bands, dtype=np.uint16):
    """
    HSIデータを読み込む。
    """
    with open(file_path, "rb") as f:
        raw_data = np.fromfile(f, np.uint16, -1)
    img = np.reshape(raw_data, (height, bands, width))
    img = np.transpose(img, (0, 2, 1))
    return img

# ビューア関数
def interactive_band_viewer(hsi_data, metadata):
    """
    スライダーでバンドを切り替えながら画像を表示する。
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
        band = int(slider.val)
        band_image = hsi_data[:, :, band]
        img.set_data(band_image)
        img.set_clim(vmin=band_image.min(), vmax=band_image.max())
        title_text = f"Band {band} ({350 + 5 * band} nm)\n" \
                     f"scan: {metadata.get('scan', 'N/A')}, gain: {metadata.get('gain', 'N/A')}, " \
                     f"exposure: {metadata.get('exposure', 'N/A')}, wavelength: {metadata.get('wavelength', 'N/A')}"
        ax.set_title(title_text)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

# メイン処理
if __name__ == "__main__":
    # ファイルを選択
    file_path = select_file()
    if not file_path or not os.path.exists(file_path):
        print("ファイルが選択されなかったか存在しません。")
        exit()

    print(f"選択されたファイル: {file_path}")

    # ファイル名からメタデータを解析
    metadata = parse_filename(os.path.basename(file_path))
    print("ファイルのメタデータ:", metadata)

    # データの解像度とバンド数
    height, width, bands = 1080, 2048, 151  # カメラの仕様
    dtype = np.uint16  # 12ビットデータ → np.uint16として扱う

    try:
        # HSIデータを読み込む
        hsi_data = load_hsi_data(file_path, height, width, bands, dtype)
        print(f"HSIデータの形状: {hsi_data.shape}")

        # インタラクティブビューアを起動
        interactive_band_viewer(hsi_data, metadata)
    except Exception as e:
        print(f"エラーが発生しました: {e}")