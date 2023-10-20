import re
import shlex
from pyisemail import is_email


def is_valid_amount(amount: str):
    if amount.isdigit():
        return int(amount)
    else:
        try:
            return float(amount)
        except(ValueError):
            return False
        
def is_valid_target(target : str):
    with open("existing_users.txt", 'r') as existing_users:
        target = target.split("@")[0]
        return True if target+'\n' in existing_users else False
        
def load_phrases():
    with open("storage_phrases.txt", "r") as storage_phrases:
        storage_phrases_dict = {}
        key = None  # store the most recent "command" here
        for line in storage_phrases.readlines():
            if line[0] == '*':
                key = line.strip("*\n") # your "command"
                storage_phrases_dict[key] = []
            else:
                storage_phrases_dict[key].append(shlex.split(line))
    return storage_phrases_dict

    
def parse_subject(subject_entered : str, email_from : str, body : str):
    subject = subject_entered.lower()
    parse_subject_dict = {'request_type': 1, 'query': False, 'positive_verb': False, 'negative_verb': False, 'target_not_sender': False, 'valid_request': True, 'email': email_from, 'body': body}
    storage_phrases = load_phrases()
    if any(keyword in subject for keyword in storage_phrases['keywords'][0]):
        parse_subject_dict['request_type'] = 1
    if any(query in subject for query in storage_phrases["queries"][0]):
       parse_subject_dict['query'] = True
    if any(positive_verb in subject for positive_verb in storage_phrases["verbs_positive"][0]):
        parse_subject_dict['positive_verb'] = True
    if any(negative_verb in subject for negative_verb in storage_phrases["verbs_negative"][0]):
        parse_subject_dict['negative_verb'] = True
    if any(target in subject for target in storage_phrases["targets"][0]) and not any(self_target in subject for self_target in storage_phrases["selftargets"][0]):
        parse_subject_dict['target_not_sender'] = True
    # if (positive_verb and negative_verb):
    #     print("Sorry, I couldn't comprehend your request. The subject contains both a positive: '", positive_verb, "' and a negative '", negative_verb, "'")
    #     valid_request = False
    #     return valid_request
    return parse_subject_dict


def parse_body(target_not_sender: bool, body: str, query: bool):
    body_words = body.split()
    amount = {"modifier": None, "amount": None, "unit": None, "target": None}
    storage_phrases = load_phrases()
    modifiers = storage_phrases["modifiers"][0]
    targets = storage_phrases["targets"][0]
    if not query: 
        pattern = r'(\S+\s+\S+)\s*(GB)'
        matches = re.findall(pattern, body, re.IGNORECASE)
        if any((match := modifier) in matches[0][0] for modifier in modifiers) and is_valid_amount(matches[0][0].strip(match)):
                    amount["modifier"] = match
                    amount['amount'] = matches[0][0].strip(f'{match} ')
                    amount['unit'] = matches[0][1]
    
    if any((match := target) in body_words for target in targets): # add more options for default and for multiple users
        target_index = body_words.index(match)
        username = body_words[target_index + 1]
        amount['target'] = "default user" if match == "default" else username

    elif amount['target'] is None:
        for target in body_words:
                amount['target'] = target if is_email(target) else None

    elif not target_not_sender:
        amount['target'] = None
    return amount
    
    # else: 
    #     with open('existing_users', 'r') as existing_users:  #TODO create matching for all emails if user exists
    #         if any((match := user) in body_words for user in existing_users):
    #             amount['target'] = match
    #         else:
                
    #         return amount


    
def execute_request(parse_subject_dict : dict):
    if parse_subject_dict['request_type'] == 1:
        storage_request_contents = parse_body(parse_subject_dict['target_not_sender'], parse_subject_dict['body'], parse_subject_dict['query'])
        storage_request_contents['target'] = parse_subject_dict['email'] if storage_request_contents['target'] is None else storage_request_contents['target']
        storage_request_contents['valid_target'] = is_valid_target(storage_request_contents['target'])
        storage_request_contents['positive_action'] = parse_subject_dict['positive_verb']
        storage_request_contents['query'] = parse_subject_dict['query']
        return storage_request_contents
