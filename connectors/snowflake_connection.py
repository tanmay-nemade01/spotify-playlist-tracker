from snowflake.snowpark.session import Session
import json
import streamlit as st
from pathlib import Path

def connector_parameters():
    snowflake_json = Path(__file__).parent.parent / "configs" / "snowflake.json"
    try:
        with open(snowflake_json, 'r') as file:
            data = json.load(file)
        account = data['SNOWFLAKE'][0]['ACCOUNT']
        user = data['SNOWFLAKE'][1]['USER']
        password = data['SNOWFLAKE'][2]['PASSWORD']
    except:
        st.header('Enter Snowflake Credentials')
        account = st.text_input('Enter Account Identifier')
        user = st.text_input('Enter Username')
        password = st.text_input('Enter Password',type='password')
    
    if account != '' and user != '' and password != '':
        conn = {
            "account":account,
            "user":user,
            "password":password,
            "role":'ACCOUNTADMIN',
            "warehouse":'COMPUTE_WH'
        }
        return conn

def create_session():
    conn = connector_parameters()
    if conn is not None:
        session = Session.builder.configs(conn).create()
        st.success('Snowflake Connection Successful')
        return session