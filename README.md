# musicforprogramming-download

download mp3 files from https://musicforprogramming.net/about

docker run --name musicforprogramming-download \
-v $(pwd)/music_for_programming:/data/music \
lostsquirrel/musicforprogramming-download