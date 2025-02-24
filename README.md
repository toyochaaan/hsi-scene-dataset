# HSI Scene Dataset

## 概要
HSI Scene Dataset リポジトリは、ハイパースペクトル画像 (HSI) の処理と解析を行うためのツール群を提供する。NH9 形式のファイルを解析し、データの抽出、可視化、変換が可能。

## ディレクトリ構成
```
├── extract_id.py        # NH9 ファイルの ID とファイル情報を JSON に保存
├── hs_to_rgbV2.py       # NH9 ファイルから RGB 画像を生成
├── mainCUI.py           # NH9 ファイルを HDF5 形式に圧縮・保存
├── spectralview.py      # NH9 ファイルのスペクトルバンドを可視化
├── tagcount.py          # メタデータ JSON 内のタグを集計・可視化
├── metadata.json        # HSI 画像のメタデータ（オブジェクトタグ・シーンタグを含む）
└── README.md            # 本ドキュメント
```

## 各スクリプトの説明

### extract_id.py
指定したディレクトリ内の NH9 ファイルをスキャンし、以下の情報を JSON に保存。
- ファイル名から抽出した日時情報
- フォルダ階層から取得した「日時フォルダ」「場所フォルダ」

**実行方法:**
```sh
python extract_id.py /path/to/nh9_files output.json
```

---

### hs_to_rgbV2.py
NH9 ファイルを読み込み、特定のバンドを抽出して RGB 画像に変換。
- 赤 (R) バンド: 54~70
- 緑 (G) バンド: 30~40
- 青 (B) バンド: 20~30

**実行方法:**
```sh
python hs_to_rgbV2.py /path/to/nh9_data
```

---

### mainCUI.py
NH9 ファイルを HDF5 形式に圧縮し、フォルダ構成を維持したまま保存。

**実行方法:**
```sh
python mainCUI.py
```
(CUIでフォルダのパスを入力)

---

### spectralview.py
NH9 ファイルを選択し、viewerを起動する。
- 各バンドの画像をスライダーで切り替え可能

**実行方法:**
```sh
python spectralview.py
```
(ファイル選択ダイアログが表示される)

---

### tagcount.py
JSON 内のオブジェクトタグ・シーンタグの出現回数をカウントし、可視化。

**実行方法:**
```sh
python tagcount.py
```

---

## 必要なライブラリ
このリポジトリのスクリプトを実行するには、以下の Python ライブラリが必要。

```sh
pip install numpy opencv-python tqdm h5py matplotlib
```



