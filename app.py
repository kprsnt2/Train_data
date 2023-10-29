import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter

# Function to transform data
def transform_data(source_df, destination_df):
    # Define a mapping from source column names to destination column names
    column_mapping = {
        "Date": "DATE",  # Map source "Trip Id" to destination "EFT NO"
        "EFT No.": "EFT NO",  # Map source "Excess Fare Tkt" to destination "DATE"
        "Train No.": "TRAIN NO",
        "Cause of Charge": "REASON",
        "From Stn": "FROM",
        "To Stn": "TO",
        "Amt of excess fare realised": "FARE",
        "Excess Charges (Penalty)": "PENALTY",
        "Total EFT Amt(Incld GST)": "TOTAL",
    }    
        # Merge the source data into the destination data based on the mapping
    for source_col, dest_col in column_mapping.items():
        destination_df[dest_col] = source_df[source_col]

    # No need to drop duplicate columns since we've updated the destination columns
    transformed_data = destination_df


    return destination_df
# Title and file upload widgets
st.title("Excel Data Transformation App")
source_file = st.file_uploader("Upload the source Excel file", type=["xls", "xlsx"])
destination_file = st.file_uploader("Upload the destination Excel file", type=["xls", "xlsx"])

if source_file and destination_file:
    # Read Excel files into dataframes
    source_df = pd.read_excel(source_file, header=6)  # No header
    destination_df = pd.read_excel(destination_file, header=2)  # Header is in the 3rd row

    # Transform the source data
    transformed_data = transform_data(source_df, destination_df)

    # Update the existing Excel file with transformed data
    with pd.ExcelWriter(destination_file, engine='openpyxl', mode='a') as writer:
        transformed_data.to_excel(writer, sheet_name='Transformed Data', index=False)

    # Allow your friend to download the transformed data as a new Excel file
    st.markdown("### Download Transformed Data")
    st.markdown("Click below to download the updated data.")
    
    # Create a BytesIO object to store the Excel data for download
    excel_buffer = BytesIO()
    transformed_data.to_excel(excel_buffer, index=False)
    st.download_button("Download Transformed Data", excel_buffer.getvalue(), key="download", file_name="transformed_data.xlsx")
