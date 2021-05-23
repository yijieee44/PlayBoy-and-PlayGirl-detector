import tinder_api_sms
import time


compiled_messages = {}
latest_message = {}


def process_messages(messages_all, my_id):
    """
    :param messages_all: the last message from each matched individuals' chat
    :param my_id: your acc's tinder id, "_id_" from get_self()
    :return: 3 lists
    processed_messages - a list containing the last message received from each matched individuals
    ids = a list of the matched individuals' id "_id"
    match_ids = a list of the matched individuals' match_id "match_id"
    """
    processed_messages = []
    ids = []
    match_ids = []
    for messages in messages_all:
        individual_messages = ""
        if messages:
            first = messages[0]
            ids.append(first["_id"])
            match_ids.append(first["match_id"])
            for message in messages:
                if message['from'] != my_id:
                    individual_messages += str(message['message'])
            processed_messages.append(individual_messages)
    return processed_messages, ids, match_ids


def check_duplicate(proc, ids):
    global compiled_messages
    if not compiled_messages:
        for index in range(len(proc)):
            compiled_messages[ids[index]] = proc[index]

    for i in range(len(proc)):
        if ids[i] in compiled_messages:
            compiled = compiled_messages[ids[i]]
            if proc[i] != "":
                if proc[i] not in compiled:
                    compiled = compiled + " " + proc[i]
                    compiled_messages[ids[i]] = compiled
        else:
            compiled_messages[ids[i]] = proc[i]


def get_message_every_1_sec(my_id, matches_info):
    global latest_message
    while True:
        try:
            messages_all = []
            for match in matches_info:
                messages_all.append(match.get('messages'))
            proc, ids, match_ids = process_messages(messages_all, my_id)
            latest_message = proc
            check_duplicate(proc, ids)
            time.sleep(1)
        except:
            print("Error getting message...maybe token expired")
            break


if __name__ == "__main__":
    my_id = tinder_api_sms.get_self().get("_id")
    matches = tinder_api_sms.all_matches()
    matches_info = matches.get('data').get('matches')
    get_message_every_1_sec(my_id, matches_info)