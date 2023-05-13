from PIL import Image, ImageFilter, ImageDraw, ImageFont


class Thumbnail:
    def __init__(self):
        self.twitch_logo = Image.open(r"./image/twitch.png")
        self.twitch_size = self.twitch_logo.size
        self.font = ImageFont.truetype("SourceSans3-Black.otf", size=200)
        self.font2 = ImageFont.truetype("SourceSans3-Black.otf", size=100)

    def create_thumbnail(self, streamer_name, number):
        print("creating the thumbnail")
        background = Image.open(r"./image/background.png")
        background = background.filter((ImageFilter.GaussianBlur(1.8)))
        bg_size = background.size
        text = ImageDraw.Draw(background)
        font_size = self.font.getbbox(streamer_name)
        background.paste(self.twitch_logo, (int(bg_size[0] / 2) - int(self.twitch_size[0] / 2),
                                            int(bg_size[1] / 2) - int(self.twitch_size[1] / 2) + int(bg_size[1] / 7)),
                         mask=self.twitch_logo)
        text.text((int(bg_size[0] / 2) - int(font_size[2] / 2),
                   int(bg_size[1] / 2) - int(font_size[3] / 2) - int(bg_size[1] / 4)), streamer_name, font=self.font,
                  stroke_fill="black", stroke_width=12)
        text.text((20, -10), number, font=self.font2, stroke_fill="black", stroke_width=5)
        background.save("thumbnail/thumbnail.png")


Thumbnail()
