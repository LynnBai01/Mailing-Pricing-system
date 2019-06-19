# -*-coding:utf-8-*-

import data_manager as dm
import user
import admin

def main():
    dm.importData()
    select = ''
    while True:
        select = getMenuInput()
        if(select == '1'):
            user.main()
        elif(select == '2'):
            admin.main()
        elif(select == '3'):
            break
        else:
            print('Input error, try input again')

# Print the main menu:
def getMenuInput():
    return input('''
    Please select the following：
    1. The Customer System
    2. The Admin System
    3. Quit
    ''')

if __name__ == '__main__':
    main()
