import json
import matplotlib.pyplot as plt
from collections import Counter

def count_tags_and_plot(file_path):
    """
    JSONファイルからオブジェクトタグとシーンタグの出現回数をカウントし、可視化する。

    - JSONファイル内の `object_tags` と `scene_tags` を集計。
    - 事前に指定した無視するタグを除外。
    - カウント結果を降順にソートし、棒グラフとしてプロット。

    Args:
        file_path (str): 処理するJSONファイルのパス。

    Returns:
        None
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    object_tags_counter = Counter()
    scene_tags_counter = Counter()

    ignored_scene_tags = {
        "indoor", "outdoor natural", "outdoor man-made", "shopping and dining", "workplace",
        "home or hotel", "transportation", "water", "ice", "snow", "forest,field,jungle",
        "sports field,parks,leisure spaces", "cultural or historical", "commercial buildings,shops,markets,cities,and towns",
        "shopping and dining,great hall", "indoor, shopping and dining, great hall",
        "houses,cabins,gardens,and farms", "water,ice,snow", "False"
    }
    ignored_object_tags = {"False"}

    for item in data:
        object_tags = item.get("object_tags", [])
        scene_tags = item.get("scene_tags", [])

        object_tags_counter.update(tag for tag in object_tags if tag not in ignored_object_tags)
        scene_tags_counter.update(tag for tag in scene_tags if tag not in ignored_scene_tags)

    sorted_object_tags = sorted(object_tags_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_scene_tags = sorted(scene_tags_counter.items(), key=lambda x: x[1], reverse=True)

    if sorted_object_tags:
        plot_bar_chart(sorted_object_tags, "Object Tags Count", "blue", step=1000)

    if sorted_scene_tags:
        plot_bar_chart(sorted_scene_tags, "Scene Tags Count", "green", step=150)

def plot_bar_chart(sorted_tags, title, color, step=500):
    """
    タグのカウント結果を横向きの棒グラフとして描画する。

    Args:
        sorted_tags (list of tuple): [(タグ名, 出現回数)] のリスト（降順）。
        title (str): グラフのタイトル。
        color (str): 棒グラフの色（"blue" or "green"）。
        step (int, optional): X軸の目盛り間隔。デフォルトは500。

    Returns:
        None
    """
    plt.figure(figsize=(6, len(sorted_tags) * 1.5))  
    tags, counts = zip(*sorted_tags)
    plt.barh(tags, counts, color=color, height=0.5)
    
    plt.title(title, fontsize=30, weight='bold')
    plt.xlabel("Count", fontsize=26, weight='bold')
    plt.ylabel("Tags", fontsize=26, weight='bold')
    plt.yticks(fontsize=18, weight='bold')
    plt.xticks(fontsize=20, weight='bold')

    plt.gca().invert_yaxis()  
    plt.xlim(0, max(counts) * 1.1)  
    plt.xticks(range(0, int(max(counts) * 1.1) + 1, step), fontsize=20, weight='bold')  

    plt.subplots_adjust(left=0.45)  
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    """
    メイン処理:
    - JSONファイル `metadata.json` を解析し、オブジェクトタグとシーンタグを集計。
    - 集計結果をグラフとして描画。

    Raises:
        FileNotFoundError: 指定したJSONファイルが存在しない場合にエラーメッセージを表示して終了する。
    """
    file_path = "metadata.json"
    count_tags_and_plot(file_path)
