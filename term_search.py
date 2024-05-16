import streamlit as st
import streamlit.components.v1 as components
from streamlit_tags import st_tags
import ftputil
import re
import requests

ip = requests.get('https://api64.ipify.org').text

st.markdown("""
    <style>
    div.stSpinner > div {
        text-align: center;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img style="width: 100px; margin-right: 15px;" src="https://pss-application-assets.s3.amazonaws.com/code-digger/code_digger-logo2.png" />
        <h1>Code Digger</h1>
    </div>
    """, unsafe_allow_html=True)
st.write("""
    This app helps search for the_field and the_sub_field ACF fields.
    Please enter the FTP credentials below and the theme folder as it
    appears in the directory.
    """)

def term_search(FTP_HOST, FTP_USER, FTP_PASS, THEME_FOLDER, TERMS):
    files = []

    # Connect to the FTP server and search for the TERMS in the theme folder
    with ftputil.FTPHost(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        try:
            path = f'/public_html/wp-content/themes/{THEME_FOLDER}'
            for (dirnames, subdirs, filename) in ftp.walk(path):
                for name in filename:
                    if name.endswith(('.php', '.css', '.html', '.js')): # Only search for php, css, html, and js files
                        file_path = f"{dirnames.rstrip('/')}/{name}"
                        with ftp.open(file_path, 'r', encoding='utf8') as file_obj:
                            content = file_obj.read()
                            pattern = '(?:% s)' % '|'.join(TERMS) # regex pattern to search for TERMS in the file content
                            results = re.findall(pattern, content, re.IGNORECASE)
                            if results:
                                count = {term: results.count(term) for term in set(results)}
                                files.append(f"{file_path} - " + ', '.join(f"[{key} - {value} times]" for key, value in count.items()))
        except Exception as e:
            return f'error: {str(e)}'

        return files

default_values = {
    'FTP_HOST': '',
    'FTP_USER': '',
    'FTP_PASS': '',
    'THEME_FOLDER': '',
    'results': [],
    'TERMS': '',
    'query_complete': False,
}
 # Set the default values for the session state variables
for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value


with st.form('my_form'):
    # form fields
    st.session_state['FTP_HOST'] = st_tags(label='FTP Host', text='Press Enter to add the host', suggestions=['92.204.128.116', '92.204.139.144',  '92.204.139.241'], maxtags=1, key=None)
    st.session_state['FTP_USER'] = st.text_input('FTP User', key=None)
    st.session_state['FTP_PASS'] = st.text_input('FTP Password', type="password", key=None)
    st.session_state['THEME_FOLDER'] = st_tags(label='Theme Folder', text='Press Enter to add folder', suggestions=['pss-theme', 'click5-wp'], maxtags=1, key=None)
    st.session_state['TERMS'] = st_tags(label='What do you want to search for?', text='Press Enter to add terms', value=['the_field', 'the_sub_field'])
    submit_button = st.form_submit_button("Submit")

    # on form submit, run the search function
    if submit_button:
        st.markdown("""
                <style>
                    .miner {
                        display: flex;
                        justify-content: center;
                    }
                </style>
            """, unsafe_allow_html=True)
        st.markdown("""
                <div class="miner">
                    <img style="width: 470px; height: 75px; object-fit: cover;" src="https://pss-application-assets.s3.amazonaws.com/code-digger/miner.gif" />
                </div>
            """, unsafe_allow_html=True)
        if all(st.session_state.get(key) for key in ['FTP_HOST', 'FTP_USER', 'FTP_PASS', 'THEME_FOLDER', 'TERMS']):
            with st.spinner('Working on your request...'):
                results = term_search(st.session_state['FTP_HOST'][0], st.session_state['FTP_USER'], st.session_state['FTP_PASS'], st.session_state['THEME_FOLDER'][0], st.session_state['TERMS'])
                st.session_state['results'] = results
                st.session_state['query_complete'] = True
            st.markdown("""
                    <style>
                        .miner {
                            display: none;
                        }
                    </style>
                """, unsafe_allow_html=True)
        else:
            st.error('Please fill all the fields before submitting!')
            st.markdown("""
                    <style>
                        .miner {
                            display: none;
                        }
                    </style>
                """, unsafe_allow_html=True)

if st.session_state['query_complete'] is True:
    st.write('Search Results:')
    st.divider()
    if len(st.session_state['results']) == 0:
        st.write('There are no instances found...')
    else:
        st.write(len(st.session_state['results']), 'were found')
        for el in st.session_state['results']:
            st.write(el)

st.write("Server IP: " + str(ip))
