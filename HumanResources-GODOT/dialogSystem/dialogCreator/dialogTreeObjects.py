import sys

# dialog tree object to store all the nodes and print to file
class dialogTree:
    nodes = []
    key = "dialog"
    title = "None"
    def __init__(self, title):
        self.title = title
    def __str__(self):
        string = '{' + f'"{self.key}": \n\t['
        nodelist = node_list()
        for node in nodelist:
            string = string + str(node) + ","
        string = string + "\n\t]\n}"
    def set_custom_key(self, key):
        self.key = key
    def node_list(self):
        keys = self.nodes.keys()
        keys.sort()
        nodelist = [self.nodes[x] for x in keys]
        return nodelist
    def add_node(self, node):
        self.nodes.append(node)
    def delete_node(self, index):
        node = self.nodes.pop(index, None)
        del node
    def create_file(self, filepath):
        filepath = filepath + f'/{self.title}.json'
        stdout_default = sys.stdout
        with open(filepath, 'w') as f:
            sys.stdout = f
            print(self)
            sys.stdout = stdout_default
    
# dialog node object to store related pages, allow choice traversal
class dialogNode:
    pages = []
    newPagesPossible = True
    toNodes = set([])
    fromNodes = set([])
    title = "Start"
    def __init__(self, title):
        self.title = title
    def __str__(self):
        string = '{' + f'"{self.title}": \n\t['
        pagelist = self.page_list()
        for page in pages:
            string = string + str(page) + ","
        string = string + "\n\t]\n}"
        return string
    def connect_to(self, node):
        self.toNodes.add(node)
        node.fromNodes.add(self)
    def connect_from(self, node):
        self.fromNodes.add(node)
        node.toNodes.add(self)
    def print_title(self):
        return self.title
    def add_page(self, page):
        self.pages.append(page)
    def delete_page(self, index):
        self.pages.pop(index, None)
        del page
    def toggle_new_pages(self):
        self.newPagesPossible = not self.newPagesPossible

# dialog page object to store actual dialog data
class dialogPage:
    choices = []
    choicesPossible = True
    speaker = "none"
    emotion = "none"
    text = "filler"
    def __init__(self, parent_node):
        self.parent_node = parent_node
    def __str__(self):
        string = [  
                    '{', 
                    f'"speaker":"{self.speaker}",',
                    f'"emotion":"{self.emotion}",',
                    f'"text":"{self.text}",',
                 ]
        # if there are any choices, append them
        if len(choices) > 0:
            string.append('"choices":\n\t{')
            for choice in choices:
                string.append(f'\t{str(choice)}')
            string.append('\n\t}')
        else:
            string.append('"choices":"none"')
        string = '\n\t'.join(string)
        string += '\n}'
        return string
    def set_speaker(self, speaker):
        self.speaker = speaker
    def set_emotion(self, emotion):
        self.emotion = emotion
    def set_text(self, text):
        self.text = text
    def add_choice(self, choice):
        self.choices.add(choice)
        if len(self.choices) == 4:
            self.choicesPossible = False 
        elif len(self.choices == 1):
            self.parent_node.toggle_new_pages()
    def delete_choice(self, index):
        choice = self.choices.pop(index, None)
        self.choicesPossible = True
        del choice
        if len(self.choices) == 0:
            self.parent_node.toggle_new_pages()
        
        
# dialog choice object to store choice data/outcomes
class dialogChoice:
    text = "filler"
    emotion = "default"
    consequence = "none"
    target_node = "none"
    def __init__(self, parent_node):
        self.parent_node = parent_node
    def __str__(self):
        string = [
                    '{',
                    f'"emotion":"{self.emotion}",',
                    f'"text":"{self.text}",',
                    f'"consequence":"{self.consequence}"',
                    f'"target":"{self.parent_node.print_title()}"'
                 ]
        string = '\n\t'.join(string)
        string += '\n}'
        return string
    def set_emotion(self, emotion):
        self.emotion = emotion
    def set_text(self, text):
        self.text = text
    def set_consequence(self, consequence):
        self.consequence = consequence
    def set_target_node(self, node):
        self.target_node = node
        
# function to turn dialog directory into treeView
