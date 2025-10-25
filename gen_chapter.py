# gen_chapter.py
# 自动生成漫画章节 JS 文件（支持批量配置）

import os, re

# === 配置漫画列表 ===
# type: 'jp' 或 'kr'
# folder: images/kr_manga/ 或 images/jp_manga/ 下的漫画文件夹名
# out: 输出 JS 文件名
MANGAS = [
    {"type": "kr", "folder": "請玷汙我女友", "out": "chapters_kr_manga_01.js"},
    {"type": "kr", "folder": "男人配額制", "out": "chapters_kr_manga_02.js"},
    # {"type": "jp", "folder": "某日本漫画", "out": "chapters_jp_manga_01.js"},
]

# === 正则模式 ===
pattern = re.compile(r'(\d+)\s*\(\s*(\d+)\s*\)', re.I)

for manga in MANGAS:
    manga_type = manga["type"]
    BASE_DIR = manga["folder"]
    OUT_FILE = manga["out"]

    manga_path = os.path.join("images", f"{manga_type}_manga", BASE_DIR)
    if not os.path.isdir(manga_path):
        print(f"❌ 找不到漫画文件夹：{manga_path}")
        continue

    files = [f for f in os.listdir(manga_path) if os.path.isfile(os.path.join(manga_path, f))]
    files = [f for f in files if re.search(r'\.(jpe?g|png|webp|gif)$', f, re.I)]

    if not files:
        print(f"⚠️ {BASE_DIR} 文件夹里没有图片。")
        continue

    # === 处理章节 ===
    chap = {}
    others = []

    for f in sorted(files, key=lambda x: x.lower()):
        m = pattern.search(f)
        if m:
            ch = m.group(1).zfill(2)
            pg = int(m.group(2))
            chap.setdefault(ch, []).append((pg, f))
        else:
            m2 = re.match(r'^(\d+)', f)
            if m2:
                ch = m2.group(1).zfill(2)
                chap.setdefault(ch, []).append((None, f))
            else:
                others.append(f)

    # === 排序章节页 ===
    chap_sorted = {}
    for k in sorted(chap.keys(), key=lambda x: int(x)):
        pages = sorted(chap[k], key=lambda t: (t[0] if t[0] is not None else 9999, t[1]))
        chap_sorted[k] = [f"images/{manga_type}_manga/{BASE_DIR}/{fn}" for _, fn in pages]

    # === 写入 JS ===
    js_lines = []
    js_lines.append(f"// Auto-generated for {BASE_DIR}")
    js_lines.append("const CHAPTERS = {")
    for k in chap_sorted:
        title = f"第{k}话"
        pages_array = ", ".join([f'\"{p}\"' for p in chap_sorted[k]])
        js_lines.append(f'  \"{k}\": {{ title: \"{title}\", pages: [{pages_array}] }},')
    js_lines.append("};\n")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(js_lines))

    print(f"✅ 已生成 {OUT_FILE}（漫画名：{BASE_DIR}，共 {len(chap_sorted)} 章节）")
