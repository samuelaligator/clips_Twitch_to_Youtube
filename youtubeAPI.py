from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

class YoutubeAPI:
    def __init__(self):
        # loggin into the channel
        self.channel = Channel()
        self.channel.login("client_secrets.json", "credentials.storage")
        # setting up the video that is going to be uploaded
        self.video = LocalVideo(file_path="video/video.mp4")

    def upload_to_youtube(self, title, description, tags_list, privacy, thumbnail_path):
        print("uploading the video to youtube")
        # setting snippet
        self.video.set_title(title)
        self.video.set_description(description)
        self.video.set_tags(tags_list)
        self.video.set_category("gaming")
        self.video.set_default_language("fr-FR")

        # setting status
        self.video.set_embeddable(True)
        self.video.set_privacy_status(privacy)
        self.video.set_public_stats_viewable(True)

        # setting thumbnail
        self.video.set_thumbnail_path(thumbnail_path)

        # uploading video and printing the results
        self.video = self.channel.upload_video(self.video)
        print(self.video.id)
        print(self.video)

        # liking video
        self.video.like()