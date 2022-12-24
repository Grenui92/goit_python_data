import difflib
def bug_catcher(func):

    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as exc:
            return exc.args[0]
        except KeyError as exc:
            return f"Wrong information: {exc.args[0]}"
        except Warning as exc:
            return find_word_with_wrong_key(exc.args[0], exc.args[1])
        except IndexError:
            return f"Not enough information for this command."
        except TypeError as exc:
            return exc.args[0]
        except FileExistsError as exc:
            return exc.args[0]
        except FileNotFoundError as exc:
            return exc.args[0]

    return inner

def find_word_with_wrong_key(srch: str, com) -> str:
    search_words = srch.split("_")
    result_list,result_dict  = [], {}
    print("commands keys", com)
    # com = ['help', 'instruction', 'create_contact', 'show_contact_book', 'show_contact', 'show_contact_page', 'clear_contact_book', 'delete_contact',
    #        'add_to_contact', 'edit_contact', 'edit_contact_name', 'search_in_contacts', 'show_birthdays', 'days_to_birthday', 'show_all_birthdays',
    #        'create_note', 'show_note_book', 'show_note', 'show_note_page', 'clear_note_book', 'delete_note', 'add_to_note', 'edit_note',
    #        'edit_note_name', 'search_in_notes', 'sorted_by_tags', 'file_sorter', 'exit']
    for words in com:
        cnt = 0
        for word_from_commands in words.split("_"):
            for word_from_search in search_words:
                cnt += 1 if word_from_search == word_from_commands else 0
        mathcer = difflib.SequenceMatcher(None, srch, words)
        if mathcer.ratio() >= 0.5:
            result_dict[words] = f"{round(mathcer.ratio(), 2)*100}%"
        if cnt >= 1:
            result_list.append([cnt, words])

    return f"\nI can't find command '{srch}'.\n" \
           f"Did you mean:\n" \
           f"{[v[1] for v in sorted(result_list, reverse=True)] if result_list else '<<<I cant find something similar.>>>'}\n" \
           f"Or you can find your command here:\n" \
           f"{[f'{k}: {value}' for k, value in result_dict.items()] if result_dict else '<<<I cant find something similar.>>>'}"
