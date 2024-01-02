import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
cred = credentials.Certificate(r'C:\Users\522an\Downloads\myapp-20240102T172855Z-001\myapp\secret\sales-report-aacf5-d50b776c52aa.json')
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