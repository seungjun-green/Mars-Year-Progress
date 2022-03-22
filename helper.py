import tweepy as twitter
import keys
from datetime import datetime
from PIL import Image
import requests
from bs4 import BeautifulSoup

class Data:
    auth = twitter.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
    api = twitter.API(auth)
    sol = 88775
    mars_year=59301700

class Start:
    start_date = datetime(2021, 2, 7, 0, 0, 0)


def get_difference():
    today = datetime.today()
    difference = (today - Start.start_date).total_seconds()
    difference = difference%Data.mars_year
    return difference


def recent_one():
    text = Data.api.user_timeline(user_id='@marsyrprogress', count=1)[0]._json['text']
    word = ""
    spotted = False

    for letter in text:
        if spotted == False:
            if letter == '\n':
                spotted = True
            else:
                pass
        else:
            if letter == ' ':
                break
            else:
                word += letter

    return word[:-1]

def create_img(percentage):
    x = 800
    y = 100
    img = Image.new("RGB", (800, 400), (55, 66, 91))
    bar = Image.new("RGB", (760, y), (255, 255, 255))
    progress = Image.new("RGB", (int(760 * float(percentage) / 100), y), (22, 193, 124))
    bar.paste(progress, (0, 0))
    img.paste(bar, (int((800 - x) / 2) + 20, int((400 - y) / 2)))
    # img.show(bar)
    img.save("img.png")
    file_path = "./" + "img.png"
    return file_path


def getHashtags():
    url = 'https://sites.google.com/view/mybotshashtags/home'
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    for t in text:
        if t.parent.name in {'p'}:
            output += '{} '.format(t)

    return output


def send_tweet(day, percentage):
    hashtags = getHashtags()
    text = f"Sol {day} of 668\n{percentage}% of a year passed\n{hashtags}"
    img = create_img(percentage)
    try:
        Data.api.update_status_with_media(text, img)
        print(f"Successfully tweeted on {datetime.today()}! \n {text}")

        if percentage == 100:
            Data.api.update_status("HAPPY NEW YEAR MARS!🥳🎉")
            print("Successfully tweeted New Year Celebration Tweet")

    except twitter.errors.TweepyException as e:
        print(f"Error Happend: {e}")