import streamlit as st
import sqlite3
import pickle
from PIL import Image
import numpy as np

# Load models
LogReg_model = pickle.load(open('LogReg_model1.pkl', 'rb'))
DecisionTree_model = pickle.load(open('DecisionTree_model1.pkl', 'rb'))
NaiveBayes_model = pickle.load(open('NaiveBayes_model1.pkl', 'rb'))
RF_model = pickle.load(open('RF_model1.pkl', 'rb'))

def classify(answer):
    return answer[0] + " is the best crop for cultivation here."

# Database functions
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    if not user_exists(username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    else:
        return False

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = c.fetchone()
    conn.close()
    return data is not None

# Ensure the user table exists
create_user_table()

def main():
    st.title("CROP PREDICTION SYSTEM")

    # Login functionality
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        choice = st.sidebar.selectbox('Login/SignUp', ['Login', 'Sign Up'])

        if choice == 'Login':
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = verify_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                else:
                    st.error("Invalid username or password")
        else:
            st.subheader("Sign Up")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Sign Up"):
                if add_user(new_username, new_password):
                    st.success("Account created successfully")
                else:
                    st.error("Username already exists")
    else:
        # Main crop prediction functionality
        st.sidebar.write(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            

        image = Image.open('cc.jpg')
        st.image(image)
        html_temp = """
        <div style="background-color:teal; padding:10px">
        <h2 style="color:white;text-align:center;">Find The Most Suitable Crop</h2>
        </div>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        activities = ['Naive Bayes (The Best Model)', 'Logistic Regression', 'Decision Tree', 'Random Forest']
        option = st.sidebar.selectbox("Which model would you like to use?", activities)
        st.subheader(option)
        sn = st.text_input('NITROGEN (N)')
        sp = st.text_input('PHOSPHOROUS (P)')
        pk = st.text_input('POTASSIUM (K)')
        pt = st.text_input('TEMPERATURE')
        phu = st.text_input('HUMIDITY')
        pPh = st.text_input('Ph')
        pr = st.text_input('RAINFALL')

        # Convert inputs to numeric values
        try:
            inputs = [[float(sn), float(sp), float(pk), float(pt), float(phu), float(pPh), float(pr)]]
        except ValueError:
            st.error("Please enter valid numeric values for all fields.")
            return

        if st.button('Classify'):
            if option == 'Logistic Regression':
                st.success(classify(LogReg_model.predict(inputs)))
            elif option == 'Decision Tree':
                st.success(classify(DecisionTree_model.predict(inputs)))
            elif option == 'Naive Bayes':
                st.success(classify(NaiveBayes_model.predict(inputs)))
            else:
                st.success(classify(RF_model.predict(inputs)))

if __name__ == '__main__':
    main()
