
# it-helpdesk

This is an open-source, plaintext, email based automated IT helpdesk created for the EMPT IT suite. When hooked up to an email client, it takes piped in emails, parses them based on fully and easily customizable phrasebooks, and runs Ansible playbooks to accomplish typical IT duties like managing users. More and custom use cases can be added simply by creating an Ansible playbook and its matching phrasebook — no code needs to be touched.

## Requirements
Aside from the Python dependencies that pip will install for you upon running the below installation, there are a few things that are needed for the helpdesk to work.
- A working Ansible setup with a Unix control node and some managed nodes
- A complete Inventory file for your Ansible installation
- A working mail server and client:
    - This can be done with any email provider, or your own local server. If using an external providers services, you will need to set up a local mail client that can pull and pipe emails to scripts, like FDM or Postfix, and SMTP credentials to fetch and send mail
- Python version >3.10

If you are using this with the EMPT IT suite, all of this will be preconfigured for you and won't need to be set up.


## Installation

The it-helpdesk can be installed using pip. This will install all of its dependencies as well, if they are not already present in the install environment.
```bash
  pip3 install it_helpdesk
```
Once installed, you can run the below command in the same environment to set up the necessary configuration files that the helpdesk will use.
```bash
  setup_helpdesk
```
This will bring up a CLI where you will enter the necessary information to be able to use the helpdesk, like directory paths and credentials. By default, the installer stores everything in an it-helpdesk directory inside the user's home directory


## Usage/Examples
After installing in the chosen directory, the relevant file structure will look like the following:
```bash
.it-helpdesk
├── ansible
│   ├── help_templates
│   │   ├── manage_users_help.txt
│   │   └── storage_help.txt
│   ├── inventory
│   ├── phrasebooks
│   │   ├── account_phrases.txt
│   │   ├── approved_commands.txt
│   │   ├── help_phrases.txt
│   │   ├── manage_account_phrases.txt
│   │   ├── manage_users_phrases.txt
│   │   └── storage_phrases.txt
│   ├── playbooks
│   │   ├── help.yaml
│   │   ├── manage_users.yaml
│   │   └── storage.yaml
│   └── vars
│       ├── ansible.cfg
│       └── it_helpdesk_config.yaml
└── mail_script.py
```
The mail_script.py in the root of the directory is the script that calls the entire helpdesk software. Connect this to the desired email so that incoming emails are piped through the script for parsing and automation. I did this locally with fdm and my Gmail account as follows, sending to an interim bash script that activated the venv I was working in. It works the same with the Python script.
```bash
    action "inbox" maildir "~/Maildir/INBOX"
    action "piping" pipe "/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/activate_venv.sh argv=%[mail_file]" 
    account "my_email@gmail.com" imaps server "imap.gmail.com" port 993 user "my_email@gmail.com" pass "my_smtp_password" new-only cache "~/.imapcache"
    # Match all other mail and deliver using the 'inbox' action.
    # match all action "inbox"
    match all action "piping"
```
and a simple bash script to pull from my Gmail
```bash
#!/bin/sh
while true; do
	fdm -kmvv fetch 2>&1 | tee -a ~/.fdm.log
	sleep 5
done
```
However you do it, once the piping works the helpdesk is online, and will parse all incoming emails to it for tasks to automate, assuming you have filled the inventory file with the addresses of the machines.

### Phrasebooks and keywords
Phrasebooks work in matched pairs with Ansible playbooks in order to define the information that needs to be in the email sent to the it-helpdesk for a task to complete. They can be as simple or complicated as you would like, as long as it matches the playbook and is formatted correctly it will work.
#### Phrasebooks
This is how phrasebooks are formatted, taken from the above ```ansible/phrasebooks/storage_phrases.txt```
```
*targets*
employee: user: username: account:
*selftargets*
my me myself i
*verbs_positive*
add more increase
*verbs_negative*
reduce decrease less
*queries*
'how much' left 'what is' 'have i' 'query'
*modifiers*
by to
*unit*
gb
```

#### How to use phrasebooks
Sections in the phrasebooks are separated by their labels within asterisks. These labels will be used when writing Ansible playbooks as well, so choose meaningful names for each section.

Every section here aside from ```*targets*``` and ```*selftargets*``` sections are completely optional. These search for matching phrases for each section in the email, and if found, creates a True/False flag applying to the section. For example, an email body snippet of ```Increase my storage allocation by 5gb``` would give ```{verbs_positive: True, verbs_negative: False, queries: False, selftargets: True, modifiers: by, unit: gb}```
These are then used in the Ansible playbook to decide what the email is asking to be done.
The ```*targets* , *modifiers*, and *unit*``` flags are unique. The ```*modifiers* and *unit*``` flags are unique and have coded exceptions for them that parse anything in the format of ```action amount unit``` like for increasing/decreasing storage. However, this means that it will as such rarely be used, and when needed can be implemented like this. 

The ```*targets*``` flag is the only flag that can get values for variables that might be needed for your Ansible playbook. It searches the email for *each* of its phrases, and if it finds any, captures the next token and stores it as a key-value pair for that phrase. This allows for more complex tasks that cannot be accomplished with just True/False flags. The snippet: ```Increase the storage allocation for the user: alicesmith to 3.5gb``` would give ```{targets: alicesmith, verbs_positive: True, verbs_negative: False, queries: False, selftargets: True, modifiers: to, unit: gb}```

The first target in the phrasebook will always occupy the ```targets: value``` role. If additional targets are searched for, they will be stored in ```target_name: target_value``` that can be accessed in ansible with their ```target_name```. For example, if you have the targets ```username: password: name:``` as your desired information, the snippet ```username: john password: 1234 and name: johnathan``` would store as ```{targets: john, password: 1234, name: johnathan}``` along with whatever other flags you set to search for in the phrasebook.

#### Keywords
The phrasebook used to parse the email is determined without having to search all of the phrasebooks and finding matches by the use of a separate, but linked, keyword file. This contains a few words/phrases that have to exist in the *subject* of the email in order to cut down on parsing time for efficiency. There is a single keyword file that contains all of the keywords for every playbook and phrasebook that exists, and the keywords must be unique. When a match is found, it is looked up in the ```it_helpdesk_config.yaml```'s request directory for reference and organization.
Default ```.keywords.txt``` file:
```
*help*
documentation help
*storage*
storage space quota
*manage_account*
username permissions password 'change username' 
*query_account*
'query account'
*manage_users*
new 'new user' 'new employee' onboarding delete 'delete user' remove 'add user'
```
```
requests_directory: {1: 'help',
                     2: 'storage',
                     3: 'manage_account', 
                     4: 'query_account',
                     5: 'manage_users',
                     }
```
#### How to use keywords
The keywords file functions similarly to the phrasebooks. It flags the sections True/False if any of its keywords are found in the email subject, and returns the request type after looking it up in the ```it_helpdesk_config.yaml```'s request directory. For example, if the subject of the email is ```Increase Storage Quota```, it will flag ```storage``` as True, and return ```request_type: 2``` to the helpdesk so it can start the parsing. The order of entries in the ```.keywords.txt``` file has to match the ```requests_directory``` in order for the system to work. 

### Naming conventions

When adding new automation capabilities to the helpdesk by creating new playbooks and phrasebooks, a few naming conventions must be adhered to. Beyond that, as long as they match each other, they will link and whatever functionality you add will work in the helpdesk. 

When creating a new capability for the desk, it must hold to the following:
- Playbook: ```{playbook_task}.yaml```
- Phrasebook: ```{playbook_task}_phrases.yaml```
- Keyword Line ```*playbook_task*```
- Help file: ```{playbook_task}_help.txt```
- Requests directory: ```id: '{playbook_task}'```

From the above directory, we have the following example:
- Playbook: ```manage_users.yaml```
- Phrasebook: ```manage_users_phrases.yaml```
- Keyword Line ```*manage_users*```
- Help file: ```manage_users_help.txt```
- Requests_directory: ```5: 'manage_users'```

### The it_helpdesk_config file
The it_helpdesk_config file is generated when you run the ```setup_helpdesk``` command for the first time alongside the rest of the files. It is populated with your responses for information that the helpdesk needs to accomplish its tasks. The helpdesk will not work without having this config file, and at least the ```helpdesk_dir``` needs to be filled out to the location of the ```it-helpdesk``` directory. If moving the directory, ensure that the config file is changed to match, or it will search the old location. 

Any configurations, settings, or saved information that is repeatedly used by the helpdesk should be stored here, with a variable name that can be called from within the playbooks when needed. If you add any new playbooks, ensure that you add it to the ```requests_directory``` within this file as well.

If you want to create additional config files, it will work as long as you load them into your Ansible playbooks as well. Just make sure to keep the `helpdesk_dir` and `requests_directory` in the original file, updated for all changes.

### Help files
Help files are ```.txt``` documents that go in the ```/help_templates``` directory with a matching name to their playbook/phrasebook. These get automatically sent to users who send an email containing ```help with: {{ functionality }}```, as long as the name matches. It is beneficial to add an error message with a basic reply of how to send a help message like 
```If you need help with this functionality, send an email with the subject: Help and body: help with: manage_users```
Once they send the email, they will quickly receive a reply whos body is the ```{playbook_task}_help.txt``` The ```manage_users_help.txt``` looks like this:

```
Here is an exemplar of how to use the manage users function of the IT-Helpdesk to create and delete users in your organization. Any words within quotes should be replaced with your desired values, WITHOUT the quotes.

Creating Users:

Subject: New User
Body:
I'd like to create a new user with the following information:
username: 'desired username'
password: 'desired password'
first_name: 'employee first name'
last_name: 'employee last name'


Deleting Users:

Subject: Delete User
Body:
I'd like to delete the account with the username: 'desired account to delete'
```

This allows the user to quickly copy and paste the template and fill in their values if they were struggling beforehand.

### Making playbooks

Making playbooks is much too complicated to give a complete overview of here, but Ansible can be used to basically automate any IT tasks. It has support for a variety of plugins and capabilities, and is basically English as well. It is extremely beginner friendly. For an example of how an Ansible playbook can be made/used, check the below playbook snippet of user storage allocation.

```
  
  vars:
    ansible_user: ansible

    undefined_variables: []

    request_amount: "{{ amount | float}}"

    request_unit: "gb"

    request_action: "{{ 'increase' if (verbs_positive|bool == True) else 'decrease'}}"

    request_net_change: "{{ request_amount if request_action == 'increase' else request_amount * -1 }}"

    current_quota: '{{ (ansible_zfs_datasets[0].reservation | replace("G", "")) | float}}'

    increase_amount: '{{(current_quota|float + request_net_change|float) if modifiers == "by" else request_amount|float }}'

  vars_files:
    - ../vars/shared_vars.yaml

  tasks:
    - name: "Send email notifying of invalid request"
      community.general.mail:
              host: '{{ mail_server }}'
              port: '{{ mail_port }}'
              secure: always
              username: '{{ helpdesk_email }}'
              password: '{{ helpdesk_password }}'
              to: '{{ from }}'
              from: '{{ helpdesk_email }}'
              subject: "Could not execute your recent user management request"
              body: "We couldn't understand what you wanted from your previous user management request. Please ensure that all necessary information is included. Send an email with the subject: Help and body: 'help with: manage_users' to see how to properly format your request.'"
      when: verbs_positive == None and verbs_negative == None and queries == None

    - name: "Exit playbook run if invalid request"
      ansible.builtin.fail:
        msg: "Invalid request"
      when: verbs_positive == None and verbs_negative == None and queries == None

    - name: User Storage Query
      community.general.zfs_facts:
        dataset: 'zroot/empt/homes/{{ targets }}'
      register: zfs_query
      ignore_errors: true

    - name: "Send email notifying if target username is undefined"
      community.general.mail:
        host: '{{ mail_server }}'
        port: '{{ mail_port }}'
        secure: always
        username: '{{ helpdesk_email }}'
        password: '{{ helpdesk_password }}'
        to: '{{ from }}'
        from: '{{ helpdesk_email }}'
        subject: "Could not execute your recent user management request"
        body: "The username provided: {{ targets }} is not a valid user. Please ensure to include a user with the format 'username: targeted_username', and that the user exists in your organization."
      when: targets == None or zfs_query is failed

    - name: "Exit playbook run if no username is provided"
      ansible.builtin.fail:
        msg: "A username was not provided in the email request"
      when: targets == None or zfs_query is failed
```


## Authors

- [Github](https://www.github.com/Arnav-Sajith)
- [LinkedIn](https://www.linkedin.com/in/arnav-sajith)



## License

[MIT](https://choosealicense.com/licenses/mit/)

```
MIT License

Copyright (c) 2023 Arnav-Sajith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```

