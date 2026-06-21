#!/usr/bin/env python3
# Inlines quiz/questions.json into a single standalone HTML for offline phone use.
import json, re, sys, pathlib
root = pathlib.Path(__file__).parent
html = (root/"quiz"/"index.html").read_text(encoding="utf-8")
data = json.loads((root/"quiz"/"questions.json").read_text(encoding="utf-8"))
inject = "<script>window.QUESTIONS = " + json.dumps(data, ensure_ascii=False) + ";</script>\n</head>"
out = html.replace("</head>", inject, 1)
for name in ("UPTET-Quiz.html", "index.html"):   # index.html = root file GitHub Pages serves
    (root/name).write_text(out, encoding="utf-8")
print(f"Built UPTET-Quiz.html + index.html  ({len(out)//1024} KB, {len(data['questions'])} questions)")
