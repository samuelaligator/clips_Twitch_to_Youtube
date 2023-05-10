import time
from GetElementsFromTwitch import GetElementsFromTwitch
from Database import Database
from MountVideo import MountVideo
from youtubeAPI import YoutubeAPI
from Thumbnail import Thumbnail
from datetime import datetime
import urllib


class App:
    def __init__(self):
        self.scraping = GetElementsFromTwitch()
        self.database = Database()
        self.montage = MountVideo()
        self.streamer_name = ""

        while True:
            self.download = self.database.select_data("download", "StreamersName", "ORDER BY download LIMIT 1")

            if len(self.download) == 0 or self.download[0][0] == 1:
                self.fill_StreamersName()
            else:
                self.streamer_name = self.database.select_data("streamer", "StreamersName", "ORDER BY download LIMIT 1")[0][0]
                id = self.database.select_data("id", "StreamersName", "ORDER BY download LIMIT 1")[0][0]
                self.fill_Clips()
                self.download_clips()
                self.mount_video()
                self.create_thumbnail()
                hour = int(datetime.now().strftime('%H'))
                while not hour == 7 or hour == 17:
                    time.sleep(600)
                    hour = int(datetime.now().strftime('%H'))
                self.upload_video()
                self.database.update("Streamers_name", "download", "id", 1, id)

    def fill_StreamersName(self):
        self.database.delete_table("StreamersName")
        self.database.create_table("StreamersName")
        self.database.add_column("StreamersName", "streamer", "TEXT")
        incr = 0
        self.database.create_table("StreamersName")
        streamers_name = self.scraping.get_streamers()
        for i in streamers_name:
            if not incr % 2 == 0:
                self.database.fill_StreamersName(i.text)
            incr += 1
        self.database.add_column("StreamersName", "download", "INTEGER")

    def fill_Clips(self):
        page_link = f"https://twitch.tv/{self.streamer_name}"
        self.database.delete_table("Clips")
        self.database.create_table("Clips")

        # adding columns into Clips
        column = {0: ["title", "TEXT"], 1: ["views", "INTEGER"], 2: ["category", "TEXT"], 3: ["streamer", "TEXT"],
                  4: ["author", "TEXT"], 5: ["link", "TEXT"]}
        for i in range(6):
            self.database.add_column("Clips", column[i][0], column[i][1])

        # scrape clips information from twitch
        clips_informations = self.scraping.get_information_from_clips(page_link, self.streamer_name)
        self.database.fill_Clips(clips_informations)
        self.scraping.initialize_clip_var()
        self.len_clips = self.database.table_length("Clips")

    def download_clips(self):
        # adding columns into Clips
        column = {0: ["download_link", "TEXT"], 1: ["download", "INTEGER"], 2: ["ranking", "INTEGER"]}
        for i in range(3):
            self.database.add_column("Clips", column[i][0], column[i][1])

        # adding a ranking by the number of views
        select_id = self.database.select_data("id", "Clips", "ORDER BY views DESC")
        for i in range(self.len_clips):
            self.database.update("Clips", "ranking", "id", i, select_id[i][0])

        # getting clip download link and populate database (Clips)
        for i in range(self.len_clips):
            link = self.database.select_data("link", "Clips", "ORDER BY download_link LIMIT 1")[0][0]
            download_link = self.scraping.get_video_download_link(self.len_clips, link)
            self.database.update("Clips", "download_link", "link", download_link, link)

        # download_the_clips
        for i in range(self.len_clips):
            download_link = self.database.select_data("download_link", "Clips", "ORDER BY download LIMIT 1")[0][0]
            if download_link:
                ranking = self.database.select_data("ranking", "Clips", "ORDER BY download LIMIT 1")[0][0]
                print(f"downloading the {ranking} clip")
                urllib.request.urlretrieve(download_link, f"clip/{ranking}.mp4")
                self.database.update("Clips", "download", "ranking", 1, ranking)

    def mount_video(self):
        final = []
        for i in range(self.len_clips):
            category = self.database.select_data("category", "Clips", f"WHERE ranking = {i}")[0][0]
            final = self.montage.concatenate_clips(i, category)
        self.montage.write_videofile(final, 30)

    def create_thumbnail(self):
        self.montage.save_a_frame()
        date = self.date()
        thumbnail = Thumbnail()
        thumbnail.create_thumbnail(self.streamer_name, date)

    def upload_video(self):
        youtube_api = YoutubeAPI()
        self.database = Database()
        streamer = self.database.select_data("streamer", "Clips", "ORDER BY ranking")
        category = self.database.select_data("category", "Clips", "ORDER BY ranking")
        author = self.database.select_data("author", "Clips", "ORDER BY ranking")
        link = self.database.select_data("link", "Clips", "ORDER BY ranking")
        title = self.database.select_data("title", "Clips", "ORDER BY ranking")
        description = ""

        # create description
        for i in range(len(streamer)):
            description = description + f"{i + 1}) Clip de {streamer[i][0]} sur {category[i][0]} par {author[i][0]} :\n {link[i][0]} \n titre du clip : {title[i][0]} \n\n"

        # create the tag_list with the streamers and categories names
        tag_list = []
        for i in range(len(streamer)):
            if not streamer[i][0] in tag_list:
                tag_list.append(streamer[i][0])
            if not category[i][0] in tag_list:
                tag_list.append(category[i][0])

        date = self.date()

        # upload the video
        youtube_api.upload_to_youtube("Best Of du TWITCH français #1",
                                      f"Petit Best Of des meilleurs clips Twitch de {streamer[0]} du mois de {date} \n\n {description}",
                                      tag_list, "public", "./thumbnail/thumbnail.png")

    def date(self):
        # current month and year
        now = datetime.now()
        month_converter = {1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
                           7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre",
                           12: "décembre"}
        month = month_converter[now.month]
        year = now.year
        return f"{month} {year}"

App()

