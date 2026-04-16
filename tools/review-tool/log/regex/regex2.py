import streamlit as st
import pandas as pd
import glob
import os
import json
from io import BytesIO
import sqlite3

st.title("Regex Data Collector Tool")

st.write("Paste the full data string to extract the regex code and collect matching data from CSV files.")

input_data = st.text_area("Paste full data string", "")

regex_code = ""
if st.button("Extract Regex Code") and input_data.strip():
    regex_code = input_data.strip().split()[0]
    st.session_state['regex_code'] = regex_code
    st.write(f"Extracted regex code: `{regex_code}`")

# Initialize scanned data database
scanned_db = "scanned_data.db"
conn = sqlite3.connect(scanned_db)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS scanned (regex_code TEXT, _id TEXT, feature_raw TEXT, PRIMARY KEY (regex_code, _id))''')
try:
    cursor.execute("ALTER TABLE scanned ADD COLUMN feature_raw TEXT;")
except sqlite3.OperationalError:
    pass  # Column already exists
cursor.execute('''CREATE TABLE IF NOT EXISTS classifications (name TEXT, regex_code TEXT, last_order INTEGER DEFAULT 0, PRIMARY KEY (name, regex_code))''')
conn.commit()

if 'regex_code' in st.session_state:
    regex_code = st.session_state['regex_code']
    
    # Directory for CSV files
    csv_dir = "/home/gsbu/ml/tools/review-tool/log"
    if not os.path.exists(csv_dir):
        csv_dir = "."
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    
    if not csv_files:
        st.error("No CSV files found in the directory.")
    else:
        st.write(f"Scanning {len(csv_files)} CSV files...")
        
        all_matches = []
        cursor.execute("SELECT _id FROM scanned WHERE regex_code = ?", (regex_code,))
        scanned_ids = set(row[0] for row in cursor.fetchall())
        
        for csv_path in csv_files:
            try:
                df = pd.read_csv(csv_path, encoding='utf-8-sig')
                if 'feature_raw' in df.columns and '_id' in df.columns:
                    # Extract the first part of feature_raw (before space) and match exactly with regex_code
                    first_part = df['feature_raw'].str.split().str[0]
                    mask = first_part.str.lower() == regex_code.lower()
                    matches = df[mask]
                    for _, row in matches.iterrows():
                        _id = row.get('_id')
                        if _id not in scanned_ids:
                            record = {
                                '_id': _id,
                                'feature_raw': row.get('feature_raw', ''),
                                'first_seen_time': row.get('first_seen_time', ''),
                                # Add all columns
                                **{col: row.get(col, '') for col in df.columns}
                            }
                            all_matches.append(record)
            except Exception as e:
                st.write(f"Error reading {csv_path}: {e}")
        
        if all_matches:
            df_matches = pd.DataFrame(all_matches)
            total_matches = len(df_matches)
            st.write(f"Total new matching rows: {total_matches}")
            
            # Pagination
            page_size = 50
            total_pages = (total_matches + page_size - 1) // page_size
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
            start = (page - 1) * page_size
            end = start + page_size
            df_page = df_matches.iloc[start:end]
            
            st.subheader(f"Preview (Page {page} of {total_pages}, showing {len(df_page)} rows)")
            st.dataframe(df_page)
            
            # Detailed view
            st.subheader("Detailed View")
            selected_row = st.selectbox("Select a row for details", df_matches['_id'].tolist())
            # if selected_row:
            #     row_details = df_matches[df_matches['_id'] == selected_row].iloc[0]
            #     st.json(row_details.to_dict())
            
            # Classification Name Input
            st.subheader("Classification")
            classification_name = st.text_input("Enter classification name (e.g., get_slash)", "")
            
            if classification_name.strip():
                # Get current order for classification
                cursor.execute("SELECT last_order FROM classifications WHERE name = ? AND regex_code = ?", (classification_name, regex_code))
                result = cursor.fetchone()
                current_order = result[0] if result else 0
                
                # Get total classified for this name
                cursor.execute("SELECT SUM(last_order) FROM classifications WHERE name = ?", (classification_name,))
                result_total = cursor.fetchone()
                total_classified = result_total[0] if result_total and result_total[0] else 0
                
                # Get number of different regex codes for this classification
                cursor.execute("SELECT COUNT(*) FROM classifications WHERE name = ?", (classification_name,))
                result_num = cursor.fetchone()
                num_regex = result_num[0] if result_num else 0
                
                st.write(f"Total rows classified under '{classification_name}': {total_classified}")
                st.write(f"Number of different regex codes for this classification: {num_regex}")
                st.write(f"Current order for this regex code: {current_order}")
                
                # # Show details of existing classifications
                # if num_regex > 0:
                #     st.subheader("Existing Classifications Details")
                #     cursor.execute("SELECT regex_code, last_order FROM classifications WHERE name = ?", (classification_name,))
                #     details = cursor.fetchall()
                #     for reg, last in details:
                #         cursor.execute("SELECT feature_raw FROM scanned WHERE regex_code = ? LIMIT 1", (reg,))
                #         sample_result = cursor.fetchone()
                #         sample = sample_result[0] if sample_result and sample_result[0] else "No sample available"
                #         st.write(f"**Regex Code:** {reg} | **Last Order:** {last} | **Total Count:** {last} | **Sample Feature Raw:** {sample[:100]}...")  # Truncate sample
                
                # Generate preview with labels
                df_export_preview = df_matches.copy()
                df_export_preview['label'] = [f"{classification_name}_{(current_order + i + 1):02d}" for i in range(len(df_export_preview))]
                st.subheader("Export Preview")
                st.dataframe(df_export_preview.head(10))  # Show first 10 rows as preview
            
            if st.button("Mark as Scanned and Export"):
                if not classification_name.strip():
                    st.error("Please enter a classification name before exporting.")
                else:
                    # Mark as scanned
                    new_ids = df_matches['_id'].tolist()
                    for _id in new_ids:
                        feature_raw = df_matches[df_matches['_id'] == _id]['feature_raw'].iloc[0]
                        cursor.execute("INSERT OR IGNORE INTO scanned (regex_code, _id, feature_raw) VALUES (?, ?, ?)", (regex_code, _id, feature_raw))
                    conn.commit()
                    
                    # Get current order for classification
                    cursor.execute("SELECT last_order FROM classifications WHERE name = ? AND regex_code = ?", (classification_name, regex_code))
                    result = cursor.fetchone()
                    current_order = result[0] if result else 0
                    
                    # Export with labels
                    df_export = df_matches.copy()
                    df_export['label'] = [f"{classification_name}_{(current_order + i + 1):02d}" for i in range(len(df_export))]
                    output_file = f"{classification_name}.xlsx"
                    
                    # Determine sheet name
                    sheet_name = f'{regex_code.replace("|", "_")}_{current_order + 1}-{current_order + len(df_export)}'
                    
                    # Write to Excel, appending if exists
                    mode = 'a' if os.path.exists(output_file) else 'w'
                    with pd.ExcelWriter(output_file, engine='openpyxl', mode=mode) as writer:
                        df_export.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # Read the file for download
                    with open(output_file, 'rb') as f:
                        buffer = BytesIO(f.read())
                    
                    st.success("Data marked as scanned. Click below to download the Excel file.")
                    st.download_button(
                        label="Download Excel",
                        data=buffer,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # Update last_order
                    new_last_order = current_order + len(df_export)
                    cursor.execute("INSERT OR REPLACE INTO classifications (name, regex_code, last_order) VALUES (?, ?, ?)", (classification_name, regex_code, new_last_order))
                    conn.commit()
        else:
            st.write("No new matching data found.")
