from mycroft import MycroftSkill, intent_handler, intent_file_handler
from adapt.intent import IntentBuilder
from .SimpleNoteManagerClass import SimpleNoteManagerClass

class SimpleNoteManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.sn = None

    def initialize(self):
        ''' retrieve online settings from https://account.mycroft.ai/skills
            and create SimpleNote manager instance
        '''
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.sn = SimpleNoteManagerClass(username,password)
    
    def stop(self):
        pass



    @intent_handler('create.note.intent')
    def createNote(self,message):
        ''' Function to create a note or pinned note
        '''
        #retrieve the title and tag
        (title,tag) = self.retrieveTitleAndTag(message)
        if title is None:
            return

        #determine if note should be pinned
        utterance = message.data.get('utterance')
        if (self.voc_match(utterance,'pinned')):
            pinned = True
        else:
            pinned = False

        #create note and say so
        self.speak_dialog('create.note', {'title':title})
        self.sn.createNote(title,tag,pinned)

    @intent_handler('add.to.note.intent')
    def addToNote(self,message):
        ''' function to add lines or list items to a note
        '''
        #assume not a list
        list_item = False

        #retrieve the title and tag of the note
        (title,tag) = self.retrieveTitleAndTag(message)
        if title is None:
            return
        if (title == 'shopping list'):
            list_item = True

        #retrieve the content to add to the note
        content = self.retrieveContent(message,title,'add to')

        #add the content and say so
        self.speak_dialog('add.to.note',{'title':title,'content':content})
        self.sn.addContent(self.sn.findNote(tag),content,list_item)

        another = True
        while another:
            another = False
            response = self.get_response('anything.else', data = {'action':'add'}, num_retries=0)
            if ((response is None) or
                (self.voc_match(response,'no'))):
                self.speak_dialog('ok')
                return
            else:
                another = True
                content = response
                self.speak_dialog('add.to.note',{'title':title,'content':content})
                self.sn.addContent(self.sn.findNote(tag),content,list_item)
        

    @intent_handler('remove.from.note.intent')
    def removeFromNote(self,message):
        ''' function to remove search tems or checked items from a note
        '''
        #retrieve the title and tag of the note
        (title,tag) = self.retrieveTitleAndTag(message)
        if title is None:
            return
        
        #determine if checked items are to be removed
        utterance = message.data.get('utterance')
        # if ((utterance.find('checked boxes') != -1) or
        #     (utterance.find('checked items') != -1) or
        #     (utterance.find('checkboxes') != -1)):
        if (self.voc_match(utterance,'checked.items')):

            #if so, remove them and say so
            self.speak_dialog('remove.from.note',{'title':title,'content':'checked boxes'})
            self.sn.removeCheckedItems(self.sn.findNote(tag))

        #otherwise, retrieve the search term, remove those lines, and say so
        else:
            content = self.retrieveContent(message,title,'remove from')

            self.speak_dialog('remove.from.note',{'title':title,'content':content})
            self.sn.removeSearchLine(self.sn.findNote(tag),content)
    

    @intent_handler('read.note.intent')
    def readNote(self,message):
        ''' function to read a note line by line
        '''
        #retrieve title and tag of note to read, and say so
        (title,tag) = self.retrieveTitleAndTag(message)
        if title is None:
            return
        self.speak_dialog('read.note',{'title':title})

        #actually retrieve and read each line
        contentlines = self.sn.getContentLines(self.sn.findNote(tag))
        for line in contentlines:
            self.speak(line)


    @intent_handler('find.in.note.intent')
    def findInNote(self,message):
        ''' function to find content in a note and read the line
        '''
        (title,tag) = self.retrieveTitleAndTag(message)
        content = self.retrieveContent(message,title,'find in')
        if title is None or content is None:
            return
        
        (success,contentlines) = self.sn.searchNote(self.sn.findNote(tag),content)
        if (contentlines == []):
            self.speak_dialog('not.found',data={'content':content})
            return
        else:
            self.speak_dialog('yes')
            for line in contentlines:
                self.speak(line[1])


    def retrieveTitleAndTag(self,message):
        ''' function to retrieve the desired title and tag from an utterance
        '''
        #retrieve full spoken string, the utterance
        utterance = message.data.get('utterance')

        #handle the shopping list special, to simplify which utterances trigger it
        if (self.voc_match(utterance,'shopping.list')):
            title = 'shopping list'
            tag = 'shopping_list'
        
        #if its not the shopping list, retrieve the title
        else:
            title = message.data.get('title')
            if title is None:
                #if the utterance didnt contain the title, ask again, with 1 retry
                response = self.get_response('get.title', num_retries=1)
                if response is None:
                    self.speak_dialog('failed.to.get.title')
                    return (None,None)
                title = response
            tag = '_'.join(title.split(' '))
        return (title,tag)

    def retrieveContent(self,message,title,action):
        content = message.data.get('content')
        if content is None:
            response = self.get_response('get.content',data={'action':action,'title':title}, num_retries=1)
            if response is None:
                return
            content = response
        return content
    


def create_skill():
    return SimpleNoteManager()

