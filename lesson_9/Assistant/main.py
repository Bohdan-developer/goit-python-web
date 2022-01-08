import os
import shutil
import time
from abc import ABC, abstractmethod
from collections import Counter, OrderedDict
from sqlalchemy.orm import joinedload
from prettytable import PrettyTable

from db import *
from models import *

try:
    from AddressBook import *
except:
    from .AddressBook import *

AB = AddressBook()

wrong = lambda: 'Please retype the command correctly'


class InfoInterface(ABC):
    @abstractmethod
    def print_info():
        pass


class AllContacts(InfoInterface):
    def print_info():
        pretty_contacts = PrettyTable()
        pretty_contacts.field_names = ['Name', 'Address', 'Phone', 'Email', 'Birthday']

        list_info = list()

        result = session.query(Contact).options(joinedload('phones_rel'), joinedload('birthdays_rel'),
                     joinedload('address_rel'), joinedload('emails_rel')).all()

        for name in result:
            list_info.append(name.name)
            if name.address_rel:
                for address in name.address_rel:
                    list_info.append(address.address)
            else:
                list_info.append("")
            for phone in name.phones_rel:
                list_info.append(phone.phone)
            if name.emails_rel:
                for email in name.emails_rel:
                    list_info.append(email.email)
            else:
                list_info.append("")
            for birthday in name.birthdays_rel:
                list_info.append(birthday.birthday)
            pretty_contacts.add_row(list_info)
            list_info = list()
        return pretty_contacts    


class AllNoteTags(InfoInterface):
    def print_info():
        search_path = '.'
        file_type = '.txt'
        taglist = []
        if not (search_path.endswith("/") or search_path.endswith("\\")):
            search_path = search_path + "/"


class Help(InfoInterface):
    def print_info():
        table = PrettyTable()
        table.title = 'Use these commands bellow or "exit" to stop work'
        table.field_names = ['ADD INFO', 'CHANGE INFO',
                             'Notes&Tags', 'Additionally']

        table.add_rows(
            [
                ['add contact', 'change contact', 'create note', 'near birthday'],
                ['add address', 'find contact', 'change note', 'search by tags'],  # Correction shortened search by tags
                ['add email', 'show contacts', 'change tag', 'search by text'],  # Correction shortened search by text
                ['add birthday', 'delete contact', 'delete note', 'sorting files'],
                ['', '', 'read note', 'show all tags']
            ]
        )
        return table


class NearbyBirthday(InfoInterface):
    def print_info():
        n_days = input('Enter number of days: ')
        return AB.nearby_birthday(n_days)


def add_contact():
    name = input('Enter Name: ')
    phone = input('Enter Phone number: ')
    birthday = input('Enter Birthday in format 01.01.1990: ')
    if AB.validate_birthday(birthday) and AB.validate_phone(phone):

        contact = Contact(name=name)
        session.add(contact)
        session.commit()
        result = session.query(Contact.contact_id).filter(Contact.name==name).first()
        contact_birthday = Birthday(contact_id = result.contact_id, birthday=birthday)
        contact_phone = Phone(contact_id = result.contact_id, phone=phone)
        session.add(contact_phone)
        session.add(contact_birthday)
        session.commit()
              
        AB.add_contact(name, phone, birthday)
        return f'Contact {name} with phone number {phone} and birthday {birthday} created.'
    else:
        return f'Incorrect number. Try in format +380123456789'


def add_email():
    name = input('Enter Name: ')
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found" 
    



    email = input('Enter Email: ')
    if AB.validate_email(email):
        if result : 
            
            contact_email = Email(contact_id = id, email=email)
            session.add(contact_email)
            session.commit()
          
            return f'{name}`s email {email} has been saved'
    else:
        return f'Incorrect email'


def add_address():
    name = input('Enter Name: ')
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found"  
    address = input('Enter Address: ')
    contact_address = Address(contact_id = id, address=address)
    session.add(contact_address)
    session.commit()
    return f'{name}`s address is {address}'


def add_birthday():
    name = input('Enter Name: ')
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found" 
    birthday = input('Enter Birthday in format 01.01.1990: ')
    print(birthday)
    if AB.validate_birthday(birthday):
        
        session.query(Birthday).filter(Birthday.contact_id==id).\
                update({Birthday.birthday : birthday}, synchronize_session=False)
        session.commit()
       
        return f'{name}`s birthday {birthday} has been saved'
    else:
        return f'Incorrect date'


def change_contact():
    
    name = input('Enter Name: ')
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found" 
    
    address = input('Enter Address: ')
    phone = input('Enter Phone number: ')
    email = input('Enter Email: ')
    birthday = input('Enter Birthday: ')

    if AB.validate_birthday(birthday) and AB.validate_email(email) and AB.validate_phone(phone):
        
        if session.query(Address.address).filter(Address.contact_id==id):
            session.query(Address).filter(Address.contact_id==id).\
                        update({Address.address : address}, synchronize_session=False)

        if session.query(Phone).filter(Phone.contact_id==id):
            session.query(Phone).filter(Phone.contact_id==id).\
                        update({Phone.phone : phone}, synchronize_session=False)

        if session.query(Email).filter(Email.contact_id==result.id):
            session.query(Email).filter(Email.contact_id==result.id).\
                        update({Email.email : email}, synchronize_session=False)

        if session.query(Birthday).filter(Birthday.contact_id==result.id):
            session.query(Birthday).filter(Birthday.contact_id==result.id).\
                        update({Birthday.birthday : birthday}, synchronize_session=False)

        session.commit()

        AB.change_contact(name, address, phone, email, birthday)
        return f'{name}`s :\n Address: {address}, Phone: {phone}, Email: {email}, Birthday: {birthday}'
    else:
        return 'Incorrect data (email, phone number or birthday)'


def find_contact():
    name = input('Enter Name of the contact: ')
    
    pretty_contact = PrettyTable()
    pretty_contact.field_names = ['Name', 'Address', 'Phone', 'Email', 'Birthday']
    
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found" 
   
    email=["",]
    address=["",]

    if result : 
        name = result.name
        
        if session.query(Address.address).filter(Address.contact_id==id).first():
            address = session.query(Address.address).filter(Address.contact_id==id).first()
        
        phone = session.query(Phone.phone).filter(Phone.contact_id==id).first()
        
        if session.query(Email.email).filter(Email.contact_id==id).first():
            email = session.query(Email.email).filter(Email.contact_id==id).first()
        
        birthday = session.query(Birthday.birthday).filter(Birthday.contact_id==id).first()
        
        pretty_contact.add_row([name, address[0], phone[0], email[0], birthday[0]])

    return pretty_contact
         

def delete_contact():
    name = input('Enter Name of the contact: ')
    try:
        result = session.query(Contact).filter(Contact.name==name).first()
        id = result.contact_id
    except:
        return f"This {name} contact not found" 
    
    

    if result : 
        result = session.query(Contact).get(id) 
        session.delete(result)
        session.commit()

        return f'Contact {name} was deleted!'


def create_new_note():
    tags = input('Enter tags separated by space and starting with "#": ')
    note = input('Enter text of your note: ')
    data = f'{tags}\n\n{note}'
    t = str(time.time()).split('.')[0]
    filename = t + ".txt"  # Name would be similar to 1630063227.txt
    try:
        with open(filename, "w") as file:
            file.write(data)
    except IOError:
        print("File not accessible")
    return f'You have created a note {filename}'


def delete_note():
    filename = input("Enter FileName: ")
    path = os.getcwd()
    if os.path.isfile(filename):
        os.remove(os.path.join(path, filename))
        return f'{filename} deleted'
    else:
        return 'wrong FileName'


def read_note():
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, encoding='utf8') as file:
            data = file.read()
        return (data)  # Correction changed to return
    except:
        return ('File not found')  # Correction changed to return


def note_search():
    search_path = '.'
    file_type = '.txt'
    search_str = input('Please enter the text/word you are looking for: ')

    if not (search_path.endswith("/") or search_path.endswith("\\")):
        search_path = search_path + "/"

    for fname in os.listdir(path=search_path):
        if fname.endswith(file_type):
            fo = open(search_path + fname)
            line = fo.readline()
            line = fo.readline()
            line = fo.readline()
            index = line.find(search_str)
            if (index != -1):
                print(fname, line, sep=" ")
            fo.close()
    return 'Search complete'


def note_update():
    global note
    file_to_open = input('Enter the full name of the note you want to update: ')
    try:
        with open(file_to_open, 'r') as file:
            data = file.readlines()

        print('Current note is: ')
        print(data[1][:-1])
        note = input("Update a note: ") + '\n'  # note input
        data[-1] = note

        with open(file_to_open, 'w') as file:
            file.writelines(data)
    except IOError:
        print("File not accessible")
    return f'The note {file_to_open} is changed to: {note}'


def tag_search_helper(tag: str, flist: list, filename: str, text: str):
    # Tags we're looking for in the first line, lowercase
    if tag != '%%%%%%%%%%' and ((tag.lower() + ' ') in text.lower()):
        flist.append(filename)
    return flist


def tag_search():
    deftags = ['%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%', '%%%%%%%%%%']
    tags = input('Enter up to six tags separated by space: ')  # Correction Separated by space
    tags = tags.split(' ')
    tags.extend(deftags)
    tags = tags[:6]
    search_path = '.'
    file_type = '.txt'
    flist = []

    if not (search_path.endswith("/") or search_path.endswith("\\")):
        search_path = search_path + "/"

    for fname in os.listdir(path=search_path):
        if fname.endswith(file_type):
            fo = open(search_path + fname)
            line = fo.readline()
            flist = tag_search_helper(tags[0], flist, fname, line)
            flist = tag_search_helper(tags[1], flist, fname, line)
            flist = tag_search_helper(tags[2], flist, fname, line)
            flist = tag_search_helper(tags[3], flist, fname, line)
            flist = tag_search_helper(tags[4], flist, fname, line)
            flist = tag_search_helper(tags[5], flist, fname, line)
            fo.close()

    result = Counter(flist)
    result = OrderedDict(result.most_common())
    if not result:
        return 'No match!'
    else:
        print("Matches in Files:")
        for key, value in result.items():
            print(f'{value} : {key}')
    return 'Sorted in descending order'


def tag_update():

    global tags
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, 'r') as file:
            data = file.readlines()

        print('Current tags are: ')
        print(data[0][:-1])
        tags = input('Write tags: ') + '\n'
        data[0] = tags

        with open(file_to_open, 'w') as file:
            file.writelines(data)

    except IOError:
        print("File not accessible")
    return f'New tags of the note {file_to_open} are as follows: {tags}'


def sorting_files():
    p = input('Enter to the path to the directory: ')
    if not p:
        return 'path to directory not specified'
    else:
        print(f'Started in {p}')

        images_list = list()
        video_list = list()
        documents_list = list()
        music_list = list()
        archives_list = list()

        suffix_imeges = ".jpeg", ".png", ".jpg"
        suffix_videos = ".avi", ".mp4", ".mov"
        suffix_documents = ".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"
        suffix_music = ".mp3", ".ogg", ".wav", ".amr"
        suffix_archiv = ".zip", ".tar", ".gztar", ".bztar", ".xztar"

        ignor = "archives", "images", "music", "videos", "documents"

        def serch(p):

            for i in os.listdir(p):
                if i not in ignor:
                    if os.path.isdir(p + "\\" + i):
                        serch(p + "\\" + i)

            for root, dirs, files in os.walk(p):
                for file in files:
                    i = os.path.join(root, file)
                    sort_file(i, file)
                    unpuck_archives(i, file)

                for folder in dirs:
                    f = os.path.join(root, folder)
                    remove_folder(f)

        def creat_folder():

            if len(images_list) != 0:
                if not os.path.exists(p + "\\images"):
                    os.mkdir(p + "\\images")
            if len(video_list) != 0:
                if not os.path.exists(p + "\\videos"):
                    os.mkdir(p + "\\videos")
            if len(documents_list) != 0:
                if not os.path.exists(p + "\\documents"):
                    os.mkdir(p + "\\documents")
            if len(music_list) != 0:
                if not os.path.exists(p + "\\music"):
                    os.mkdir(p + "\\music")
            if len(archives_list) != 0:
                if not os.path.exists(p + "\\archives"):
                    os.mkdir(p + "\\archives")

        def sort_file(i, file):

            if file.endswith(suffix_imeges):
                if file not in images_list:
                    images_list.append(file)
                creat_folder()
                if i != p + "\\images" + "\\" + file:
                    os.replace(i, p + "\\images" + "\\" + file)
            elif file.endswith(suffix_videos):
                if file not in video_list:
                    video_list.append(file)
                creat_folder()
                if i != p + "\\videos" + "\\" + file:
                    os.replace(i, p + "\\videos" + "\\" + file)
            elif file.endswith(suffix_documents):
                if file not in documents_list:
                    documents_list.append(file)
                creat_folder()
                if i != p + "\\documents" + "\\" + file:
                    os.replace(i, p + "\\documents" + "\\" + file)
            elif file.endswith(suffix_music):
                if file not in music_list:
                    music_list.append(file)
                creat_folder()
                if i != p + "\\music" + "\\" + file:
                    os.replace(i, p + "\\music" + "\\" + file)

        def remove_folder(f):
            if not os.listdir(f):
                os.removedirs(f)

        def unpuck_archives(i, file):

            if file.endswith(suffix_archiv):
                if file not in archives_list:
                    archives_list.append(file)
                creat_folder()
                name_folder_archive = file.split(".")
                shutil.unpack_archive(i, p + "\\archives" + "\\" + name_folder_archive[0])

        serch(p)
        return (f"Sorting files by the specified path {p} completed succesfully!")


OPERATIONS = {
    'add contact': add_contact,
    'add address': add_address,
    'add email': add_email,
    'add birthday': add_birthday,
    'change contact': change_contact,
    'find contact': find_contact,
    'near birthday': NearbyBirthday.print_info,
    'delete contact': delete_contact,
    'show contacts': AllContacts.print_info,
    'create note': create_new_note,
    'delete note': delete_note,
    'change note': note_update,
    'change tag': tag_update,
    'search by tags': tag_search,  # Correction shortened search by tags
    'search by text': note_search,  # Correction shortened search by text
    'sorting files': sorting_files,
    'help': Help.print_info,
    'show all tags': AllNoteTags.print_info,
    'read note': read_note
}


def get_handler(operator):
    if not OPERATIONS.get(operator):
        return wrong
    return OPERATIONS[operator]


if __name__ == '__main__':
    # Start of the cli

    print('Hello, User! Welcome to our CLI-bot. Enter "help" in case you need to see the commands again')
    print(Help.print_info())

    while True:
        try:
            command = input('Enter your command: ')
        except EOFError:
            break

        if command == '.' or command == 'exit' or command == 'close':
            
            print('Goodbye, User!')
            break
        handler = get_handler(command)
        answer = handler()
        print(answer)


