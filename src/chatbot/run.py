import tinder_api_sms
import time
from src import chatbot


compiled_messages = {}
chatbot_1 = chatbot.Chatbot()


def process_messages(messages_all, my_id):
    """
    :param messages_all: the last message from each matched individuals' chat
    :param my_id: your acc's tinder id, "_id_" from get_self()
    :return: 3 lists
    processed_messages - a list containing the last message received from each matched individuals
    ids = a list of the matched individuals' id "_id"
    match_ids = a list of the matched individuals' match_id "match_id"
    """
    processed_messages = {}
    match_ids = []
    for messages in messages_all:
        individual_messages = ""
        if messages:
            first = messages[0]
            match_ids.append(first["match_id"])
            for message in messages:
                if message['from'] != my_id:
                    individual_messages += str(message['message'])
            processed_messages[first["match_id"]] = individual_messages
    return processed_messages, match_ids


def check_duplicate(proc, match_id):
    global compiled_messages
    if not compiled_messages:
        compiled_messages = proc

    for i in range(len(proc)):
        if match_id[i] in compiled_messages:
            compiled = compiled_messages[match_id[i]]
            if proc[match_id[i]] != "":
                if proc[match_id[i]] not in compiled:
                    compiled = compiled + " " + proc[match_id[i]]
                    compiled_messages[match_id[i]] = compiled
        else:
            compiled_messages[match_id[i]] = proc[match_id[i]]


def send_message(response):
    sent = []
    for each in response:
        if response[each] != '':
            sent.append(tinder_api_sms.send_msg(each, response[each]))

    return sent


def get_message_every_1_sec(my_id):
    while True:
        try:
            matches = tinder_api_sms.all_matches()
            matches_info = matches.get('data').get('matches')
            messages_all = []
            for match in matches_info:
                messages_all.append(match.get('messages'))
            proc, match_ids = process_messages(messages_all, my_id)
            response = chatbot_1.get_responses(proc)
            send_message(response)
            check_duplicate(proc, match_ids)
            time.sleep(1)
        except:
            print("Error getting message...maybe token expired")
            break


if __name__ == "__main__":
    my_id = tinder_api_sms.get_self().get("_id")
    get_message_every_1_sec(my_id)