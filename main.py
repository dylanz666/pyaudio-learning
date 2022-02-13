import audioop
from multiprocessing import Process

import fire
import pyaudio
import wave

stream_format = pyaudio.paInt16
pyaudio_instance = pyaudio.PyAudio()
sample_width = pyaudio_instance.get_sample_size(stream_format)
global audio_frames


class Detector(object):
    def __init__(self):
        self.source_file = ""
        self.channels = None
        self.rate = None
        self.chunk = None
        self.audio_min_rms = None
        self.max_low_audio_flag = None
        self.recording = False
        self.recording_file = ""
        self.audio_frames = []

    def __str__(self):
        return ""

    def play(self, source_file="", chunk=None):
        source_file = source_file if not self.source_file else self.source_file
        chunk = chunk if not self.chunk else self.chunk

        f = wave.open(source_file, "rb")
        p = pyaudio.PyAudio()

        file_format = p.get_format_from_width(f.getsampwidth())
        stream = p.open(format=file_format, channels=f.getnchannels(), rate=f.getframerate(), output=True)

        data = f.readframes(chunk)

        while data != b"":
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        return self

    def detect_audio(self, channels=None, rate=None, chunk=None, audio_min_rms=None, max_low_audio_flag=None,
                     recording=False, recording_file=""):
        channels = channels if not self.channels else self.channels
        rate = rate if not self.rate else self.rate
        chunk = chunk if not self.chunk else self.chunk
        audio_min_rms = audio_min_rms if not self.audio_min_rms else self.audio_min_rms
        max_low_audio_flag = max_low_audio_flag if not self.max_low_audio_flag else self.max_low_audio_flag
        recording = recording if not self.recording else self.recording
        recording_file = recording_file if not self.recording_file else self.recording_file
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.recording = recording
        self.recording_file = recording_file

        print("* start detecting audio ~")
        self.channels = channels
        self.rate = rate

        stream = pyaudio_instance.open(format=stream_format,
                                       channels=channels,
                                       rate=rate,
                                       input=True,
                                       frames_per_buffer=chunk)
        low_audio_flag = 0
        detect_count = 0
        while True:
            detect_count += 1

            stream_data = stream.read(chunk)

            rms = audioop.rms(stream_data, 2)
            print(f"the {detect_count} time detecting：", rms)

            low_audio_flag = 0 if rms > audio_min_rms else low_audio_flag + 1

            # 100 为经验值，即连续 100 次采样都是小音量，则可以认为没有音频，根据实际情况设置
            if low_audio_flag > max_low_audio_flag:
                print("* no audio detected, stop detecting ~")
                break
            self.audio_frames.append(stream_data)
        stream.stop_stream()
        stream.close()
        pyaudio_instance.terminate()
        if recording:
            self.record()
        return self

    def record(self, recording_file=""):
        recording_file = recording_file if not self.recording_file else self.recording_file
        self.recording_file = recording_file

        wf = wave.open(recording_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()
        return self

    def play_and_detect(self, source_file, channels, rate, chunk, audio_min_rms, max_low_audio_flag, recording,
                        recording_file):
        self.source_file = source_file
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.recording = recording
        self.recording_file = recording_file

        play_process = Process(target=self.play)
        detect_process = Process(target=self.detect_audio)
        play_process.start()
        detect_process.start()

        play_process.join()
        detect_process.join()
        return self


if __name__ == '__main__':
    fire.Fire(Detector)
