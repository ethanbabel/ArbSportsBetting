import streamlit as st
import pandas as pd
import ast
import update_database

# Get arbitrage opportunites
arbs = update_database.get_arbitrage_list()

# Create a DataFrame from the sample data
columns = ["Sport/League", "Spread", "Line 1", "Bookmaker 1", "Line 2", "Bookmaker 2", "Return"]
data = [
    {
        "Sport/League": opp[1],
        "Spread": opp[3],
        "Line 1": opp[4],
        "Bookmaker 1": opp[5],
        "Line 2": opp[6],
        "Bookmaker 2": opp[7],
        "Return": f"{opp[8] * 100:.2f}%"  # Convert return to percentage
    }
    for opp in arbs
]

df = pd.DataFrame(data, columns=columns)

# Streamlit app
st.title("Arbitrage Opportunities")

# Display the DataFrame as a table
st.table(df)

# Footer
st.markdown("## Arbitrage Opportunities Updated Daily")