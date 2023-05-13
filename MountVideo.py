from moviepy.editor import *


class MountVideo:
    def __init__(self):
        self.clip = []

    def concatenate_clips(self, i, streamer):
        print(f"concatenating clips in a variable and adding a caption ({i + 1} - {streamer})")
        self.clip.append(VideoFileClip(f"./clip/{i}.mp4").fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5))
        txt_clip = TextClip(f"{i + 1} - {streamer}", font="Source-Sans-3-Black", fontsize=80, color='white',
                            stroke_color="black", stroke_width=3.5)
        txt_clip = txt_clip.set_position('bottom').set_duration(5)
        self.clip[i] = CompositeVideoClip([self.clip[i], txt_clip])
        return concatenate_videoclips(self.clip)

    def write_videofile(self, final, fps):
        print("writing video file")
        final.write_videofile("./video/video.mp4", fps=fps)

    def save_a_frame(self):
        print("saving a frame from the thumbnail")
        clip = VideoFileClip("./clip/1.mp4")
        clip.save_frame("./image/background.png", t=2)
