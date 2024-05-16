<h1 style='text-align: center'>Code Digger</h1>

<h2 style='text-align: center'>Introduction</h2>
Recently, the Advanced Custom Fields (ACF) - both free and Pro versions - plugin update broke our WordPress websites. The break comes in the form of the_field and the_sub_field parameters that normally inject code into the frontend being sanitized. The sanitization now shows the code on the frontend. Our team’s practice consists of adding the two parameters statically in php files. I’m not 100% sure if they are added in.html, .css, or .js files at the time of this writing. The fix for the broken behavior is to search through all of the theme files and replace the instance of the parameters with the corrected representation according to the ACF documentation. To do this for over 200 websites, we are expecting to spend ~40 minutes for each site which totals ~137 hours.
<br><br>

The reason I created this tool was to help speed up the process of fixing the_field and the_sub_field parameters in the php files. This helps save 60 - 70% of time checking each file if the term exists. With over 200 sites to check, we dropped our expected time of completion from 137 hours to 61.5 hours. Of course, this changes depending on how many instances are on each site.

<h2 style='text-align: center'>How is this achieved?</h2>

I used Python as my choice of language. Within that, I used a few packages: *ftputil*, *streamlit*, *streamlit_tags*, *re*, and *requests*. *ftputil* helps me crawl the directories. *streamlit* and *streamlit_tags* allow me to create a UI and host the app online. *re* is for my regular expression `findall` function that searches the content within the files. And *requests* is only used to get the IP of the server in order to whitelist on our hosts.<br>

```python
import streamlit as st
import streamlit.components.v1 as components
from streamlit_tags import st_tags
import ftputil
import re
import requests

ip = requests.get('https://api64.ipify.org').text
```

Our primary workhorse for this app is going to be the term_search function. I define this function passing in 5 arguments - `FTP_HOST`, `FTP_USER`, `FTP_PASS`, `THEME_FOLDER`, and `TERMS`. These variables have pretty straightforward explanations, however, most of their data types are not what is expected. `FTP_HOST`, `THEME_FOLDER`, and `TERMS` are all lists (`[]`). The reason why I decided to make `FTP_HOST` and `THEME_FOLDER` lists is because of the use of *streamlit_tags*. This field allows for a type of autocomplete feature to the fields. A good question I do get a lot is, ‘Why not just use a select field with options?’ Because of the way `streamlit` works. `streamlit` select field allows for options, however, if you need something besides one of the options, like an IP address that is not within our hosts or a theme folder that we don’t normally come across, then you can simply add it yourself without being stuck with options available. This feature helps us quickly enter in repeat information as well which aids in the time saver explained earlier in this writing.

```python
def term_search(FTP_HOST, FTP_USER, FTP_PASS, THEME_FOLDER, TERMS):
```
