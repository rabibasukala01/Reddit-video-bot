"""
TODO
READ THIS https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content/
""" 

from fileinput import filename
import time
from playwright.sync_api import sync_playwright
import json,os,random


def upload_file(page,filename):
    print("Posting video to tiktok, might take some time")
    page.locator('input[type=file]').set_input_files(filename)
    time.sleep(5)

    # in tiktok , while uploading the class is  class="jsx-1979214919 info-progress info" changes to class="jsx-1979214919 info-progress success" after upload
    # so we can check if the class is success or not, to know if the upload is done
    # Wait for the progress element to change from "info" to "success"
    page.wait_for_selector(
        '.jsx-1979214919.info-progress.success', 
        state='visible',  # Wait for the element to become visible
        timeout=180000  # Timeout after x seconds (adjust as necessary) upload maybe slow
    )
    time.sleep(1)

    # write the description
    #TODO: add description

    # Click the button using its data-e2e attribute to upload the video
    time.sleep(10)
    page.locator('[data-e2e="post_video_button"]').click()


def is_logged_in():
    return True


def upload_to_tiktok(filename):


    """
    use debugger to store cookies if you don't want to do that mannually
    how: 
    - run the script as it  by setting has_cookies=False
    - hold on homepage and start login mannually and contiune the script after logged in
    
    """
    # ----IMPORTANT---- #
    has_cookies=True  # set to false for first times runs and see comments above

    # make cookies.json file
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    COOKIES_PATH = os.path.join(SCRIPT_DIR, 'cookies.json')


    with sync_playwright() as p:
        # Launch the browser
        browser = p.firefox.launch(headless=False)

        context = browser.new_context()

        if has_cookies:
            # Load cookies from the file
            with open(COOKIES_PATH, 'r') as f:
                cookies = json.load(f)
            # Add cookies to the context
            context.add_cookies(cookies)
        
        # Open a new page
        page = context.new_page()
        time.sleep(2)
        # Navigate to the website with cookies
        page.goto('https://www.tiktok.com/tiktokstudio/upload?from=upload')
        time.sleep(5)
        upload_file(page,filename)

        # Save the cookies to a file for next time use(hopefully get refresh tokens)
        if is_logged_in():
            with open(COOKIES_PATH, 'w') as f:
                json.dump(context.cookies(), f)

        # Close the browser
        browser.close()
# 1735966998
 

if __name__ == "__main__":
        
    filename = r".\results\jokes+dadjokes\If you start watching Avengers Endgame on New years eve at exactly 92930 at exactly midnight.mp4"
    upload_to_tiktok(filename)
