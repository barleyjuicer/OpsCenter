from typing import Any

import pandas as pd
import streamlit as st


def apply_style() -> None:
    st.markdown(
        """
        <style>
            :root {
                --ops-border: #d8dee8;
                --ops-panel: #ffffff;
                --ops-muted: #64748b;
                --ops-ink: #172033;
                --ops-accent: #2563eb;
                --ops-good: #047857;
                --ops-warn: #b45309;
                --ops-bad: #b91c1c;
            }
            .main .block-container {
                max-width: 1180px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            h1, h2, h3 {
                color: var(--ops-ink);
                letter-spacing: 0;
            }
            [data-testid="stSidebar"] {
                background: #f8fafc;
                border-right: 1px solid var(--ops-border);
            }
            .metric-card {
                background: var(--ops-panel);
                border: 1px solid var(--ops-border);
                border-radius: 8px;
                padding: 18px 18px 16px;
                min-height: 112px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
            }
            .metric-label {
                color: var(--ops-muted);
                font-size: 0.84rem;
                font-weight: 650;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }
            .metric-value {
                color: var(--ops-ink);
                font-size: 2rem;
                line-height: 1.15;
                font-weight: 760;
                margin-top: 10px;
            }
            .metric-note {
                color: var(--ops-muted);
                font-size: 0.9rem;
                margin-top: 6px;
            }
            .section-title {
                margin-top: 1.5rem;
                margin-bottom: 0.4rem;
                font-weight: 760;
                color: var(--ops-ink);
            }
            div[data-testid="stForm"] {
                border: 1px solid var(--ops-border);
                border-radius: 8px;
                padding: 1rem;
                background: #ffffff;
            }
            .stButton > button {
                border-radius: 7px;
                font-weight: 650;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, caption: str) -> None:
    st.title(title)
    st.caption(caption)


def metric_card(label: str, value: int, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_table(rows: list[dict[str, Any]], empty_message: str) -> None:
    if not rows:
        st.info(empty_message)
        return
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
