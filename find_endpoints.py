import re
from pathlib import Path

print("开始扫描 tests 目录...")
pattern = re.compile(r"['\"](/[a-zA-Z0-9_/]+)['\"]")
endpoints = set()

for py_file in Path("tests").rglob("*.py"):
    print(f"扫描文件：{py_file}")
    text = py_file.read_text(encoding="utf-8", errors="ignore")
    for match in pattern.findall(text):
        print(f"发现路径：{match}")
        endpoints.add(match)

print("扫描完成，结果如下：")
for ep in sorted(endpoints):
    print(ep)
