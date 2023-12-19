
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.

from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog
from Profile import *
from ds_messenger import *
#import data_storage as ds

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.current_path=None
        self.selected_username=None
        self.my_name = 'wobuzhidao'
        self.my_psw = '123'

        # a list of the Post objects available in the active DSU file
        self._contacts = []

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    



    def get_selected_username(self)->str:
        'get the name selected in the treeview and then return it'
        try:
            index = int(self.posts_tree.selection()[0])
            selected_username=self.posts_tree.item(index)['text']
            #print(selected_username)
            #self.load_local_history(selected_username)
            self.selected_username = selected_username
            p = Path(".").joinpath(self.selected_username + '_TO_'+self.my_name+".dsu")
            self.current_path = p

            return selected_username
        except:
            pass


    def load_dm_list(self,dm_list:[str])->[DirectMessage]:
        '''Given a list which contians the string format of DirectMessage objects,transfer
        the string into the DirectMessage objects and return a list contian these DirectMessage objects.
        '''
        result = []
        for i in dm_list:
            if i.strip('\n') != '':
                obj = json.loads(i.strip('\n'))
                dm = DirectMessage()
                dm.sender = obj['sender']
                dm.recipient = obj['recipient']
                dm.message = obj['message']
                dm.timestamp = obj['timestamp']
                result.append(dm)

        #for i in result:
            #print(i.recipient)
            #print(i.message)
            #print(i.timestamp)
        return result


    def select_contact(self,event)->None:
        '''When the username in the treeview is selected, open the local file which stores the chat history with the
        selected user. Read DirectMessage from the file and load the contents by transferring string into DirectMessage
        objects. Clear out original contents in the display_editor text box and then post the loaded messege into the box.'''
        self.display_editor.delete(0.0, 'end')
        self.get_selected_username()
        with open(self.current_path, 'r') as f:
            local_contents = f.readlines()

        dm_list=self.load_dm_list(local_contents)
        self.process_dm_list( dm_list)



    def process_dm_list(self,dm_list:[DirectMessage]):
        '''Given a list of DirectMessage, sorted them according to the timestamp, and then post them in the
        display_editor text box along with the sender's name.'''
        sorted_list = sorted(dm_list, key=lambda x: float(x.timestamp))
        for dm in sorted_list:
           if dm.sender == self.selected_username or dm.sender == self.my_name:
                text=dm.sender.upper()+': '+dm.message
                self.display_editor.insert('end', text + '\n')
                self.display_editor.tag_add('others', '0.0', float(len(text)))
                self.display_editor.tag_config('others', justify='left', foreground="green")

            #self.display_editor.tag_add('me', '0.0', float(len(text)))




    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()



    def send_entry(self, text:str):
        '''Clear out messages in the entry_editor text box and insert such message into the display_editor text box.
        Display the text in green color.'''
        self.entry_editor.delete(0.0, 'end')
        text = self.my_name.upper() + ': ' + text
        self.display_editor.insert('end', text + '\n')
        self.display_editor.tag_add('others', '0.0', float(len(text)))
        self.display_editor.tag_config('others', justify='left', foreground="green")



    def insert_username(self, username:str):
        'Inserts the newly added unsername into the post_tree widget. Meanwhile, append the contacts list with the new username.'
        self._contacts.append(username)
        id = len(self._contacts) - 1  # adjust id for 0-base of treeview widget
        self._insert_post_tree(id, username)

    def _insert_post_tree(self, id, username:str):
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(username) > 25:
            username = username[:24] + "..."

        self.posts_tree.insert('', id, id, text=username)



    def reset_ui(self):
        """
            Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
            as when a new DSU file is loaded, for example.
        """
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []



    def _draw(self):
        'Call only once upon initialization to add widgets to the frame'
        posts_frame = tk.Frame(master=self, width=100)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.select_contact)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        display_frame = tk.Frame(master=self, bg="red",height=200)
        display_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="green")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.entry_editor = tk.Text(editor_frame, width=50,height=5)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=0, pady=0)

        self.display_editor = tk.Text(display_frame, width=0)
        self.display_editor.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False, padx=0, pady=0)



"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, add_user_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._add_user_callback = add_user_callback
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()



    def save_click(self):
        """
           Calls the callback function specified in the save_callback class attribute, if
           available, when the Send button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()

    def add_user_click(self):
        """
            Calls the callback function specified in the save_callback class attribute, if
            available, when the Send button has been clicked.
        """
        if self._save_callback is not None:
            self._add_user_callback()
    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)




    def _draw(self):
        'Call only once upon initialization to add widgets to the frame'
        save_button = tk.Button(master=self, text="Send", width=10)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

        user_button = tk.Button(master=self, text="Add User", width=10)
        user_button.configure(command=self.add_user_click)
        user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._my_name=None
        self._my_psw=None
        self._current_path =None
        self._current_profile =None
        self._current_recipient=None
        self.messenger=None
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self._load_history() # Retrieve all the messages received before everytime we open the program.



    def _load_history(self):
        '''Initialize a DirectMessenger object using my username and my password(it can be default or a changed account
        input by the user. Using this DirectMessenger object to retrieve all the chat history in the get_all_history() function
        and then add these retrieved chat history to the GUI.'''
        for item in self.body.posts_tree.get_children():
            self.body.posts_tree.delete(item)
        self._my_name = self.body.my_name
        # print(self._my_name)
        self._my_psw = self.body.my_psw
        # print(self._my_psw )
        self.messenger = DirectMessenger('168.235.86.101', self._my_name, self._my_psw)
        # print(self.messenger )
        try:
            all_history = self.get_all_history()
            self.add_retrived_history(all_history, self._my_name)
        except:
            self.display_error_message()


    def get_all_history(self)->{str:[DirectMessage]}:
        '''Using the DirectMessenger object initialized with my username and my password to retrieve all the chat history and get
        a list of DirectMessage objects. Putting these objects into a dictionary whose keys are the sender of these DirectMessage objects.
        Thus, we can get a list of DirectMessage objects followed by the same sender in a returned dictionary.'''
        lst = self.messenger.retrieve_all()
        #print(self.messenger)
        print(lst)

        hist = {}
        temp_lst = []
        for i in lst:
            set = [i.sender, i]
            temp_lst.append(set)
        for p in range(len(temp_lst)):
            if temp_lst[p][0] in hist.keys():
                hist[temp_lst[p][0]].append(temp_lst[p][1])
            else:
                hist[temp_lst[p][0]] = [temp_lst[p][1]]

        return hist


    def add_retrived_history(self,hist, my_name) -> None:
        '''Given the dictionary returned in the function get_all_history(), getting its keys--the sender of the
        DirectMessage-- and insert these senders into the treeview of the GUI. For each sender,
        create a corresponding dsu file locally with the name of the sender plus '_TO_' and my name. If the file
        already exists, it is unnecessary to create another file since the retrieved message has already been loaded.
        If the path does not exist, create a file and loaded all the DirectMessage sent from this sender into the file."
        '''
        try:
            for i in hist:
                #print(i)
                self.body.insert_username(i)
                p = Path('.').joinpath(i +'_TO_'+ self._my_name+'.dsu')
                print(p)
                if not p.exists():
                    p.touch()
                    for dm in hist[i]:
                        dm.save(p)
                else:
                    continue

        except:
            pass

    """
    Closes the program when the 'Close' menu item is clicked.
    
    def close(self):
        self.root.destroy()
    """

    def save_profile(self):
        '''This function will be called when the Send button has been clicked, to save the message sent into the local
        dsu file. To get the path for the dsu file, we assigned the current_path attribute stored in the body to the
        current_path attribute here( MainApp class). To store the message, we need to convert the string into a DirectMessage
        object, so we need the sender and the recipient of the message. Clearly, the sender will be my_name, and the recipient
        will be the name selected in the treeview so we get these values from the attributes stored in the Body class.
        The message of the DirectMessage object will be the contents in the entry_editor text box, so we call the
        get_text_entry() function. To send the message, we use the DirectMessenger object stored to send the message to the
        server. Finally, insert the message to the display textbox and delete contents in the entry_editor box.'''

        self._current_path = self.body.current_path  # To get the path for the dsu file to store the message

        self._my_name = self.body.my_name
        self._current_recipient = self.body.selected_username
        msg = self.body.get_text_entry()  # Get the contents in the entry_editor text box to send
        sent_dm=DirectMessage(self._my_name, self._current_recipient, msg, time.time()) #To  create the DirectMessage object

        sent_dm.save(self._current_path) # store the object into the dsu file. The save function is in the module of ds_messenger.py

        self.messenger.send(msg,self._current_recipient) # send the messge to the selected contact in the treeview using DirectMessenger object
        self.body.send_entry(msg)  # Clear the entry_editor textbox and insert the message into the display_editor text box.




    def new_chat_history(self,username):
        'If the new user is added into the treeview, we will create a corresponding dsu file locally to store the chat history.'
        p1 = Path(".").joinpath(username + '_TO_'+self._my_name+".dsu")
        if not p1.exists():  # check to see if temp_file.txt exists
            p1.touch()  # if temp_file.txt does not exist, create i


    def add_user(self) -> str:
        '''ask the user to add the username of the new contact and the insert the new username into the treeview.
        This function will be called when the add_user button has been clicked.'''
        username = tk.simpledialog.askstring('Add User', "Please input a new contact's username.")
        self.body.insert_username(username)
        self.new_chat_history(username)


    def change_account(self) -> str:
        '''Ask the user to set the username of the my account. This function will be called when the user clicked the change
        account menu. The program will ask the user for the new username and the new password. The the new accound has been added,
        the program will call self._load_history() again to get a new interface by deleting the original chat history and
         loaded the new chat history thought the function of retrieve all.'''

        self.body.my_name = tk.simpledialog.askstring('Set My Username', "Please input your username.")
        self.body.my_psw= tk.simpledialog.askstring('Set My password', "Please input your password.")
        self._load_history()

    def display_error_message(self):
        tk.messagebox.showerror(title='Error', message='The server does not respond. Please check the connection and ensure that your username or password are valid.')

    def _draw(self):
        'Call only once, upon initialization to add widgets to root frame'
        # Build a menu and add it to the root frame.

        menu_bar = tk.Menu(self.root)

        self.root['menu'] = menu_bar

        settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings, label='Settings')
        settings.add_command(label='Change the Account', command=self.change_account)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        #self.body = Body(self.root, self._current_path)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, save_callback=self.save_profile,add_user_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


    def load_new_message(self):
        """Retrieve new message per 2 seconds and get a list of DirectMessages. Using the function process_dm_list(new_dms) to
        send the message into the display_editor textbox. Save the message locally at the same time."""
        try:
            new_dms=self.messenger.retrieve_new()

            #print(dm_list)
            self.body.process_dm_list(new_dms)
            for i in new_dms:
                i.save(self._current_path)

            self.root.after(2000, self.load_new_message)
        except:
            self.display_error_message()



if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Final Project")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("780x540")

    # adding this option removes some legacy behavior with menus that modern OSes don't support.
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).


    main.after(2000, app.load_new_message)
    main.mainloop()
