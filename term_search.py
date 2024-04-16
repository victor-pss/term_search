import streamlit as st
import ftputil
import re

st.title("Term Search App")
st.write("""
    This app helps search for the_field and the_sub_field ACF fields.
    Please enter the FTP credentials below and the theme folder as it
    appears in the directory.
    """)

def term_search(FTP_HOST, FTP_USER, FTP_PASS, THEME_FOLDER):
    files = []
    with ftputil.FTPHost(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        for (dirnames, subdirs, filename) in ftp.walk('/public_html/wp-content/themes/' + THEME_FOLDER):
            for name in filename:
                dir = dirnames
                if dir[-1] != '/':
                    dir += '/'
                f = dir + name
                # print(f)
                if name.endswith('.php') or name.endswith('.css') or name.endswith('.html') or name.endswith('.js'):
                    with ftp.open(f, 'r', encoding='utf8') as obj:
                        file = obj.read()
                        if re.search("the_field", file, re.IGNORECASE) != None or re.search("the_sub_field", file, re.IGNORECASE) != None:
                            files.append(f)
    return files

form = st.form(key='my_form')
FTP_HOST = form.text_input("FTP Host", key=None)
FTP_USER = form.text_input("FTP User", key=None)
FTP_PASS = form.text_input("FTP Password", key=None)
THEME_FOLDER = form.text_input("Theme Folder", key=None)
submit_button = form.form_submit_button("Submit")

# st.write('FTP_HOST:', FTP_HOST)
# st.write('FTP_USER:', FTP_USER)
# st.write('FTP_PASS:', FTP_PASS)
# st.write('THEME_FOLDER:', THEME_FOLDER)

# FTP_HOST = '92.204.128.116'
# FTP_USER = 'harrisonleeplast'
# FTP_PASS = 'HGkU!3+Cq+_TD_LZUB'
    
if submit_button:
    if FTP_HOST and FTP_USER and FTP_PASS and THEME_FOLDER:
        with st.spinner('Working on your request...'):
            results = term_search(FTP_HOST, FTP_USER, FTP_PASS, THEME_FOLDER)
            for el in results:
                st.write(el)
            st.success(results)
    else:
        st.error('Please fill all the fields before submitting!')

# st.write(files)
# print("==========================================")
# print("", len(files), "files with the_field or the_sub_field")
# print("==========================================")
# for x in files:
# 	print(x)

