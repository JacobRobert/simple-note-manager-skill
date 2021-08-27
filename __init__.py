from mycroft import MycroftSkill, intent_file_handler
from SimpleNoteManagerClass import SimpleNoteManagerClass

class SimpleNoteManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.sn = SimpleNoteManagerClass(username,password)
    
    def stop(self):
        pass


    @intent_file_handler('manager.note.simple.intent')
    def handle_manager_note_simple(self, message):
        content = message.data.get('content')
        line = message.data.get('line')
        title = message.data.get('title')

        self.speak_dialog('manager.note.simple', data={
            'content': content,
            'line': line,
            'title': title
        })


def create_skill():
    return SimpleNoteManager()

