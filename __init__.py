from mycroft import MycroftSkill, intent_file_handler


class SimpleNoteManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

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

