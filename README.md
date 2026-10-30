# Chinese Character Reading Quiz

A Streamlit quiz using the vocabulary bundled in `characters.csv`.

## Vocabulary

The dataset was extracted from `hanzi_shifu_4.0.xlsx`, worksheet `Znaki`:
- Excel column A: Chinese character
- Excel column C: pinyin reading

The CSV contains one row per character-reading pair. Where the source lists
multiple readings separated by slashes or parentheses, each reading is treated
as an accepted reading. The quiz randomly chooses one accepted reading for
the character displayed.

## Run in GitHub Codespaces

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Push all three files (`app.py`, `characters.csv`, and `requirements.txt`) to
your GitHub repository. In Streamlit Community Cloud, create an app from that
repository and select `app.py` as the main file.

The vocabulary is bundled with the app, so players do not need to upload an
Excel file.
