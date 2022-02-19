from pydub import AudioSegment
import random

def wav_split(filename):
    audio = AudioSegment.from_wav(filename)
    if audio.duration_seconds < 29:
        pass
    elif audio.duration_seconds <= 60:
        split_audio = audio
        split_audio.export('output/audio/splitted{}.wav', format="wav")
    
    else:
        total_ms = len(audio)
        num_seg = int(total_ms / 30000) 
        if num_seg > 3:     ##temp fix
            num_seg = 3

        for i in range(num_seg):
            start = i * 30000 #random.randint(5000, total_ms - 35000) # exclude first 5 seconds and last 5 seconds
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

