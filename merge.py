#!/usr/bin/env python3
"""Merge per-chunk extraction JSON into quiz/questions.json.
- Canonicalises messy subject labels into 6 buckets (infers blanks from the
  fixed UPTET primary paper structure by question number).
- De-dupes by normalised question text within a paper (numbering is unreliable
  because language sections reuse numbers and OCR mis-reads small digits).
"""
import json, glob, os, re, collections

# which papers to include and their exam-year label
PAPERS = {"p09":"2019", "p07":"2018", "p06":"2017", "p08":"2021"}
ORDER  = ["p08","p09","p07","p06"]   # 2021, 2019, 2018, 2017

def canon_subject(s, q):
    s = (s or "")
    low = s.lower()
    if "बाल विकास" in s or "child" in low or "pedagog" in low:      return "बाल विकास एवं शिक्षाशास्त्र (CDP)"
    if "संस्कृत" in s or "sanskrit" in low:                          return "संस्कृत (भाषा-II)"
    if "अंग्रेज" in s or "english" in low:                           return "अंग्रेज़ी (भाषा-II)"
    if "गणित" in s or "math" in low:                                 return "गणित (Math)"
    if "पर्यावरण" in s or "environ" in low or "evs" in low:          return "पर्यावरण अध्ययन (EVS)"
    if "हिन्दी" in s or "hindi" in low or "भाषा-i" in low or "भाषा-1" in low: return "हिन्दी (भाषा-I)"
    # blank/unknown -> infer from question number bucket
    if isinstance(q, int):
        if   1  <= q <= 30:  return "बाल विकास एवं शिक्षाशास्त्र (CDP)"
        elif 31 <= q <= 60:  return "हिन्दी (भाषा-I)"
        elif 61 <= q <= 90:  return "भाषा-II (अंग्रेज़ी/संस्कृत)"
        elif 91 <= q <= 120: return "गणित (Math)"
        elif 121<= q <= 160: return "पर्यावरण अध्ययन (EVS)"
    return "सामान्य"

def clean_opt(o):
    # drop a leading option marker like "(a)", "a)", "a.", "(अ)" — the UI adds its own A/B/C/D
    return re.sub(r"^\s*\(?\s*[a-dA-Dअआइई१२३४]\s*[\)\.।]\s*", "", str(o)).strip()

def norm(t):
    return re.sub(r"\s+", "", re.sub(r"[।.,?:;()\-–'\"]", "", (t or ""))).lower()

out, errors = [], []
counts = collections.Counter()
for pre in ORDER:
    seen = set()
    for f in sorted(glob.glob(f"extract/{pre}_*.json")):
        try:
            arr = json.load(open(f))
        except Exception as e:
            errors.append(f"{f}: {e}"); continue
        for o in arr:
            qtext = (o.get("question") or "").strip()
            opts  = o.get("options") or []
            ans   = o.get("answer")
            if len(qtext) < 5 or len(opts) < 2: continue
            if not isinstance(ans, int) or not (0 <= ans < len(opts)): continue
            key = norm(qtext)
            if key in seen: continue
            seen.add(key)
            out.append({
                "id":      f"{pre}-{len(out):04d}",
                "year":    PAPERS[pre],
                "src":     "UPTET " + PAPERS[pre],
                "subject": canon_subject(o.get("subject"), o.get("q")),
                "question": qtext,
                "options": [clean_opt(x) for x in opts],
                "answer":  ans,
                "summary": (o.get("summary") or "").strip(),
                "mnemonic":(o.get("mnemonic") or "").strip(),
            })
        counts[pre] += 1

os.makedirs("quiz", exist_ok=True)
json.dump({"meta":{"title":"UPTET Primary (I-V) — Previous Year Questions",
                   "years": sorted({PAPERS[p] for p in ORDER}, reverse=True)},
           "questions": out},
          open("quiz/questions.json","w"), ensure_ascii=False, indent=1)

print("TOTAL:", len(out))
print("\nby year:")
for y in sorted({PAPERS[p] for p in ORDER}, reverse=True):
    print(f"  {sum(1 for q in out if q['year']==y):4d}  {y}")
print("\nby subject:")
for k,v in collections.Counter(q["subject"] for q in out).most_common():
    print(f"  {v:4d}  {k}")
if errors: print("\nERRORS:", *errors, sep="\n  ")
