import xml.etree.ElementTree as ET
import os, sys
from pdf2image import convert_from_path
from moviepy.editor import *
import numpy as np

name = sys.argv[1].split('.')[0]

xml_files = os.listdir('xmlfiles')
slide_images = convert_from_path(name + '.pdf')

audio_files = []

for xml_file in xml_files:
    tree = ET.parse(os.path.join('xmlfiles', xml_file))
    root = tree.getroot()
    for child in root:
        mediafile = child.attrib['Target']
        if mediafile.endswith('.wav'):
            slide_number = int(xml_file.split('.')[0][5:])
            audio_files.append((slide_number, mediafile[3:]))

slide_clips = []

for img in slide_images:
    size = np.array(img.size)*0.5
    size = size.round()
    slide_clips.append([img.resize((int(size[0]), int(size[1]))), None])

for audio_file in audio_files:
    slide_number = audio_file[0]
    try:
        slide_clips[slide_number - 1][1] = AudioFileClip(audio_file[1])
    except OSError:
        slide_clips[slide_number -1][1] = None

final_clips = []
for clip in slide_clips:
    if clip[1]:
        ic = ImageClip(np.array(clip[0])).set_duration(clip[1].duration + 1)
        ic = ic.set_audio(clip[1])
    else:
        ic = ImageClip(np.array(clip[0])).set_duration(3)
    final_clips.append(ic)

video = concatenate(final_clips, method="compose")
video.write_videofile(name + '.mp4', fps=24)

