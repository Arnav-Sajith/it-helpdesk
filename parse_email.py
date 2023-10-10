headers_dictionary = {}
headers_dictionary['from'] = 'arnavsajith@arnav.local'
headers_dictionary['id'] = 'F2670D23433'
headers_dictionary['to'] = 'arnavsajith@arnav.local'
headers_dictionary['subject'] = 'Increase User Storage'
headers_dictionary['message-id'] = '20231010040739.F2670D23433@arnav.local'
headers_dictionary['date'] = 'Tue 10 Oct 2023 00:07:39 -0400 (EDT)'
headers_dictionary['body'] = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices pellentesque nibh, eget aliquet ex faucibus molestie. Mauris tempor, leo vitae semper sodales, risus nibh efficitur risus, in varius nibh leo vel nisl. Ut at sapien nec quam lacinia auctor ac ac velit. Ut non semper dolor. Nunc vel vehicula urna. Nam scelerisque dolor quis auctor sagittis. Vestibulum dapibus fringilla dolor in sollicitudin. Phasellus ut dapibus nibh. Nam tempus placerat convallis. Duis id diam molestie mauris aliquam facilisis. Aenean dapibus vel arcu ultricies sodales. Donec ut mauris nisl. Donec tincidunt ultricies justo.
Fusce dui felis, venenatis at sem nec, sollicitudin efficitur odio. Donec accumsan finibus mi at venenatis. Integer condimentum arcu vitae diam commodo pellentesque. Fusce vitae efficitur urna, a eleifend turpis. Vivamus volutpat sollicitudin odio. Vivamus eu facilisis mauris. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque accumsan gravida interdum. Aenean at vestibulum magna. Nam pellentesque a mi vitae pellentesque. In fringilla magna est, vitae scelerisque nunc bibendum at. In nec euismod erat, vel tempor arcu. Fusce quis nisl diam. Integer et fringilla sem, sed iaculis justo.
Fusce sit amet rutrum velit. Sed metus libero, hendrerit eget posuere ac, rutrum a erat. Maecenas efficitur quam ac tortor vehicula, vitae dapibus ligula iaculis. Sed in odio augue. Duis eget massa id arcu posuere semper. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi lorem justo, vulputate a tempus ac, suscipit eget enim. Nulla facilisi. Cras ac augue dui. Integer nunc sem, pulvinar sed leo non, tincidunt commodo nisl. Sed rutrum semper leo at laoreet. Aliquam non massa eu nisi ultrices maximus ut eu felis. Suspendisse consectetur ante sit amet risus condimentum rutrum. Phasellus sit amet sem eu turpis viverra hendrerit et sed erat. Suspendisse facilisis feugiat venenatis. Pellentesque mi ex.'''

storage_phrases_dict = {}

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
    valid_request = False
    storage_phrases = load_phrases()
    print(storage_phrases)
    subject = headers_dictionary['subject'].lower()
    body = headers_dictionary['body'].lower()
    if any(keyword in subject for keyword in storage_phrases['keywords'][0]):
        storage_request = True
        print("Request = storage_request")
    else:
        exit
    if any((match := positive_verb) in subject for positive_verb in storage_phrases["verbs_positive"][0]):
        positive_verb = True
        print("Request type = positive verb", match)
    if any((match := negative_verb) in subject for negative_verb in storage_phrases["verbs_negative"][0]):
        negative_verb = True
        print("Request type = negative verb", match)
    if any((match := target) in subject for target in storage_phrases["targets"][0]):
        target_not_sender = True
        print("target found:", match)
    else:
        target_not_sender = False
    if (positive_verb and negative_verb):
        print("Sorry, I couldn't comprehend your request. The subject contains both a positive: '", positive_verb, "' and a negative '", negative_verb, "'")
        valid_request = False
        return valid_request
    
    return valid_request, storage_request, positive_verb, negative_verb, target_not_sender

def parse_body(valid_request: bool, storage_request: bool, positive_verb: bool, negative_verb: bool, target_not_sender: bool):    
    pass

    

parse_subject(headers_dictionary)