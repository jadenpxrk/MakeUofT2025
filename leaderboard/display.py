import pandas as pd
import streamlit as st

def style_leaderboard(df):
    def color_row(row):
        medal = row["Medal"]
        if medal == "Gold":
            return ["background-color: gold"] * len(row)
        elif medal == "Silver":
            return ["background-color: silver"] * len(row)
        elif medal == "Bronze":
            return ["background-color: #cd7f32"] * len(row)
        else:
            return ["" for _ in row]
    styled_df = df.style.apply(color_row, axis=1)
    styled_df = styled_df.set_table_styles(
        [{"selector": "table", "props": [("width", "100%")]}]
    )
    st.write(styled_df)
