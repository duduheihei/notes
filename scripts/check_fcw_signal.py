from pathlib import Path

if __name__ == '__main__':
    rootDir = Path(r'F:\database\BYD\BYD测试素材')
    for dirName in rootDir.iterdir():
        if not dirName.is_dir():
            continue
        resultFiles = list(dirName.glob('{}.txt'.format(dirName.stem)))
        if len(resultFiles) <=0:
            print('cannot find result file in ',dirName)
            continue
        
        with resultFiles[0].open(r'r') as f:
            lines = f.readlines()[1:]
        print(dirName)
        for line in lines:
            if 'FCW:1' in line:
                print(line)
