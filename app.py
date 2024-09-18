import streamlit as st
import pandas as pd
import ast
import update_database

# Get arbitrage opportunites
arbs = update_database.get_arbitrage_list()
avg_return = update_database.get_historical_average()

# Create a DataFrame from the sample data
columns = ["Sport/League", "Underdog", "Favorite", "Spread", "Line 1", "Bookmaker 1", "Line 2", "Bookmaker 2", "Return"]
data = [
    {
        "Sport/League": opp[1],
        "Underdog": opp[4],
        "Favorite": opp[7],
        "Spread": f"{opp[3]:g}",  # Format as general number
        "Line 1": f"{opp[5]:g}",  # Format as general number
        "Bookmaker 1": opp[6],
        "Line 2": f"{opp[8]:g}",  # Format as general number
        "Bookmaker 2": opp[9],
        "Return": f"{opp[10] * 100:.2f}%"  # Convert return to percentage
    }
    for opp in arbs
]

df = pd.DataFrame(data, columns=columns)

# Streamlit app
st.set_page_config(layout="wide")  # Set the page layout to wide
st.title("Arbitrage Opportunities")
st.subheader(f"Lifetime Average Return: {round(avg_return, 2)}%")

# Display the DataFrame as a table
st.table(df)

# Smaller footer text
footer = """
<div style="text-align: center;">
    <p style="font-size:15px; margin-top: 20px;">Arbitrage Opportunities Updated Daily at ~8 - 8:30pm EST</p>
</div>
"""

# Display the footer
st.markdown(footer, unsafe_allow_html=True)