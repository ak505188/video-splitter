import urllib.request
import zipfile
import shutil
import os
import fnmatch

url = "http://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20170418-6108805-win64-static.zip"

def download(url, filename):
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url, filename)

def unzip(filename, path):
    archive = zipfile.ZipFile(filename)
    archive.extractall(path)

# download(url, "./tmp/ffmpeg.zip")
# unzip("./tmp/ffmpeg.zip", "./")

dirname = fnmatch.filter(os.listdir('.'), 'ffmpeg*win64*')[0]
os.rename(dirname, 'ffmpeg')
