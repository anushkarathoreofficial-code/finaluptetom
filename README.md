# UPTET Quiz 📚

A phone-friendly quiz built from the UPTET Primary (Class I–V) previous-year solved papers.

## 📱 Use it on your phone (the main thing)

Open **`UPTET-Quiz.html`** — it is a single self-contained file with all **709 questions** embedded. No internet, no server needed.

To get it onto your phone:
- **iPhone:** AirDrop `UPTET-Quiz.html` from your Mac → tap to open in Safari/Chrome.
- **Any phone:** email it to yourself / put it in Google Drive / WhatsApp it to yourself → open the file → it opens in the browser.
- Tip: in the browser menu choose **"Add to Home Screen"** to get an app-like icon.

### What it does
- Tap an option → instantly shows ✅ correct / ❌ wrong.
- **Every** question shows a **📖 सारांश (summary)** and a **🧠 Hinglish memory trick** after you answer — right or wrong.
- Wrong answers collect in the **🔁 गलत (Wrong)** tab. Re-attempt them anytime; once you get one right it **automatically leaves** the wrong list.
- **⭐ याद** tab = questions you've gotten right. **📊 आँकड़े** = your stats.
- Filter by **year (2017 / 2018 / 2019 / 2021)** and by **subject** (CDP, Hindi, English/Sanskrit, Math, EVS), or 🔀 shuffle.
- Your progress is saved on your phone (browser localStorage) and survives closing the app.

## 🗂️ How the questions are stored (the "efficient way")

Questions are **not** hardcoded in the app's logic. They live as **data**:

```
quiz/index.html       ← the quiz "engine" (generic logic only)
quiz/questions.json   ← all 709 questions as data (the editable source of truth)
UPTET-Quiz.html       ← built artifact: engine + data inlined into one file (for the phone)
```

The engine just loads the JSON. To add/edit questions, edit `quiz/questions.json` and rebuild.

## 🔧 Rebuild / extend

```bash
python3 merge.py     # rebuild quiz/questions.json from extract/*.json
python3 build.py     # inline it into the standalone UPTET-Quiz.html
```

- `extract/*.json` — raw per-chunk transcriptions (one file per ~8 page-columns).
- `pages_col/` — the rendered column images the questions were OCR'd from (kept so more papers can be added later).
- Papers currently included: **UPTET 2017, 2018, 2019, 2021**. (2011/2013/2014/2016 papers are also in the source PDFs and can be added the same way.)

## ⚠️ Note on accuracy
Questions were transcribed from the scanned papers by OCR. Answers come from the printed `Ans :` key in the source, so they're reliable, but a stray typo in Hindi text is possible across 709 questions — trust the printed paper if anything looks off, and feel free to fix `questions.json`.
