from yt_downloader import YTDownloader

print('''
Please, select a option...
[1] Download and cut a Youtube Video
[2] Cut a Video of ../videos/
[3] Quit
''')

answ = input('Choice: ')
if answ == '1' or answ == '2':
    quality = input('Quality (low, medium, high): ')
    if answ == '1':
        link = input('Respective Link to Download: ')
        yt = YTDownloader(url=link, resolution=quality)
        yt.download()
        yt.get_lenght()
        print('') 
        print('Now Please, put the Informations to cut the Video')
        print('Examples:')
        print('-------------------------------------------------')
        print('from: start\nto: 5m')
        print('-------------------------------------------------')
        print('from: 6m10s\nto: 7m3s')
        print('-------------------------------------------------')
        print('from: 5m2s\nto: end')
        print('-------------------------------------------------')
        print('')
        _from = input('from: ')
        _to = input('to: ')

    elif answ == '2':
        pass
    else:
        pass
