cd /home/veleslavia/veleslavia/AMC/data/
find . -iname "*.mp3" -exec lame '--decode' '{}' ';'
find . -iname '*.wav' -exec sox '{}' '{}.wav' trim 0 30.0 ';'
find . -iname '*.mp3.wav' -exec rm '{}' ';'
find . -iname '*.mp3' -exec rm '{}' ';'