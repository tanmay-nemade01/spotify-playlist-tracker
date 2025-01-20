from snowflake.snowpark.session import Session
import json
import streamlit as st
from pathlib import Path

def connector_parameters():
    snowflake_json = Path(__file__).parent.parent / "configs" / "snowflake.json"
    with open(snowflake_json, 'r') as file:
        data = json.load(file)
    conn = {
        "account":data['SNOWFLAKE'][0]['ACCOUNT'],
        "user":data['SNOWFLAKE'][1]['USER'],
        "password":data['SNOWFLAKE'][2]['PASSWORD'],
        "role":'ACCOUNTADMIN',
        "warehouse":'COMPUTE_WH'
    }
    return conn

def create_session():
    conn = connector_parameters()
    session = Session.builder.configs(conn).create()
    print('Snowflake Connection Successful')
    return session