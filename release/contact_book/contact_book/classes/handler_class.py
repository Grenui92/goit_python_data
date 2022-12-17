from classes.abstract_class import MainMethods, ShowMethods
from classes.class_contact_book import ContactBook, Record, Birthday
from classes.class_note_book import NoteBook, Note
from classes.decorators import bug_catcher
from classes.file_checker import FileSorter
from datetime import date, timedelta
from os import path



class WorkContact(MainMethods, ShowMethods):
    def __init__(self):
        self.book = ContactBook()
        try:
            self.book.load_from_file()
        except FileNotFoundError:
            self.book.save_to_file()

    def create(self, name: str, *_) -> str:
        if name in self.book.keys():
            return f"Contact with name {name} already exist. Try another name."
        elif not name:
            return "You can't create empty name contact."
        else:
            self.book[name] = Record(name)
            return f"Contact {name} successfully created."

    def add_values(self, name, info):
        record = self.book[name]
        field = info[0]
        if field == "phones":
            return record.add_phone(info[1])
        elif field == "emails":
            return record.add_email(info[1])
        elif field == "address":
            return record.add_address(" ".join(info[1:]))
        elif field == "birthday":
            return record.set_birthday(info[1])
        else:
            return f"I can't find field '{field}'."

    def show_all(self, *_) -> list:
        result = []
        for k, v in self.book.items():
            result.append(f"Contact {k} has information:\n"
                          f"\tphones: {[num.value for num in v.phones] if v.phones else v.phones}\n"
                          f"\temails: {[mail.value for mail in v.emails] if v.emails else v.emails}\n"
                          f"\taddress: {[adr.value for adr in v.address] if v.address else v.address}\n"
                          f"\tbirthday: {v.birthday.value if isinstance(v.birthday, Birthday) else v.birthday}\n")
        return result

    def show_one(self, name: str, *_) -> str:
        v = self.book[name]
        return f"Contact {name} has information:\n" \
               f"\tphones: {[num.value for num in v.phones] if v.phones else v.phones}\n" \
               f"\temails: {[mail.value for mail in v.emails] if v.emails else v.emails}\n" \
               f"\taddress: {[adr.value for adr in v.address] if v.address else v.address}\n" \
               f"\tbirthday: {v.birthday.value if isinstance(v.birthday, Birthday) else v.birthday}\n"

    def show_page(self, number, *_):
        all_book = []
        for n_contacts in self.book.iterator(number):
            # result = []
            # for contact in n_contacts:
            #     result.append(f"Contact {contact.name.value} has information:\n"
            #                   f"\tphones: {[num.value for num in contact.phones] if contact.phones else contact.phones}\n"
            #                   f"\temails: {[mail.value for mail in contact.emails] if contact.emails else contact.emails}\n"
            #                   f"\taddress: {[adr.value for adr in contact.address] if contact.address else contact.address}\n"
            #                   f"\tbirthday: {contact.birthday.value if isinstance(contact.birthday, Birthday) else contact.birthday}\n")
            all_book.append(n_contacts)
        return all_book

    def delete_all(self, *_) -> str:
        answer = input("You want to delete all your contacts. Are you sure? Y/N: ")
        if answer.upper() == "Y":
            self.book.clear()
            return "ContactBook is clear."
        else:
            return "Operation 'delete all contacts' canceled."

    def delete_one(self, name, *_) -> str:
        del self.book[name]
        return f"Contact named {name} successfully deleted."

    def save_to_file(self, *_):
        return self.book.save_to_file()

    def load_from_file(self, *_):
        return self.book.load_from_file()

    def edit_information(self, name, data):
        record = self.book[name]  # Check if this record exists
        field, old, new = data[0], data[1], data[2]
        return record.edit_contact_information(field, old, new)

    def edit_name(self, old_name, info):
        new_name = info[0]
        if old_name == new_name:
            return f"Old name '{old_name}' == New name '{new_name}'."
        if new_name not in self.book:
            self.book[old_name].name.value = new_name
            self.book[new_name] = self.book[old_name]
        del self.book[old_name]
        return f"Name '{old_name}' successfully changed to '{new_name}'."

    def search_in(self, name: str, data: list):
        search = " ".join([name, *data])
        result = []
        for key, record in self.book.items():
            if search in key:
                result.append(f"Combination {search} find in contact name {key}.")
            for number in record.phones:
                if search in number.value:
                    result.append(f"Combination {search} find in telephone number {number.value} named {key}.")
            for email in record.emails:
                if search in email.value:
                    result.append(f"Combination {search} find in email {email.value} named {key}.")
            for address in record.address:
                if search in address.value:
                    result.append(f"Combination {search} find in address {address.value} named {key}.")
        return result

    def show_nearest_birthdays(self, days: str, *_) -> list:
        """Here we call information about birthdays which will happen within the next DAYS days.
        If DAYS argument is empty - default DAYS in show_upcoming_birthday() == 7"""

        if days:
            n = int(days)
        else:
            n = 7
        result = []
        for k, v in self.book.items():
            if isinstance(v.birthday, Birthday):
                next_birthday = date(year=date.today().year, month=v.birthday.value.month, day=v.birthday.value.day)
                if next_birthday - date.today() <= timedelta(0):
                    next_birthday = date(year=date.today().year + 1, month=v.birthday.value.month, day=v.birthday.value.day)
                if next_birthday - date.today() < timedelta(n):
                    result.append(f"{k} birthday in {v.birthday.value}.")
        return result

    def days_to_birthday(self, name: str, *_) -> str:
        record = self.book[name]  # Check if this record exists
        return record.days_to_birthday()

    def days_to_birthday_for_all(self, *_) -> list:
        result = []
        for k, v in self.book.items():
            if isinstance(v.birthday, str):
                result.append(f"Days to {v.name.value}'s birthday UNKNOWN.")
            else:
                next_birthday = date(year=date.today().year, month=v.birthday.value.month, day=v.birthday.value.day)
                if next_birthday - date.today() <= timedelta(0):
                    next_birthday = date(year=date.today().year + 1, month=v.birthday.value.month, day=v.birthday.value.day)
                result.append(f"Days to {v.name.value}'s birthday {(next_birthday - date.today()).days}.")
        return result


class WorkNote(MainMethods, ShowMethods):
    def __init__(self):
        self.notes = NoteBook()
        try:
            self.notes.load_from_file()
        except FileNotFoundError:
            self.notes.save_to_file()

    def create(self, name: str, info: list) -> str:
        if name in self.notes:
            raise KeyError(f"Note with name {name} already exist.")
        elif not name:
            return "You can't create empty note."
        else:
            tags = []
            for piece in info:  # Search tags in all text
                if piece.startswith("#"):
                    tags.append(piece)
            info_new = " ".join(info)
            self.notes[name] = Note(name, tags, info_new)
            return f"Note with name {name} successfully create."

    def add_values(self, name, info):
        record = self.notes[name]
        return record.add_content(" ".join(info))

    def show_all(self, *_) -> list:
        result = []
        for name, note in self.notes.items():
            result.append(f"Name: {note.name}\n"
                          f"\tTags: {note.tags}\n"
                          f"\tText: {note.text}\n")
        return result

    def show_one(self, name: str, *_) -> str:
        note = self.notes[name]
        return f"Name: {note.name}\n" \
               f"\tTags: {note.tags}\n" \
               f"\tText: {note.text}\n"

    def show_page(self, number: str, *_):
        all_book = []
        for n_notes in self.notes.iterator(number):
            # result = []
            # for note in n_notes:
            #     result.append(f"Name: {note.name}\n"
            #                   f"\tTags: {note.tags}\n"
            #                   f"\tText: {note.text}\n")
            all_book.append(n_notes)
        return all_book

    def delete_all(self, *_):
        answer = input("You want to delete all your notes. Are you sure? Y/N: ")
        if answer.upper() == "Y":
            self.notes.clear()
            return "Note book successfully cleared"
        else:
            return "Operation 'delete all notes' canceled."

    def delete_one(self, name, *_) -> str:
        del self.notes[name]
        return f"Note named {name} successfully deleted."

    def save_to_file(self, *_):
        return self.notes.save_to_file()

    def load_from_file(self, *_):
        return self.notes.load_from_file()

    def edit_information(self, name, info):
        record = self.notes[name]
        record.clear_tags()
        record.clear_text()
        return record.add_content(info)

    def edit_name(self, old_name, info):
        new_name = info[0]
        if old_name == new_name:
            return f"Old name '{old_name}' == New name '{new_name}'."
        if new_name not in self.notes:
            self.notes[old_name].name.value = new_name
            self.notes[new_name] = self.notes[old_name]
        del self.notes[old_name]
        return f"Name '{old_name}' successfully changed to '{new_name}'."

    def search_in(self, name: str, data: list):
        info = " ".join([name, *data])
        result = []
        for note in self.notes.values():
            if info in note.text or info == note.name or info in note.tags:
                if not result:
                    result = [f"Search results for {info} in text:\n"]
                result.append(f"Name: {note.name}\n"
                              f"\tTags: {note.tags}\n"
                              f"\tText: {note.text}\n")
        return result if result else [f"Search results for {info} in text:\nEmpty"]

    def sorted_by_tags(self, *args):
        tags = [*args]
        result = []
        for note in self.notes.values():
            cnt = 0
            for tag in tags:  # Считаем сколько раз сумарно встречается каждый элемент из списка тегов в тегах записи
                if tag in note.tags:
                    cnt += 1 if tag in note.tags else 0
            result.append(f"Coincidences with tags {[i for i in tags if i]}: {cnt}\n"
                          f"Name: {note.name}\n"
                          f"\tTags: {note.tags}\n"
                          f"\tText: {note.text}\n")
        return sorted(result, reverse=True)


class Handler:

    def __init__(self):
        self.book = WorkContact()
        self.notes = WorkNote()
        self.commands = {"help": self.__help_me,
                         "instruction": self.__instructions,

                         "create_contact": self.book.create,
                         "show_contact_book": self.book.show_all,
                         "show_contact": self.book.show_one,
                         "show_contact_page": self.book.show_page,
                         "clear_contact_book": self.book.delete_all,
                         "delete_contact": self.book.delete_one,
                         "add_to_contact": self.book.add_values,
                         "edit_contact": self.book.edit_information,
                         "edit_contact_name": self.book.edit_name,
                         "search_in_contacts": self.book.search_in,
                         "show_birthdays": self.book.show_nearest_birthdays,
                         "days_to_birthday": self.book.days_to_birthday,
                         "show_all_birthdays": self.book.days_to_birthday_for_all,

                         "create_note": self.notes.create,
                         "show_note_book": self.notes.show_all,
                         "show_note": self.notes.show_one,
                         "show_note_page": self.notes.show_page,
                         "clear_note_book": self.notes.delete_all,
                         "delete_note": self.notes.delete_one,
                         "add_to_note": self.notes.add_values,
                         "edit_note": self.notes.edit_information,
                         "edit_note_name": self.notes.edit_name,
                         "search_in_notes": self.notes.search_in,
                         "sorted_by_tags": self.notes.sorted_by_tags,

                         "file_sorter": self.__file_sorter,

                         "exit": self.__good_bye}

    def main(self):
        while True:
            print("\nCommand 'help' will help you.")
            data = self.__input_user_text()
            result = self.__parse_user_text(data)
            self.__show_results(result)

    """MAIN"""

    @bug_catcher
    def __parse_user_text(self, text: str) -> list:
        """Search command and other information in user input."""

        data = text.split()
        if len(data) == 1:
            return self.__handler(command=data[0], name="", data="")
        else:
            return self.__handler(command=data[0], name=data[1], data=data[2:])

    @bug_catcher
    def __handler(self, command: str, name: str, data) -> str | list:
        """Here we find signatures and call functions"""
        if command in self.commands:
            return self.commands[command](name, data)
        else:
            raise Warning(command)

    @staticmethod
    @bug_catcher
    def __input_user_text() -> str:
        """User input."""
        data = input("Please enter what do you want to do: ")
        return data

    @staticmethod
    @bug_catcher
    def __show_results(result: str | list):
        """Print all results and information which functions return to us."""
        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)

    @bug_catcher
    def __good_bye(self, *_):
        print(self.book.save_to_file())
        print(self.notes.save_to_file())
        exit("Bye")

    @staticmethod
    @bug_catcher
    def __help_me(*_):
        return "If you want to know how to use this script - use command 'instruction' with:\n" \
               "'contacts' - to read about ContactBook commands.\n" \
               "'notes' - to read about NoteBook.\n" \
               "'file' - to read about FileSorter.\n" \
               "Or use 'exit' if you want to leave."

    @staticmethod
    @bug_catcher
    def __instructions(category, *_):
        if category == "contacts":
            main_path = path.join("instructions", "contact_book.txt")
        elif category == "notes":
            main_path = path.join("instructions", "note_book.txt")
        elif category == "file":
            main_path = path.join("instructions", "file_sorter.txt")
        else:
            raise ValueError(f"I can't find instruction for {category}.")
        with open(main_path, "r") as file:
            result = file.read()
        return result

    """END MAIN"""

    """FILE SORTER"""

    @staticmethod
    @bug_catcher
    def __file_sorter(path_for_sorting, *_):
        one_time = FileSorter(path_for_sorting)
        one_time.job()

    """END FILE SORTER"""
