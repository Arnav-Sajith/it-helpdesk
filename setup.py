import os
import sys
import shutil
import it_helpdesk

def main():
    helpdesk_file_path = os.path.join(os.path.expanduser('~'), 'it-helpdesk')
    installed_dir = os.path.dirname(it_helpdesk.__file__)
    
    try:
        os.mkdir(helpdesk_file_path)
    except OSError:
        alternative_path = os.path.join((os.getcwd()), 'it-helpdesk')
        print(helpdesk_file_path, "already exists or could not be created. The files have been placed instead at ",alternative_path)

    try:
        shutil.copytree(installed_dir, helpdesk_file_path, dirs_exist_ok=True)
    except OSError:
        shutil.copy(installed_dir, helpdesk_file_path)


    




if __name__ == '__main__':
    main()
