from pydub import AudioSegment
import random

def wav_split(filename, num_samples):
    audio = AudioSegment.from_wav(filename)
    total_ms = len(audio)

    for i in range(num_samples):
        start = random.randint(5000, total_ms - 35000) # exclude first 5 seconds and last 5 seconds
        end = start + 30000 # take 30 seconds
        split_audio = audio[start:end]
        split_audio.export('output/audio/splitted{}.wav'.format(i), format="wav")
        
#def to3_split(filename):
#    audio = AudioSegment.from_wav(filename)
#
#    splits = []
#    milis = 0
#    for i in range(10):
#        splits.append(audio[milis:milis+2999])
#        milis+=3000
#
#    #get actual file name from path
#    filetitle = filename.split('/')[2]
#
#    #export all 10 three-second clips
#    for i in range(10):
#        splits[i].export('output/audio/{0}{1}.wav'.format(filetitle, i), format="wav")
#
#def to3_direct(directory):

