from pydub import AudioSegment
import random

def wav_split(filename, num_samples, method):
    audio = AudioSegment.from_wav(filename)
    total_ms = len(audio)

    if num_samples == 1:
        audio.export('output/audio/splitted0.wav', format="wav")

    if method == 'sampling':    
        for i in range(num_samples):
            start = random.randint(2500, total_ms - 32500) # exclude first 5 seconds and last 5 seconds
            end = start + 30000 # take 30 seconds
            split_audio = audio[start:end]
            split_audio.export('output/audio/splitted{}.wav'.format(i), format="wav")

    elif method == 'BME':
        split_audio = audio[0:30000]
        split_audio.export('output/audio/splitted0.wav', format="wav")
        split_audio2 = audio[(total_ms / 2) - 15000:(total_ms / 2) + 15000]
        split_audio2.export('output/audio/splitted1.wav', format="wav")
        split_audio3 = audio[total_ms - 30000, total_ms-1]
        split_audio3.export('output/audio/splitted3.wav', format="wav")

    elif method == 'quart':
        split_audio = audio[(total_ms / 4) - 15000:(total_ms / 4) + 15000]
        split_audio.export('output/audio/splitted0.wav', format="wav")
        split_audio2 = audio[(total_ms / 2) - 15000:(total_ms / 2) + 15000]
        split_audio2.export('output/audio/splitted1.wav', format="wav")
        split_audio3 = audio[(total_ms * 3 / 4) - 15000:(total_ms * 3 / 4) + 15000]
        split_audio3.export('output/audio/splitted3.wav', format="wav")

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

