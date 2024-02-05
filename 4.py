import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Plots!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Credit Union Plots")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Database connection parameters
dbname = "postgres"
user = "postgres"
password = "Aiva@2024"
host = "192.168.1.10"
port = "5432"  # default is 5432

# Connect to your postgres DB
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Open a cursor to perform database operations
cur = conn.cursor()
curr1 = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM database10year")
curr1.execute("SELECT * FROM branch")
# Retrieve query results
records = cur.fetchall()
records1 = curr1.fetchall()
# Convert to DataFrame
df = pd.DataFrame(records, columns=[desc[0] for desc in cur.description])
df2 = pd.DataFrame(records1,columns=[desc[0] for desc in curr1.description])
# Close the cursor and connection
cur.close()
curr1.close()
conn.close()

# Use Streamlit to display the dataframe
st.write(df)
st.write(df2)


df_combined = pd.merge(df, df2[['cu_number', 'cu_name', 'statecode', 'peer_group']], on="cu_number", how="left")
    
    # Sidebar with CU_NAME selection
selected_cu_name = st.sidebar.selectbox("Select CU Name", df_combined["cu_name"].unique())
selected_data = df_combined[df_combined["cu_name"] == selected_cu_name]

# Display selected CU's information
st.title("Credit Union Information Comparison")
st.subheader(f"Selected CU: {selected_cu_name}")
st.write(selected_data)

# Extract the state name for the selected CU for labeling
selected_state_name = selected_data['statecode'].values[0]

# Calculations for State and Peer Group
state_avg_assets = df_combined[df_combined['statecode'] == selected_state_name]['TOTAL ASSETS'].mean()
peer_group_avg_assets = df_combined[df_combined['peer_group'] == selected_data['peer_group'].values[0]]['TOTAL ASSETS'].mean()

# Visualization for the selected CU, its State average, and Peer Group average
# Update labels to include the name of the CU and the name of the State
labels = [selected_cu_name, f"Average in {selected_state_name}", "Peer Group Average"]
values = [selected_data['TOTAL ASSETS'].values[0], state_avg_assets, peer_group_avg_assets]

fig = px.bar(
    x=labels,
    y=values,
    labels={'x': "Category", 'y': "Total Assets"},
    title="Total Assets Comparison"
)
st.plotly_chart(fig)