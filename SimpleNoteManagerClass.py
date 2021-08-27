from tkinter import NONE
import simplenote



class SimpleNoteManagerClass():
    def __init__(self,username, password):
        #self.sn = sn
        self.sn = simplenote.Simplenote(username, password)


    def findNote(self, tag):
        '''return note object, specifically the first one with a given tag'''

        #note = self.sn.get_note_list(data=True, since=None, tags=[tag])[0][0]
        (note_list,success) = self.sn.get_note_list(data=True, since=None, tags=[tag])
        #if the notelist is retrieved and nonempty, return note
        if ((success == 0) and (len(note_list) != 0)):
                note = note_list[0]
                return note

        else:
            return None
        

    def createNote(self, title, tag, pinned=False):
        '''create an entirely new note'''

        #generate the note
        note_content = "# {} \r\n ".format(title)
        note_system_tags = ['markdown']
        if (pinned):
            note_system_tags.append('pinned')

        note = {'content' : note_content, 'tags' : [tag], 'systemtags': note_system_tags}

        #create the note online, check for success
        (note,success) = self.sn.add_note(note)
        if (success == 0):
            return note
        else:
            return None

    def addContent(self, note, newcontent, listitem,  debug = False):
        '''add items to the passed note, add it as a listitem if listitem==True'''

        #if the note doesn't exist, say so
        if (note == None):
            return False

        #retrieve content and append new content
        note_content = note['content']
        if (listitem):
            new_note_content = "{} \r\n- [ ] {}".format(note_content, newcontent)
        else:
            new_note_content = "{} \r\n{}".format(note_content, newcontent)

        #update the note online with the new content
        note['content'] = new_note_content
        self.sn.update_note(note)

        if (debug):
            print(note_content['content'])

        #if everything goes well, say so
        return True


    def removeCheckedItems(self,note):
        '''remove all lines with checked boxes from passed note'''

        #if the note doesn't exist, say so
        if (note == None):
            return False

        #search through each line
        note_content = note['content']
        note_lines = note_content.split("\n")

        #keep each unchecked line
        new_lines = []
        for line in note_lines:
            #print(line[:5])
            if (line[:5] != '- [x]'):
                new_lines.append(line)

        #update the note
        new_note_content = "\n".join(new_lines)
        note['content'] = new_note_content
        self.sn.update_note(note)

        #if everything goes well, say so
        return True


    def searchNote(self, note, search_term):
        '''search each line of a note for term, return each positive line's (index, content)'''

        #if the note doesn't exist, say so
        if (note == None):
            return (False,[])

        #go through each line
        note_content = note['content']
        note_lines = note_content.split("\n")
        found_lines = []
        for i in range(len(note_lines)):
            #store each successful line
            if (note_lines[i].lower().find(search_term.lower()) != -1):
                found_lines.append((i,note_lines[i]))
                
        #if all goes well, return true and the found lines lists
        return (True, found_lines)

    def removeSearchLine(self, note, search_term):
        '''remove every line with containing searchitem'''

        #if the note doesn't exist, say so
        if (note == None):
            return False

        #find lines containing search_term
        (success,found_lines) = self.searchNote(note, search_term)

        #if search failed, say so
        if not (success):
            return False

        #remove lines with search_term
        note_content = note['content']
        note_lines = note_content.split("\n")

        for line in found_lines:
            note_lines.pop(line[0])

        #update note online
        new_note_content = "\n".join(note_lines)
        note['content'] = new_note_content
        self.sn.update_note(note)

        #if everything goes well, say so
        return True
        

if __name__ == '__main__':
    pass
    #sn = SimpleNoteManagerClass(u,p)
    #shopping_list_note = sn.findNote('ShoppingList')

    # simplenoteinstance = simplenote.Simplenote(username, password)
    #sn.addShoppingListItem("heres hoping")
    #sn.removeCheckedItems()
    #sn.searchShoppingList("moose")
    # sn.removeSearchLine(shopping_list_note,"Remove")
    #sn.addContent(shopping_list_note,"Woot I do say", True)
    # sn.removeCheckedItems(shopping_list_note)

    # print(shopping_list_note)
    #note = sn.findNote('space')
    #print(note)
    #print(sn.createNote("Whats up space invaders!!!", "space invaders"))
