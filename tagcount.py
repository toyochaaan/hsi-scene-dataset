import json
import matplotlib.pyplot as plt
from collections import Counter

def count_tags_and_plot(file_path):
    # JSONファイルを読み込み
    with open(file_path, 'r') as f:
        data = json.load(f)

    object_tags_counter = Counter()
    scene_tags_counter = Counter()

    # 無視するタグをここに
    ignored_scene_tags = {
        "indoor", "outdoor natural", "outdoor man-made", "shopping and dining", "workplace",
        "home or hotel", "transportation", "water", "ice", "snow", "forest,field,jungle",
        "sports field,parks,leisure spaces", "cultural or historical", "commercial buildings,shops,markets,cities,and towns","shopping and dining,great hall",
        "indoor, shopping and dining, great hall","houses,cabins,gardens,and farms","water,ice,snow","False"
    }
    ignored_object_tags = {
        "False"
    }

    # タグをカウント
    for item in data:
        object_tags = item.get("object_tags", [])
        scene_tags = item.get("scene_tags", [])

        object_tags_counter.update(tag for tag in object_tags if tag not in ignored_object_tags)
        scene_tags_counter.update(tag for tag in scene_tags if tag not in ignored_scene_tags)

    # 降順でソート
    sorted_object_tags = sorted(object_tags_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_scene_tags = sorted(scene_tags_counter.items(), key=lambda x: x[1], reverse=True)

    # オブジェクトタグをプロット
    if sorted_object_tags:
        plt.figure(figsize=(6, len(sorted_object_tags) * 1.5))  
        object_tags, object_counts = zip(*sorted_object_tags)
        plt.barh(object_tags, object_counts, color='blue', height=0.5)
        plt.title("Object Tags Count", fontsize=30, weight='bold')
        plt.xlabel("Count", fontsize=26, weight='bold')
        plt.ylabel("Tags", fontsize=26, weight='bold')
        plt.yticks(fontsize=18, weight='bold')
        plt.xticks(fontsize=20, weight='bold')
        plt.gca().invert_yaxis()  
        plt.xlim(0, max(object_counts) * 1.1) 
        plt.xticks(range(0, int(max(object_counts) * 1.1) + 1, 1000), fontsize=20, weight='bold')  
        plt.subplots_adjust(left=0.45)  
        plt.tight_layout()
        plt.show()

    # シーンタグをプロット
    if sorted_scene_tags:
        plt.figure(figsize=(6, len(sorted_scene_tags) * 1.5))  
        scene_tags, scene_counts = zip(*sorted_scene_tags)
        plt.barh(scene_tags, scene_counts, color='green', height=0.5)
        plt.title("Scene Tags Count", fontsize=30, weight='bold')
        plt.xlabel("Count", fontsize=26, weight='bold')
        plt.ylabel("Tags", fontsize=26, weight='bold')
        plt.yticks(fontsize=18, weight='bold')
        plt.xticks(fontsize=20, weight='bold')
        plt.gca().invert_yaxis()  
        plt.xlim(0, max(scene_counts) * 1.1)  
        plt.xticks(range(0, int(max(scene_counts) * 1.1) + 1, 150), fontsize=20, weight='bold')  
        plt.subplots_adjust(left=0.45)  
        plt.tight_layout()
        plt.show()

file_path = "metadata.json"  # パスによってここを変更
count_tags_and_plot(file_path)
