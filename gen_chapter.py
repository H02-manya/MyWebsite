# gen_chapter.py
# 手动指定漫画文件夹名和输出文件名
# 自动生成章节 JS 文件

import os, re

# === 输入部分 ===
BASE_DIR = input("请输入漫画文件夹名（位于 images/ 下，例如：請玷汙我女友 1-23話）: ").strip()
OUT_FILE = input("请输入要输出的文件名（例如：chapters_manga1.js）: ").strip()

# === 正则模式 ===
pattern = re.compile(r'(\d+)\s*\(\s*(\d+)\s*\)', re.I)

# === 检查路径 ===
manga_path = os.path.join("images", BASE_DIR)
if not os.path.isdir(manga_path):
    print(f"❌ 找不到漫画文件夹：{manga_path}")
    exit(1)

# === 获取所有图片文件 ===
files = [f for f in os.listdir(manga_path) if os.path.isfile(os.path.join(manga_path, f))]
files = [f for f in files if re.search(r'\.(jpe?g|png|webp|gif)$', f, re.I)]

if not files:
    print(f"⚠️ {BASE_DIR} 文件夹里没有图片。")
    exit(0)

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
        # fallback: 尝试前缀数字
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
    chap_sorted[k] = [f"images/{BASE_DIR}/{fn}" for _, fn in pages]

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
