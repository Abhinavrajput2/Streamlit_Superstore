import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json


tp = st.secrets.type
project_id = st.secrets.project_id
pkid = st.secrets.private_key_id
pk=st.secrets.private_key
cemail=st.secrets.client_email
cid=st.secrets.client_id
auri=st.secrets.auth_uri
turi=st.secrets.token_uri
aprovider=st.secrets.auth_provider_x509_cert_url
cert=st.secrets.client_x509_cert_url
udom=st.secrets.universe_domain

json_string = f"""{{
    "type": {tp},
    "project_id": {project_id},
    "private_key_id": {pkid},
    "private_key": {pk},
    "client_email": {cemail},
    "client_id": {cid},
    "auth_uri": {auri},
    "token_uri": {turi},
    "auth_provider_x509_cert_url": {aprovider},
    "client_x509_cert_url": {cert},
    "universe_domain": {udom}
}}
"""
data = json.loads(json_string)


cred = credentials.Certificate(json_string)
# firebase_admin.initialize_app(cred,"App")

def app():
    choice=st.selectbox('Login/Signup',['Login','Sign Up'])
    def f():
        try: 
            user = auth.get_user_by_email(email)
            st.write('Login success')
        except:
            st.warning('Login Failed')


    if choice =="Login":
         email =st.text_input("Email Address")
         Password =st.text_input('Password', type ='password')
         st.button('Login')
    

    else:
         Username = st.text_input("Enter your unique username")
         email =st.text_input('Email Address')
         Password = st.text_input('Password',type ='password')
         if st.button("Create your account"):
             user = auth.create_user(email=email,password=Password,uid=Username)
             st.success("Account created successfully")
             st.markdown('please Login using email and password')
             st.balloons()