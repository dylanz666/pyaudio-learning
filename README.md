# pyaudio-learning

### Preparation:
* Install portaudio
```
brew install portaudio
```

* Install PyAudio
```
pip3 install PyAudio
```

### Use below commands to do testing:

#####1. Play audio file；
```
python3 main.py - play --source_file=test.wav --chunk=1024
```
#####2. Detect audio only；
```
python3 main.py - detect_audio --channels=1 --rate=44100 --chunk=1024 --audio_min_rms=500 -max_low_audio_flag=100
```
#####3. Detect audio and then record to file in the end；
```
python3 main.py - detect_audio --channels=1 --rate=44100 --chunk=1024 --audio_min_rms=500 -max_low_audio_flag=100 - record --recording_file=recording.wav
```
#####4. Play audio and detect audio at the same time and record to file in the end；
```
python3 main.py - play_and_detect --source_file=test.wav --channels=1 --rate=44100 --chunk=1024 --audio_min_rms=500 -max_low_audio_flag=100 --recording=True --recording_file=recording.wav
```

### Others
Below files are only for demo usage.
* player.py
* playerCallbackVersion.py
* recordAndPlayImmediately.py
* recordAndPlayImmediatelyCallbackVersion.py
* recorder.py