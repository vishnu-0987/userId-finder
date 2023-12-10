from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)


wiki_link = 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes'
page = requests.get(wiki_link)
soup = BeautifulSoup(page.content, 'html.parser')
user_agent = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
              ' Mobile Safari/537.36')
headers = {'user-agent': user_agent}


websites = {
        'Facebook': 'https://www.facebook.com/',
        'Twitter': 'https://twitter.com/',
        'Instagram': 'https://www.instagram.com/',
        'Youtube': 'https://www.youtube.com/user/',
        'Reddit': 'https://www.reddit.com/user/',
        'ProductHunt': 'https://www.producthunt.com/@',
        'Pinterest': 'https://www.pinterest.com/',
        'Flickr': 'https://www.flickr.com/people/',
        'Vimeo': 'https://vimeo.com/',
        'Soundcloud': 'https://soundcloud.com/',
        'Disqus': 'https://disqus.com/',
        'Medium': 'https://medium.com/@',
        'AboutMe': 'https://about.me/',
        'Imgur': 'https://imgur.com/user/',
        # returns a landing page. to do
        'Flipboard': 'https://flipboard.com/',
        'Slideshare': 'https://slideshare.net/',
        'Spotify': 'https://open.spotify.com/user/',
        'Scribd': 'https://www.scribd.com/',
        'Patreon': 'https://www.patreon.com/',
        'BitBucket': 'https://bitbucket.org/',
        'GitLab': 'https://gitlab.com/',
        'Github': 'https://www.github.com/',
        'GoodReads': 'https://www.goodreads.com/',
        'Instructable': 'https://www.instructables.com/member/',
        'CodeAcademy': 'https://www.codecademy.com/',
        'Gravatar': 'https://en.gravatar.com/',
        'Pastebin': 'https://pastebin.com/u/',
        'FourSquare': 'https://foursquare.com/',
        'HackerNews': 'https://news.ycombinator.com/user?id=',
        'CodeMentor': 'https://www.codementor.io/',
        'Trip': 'https://www.trip.skyscanner.com/user/',
        'Blogger': '.blogspot.com',
        'Wordpress': '.wordpress.com',
        'Tumbler': '.tumblr.com',
        'Deviantart': '.deviantart.com"',
        # ^ This website is either blocking/delaying the script
        'LiveJournel': '.livejournal.com',
        'Slack': '.slack.com',
    }




def get_website_membership(site, username, results):
    uname = username

    def print_fail(site):
        print(site, "Fail")

    def print_success(site):

        print(site, "Success")

    url = websites[site]

    state = "FAIL"
    msg = '--exception--'

    if not url[:1] == 'h':
        link = 'https://' + uname + url
    else:
        link = url + uname

    try:
        if site == 'Youtube' or 'Twitter':
            response = requests.get(link)
        else:
            response = requests.get(link, headers=headers)
        tag = soup.find(id=response.status_code)
        msg = tag.find_parent('dt').text
        response.raise_for_status()

    except Exception:
        results[site] = False
        print_fail(site)

    else:
        res_soup = BeautifulSoup(response.content, 'html.parser')
        if site == 'Pastebin':
            if len(res_soup.find_all('h1')) == 0:
                msg = 'broken URL'
                results[site] = False
                print_fail(site)

            else:
                state = 'SUCCESS'
                results[site] = True
                print_success(site)

        elif site == 'Wordpress':
            if 'doesn’t exist' or 'blocked' in res_soup:
                msg = 'broken URL'
                results[site] = False
                print_fail(site)
            else:
                state = 'SUCCESS'
                results[site] = True
                print_success(site)


        # elif site == 'Imgur':
        #     ToDo

        elif site == 'GitLab':
            if 'Sign in' in res_soup.title.text:
                msg = 'broken URL'
                results[site] = False
                print_fail(site)
            else:
                state = 'SUCCESS'
                results[site] = True
                print_success(site)

        elif site == 'HackerNews':
            if 'No such user.' in res_soup:
                msg = 'No Such User!'
                results[site] = False
                print_fail(site)
            else:
                state = 'SUCCESS'
                results[site] = True
                print_success(site)

        elif site == 'ProductHunt':
            if 'Page Not Found' in res_soup.text:
                msg = 'No Such User!'
                results[site] = False
                print_fail(site)
            else:
                state = 'SUCCESS'
                results[site] = True
                print_success(site)

        else:
            state = 'SUCCESS'
            results[site] = True
            print_success(site)




# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username_to_check = request.form['username']
        results = {}
        for site, url in websites.items():
            get_website_membership(site, username_to_check, results)

        return render_template('index.html', username=username_to_check, results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)