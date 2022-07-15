import json

# This is the basic TFT composition builder 

# Champion and trait information must be passed in as a json file 
# Thanks to https://github.com/aaronlam1004/hexcore-api for creating the API for the new set

set_json = 'champions-set7.json'
traits_json = 'traits-set7.json'
with open(set_json) as json_file:
    champions = json.load(json_file)

with open(traits_json) as json_file:
    traits = json.load(json_file)

# print(champions[0])
# print(traits[0])

 

# a list of champion objects in the team composition 
team_composition = [] 

team_traits = []

# this class represents a champion
class Champion:
    # takes json champion data and creates a champion object 
    def __init__(self, champ_data):
        self.name = champ_data['name']
        self.key = self.name.lower()
        self.cost = champ_data['cost']
        self.traits = []
        for trait_id in champ_data['traits']:
            self.traits.append(get_trait_name(trait_id))

# this class represents a trait 
class Trait:
    # takes a trait pair of a trait and its count to create a trait object 
    def __init__(self, trait_pair):
        trait_data = get_trait_data(trait_pair[0])
        self.name = trait_data['name']
        self.description = trait_data['description']
        self.active_count = trait_pair[1]
        self.max_count = trait_data['sets'][len(trait_data['sets']) - 1]['min']
        self.style = get_trait_style(self.active_count, trait_data)

# given a number and trait json data, returns the style level: bronze, silver, gold, chromatic 
def get_trait_style(active_count, trait_data):
    set_data = trait_data['sets']
    for set in reversed(set_data):
        if set['min'] <= active_count:
            return set['style']
    return "non-active"

# given champion data, returns the string name of the champion
def get_champ_name(champ_data):
    return champ_data['name']

# given a champion name, returns the champion json data and returns false if champion is not found 
def get_champ_data(champ_name):
    for champ in champions:
        if get_champ_name(champ).lower() == champ_name.lower():
            return champ
    return False

# given a trait name, returns the trait json data and returns false if trait is not found
def get_trait_data(trait_name):
    for trait in traits:
        if trait['name'] == trait_name:
            return trait
    return False 
    

# given trait id, returns the string name of the trait 
def get_trait_name(trait_id):
    for trait in traits: 
        if trait['key'] == trait_id:
            return trait['name']
    raise ValueError("Trait ID is not valid")

# returns a string list of all champion names in the current set
def display_all_champs_in_set():
    champ_name_list = map(get_champ_name, champions)
    champ_name_string = ""
    for name in champ_name_list:
        champ_name_string += name + "\n"
    return champ_name_string


# given a champion's json data, returns the champion's trait properties as a string 
def get_traits_from_champ_data(champ_data):
    traits_string = 'Traits: '
    length = len(champ_data['traits'])
    for x in range(length):
        traits_string += get_trait_name(champ_data['traits'][x])
        if x < length - 1:
            traits_string += ", "
    return traits_string

# given a champion's name, return's the champion's information as a string 
def display_champion_info(champ_name):
    champ_data = None
    for champ in champions: 
        if champ['name'].lower() == champ_name.lower():
            champ_data = champ
    return champ_data['name'] + "\n" + str(champ_data['cost']) + "\n" + get_traits_from_champ_data(champ_data) 

# returns a string of all the champions in the team compositon
def display_team_composition():
    if len(team_composition) == 0:
        return "There are currently no champions in the team composition "
    team = ''
    for champ in team_composition:
        team += format_display(display_champion_info_obj(champ))
    return team 

# given a champion object, returns the champion's trait properties as a string 
def get_traits_from_champ_obj(champ_obj):
    traits_string = 'Traits: '
    length = len(champ_obj.traits)
    for x in range(length):
        traits_string += champ_obj.traits[x]
        if x < length - 1:
            traits_string += ", "
    return traits_string

# given a champion object, returns the champion's information as a string 
def display_champion_info_obj(champ_obj):
    return champ_obj.name + "\n" + str(champ_obj.cost) + "\n" + get_traits_from_champ_obj(champ_obj)

# given a string to display, formats for readibility in terminal
def format_display(display_string):
    return "--------\n" + display_string + "\n--------\n"

# given a champion name, remove it from the team composition and returns true if the removal is completed 
def remove_from_composition(champ_name):
    for champ in team_composition:
        if champ.key == champ_name.lower():
            team_composition.remove(champ)
            return True 
    return False

# analyzes the team composition, counting the active traits and returning a list of pairs for active trait names and their counts
def count_traits():
    trait_list = []
    trait_count = []
    seen_list = []
    for champ in team_composition:
        trait_list += champ.traits
    for trait in trait_list:
        if trait not in seen_list:
            trait_count.append([trait, trait_list.count(trait)])
            seen_list.append(trait)
    return trait_count

# analyzes the team composition adding active team traits 
def analyze_traits():
    global team_traits 
    team_traits = []
    trait_pairs = count_traits()
    for pair in trait_pairs:
        team_traits.append(Trait(pair))

# returns a string of all the traits in the team compositon
def display_team_traits():
    if len(team_traits) == 0:
        return "There are currently no champions in the team composition "
    team = ''
    for trait in team_traits:
        team += format_display(display_trait_info_obj(trait))
    return team 

# given a trait object, returns the trait information as a string 
def display_trait_info_obj(trait_obj):
    return trait_obj.name + "\n" + "Number of Champions: " + str(trait_obj.active_count) + " / " + str(trait_obj.max_count) + "\n" + "Style: " + trait_obj.style

# returns a string displaying instructions 
def print_instructions():
    instructions = "Type 1 or type \"view champions\" to view the list of champions\n"
    instructions += "Type 2 or type \"view composition\" to view your team composition\n"
    instructions += "Type 3 or type \"view traits\" to view your team composition's traits\n"
    instructions += "Type \"add <champion name>\" to add a champion to your team composition\n"
    instructions += "Type \"remove <champion name>\" to remove a champion from your team composition\n" 
    instructions += "Type \"remove all\" to restart team composition"
    return instructions

# processes the given input, returns true if program is not quit and false if the program is quit 
def manage_command(input):
    global team_composition
    if (input == "1" or input == "view champions"):
        print("List of Champions:")
        print(display_all_champs_in_set())
        return True 
    elif (input == "2" or input == "view composition"): 
        print(display_team_composition())
        return True 
    elif (input == "3" or input == "view traits"): 
        print(display_team_traits())
        return True 
    elif ("add" in input):
        champ_request = input.replace("add ", "")
        champ_data = get_champ_data(champ_request)
        if champ_data != False: 
            team_composition.append(Champion(champ_data))
            analyze_traits()
            print("Champion has been added to the team composition")
            print(format_display(display_champion_info(champ_data['name'])))
        else:
            print("Champion name is not found")
        return True 
    elif (input == "remove all"):
        team_composition = []
        return True 
    elif ("remove" in input):
        if remove_from_composition(input.replace("remove ", "")) == False:
            print("Champion name not found in team composition")
        else: 
            analyze_traits()
            print("Champion has been removed from the team composition")
        return True
    elif (input == "count"):
        print(count_traits())
        return True 


def main():
    print("TFT Composition Builder \n We are currently using set information from: {}".format(set_json))
    print(print_instructions())
    print("User Input:", end = ' ')
    command = input()
    while manage_command(command) == True:
        # print(print_instructions())
        print("User Input:", end = ' ')
        command = input()
    
    

main()

