import os
import time
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def login(username: str, password: str):
    """
    Logs in to LinkedIn on the Selenium browser using the user's specified account
    :param str username: Contains the user's LinkedIn email-id
    :param str password: Contains the user's LinkedIn password
    :return: None
    """

    # Opens Instagram's login page on your Selenium browser
    browser.get("https://www.instagram.com/")
    time.sleep(2)

    # Code to automatically enter your credentials into the corresponding fields
    element_id = browser.find_element(by=By.XPATH, value="//input[@name='username']")
    element_id.send_keys(username)

    element_id = browser.find_element(by=By.XPATH, value="//input[@name='password']")
    element_id.send_keys(password)

    element_id.submit()

    time.sleep(8)
    print('Logged in')


def write_data(post_data: list):
    """
    Stores the details of an Instagram post into the corresponding profile's database
    :param list post_data: Contains the post's upload date, likes/views, & description
    :return: None
    """

    with open('Profiles/data.csv', 'a', newline='', encoding='utf-8') as file:
        # Code to append a post's details into the CSV file.
        writer_object = writer(file)
        writer_object.writerow(post_data)

        # Close the file object
        file.close()
        print('Post updated')


def check_database(user_id: str):
    """
    X
    :param str user_id: X
    :return: None
    """

    file_name = user_id + '.csv'
    path = 'Profiles/' + file_name
    is_exist = os.path.exists(path)
    print(is_exist)

    if not is_exist:
        header = ['Post Link', 'Post Date', 'Post Hits', 'Post Desc']
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer_object = writer(file)
            writer_object.writerow(header)
            file.close()

            print('Profile Created for ' + user_id)


def scrape_post(post_link: str):
    """
    Gets the post's upload date, description, & likes/views.
    :param str post_link: URL of the specific Instagram post
    :return: None
    """

    print(post_link)
    browser.get(post_link)

    # Code to get the relevant HTML elements which contain the data we want to scrape
    containers = browser.find_elements(by=By.CLASS_NAME, value='_7UhW9.xLCgt.MMzan.KV-D4')
    video_views = browser.find_elements(by=By.CLASS_NAME, value='_7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv.T0kll')

    # The two variables below hold the post's date of upload & the clue to whether the post is an image or clip.
    video_checker = video_views[-1].text
    date = containers[-1].text
    print(date)

    if video_checker[-5:] == 'views':
        # It's a video/clip

        hits = video_views[-1].text
        print(hits)

        desc = containers[0].text
        print(containers[0].text)

        # Calls the write_data function to store the post's details into the corresponding profile's CSV file
        write_data([post_link, date, hits, desc])

    else:
        # It's an image/GIF

        hits = containers[0].text
        print(hits)

        desc = containers[1].text
        print(desc)

        write_data([post_link, date, hits, desc])


def open_page(ig_link: str):
    """
    Opens the requested Instagram profile on Selenium & gets the URL of each post
    :param str ig_link: The profile's URL in string format
    :return: None
    """

    print(ig_link)
    browser.get(ig_link)

    post_links = []

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scrolling loop
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        var = browser.find_elements(by=By.CLASS_NAME, value='v1Nh3.kIKUG._bz0w')

        # Code to store each post link in the list post_links
        for post in var:
            link_tag = post.find_element(by=By.XPATH, value='.//a')
            href = link_tag.get_attribute('href')
            if href[25:28] == '/p/':
                if href not in post_links:
                    post_links.append(href)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(post_links)

    # Call scrape_post function to get the details for each post discovered on this profile
    for link in post_links:
        scrape_post(link)


def main():

    # Code to store your credentials for login
    username = 'jafari.ade09@hotmail.com'
    password = input("Enter your password:")
    login(username, password)

    # Calls the open_page function to  begin collecting data about the specified profile's posts
    link = 'https://www.instagram.com/zangbox.in/'
    open_page(link)

    # Code to keep the Selenium browser open until the user wishes to quit
    response = input('Quit?')
    if response in ['y', 'yes', 'Y', 'Yes']:
        browser.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    s = Service('chromedriver.exe')
    browser = webdriver.Chrome(service=s)

    main()


# Things to improve:

# 1. Put credentials in a text file to read instead of in the code
# 2. Write the docstring for each function
# 3. Improve GUI so that user does not have to type in console
# 4. Catch login error (incorrect credentials)
# 5. Catch all errors in the process & give the option to restart instead of exiting
# 6. Check whether CSV exists for IG profile. If not, create one & append to it. If yes, update changes.
# 7. Put data in a separate sub-folder
# 8. Write comments for each code block
