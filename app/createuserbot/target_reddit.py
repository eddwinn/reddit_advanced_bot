import time
import pyautogui
import speech_recognition as sr
import os
import subprocess
from app.createuserbot.query_api import google
from app.createuserbot.createuser import create_email, create_password
from app import session2
from app.createuserbot.models import Bots
from app.createuserbot.create_a_username import create_username
from app.createuserbot.get_cords import cords



PRIVATE = True
addtodb = True

''' You'll need to update based on the coordinates of your setup '''
download_location = "/home/bot/Downloads/"
pycharm_location = "/home/bot/.PyCharm2016.1/config/jdbc-drivers/"

r = sr.Recognizer()
# open firefox
FIREFOX_ICON_COORDS = (44, 154)  # Location of the Firefox icon on the side toolbar (to left click)
PRIVATE_COORDS = (121, 198)  # Location of "Open a new Private Window"
NON_PRIVATE_COORDS = (119, 181)  # Location of "Open a new regular Window"

# navigate to reddit signupusers
REDDIT_FAV_BUTTON = (164, 108)  # Location of the Firefox Search box
SIGNUP_BUTTON = (1263, 152)  # The button on reddits front page
EMAIL_INPUT = (581, 460)  # The input for email
EMAIL_BUTTON = (606,552)  # The button for email
CAPTCHA_COORDS = (429, 530)  # Coordinates of the empty CAPTCHA checkbox
CHECK_COORDS = (429, 530)  # Location where the green checkmark will be
CHECK_COORDS_OPENCHALLENGE = (433, 544)  # Location where the green checkmark will be
CHECK_COLOR = '#FFFFFF'  # Color of the green checkmark
CHECK_COLOR2 = '#009E55'  # another color i got
CHECK_COLOR3 = '#3CB47C'  # another color i got
CHECK_COLOR4 = '#F9F9F9'  # generic color? not sure if can use this

# the audio button
AUDIO_COORDS = (540, 732)  # Location of the Audio button
AUDIO_CLOSE_CORDS = (657, 78)  # Location of the Audio button
DOWNLOAD_COORDS = (592, 610)  # Location of the Download button
OK_RIGHTCLICK_BUTTON_COORDS = (656, 700)  # Location of the ok/save button for right click Download button
CLOSE_TAB_BUTTON_COORDS = (276, 88)  # Location of the tab to close for Download
VERIFY_COORDS = (664, 647)  # Verify button

# the username entry
USERNAME_INPUT = (561, 390)  # the username input
RIGHT_CLICK_COPY = (561, 453)  # the username input
PASSWORD_INPUT = (715, 488)  # the password input

#closeup and next
NEXT_BUTTON = (1092, 763)  # the finish button
FINAL_COORDS = (531, 536)  # Text entry box
CLOSE_LOCATION = (16, 10)

''' END SETUP '''



def checkcaptcha():
    """
    Check if we've completed the captcha successfully.
    """
    print("seeing the color ...")
    pyautogui.moveTo(CHECK_COORDS_OPENCHALLENGE)
    thecolor = runcommand(
        "eval $(xdotool getmouselocation --shell); xwd -root -silent | convert xwd:- -depth 8 -crop \"1x1+$X+$Y\" txt:- | grep -om1 '#\w\+'")
    print("Color: ", thecolor)
    thecolor = thecolor.decode('utf-8')
    thecolor = thecolor.upper()
    if CHECK_COLOR2 in str(thecolor) or str(CHECK_COLOR3) in str(thecolor):
        print("theres the color..it let us in")
        output = 1
    elif str(thecolor) == str(CHECK_COLOR4):
        print("Solved ..")
        output = 1

    else:
        output = 0
        print("UNKNOWN COLOR: thecolor")
    return output


def runcommand(command):
    """
    Run a command and get back its output
    """

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()[0].split()[0]



def get_a_user():
    # move to username on side...reddit makes this
    print("Entering a Username..")
    theusername = create_username()
    # copy that new username for database
    pyautogui.moveTo(USERNAME_INPUT)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(theusername, interval=0.5)
    print("Username:", theusername)

    # move to password
    print("Entering a Password..")
    pyautogui.moveTo(PASSWORD_INPUT)
    pyautogui.click()
    time.sleep(1)
    randompassword = create_password()
    newpassword = str(randompassword)
    print("Password: ", newpassword)
    pyautogui.typewrite(newpassword, interval=0.5)
    return theusername, newpassword


def addtodatabase(username,
                  password,
                  appname,
                  client_id,
                  client_secret,
                  user_agent,
                  email):
    try:
        new_person = Bots(username=username,
                          password=password,
                          appname=appname,
                          client_id=client_id,
                          client_secret=client_secret,
                          user_agent=user_agent,
                          user_email=email,
                          post_count=0,
                          karma = 0
                          )
        session2.add(new_person)
        session2.commit()
        print("successfully committed")
    except Exception as e:
        print(str(e))
        session2.rollback()



def gettowebsite():
    """
    Navigate to demo site, input user info, and download a captcha.
    """
    pyautogui.FAILSAFE = False
    print("Opening Firefox")
    pyautogui.moveTo(FIREFOX_ICON_COORDS)
    pyautogui.rightClick()
    time.sleep(.3)

    if PRIVATE is True:
        pyautogui.moveTo(PRIVATE_COORDS)
        pyautogui.click()
        time.sleep(5)
    else:
        pyautogui.moveTo(NON_PRIVATE_COORDS)
        pyautogui.click()
        time.sleep(5)

    print("Visiting Reddit..")
    pyautogui.moveTo(REDDIT_FAV_BUTTON)
    pyautogui.click()
    time.sleep(6)

    print("Create a new account..")
    pyautogui.moveTo(SIGNUP_BUTTON)
    pyautogui.click()
    time.sleep(7)

    print("Entering an Email..")
    pyautogui.moveTo(EMAIL_INPUT)
    pyautogui.click()
    time.sleep(5)
    randomemail = create_email()
    newemail = str(randomemail) + "@gmail.com"
    print("User email: ", newemail)
    pyautogui.typewrite(newemail)
    pyautogui.moveTo(EMAIL_BUTTON)
    pyautogui.click()
    time.sleep(8)
    return newemail


def downloadcaptcha():

    print("clicking captcha")
    pyautogui.moveTo(CAPTCHA_COORDS)
    pyautogui.click()
    time.sleep(10)

    # go to audio button
    print("Didnt auto pass..going for audio challenge")
    pyautogui.moveTo(AUDIO_COORDS)
    current_cords = cords()
    print(current_cords)
    pyautogui.click()
    time.sleep(2)

    #left click download
    pyautogui.moveTo(DOWNLOAD_COORDS)
    pyautogui.rightClick()
    time.sleep(3)

    # move to save link as..when you right click
    pyautogui.moveTo(OK_RIGHTCLICK_BUTTON_COORDS)
    pyautogui.click()
    time.sleep(3)

    # just press enter when the new popup opens
    pyautogui.press("enter")

    # CLOSE the new tab
    pyautogui.moveTo(CLOSE_TAB_BUTTON_COORDS)
    pyautogui.click()
    time.sleep(3)
    return 2


def removeoldfile():
    # These files may be left over from previous runs,
    # and should be removed just in case.
    print("Removing old files...")
    try:
        os.system('rm ' + download_location + 'audio.wav')
    except:
        pass
    try:
        os.system('rm ' + download_location + 'audio.mp3')
    except:
        pass
    try:
        os.system('rm ' + pycharm_location + 'audio.mp3')
    except:
        pass


def convertfile():
    print("Converting Captcha...")
    # it downloaded to weird location
    os.rename("/home/bot/.PyCharm2016.1/config/jdbc-drivers/audio.mp3", "/home/bot/Downloads/audio.mp3")
    # after it downloads to folder..convert it for google to a .wav
    os.system("ffmpeg -i " + download_location + "audio.mp3 " + download_location + "audio.wav")

    with sr.AudioFile(download_location + 'audio.wav') as source:
        audio = r.record(source)

    print("Submitting To Speech to Text:")
    determined = google(audio)
    # Instead of google, you can use ibm or bing here
    print("Text from google says ..:", determined)

    return str(determined)


def runcap():
    try:
        downloadresult = downloadcaptcha()

        # if it just let us in
        if downloadresult == 1:
            print("downloadresult is 1")
            # create username pass, get api

            result = checkcaptcha()

            return result

        # if it wanted to do captcha
        elif downloadresult == 2:

            # Convert the file to a format our APIs will understand
            findthetext = convertfile()

            print("Inputting Answer")
            # Input the captcha
            pyautogui.moveTo(FINAL_COORDS)
            pyautogui.click()
            time.sleep(.5)
            pyautogui.typewrite(findthetext, interval=.15)
            time.sleep(.5)
            pyautogui.moveTo(VERIFY_COORDS)
            pyautogui.click()

            print("Verifying Answer")
            time.sleep(2)

            # Check that the captcha is completed
            result = checkcaptcha()

            return result
        else:
            result = 3
            print("found out im a bot ..beep beep")
            return result

    except Exception as e:
        print(str(e))
        result = 4
        print("found out im a bot ..beep beep")
        return result



def confirmuser():
    pyautogui.moveTo(NEXT_BUTTON)
    pyautogui.click()
    time.sleep(4)

    # do it one more time to commit
    pyautogui.moveTo(NEXT_BUTTON)
    pyautogui.click()
    time.sleep(4)


def closebrowser():
    # close out finally
    pyautogui.moveTo(CLOSE_LOCATION)
    pyautogui.click()


def main():
    # remove old file
    removeoldfile()

    # go to website get an email
    useremail = gettowebsite()

    # get a username and password
    theuser, thepassword = get_a_user()

    # beat the captcha get the download file
    runcap()
    #
    confirmuser()
    closebrowser()
    addtodatabase(username=theuser,
              password=thepassword,
              appname="",
              client_id="",
              client_secret="",
              user_agent="",
              email=useremail,
              )








