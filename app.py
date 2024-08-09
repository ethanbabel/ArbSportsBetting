import streamlit as st
import pandas as pd
import ast
import update_database

# Get arbitrage opportunites
arbs = update_database.get_arbitrage_list()
avg_return = update_database.get_historical_average()

# Create a DataFrame from the sample data
columns = ["Sport/League", "Spread", "Line 1", "Bookmaker 1", "Line 2", "Bookmaker 2", "Return"]
data = [
    {
        "Sport/League": opp[1],
        "Spread": f"{opp[3]:g}",  # Format as general number
        "Line 1": f"{opp[4]:g}",  # Format as general number
        "Bookmaker 1": opp[5],
        "Line 2": f"{opp[6]:g}",  # Format as general number
        "Bookmaker 2": opp[7],
        "Return": f"{opp[8] * 100:.2f}%"  # Convert return to percentage
    }
    for opp in arbs
]

df = pd.DataFrame(data, columns=columns)

# Streamlit app
st.title("Arbitrage Opportunities")
st.subheader(f"Lifetime Average Return: {round(avg_return, 2)}%")

# Display the DataFrame as a table
st.table(df)

# Smaller footer text
footer = """
<div style="text-align: center;">
    <p style="font-size:15px; margin-top: 20px;">Arbitrage Opportunities Updated Daily</p>
</div>
"""

# Display the footer
st.markdown(footer, unsafe_allow_html=True)