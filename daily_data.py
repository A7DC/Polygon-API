import os

def get_gappers():
    gappers = []
    years = [name for name in os.listdir('output/') if not name.startswith('.')]
    
    for year in years:
        # year = [name for name in os.listdir('output/') if not name.startswith('.')]
        foldernames = [i for i in os.listdir('output/{}'.format(year))] # save these as global vars
        # for folder in foldernames:
            # date = [i for i in os.listdir('output/{}/{}/{}'.format(year, folder, year))] # save these as global vars
        folder_CW = [name for name in foldernames if not name.startswith('.')]

        for i in range(len(folder_CW)):
            u = os.listdir('output/{}/{}/DONE'.format(year, folder_CW[i]))
            print(u)


get_gappers()