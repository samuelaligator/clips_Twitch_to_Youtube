from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class GetElementsFromTwitch:
    CHROME_PATH = '/usr/bin/chromium'
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"

    def __init__(self):
        # open a chromium window not visible
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--lang=fr")
        chrome_options.add_argument("--window-size=%s" % GetElementsFromTwitch.WINDOW_SIZE)
        chrome_options.binary_location = GetElementsFromTwitch.CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=GetElementsFromTwitch.CHROMEDRIVER_PATH,
                                       chrome_options=chrome_options)
        self.initialize_clip_var()

    def initialize_clip_var(self):
        self.clip_view = []
        self.clip_name = []
        self.clip_category = []
        self.clip_streamer = []
        self.clip_author = []
        self.clip_link = []
        self.clip_information = []

    def get_streamers(self):
        print("getting streamers")
        self.driver.get("https://twitchtracker.com/channels/ranking/french/personality")
        self.driver.implicitly_wait(5)
        return self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr td a')

    def get_information_from_clips(self, page_link, streamer_name):
        print(f'getting clip info from "{streamer_name}"')
        self.driver.get(page_link + "/clips?filter=clips&range=30d")
        self.driver.implicitly_wait(5)
        self.get_clip_views()
        self.get_clip_name()
        self.get_clip_category()
        self.get_streamer_and_author_name()
        self.get_clip_link()
        self.create_list_of_clip_information()
        return self.clip_information

    def get_clip_views(self):
        print("getting clip views")
        list_clip_view = self.driver.find_elements(By.CSS_SELECTOR, '.gUtzBI .tw-media-card-stat')
        print(list_clip_view)
        for i in list_clip_view:
            clip_view = i.text
            if "k" in clip_view:
                clip_view = clip_view.replace(",", "")
                clip_view = [int(views) for views in clip_view.split() if views.isdigit()]
                if len(str(clip_view[0])) == 2:
                    clip_view = clip_view[0] * 100
                elif len(str(clip_view[0])) == 3:
                    clip_view = clip_view[0] * 10
                else:
                    clip_view = clip_view[0] * 1000
            else:
                clip_view = [int(view) for view in clip_view.split() if view.isdigit()]
                clip_view = clip_view[0]
            self.clip_view.append(clip_view)

    def get_clip_name(self):
        print("getting name of clips")
        clip_name = self.driver.find_elements(By.CLASS_NAME, 'dlDlel')
        for i in clip_name:
            self.clip_name.append(i.get_attribute("title"))

    def get_clip_category(self):
        print("getting category name")
        clip_category = self.driver.find_elements(By.CSS_SELECTOR, '.gxJZAm img')
        for i in clip_category:
            self.clip_category.append(i.get_attribute("alt"))

    def get_streamer_and_author_name(self):
        print("getting names of streamers and authors of clips")
        streamer_and_clip_author = self.driver.find_elements(By.CLASS_NAME, 'jiepBC')
        incr = 0
        for i in streamer_and_clip_author:
            if incr % 2 == 0:
                self.clip_streamer.append(i.text)
            else:
                self.clip_author.append(i.text.replace('Clip créé par ', ""))
            incr += 1

    def get_clip_link(self):
        print("getting the clip link")
        clip_link = self.driver.find_elements(By.CLASS_NAME, 'jYyMcQ')
        for i in clip_link:
            self.clip_link.append(i.get_attribute("href"))

    def create_list_of_clip_information(self):
        print("creating a list of clip information")
        for i in range(len(self.clip_view)):
            self.clip_information.append(
                [self.clip_name[i], self.clip_view[i], self.clip_category[i], self.clip_streamer[i],
                 self.clip_author[i],
                 self.clip_link[i]])

    def get_video_download_link(self, table_length, link):
        print("getting clip download link")
        for i in range(table_length):
            self.driver.get(link)
            self.driver.implicitly_wait(2)
            return self.driver.find_element(By.CSS_SELECTOR, '.video-ref video').get_attribute("src")

    """
    to get the information of the clips to make a general classification with all the streamers :
    
    def get_categories(self):
        print("getting main live category links")
        self.driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")
        self.driver.implicitly_wait(5)
        time.sleep(20)
        category_link = self.driver.find_elements(By.CLASS_NAME, 'game-card__link')
        for i in category_link:
            self.category_link.append(i.get_attribute("href"))
        category_name = self.driver.find_elements(By.CLASS_NAME, 'eYbmNi')
        for i in category_name:
            self.category_name.append(i.get_attribute("title"))

    def switch_to_french(self):
        print("changing the page in french")
        time.sleep(1)
        button = self.driver.find_element(By.CLASS_NAME, 'ScCoreButton-sc-1jjluui-0')
        button.click()
        time.sleep(1)
        language = self.driver.find_element(By.CLASS_NAME, 'tw-checkbox__label')
        language.click()
        time.sleep(0.5)
    """
