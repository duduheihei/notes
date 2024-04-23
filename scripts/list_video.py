from pathlib import Path


if __name__ == '__main__':
    rootDir = Path(r'F:\database\BYD\BYD测试素材')
    filename = rootDir/'fileName.txt'
    videoname = rootDir/'videoName.txt'
    with filename.open('w') as ffile:
        with videoname.open('w') as fvideo:
            for dirName in rootDir.iterdir():
                if not dirName.is_dir():
                    continue
                videos = list(dirName.glob('{}.h264'.format(dirName.stem)))
                if len(videos) <=0:
                    print('cannot find video in ',dirName)
                    assert False
                ffile.write('{}\n'.format(dirName.stem))
                fvideo.write('{}\n'.format(dirName.stem))
