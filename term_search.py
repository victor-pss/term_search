import logging
from datetime import datetime

def get_date():
    return ' - ' + str(datetime.now()) + ': '

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', filename='app.log', encoding='utf-8', level=logging.DEBUG)

logger.info(get_date() + 'Starting Imports')

import streamlit as st
import streamlit.components.v1 as components
# from streamlit_tags import st_tags
import ftputil
import re

logger.info(get_date() + 'Imports Complete')

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

def term_search(FTP_HOST, FTP_USER, FTP_PASS, THEME_FOLDER):
    files = []

    logger.info(get_date() + 'term_search function - ' +  str({'FTP_HOST': FTP_HOST, 'FTP_USER': FTP_USER, 'FTP_PASS': FTP_PASS, 'THEME_FOLDER': THEME_FOLDER}))

    with ftputil.FTPHost(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        try:
            st.write('FTP connected')
            for (dirnames, subdirs, filename) in ftp.walk('./public_html/wp-content/themes/' + THEME_FOLDER):
                st.write(str(dirnames))
                st.write(str(subdirs))
                st.write(str(filename))
                for name in filename:
                    dir = dirnames
                    if dir[-1] != '/':
                        dir += '/'
                    f = dir + name
                    st.write(f)
                    logger.info(get_date() + 'file searched - ' + f)

                    if name.endswith('.php') or name.endswith('.css') or name.endswith('.html') or name.endswith('.js'):
                        with ftp.open(f, 'r', encoding='utf8') as obj:
                            file = obj.read()
                            # if re.search("the_field", file, re.IGNORECASE) != None or re.search("the_sub_field", file, re.IGNORECASE) != None:
                            if re.search("drsalamati.com.txt", file, re.IGNORECASE) != None:
                                logger.info(get_date() + ' file found    - term found in the above file ^^^^^^^^^')
                                st.write('found ^^^^^^^^^^^^^')
                                files.append(f)
        except:
            return 'error'
        logger.info(get_date() + 'found files - ' + str(files))
        return files


if 'FTP_HOST' not in st.session_state:
    st.session_state['FTP_HOST'] = ''

if 'FTP_USER' not in st.session_state:
    st.session_state['FTP_USER'] = ''

if 'FTP_PASS' not in st.session_state:
    st.session_state['FTP_PASS'] = ''

if 'THEME_FOLDER' not in st.session_state:
    st.session_state['THEME_FOLDER'] = ''

if 'results' not in st.session_state:
    st.session_state['results'] = []

if 'query_complete' not in st.session_state:
    st.session_state['query_complete'] = False

logger.info(get_date() + 'Initial State')
logger.info(get_date() + str(st.session_state))

with st.form('my_form'):
    # st.session_state['FTP_HOST'] = st_tags(label='FTP Host', text='Press Enter to add the host', suggestions=['92.204.128.116', '92.204.139.144',  '92.204.139.241'], maxtags=1, key=None)
    st.session_state['FTP_HOST'] = st.text_input('FTP Host', key=None)
    st.session_state['FTP_USER'] = st.text_input('FTP User', key=None)
    st.session_state['FTP_PASS'] = st.text_input('FTP Password', type="password", key=None)
    # st.session_state['THEME_FOLDER'] = st_tags(label='Theme Folder', text='Press Enter to add folder', suggestions=['pss-theme', 'click5-wp'], maxtags=1, key=None) 
    st.session_state['THEME_FOLDER'] = st.text_input('Theme Folder', key=None)
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if st.session_state['FTP_HOST'] and st.session_state['FTP_USER'] and st.session_state['FTP_PASS'] and st.session_state['THEME_FOLDER']:
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
            with st.spinner('Working on your request...'):
                results = term_search(st.session_state['FTP_HOST'], st.session_state['FTP_USER'], st.session_state['FTP_PASS'], st.session_state['THEME_FOLDER'])
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

if st.session_state['query_complete'] is True:
    st.write('Search Results:')
    st.divider()
    if len(st.session_state['results']) == 0:
        st.write('There are no instances found...')
    else:
        st.write(len(st.session_state['results']), 'were found')
        for el in st.session_state['results']:
            st.write(el)