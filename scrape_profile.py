import time
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def login():
    """
    Returns a template comprising the contents of a file
    :param filename: File containing the email message
    :return: Template object
    """

    user = 'jafari.ade09@hotmail.com'
    pw = input("Enter your password:")

    browser.get("https://www.instagram.com/")

    time.sleep(2)

    element_ID = browser.find_element(by=By.XPATH, value="//input[@name='username']")
    element_ID.send_keys(user)

    element_ID = browser.find_element(by=By.XPATH, value="//input[@name='password']")
    element_ID.send_keys(pw)

    element_ID.submit()

    time.sleep(8)
    print('Logged in')


def write_data(post_data):
    """
    Returns a template comprising the contents of a file
    :param post_data: File containing the email message
    :return: Template object
    """

    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer_object = writer(file)
        writer_object.writerow(post_data)
        # Close the file object
        file.close()
        print('Post updated')


def scrape_post(post_link):
    """
    Returns a template comprising the contents of a file
    :param filename: File containing the email message
    :return: Template object
    """

    print(post_link)
    browser.get(post_link)

    div_class_name = '_7UhW9.xLCgt.qyrsm.KV-D4'

    # rebuilder = likes.split(',')
    # number_str = ''
    # for term in rebuilder:
    #     number_str = number_str + term
    # print(number_str)

    containers = browser.find_elements(by=By.CLASS_NAME, value='_7UhW9.xLCgt.MMzan.KV-D4')

    video_views = browser.find_elements(by=By.CLASS_NAME, value='_7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv.T0kll')

    video_checker = video_views[-1].text

    date = containers[-1].text
    print(date)

    if video_checker[-5:] == 'views':
        # It's a video/clip

        hits = video_views[-1].text
        print(hits)

        desc = containers[0].text
        print(containers[0].text)

        write_data([post_link, date, hits, desc])

    else:
        # It's an image/GIF

        hits = containers[0].text
        print(hits)

        desc = containers[1].text
        print(desc)

        write_data([post_link, date, hits, desc])


def open_page(ig_link):
    """
    Returns a template comprising the contents of a file
    :param filename: File containing the email message
    :return: Template object
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

    for link in post_links:
        scrape_post(link)


def main():
    """
    Returns a template comprising the contents of a file
    :param filename: File containing the email message
    :return: Template object
    """

    login()

    link = 'https://www.instagram.com/zangbox.in/'
    open_page(link)

    response = input('Quit?')
    if response in ['y', 'yes', 'Y', 'Yes']:
        browser.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    s = Service('chromedriver.exe')
    browser = webdriver.Chrome(service=s)

    main()
