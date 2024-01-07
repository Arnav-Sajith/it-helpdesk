import os
import shutil
import it_helpdesk
import yaml
from InquirerPy import prompt, inquirer
from InquirerPy.validator import PathValidator




def main():
    package_dir = os.path.dirname(it_helpdesk.__file__)
    ansible_default_files = os.path.join(package_dir, 'ansible')
    question_1 = [
        {'type': 'list',
         'name': 'interactive_install',
         'wrap_lines': True,
         'message': 'Welcome to the setup installer for the autonomous it-helpdesk. This software is intended to be used in conjunction with the EMPT IT suite. This tool will set up the directories and configuration files for all of the ansible automation you will be working with. Press Continue to proceed.',
         'choices': ['Continue'],
         'qmark': '',
         'amark': ''
        }
    ]
    prompt(questions=question_1)
    
    while True:
        question_2 = [
            {'type': 'filepath',
            'name': 'install_dir',
            'default': os.path.expanduser('~'),
            'message': f'Please specify the parent directory where the it-helpdesk folder should be stored:',
            "validate": PathValidator(is_dir=True, message="Input is not a directory"),
            "only_directories": True,
            'wrap_lines': True,
            'qmark': '',
            'amark': '',
            }
        ]
        print('')

        answer2 = prompt(questions=question_2)
        helpdesk_dir = os.path.join(answer2.get('install_dir'), 'it-helpdesk')
        if inquirer.confirm(message=f"The it-helpdesk will be installed to {helpdesk_dir}. Is this okay? (Default: No)", mandatory=True, qmark='', amark='', wrap_lines=True).execute() == True:
            try:
                os.mkdir(helpdesk_dir)
                shutil.copytree(ansible_default_files, helpdesk_ansible_dir)
                shutil.copyfile('../mail_script.py', helpdesk_ansible_dir)
                break

            except FileExistsError: 
                print("The it-helpdesk already exists in that directory. Please select another folder, or use that install.")
            

        helpdesk_ansible_dir = os.path.join(helpdesk_dir, 'ansible')

        
        question_3 = [
            {'type': 'input',
            'name': 'org_domain',
            'message': f'Please enter your organizations domain:',
            'validate': lambda answer: 'You must enter a domain for your organization.' \
                if len(answer) == 0 else True,
            'amark': '',
            'qmark': '',
            'wrap_lines': True,
            }
        ]
        answer3 = prompt(questions=question_3)
        org_domain = answer3.get('org_domain')
        
        question_4 = [
            {'type': 'input',
            'name': 'mail_server',
            'message': f'Please specify the address of your organizations mail server: (leave blank for default - localhost))',
            'amark': '',
            'qmark': '',
            'wrap_lines': True,
            }
        ]
        answer4 = prompt(questions=question_4)
        mail_server = 'localhost' if len(answer4.get('mail_server')) == 0 else answer4.get('mail_server')

        question_5 = [
            {'type': 'input',
            'name': 'helpdesk_email',
            'message': f'Please enter the email address for the it-helpdesk: (leave blank for default - it-helpdesk@{org_domain})',
            'qmark': '',
            'amark': '',
            'wrap_lines': True,
            }
            
        ]
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
        answer6 = prompt(questions=question_6)
        helpdesk_password = answer6.get('helpdesk_password')

        with open(f'{os.path.join(helpdesk_ansible_dir, "vars", "it_helpdesk_config.yaml")}', 'w') as config:
            yaml.dump({'helpdesk_dir': helpdesk_dir,
                        'org_domain': org_domain,
                        'mail_server': mail_server,
                        'mail_port': '',
                        'helpdesk_email': helpdesk_email,
                        'helpdesk_password': helpdesk_password}, config)
        inquirer.select(message=f'''The default files have been copied to {helpdesk_dir} where they can be manually changed, and the helpdesk should now work. Please
                        ensure to fill out the Ansible inventory in the directory, and to configure your helpdesks email client to run the script located at {helpdesk_dir}/mail_script.py upon receiving an email. 
                        Thank you for installing the it-helpdesk.''', choices=["Exit"], qmark='', amark='', wrap_lines=True).execute()


if __name__ == '__main__':
    main()
