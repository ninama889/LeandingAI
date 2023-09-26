#pip install "snowflake-snowpark-python[pandas]"

#pip install snowflake-snowpark-python

from snowflake.snowpark.session import Session

from snowflake.snowpark.functions import avg, sum, col, lit

import streamlit as st

import pandas as pd


def create_session_object():
    connection_parameters = {
        "account": "anblicksorg_aws.us-east-1",
        "user": "LENDINGAI",
        "password": "LendingAI@202308",
        "role": "LENDINGAI_ARL",
        "warehouse": "LENDINGAI_WH",
        "database": "LENDINGAI_DB",
        "schema": "RAW"
    }
    session = Session.builder.configs(connection_parameters).create()
    return session  # Return the created session

snowflake_session = create_session_object()



# def load_data(session, table_name):

    #with open('style_sum.css') as f:
        #st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#     snow_df = session.table(table_name)

#     return snow_df

snowflake_session = create_session_object()

# Create a Streamlit app


st.subheader("Loan Recommendation")

# Get data from Snowflake for the tables

transform_df = snowflake_session.table( 'LENDINGAI_DB.BASE.TBL_ID_TABLE')

    # Convert Snowflake DataFrames to pandas DataFrames

trans_id_data = transform_df.to_pandas()

data=trans_id_data['id'].iloc[:10000]


# colx,coly = st.columns([2,0])


# with colx:
prods = st.container()

with prods:
        
        col1, col3 = st.columns([2.1,2.1])
        
        selected_id = st.selectbox("Select Application ID:", data)

        # Filter the DataFrame based on the selected "ID"
        filtered_df = trans_id_data[trans_id_data['id'] == selected_id]
    
        # Display "EMP_TITLE" values based on the selected "ID"
        col4, col5, col6 = st.columns(3)

        with col4:
        
         st.markdown(f"<p style='text-align: center;'>Occupation of Employee</p>", unsafe_allow_html=True)
         st.success(filtered_df['EMP_TITLE'].values[0])

        # Display "TITLE" values based on the selected "ID"
        with col5:
            
         st.markdown(f"<p style='text-align: center;'>Current Loan</p>", unsafe_allow_html=True)
         st.success(filtered_df['TITLE'].values[0])

        # Display "LOAN_AMNT" values based on the selected "ID"
        with col6:
         st.markdown("<p style='text-align: center;'>Loan Amount</p>", unsafe_allow_html=True)
         st.success(filtered_df['LOAN_AMNT'].values[0])

        filtered_titles = filtered_df['TITLE'].tolist()

        #selected_title = col1.selectbox("Select title", filtered_titles)

        INPUT_LIST = [filtered_titles]

        INPUT_PRODUCT= filtered_titles

            #snowflake_array = snowflake_session.to_array(INPUT_PRODUCT)

        snowflake_array=','.join(map(str, INPUT_PRODUCT))

        k=snowflake_session.call('LENDINGAI_DB.BASE.SP_RECOMMENDER',snowflake_array)

        with col5:
            st.markdown("<p style='text-align: center;'>Recommended Loan</p>", unsafe_allow_html=True)
            st.success(k)
            


 
    

    

