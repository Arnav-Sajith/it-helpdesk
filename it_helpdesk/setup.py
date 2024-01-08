import os
import shutil
import it_helpdesk
import yaml
from InquirerPy import prompt, inquirer

def main():
    try:
        package_dir = os.path.dirname(it_helpdesk.__file__)
        ansible_default_files = os.path.join(package_dir, 'ansible')
        question_1 = [
            {'type': 'list',
            'name': 'install',
            'wrap_lines': True,
            'message': 'Welcome to the setup installer for the autonomous it-helpdesk. This software is intended to be used in conjunction with the EMPT IT suite. This tool will set up the directories and configuration files for all of the ansible automation you will be working with. Select Continue to proceed, or Exit to exit this installer.',
            'choices': ['Continue', 'Exit'],
            'default': 'continue',
            'show_cursor': False,
            'qmark': '',
            'amark': ''
            }
        ]
        answer1 = prompt(questions=question_1)
        if answer1.get('install') == 'Exit':
            exit()
        while True:
            question_2 = [
                {'type': 'filepath',
                'name': 'install_dir',
                'default': os.path.join(os.getcwd(), ''),
                'message': f'Please specify the parent directory where the it-helpdesk folder should be stored:',
                "only_directories": True,
                'wrap_lines': True,
                'qmark': '',
                'amark': '',
                }
            ]
            print('')

            answer2 = prompt(questions=question_2)
            helpdesk_dir = os.path.join(answer2.get('install_dir'), 'it-helpdesk')
            helpdesk_ansible_dir = os.path.join(helpdesk_dir, 'ansible')

            if inquirer.select(message=f"The it-helpdesk will be installed to {helpdesk_dir}. This directory will be created if it does not already exist. Is this okay?", choices=['Yes', 'No'], mandatory=True, qmark='', amark='', wrap_lines=True, show_cursor=False).execute() == 'Yes':
                try:
                    os.makedirs(helpdesk_dir)
                    shutil.copytree(ansible_default_files, helpdesk_ansible_dir)
                    shutil.copyfile(os.path.join(package_dir,'mail_script.py'), os.path.join(helpdesk_dir,'mail_script.py'))
                    break

                except FileExistsError: 
                    if inquirer.select(message=f"This directory already contains an it-helpdesk installation. Would you like to overwrite it?", choices=['Yes', 'No'], mandatory=True, qmark='', amark='', wrap_lines=True, show_cursor=False).execute() == 'Yes':
                        os.makedirs(helpdesk_dir, exist_ok=True)
                        shutil.copytree(ansible_default_files, helpdesk_ansible_dir)
                        shutil.copyfile(os.path.join(package_dir,'mail_script.py'), os.path.join(helpdesk_dir,'mail_script.py'))
                        break
                    else:
                        continue

        question_3 = [
            {'type': 'input',
            'name': 'org_domain',
            'message': f'Please enter your organizations domain:',
            'validate': lambda answer: 'You must enter a domain for your organization.' \
                if len(answer) != 0 else False,
            'amark': '',
            'qmark': '',
            'wrap_lines': True,
            }
        ]
        print('')
        answer3 = prompt(questions=question_3)
        org_domain = answer3.get('org_domain')
        
        question_4 = [
            {'type': 'input',
            'name': 'mail_server',
            'message': f'Please specify the address of your organizations mail server: (leave blank for default: localhost)',
            'amark': '',
            'qmark': '',
            'wrap_lines': True,
            }
        ]
        print('')
        answer4 = prompt(questions=question_4)
        mail_server = 'localhost' if len(answer4.get('mail_server')) == 0 else answer4.get('mail_server')

        question_5 = [
            {'type': 'input',
            'name': 'helpdesk_email',
            'message': f'Please enter the email address for the it-helpdesk: (leave blank for default: it-helpdesk@{org_domain})',
            'qmark': '',
            'amark': '',
            'wrap_lines': True,
            }
        ]
        print('')
        answer5 = prompt(questions=question_5)
        helpdesk_email = f'it-helpdesk@{org_domain}' if len(answer5.get('helpdesk_email')) == 0 else answer5.get('helpdesk_email')

        question_6 = [
            {'type': 'password',
            'name': 'helpdesk_password',
            'message': f'Please enter the password for the it-helpdesks email address',
            'qmark': '',
            'amark': '',
            'wrap_lines': True,
            }
        ]
        print('')
        answer6 = prompt(questions=question_6)
        helpdesk_password = answer6.get('helpdesk_password')

        question_7 = [ 
            {'type': 'list',
             'name': 'testing_run',
             'message': 'Would you like to do a test run with a sample email to ensure setup was successful? This can be changed with the testing_mode flag in the it_helpdesk_config.yaml file at any time. Testing mode will print out an example run without needing a mail server.',
             'choices': ['Yes', 'No'],
             'qmark': '',
             'amark': '',
             'show_cursor': False,
             'wrap_lines': True
            }
        ]
        print('')
        answer7 = prompt(questions=question_7)
        testing_mode = True if answer7.get('testing_run') == 'Yes' else False

        with open(f'{os.path.join(helpdesk_ansible_dir, "vars", "it_helpdesk_config.yaml")}', 'w') as config:
            yaml.dump({'testing_mode': testing_mode,
                        'helpdesk_dir': helpdesk_dir,
                        'org_domain': org_domain,
                        'mail_server': mail_server,
                        'mail_port': '',
                        'helpdesk_email': helpdesk_email,
                        'helpdesk_password': helpdesk_password,
                        'requests_directory': {1: 'help',
                                               2: 'storage',
                                               3: 'manage_account', 
                                               4: 'query_account',
                                               5: 'manage_users',}}, config)
        print('')
        inquirer.select(message=f'''The default files have been copied to {helpdesk_dir} where they can be manually changed, and the helpdesk should now work.\nPlease ensure to fill out the Ansible inventory in the directory, and to configure your helpdesks email client to run the script located at {helpdesk_dir}/mail_script.py upon receiving an email.\n\nThank you for installing the it-helpdesk.''', choices=["Exit"], qmark='', amark='', wrap_lines=True, show_cursor=False).execute()

    except Exception as e:
        print(e)
        print('An error occured while attempting this install. Please try again or submit a report to the repository with the above error code.')

if __name__ == '__main__':
    main()
