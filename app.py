"""
CommentWorks Local Wrapper

A tiny, fully local Streamlit app for analyzing open-ended comments.
It keeps the workflow boring on purpose:

1. Upload a CSV
2. Pick the comment column
3. Detect candidate themes from a sample
4. Review/edit the theme list
5. Tag every comment
6. Export a CSV

Run locally:
    streamlit run app.py

Notes:
- Comment text is processed on this machine.
- The model may download from HuggingFace the first time it is used, then runs from the local cache.
- Do not deploy this as a shared web app unless you have reviewed privacy, auth, and data retention.
"""

from __future__ import annotations

import os
from io import StringIO
from typing import Iterable, List

# Keep Streamlit's own telemetry off for this app when possible.
os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

import pandas as pd
import streamlit as st

import commentworks as cw


APP_TITLE = "CommentWorks Local"
DEFAULT_SAMPLE_SIZE = 75
DEFAULT_MAX_ROWS_PREVIEW = 25


@st.cache_resource(show_spinner="Loading local model…")
def load_model() -> cw.commentworks:
    """Load the local CommentWorks model once per Streamlit session."""
    return cw.commentworks(device="cpu")


def normalize_themes(raw_themes: Iterable[str]) -> List[str]:
    """Clean model/user-provided theme strings while preserving order."""
    seen = set()
    clean: List[str] = []
    for theme in raw_themes:
        value = str(theme).strip().lower()
        if not value:
            continue
        if value not in seen:
            seen.add(value)
            clean.append(value)
    return clean


def parse_theme_text(theme_text: str) -> List[str]:
    """Parse newline- or comma-separated themes from a text area."""
    chunks: List[str] = []
    for line in theme_text.splitlines():
        chunks.extend(part.strip() for part in line.split(","))
    return normalize_themes(chunks)


def to_csv_download(df: pd.DataFrame) -> bytes:
    """Return UTF-8 CSV bytes for Streamlit download."""
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="💬", layout="wide")

    st.title(APP_TITLE)
    st.caption(
        "A boring tiny tool for private, on-device comment analysis. "
        "Upload a CSV, generate candidate themes, tag comments, and export results."
    )

    with st.expander("Local/privacy notes", expanded=False):
        st.markdown(
            """
            - Comment text is sent only to the model running in this Python process.
            - The default model may download once from HuggingFace, then runs from the local cache.
            - This app does not require a database, account, server, API key, or cloud LLM.
            - Treat outputs as suggested tags, not ground truth. Review themes before using them in reporting.
            """
        )

    uploaded_file = st.file_uploader("Upload a CSV of comments", type=["csv"])
    if uploaded_file is None:
        st.info("Start by uploading a CSV with one row per comment.")
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:  # pragma: no cover - UI guardrail
        st.error(f"Could not read CSV: {exc}")
        return

    if df.empty:
        st.warning("The uploaded CSV has no rows.")
        return

    st.subheader("1. Choose the comment column")
    text_columns = [col for col in df.columns if df[col].dtype == "object"] or list(df.columns)
    comment_col = st.selectbox("Comment column", text_columns)

    working = df.copy()
    working[comment_col] = working[comment_col].fillna("").astype(str).str.strip()
    nonempty = working[working[comment_col] != ""].copy()

    st.write(f"Loaded **{len(df):,} rows** with **{len(nonempty):,} non-empty comments**.")
    st.dataframe(nonempty.head(DEFAULT_MAX_ROWS_PREVIEW), use_container_width=True)

    if nonempty.empty:
        st.warning("No non-empty comments found in the selected column.")
        return

    st.subheader("2. Detect candidate themes from a sample")
    sample_size = st.slider(
        "Sample size for theme detection",
        min_value=5,
        max_value=min(500, len(nonempty)),
        value=min(DEFAULT_SAMPLE_SIZE, len(nonempty)),
        step=5,
        help="Use a sample to keep theme discovery fast. You can edit the resulting themes before tagging all rows.",
    )

    sample_method = st.radio(
        "Sample method",
        ["First rows", "Random sample"],
        horizontal=True,
        help="Random sampling is usually better when comments are not already shuffled.",
    )

    if "candidate_themes" not in st.session_state:
        st.session_state.candidate_themes = []

    if st.button("Detect themes", type="primary"):
        sample = (
            nonempty.sample(n=sample_size, random_state=42)
            if sample_method == "Random sample"
            else nonempty.head(sample_size)
        )
        comments = sample[comment_col].tolist()

        model = load_model()
        with st.spinner("Detecting candidate themes locally…"):
            detected = model.detect_themes(comments)
        st.session_state.candidate_themes = normalize_themes(detected)

    st.subheader("3. Review/edit themes")
    current_themes = st.session_state.candidate_themes
    theme_text = st.text_area(
        "Themes to assign",
        value="\n".join(current_themes),
        height=220,
        help="One theme per line is easiest. You can also paste comma-separated themes.",
    )
    final_themes = parse_theme_text(theme_text)

    if final_themes:
        st.write(f"Ready to assign **{len(final_themes)} themes**.")
    else:
        st.warning("Add at least one theme before tagging comments.")

    st.subheader("4. Tag comments and export")
    output_col = st.text_input("Output column name", value="commentworks_themes")

    tag_all = st.button("Tag all non-empty comments", disabled=not final_themes)
    if tag_all:
        model = load_model()
        tagged = []
        progress = st.progress(0)
        status = st.empty()

        comments = nonempty[comment_col].tolist()
        total = len(comments)
        for idx, comment in enumerate(comments, start=1):
            assigned = model.assign_themes(comment, possible_themes=final_themes)
            tagged.append("; ".join(normalize_themes(assigned)))
            if idx == 1 or idx % 10 == 0 or idx == total:
                progress.progress(idx / total)
                status.write(f"Tagged {idx:,} of {total:,} comments locally…")

        result = working.copy()
        result[output_col] = ""
        result.loc[nonempty.index, output_col] = tagged
        st.session_state.result_df = result
        status.write("Done.")

    if "result_df" in st.session_state:
        result_df = st.session_state.result_df
        st.dataframe(result_df.head(DEFAULT_MAX_ROWS_PREVIEW), use_container_width=True)
        st.download_button(
            "Download tagged CSV",
            data=to_csv_download(result_df),
            file_name="commentworks_tagged_comments.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
