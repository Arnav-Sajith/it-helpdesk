import re
headers_dictionary = {}
headers_dictionary['from'] = 'arnavsajith@arnav.local'
headers_dictionary['id'] = 'F2670D23433'
headers_dictionary['to'] = 'arnavsajith@arnav.local'
headers_dictionary['subject'] = 'Increase User Storage'
headers_dictionary['message-id'] = '20231010040739.F2670D23433@arnav.local'
headers_dictionary['date'] = 'Tue 10 Oct 2023 00:07:39 -0400 (EDT)'
headers_dictionary['body'] = '''Hello, I'd like to increase congbine the storage quota for user: arnavsajith@arnav.local to 5.5gb'''

storage_phrases_dict = {}

def is_valid_amount(amount: str):
    if amount.isdigit():
        return int(amount)
    else:
        try:
            return float(amount)
        except(ValueError):
            return False

def load_phrases():
    with open("storage_phrases.txt", ) as storage_phrases:
        key = None  # store the most recent "command" here
        for line in storage_phrases.readlines():
            if line[0] == '*':
                key = line[1:].rstrip("*\n") # your "command"
                storage_phrases_dict[key] = []
            else:
                storage_phrases_dict[key].append(line.split())
    print(storage_phrases_dict)
    return storage_phrases_dict

    
def parse_subject(headers_dictionary):
    storage_request = False
    positive_verb = False
    negative_verb = False
    target_not_sender = False
    valid_request = True

    storage_phrases = load_phrases()
    subject = headers_dictionary['subject'].lower()
    if any(keyword in subject for keyword in storage_phrases['keywords'][0]):
        storage_request = True
        print("Request = storage_request")
    if any((match := positive_verb) in subject for positive_verb in storage_phrases["verbs_positive"][0]):
        positive_verb = True
        print("Request type = positive verb", match)
    if any((match := negative_verb) in subject for negative_verb in storage_phrases["verbs_negative"][0]):
        negative_verb = True
        print("Request type = negative verb", match)
    if any((match := target) in subject for target in storage_phrases["targets"][0]):
        target_not_sender = True
        print("target found:", match)
    if (positive_verb and negative_verb):
        print("Sorry, I couldn't comprehend your request. The subject contains both a positive: '", positive_verb, "' and a negative '", negative_verb, "'")
        valid_request = False
        return valid_request
    else:
        return valid_request, storage_request, positive_verb, negative_verb, target_not_sender


def execute_request(valid_request: bool, storage_request: bool, positive_verb: bool, negative_verb: bool, target_not_sender: bool):
    if valid_request == False:
        return "invalid request subject"
    if storage_request == True and target_not_sender == True:
        parse_body("storage", target_not_sender)

def parse_body(request_type, target_not_sender: bool):
   
    body = headers_dictionary['body'].lower()
    amount = {"modifier": None, "amount": None, "unit": None}
    if request_type == "storage":
        storage_phrases = load_phrases()
        amount_phrases = storage_phrases["amount"][0]
        modifiers = storage_phrases["modifiers"][0]
        targets = storage_phrases["targets"][0]
        print("\n\n")
        for x in range(len(amount_phrases)):
            pattern = fr'(\S+\s+\S+)\s*({amount_phrases[x]})'
            matches = re.findall(pattern, body)
            print(matches)
            if not matches:
                print("No", amount_phrases[x], "found")
            else:
                for y in range(len(matches)):
                    if any((match := modifier) in matches[y][0] for modifier in modifiers) and is_valid_amount(matches[y][0].strip(match)):                    
                        amount["modifier"] = match
                        amount['amount'] = matches[y][0].strip(f'{match} ')
                        amount['unit'] = matches[y][1]
        
        if any((match := target) in body.split() for target in targets):
            print(body.split().index(match))

    
        pass

    

    
execute_request(*parse_subject(headers_dictionary))