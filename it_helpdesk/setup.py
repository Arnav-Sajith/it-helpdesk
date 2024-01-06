from __future__ import print_function, unicode_literals
import os
import sys
import shutil
import it_helpdesk
import yaml
from InquirerPy import prompt
from InquirerPy.validator import PathValidator
from InquirerPy import utils, inquirer



def main():
    package_dir = os.path.dirname(it_helpdesk.__file__)
    ansible_default_files = os.path.join(package_dir, 'ansible')
    question_1 = [
        {'type': 'list',
         'name': 'interactive_install',
         'message': 'Would you like to do an interactive or manual set-up (advanced)',
         'choices': ['interactive', 'manual']
        }
    ]
    answer1 = prompt(questions=question_1)
    
    if answer1.get('interactive_install') == 'manual':
        helpdesk_dir = os.path.join(os.path.expanduser('~'), 'it-helpdesk')
        try:
            os.mkdir(helpdesk_dir)
            shutil.copytree(ansible_default_files, os.path.join(os.path.expanduser('~'), 'ansible'), dirs_exist_ok=True)

        except: 
            shutil.copytree(ansible_default_files, os.path.join(os.path.expanduser('~'), 'ansible'), dirs_exist_ok=True)
        with open(f'{os.path.join(helpdesk_dir, "ansible", "vars", "it_helpdesk_config.yaml")}', 'w') as config:
            yaml.dump({'helpdesk_dir': helpdesk_dir,
                        'org_domain': '',
                        'mail_server': '',
                        'helpdesk_email': '',
                        'helpdesk_password': ''}, config)
        print('')
        result = inquirer.select(message=f"The default files have been copied to {helpdesk_dir} and are manually configurable. Thank you for installing the it-helpdesk.", choices=["Exit"]).execute()

    else:
        question_2 = [
            {'type': 'filepath',
            'name': 'install_dir',
            'default': os.path.expanduser('~'),
            'message': f'Please specify the directory where the ansible configuration should be stored:',
            "validate": PathValidator(is_dir=True, message="Input is not a directory"),
            "only_directories": True
            }
        ]
        print('')
        answer2 = prompt(questions=question_2)
        helpdesk_dir = os.path.join(answer2.get('install_dir'), 'it-helpdesk')
        helpdesk_ansible_dir = os.path.join(helpdesk_dir, 'ansible')
    
        try:
            os.mkdir(helpdesk_dir)
            shutil.copytree(ansible_default_files, helpdesk_ansible_dir, dirs_exist_ok=True)

        except: 
            shutil.copytree(ansible_default_files, helpdesk_ansible_dir, dirs_exist_ok=True)                

        question_3 = [
            {'type': 'input',
            'name': 'org_domain',
            'message': f'Please enter your organizations domain',
            'validate': lambda answer: 'You must enter a domain for your organization.' \
                if len(answer) == 0 else True
            }
        ]
        answer3 = prompt(questions=question_3)
        org_domain = answer3.get('org_domain')
        
        question_4 = [
            {'type': 'input',
            'name': 'mail_server',
            'message': f'Please specify the address of your organizations mail server: (leave blank for default - localhost))',
            }
        ]
        answer4 = prompt(questions=question_4)
        mail_server = 'localhost' if len(answer4.get('mail_server')) == 0 else answer4.get('mail_server')

        question_5 = [
            {'type': 'input',
            'name': 'helpdesk_email',
            'message': f'Please enter the email address for the it-helpdesk: (leave blank for default - it-helpdesk@{org_domain})',
            }
        ]
        answer5 = prompt(questions=question_5)
        helpdesk_email = f'it-helpdesk@{org_domain}' if len(answer5.get('helpdesk_email')) == 0 else answer5.get('helpdesk_email')

        question_6 = [
            {'type': 'password',
            'name': 'helpdesk_password',
            'message': f'Please enter the password for the it-helpdesks email address',
            }
        ]
        answer6 = prompt(questions=question_6)
        helpdesk_password = answer6.get('helpdesk_password')

        with open(f'{os.path.join(helpdesk_ansible_dir, "vars", "it_helpdesk_config.yaml")}', 'w') as config:
            yaml.dump({'helpdesk_dir': helpdesk_dir,
                        'org_domain': org_domain,
                        'mail_server': mail_server,
                        'helpdesk_email': helpdesk_email,
                        'helpdesk_password': helpdesk_password}, config)
        result = inquirer.confirm(message=f"Installation complete. The it-helpdesk content is available at {helpdesk_dir}. Thank you for installing the it-helpdesk.").execute()


if __name__ == '__main__':
    main()
