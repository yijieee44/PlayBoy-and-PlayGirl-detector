import tinder_api_sms
import time
import os
from src import chatbot


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
    for id in match_id:
        try:
            message = proc[id]
            ospath = os.getcwd()
            ospath = ospath.replace("\\", "/")
            ospath = ospath.split("/chatbot")[0]
            filename = ospath + "/replies/" + id + ".txt"
            file = open(filename, "r")
            if message not in file:
                file.close()
                file = open(filename, "a")
                file.write(message)
                file.close()
        except FileNotFoundError:
            file = open(filename, "a+")
            file.write(message)
            file.close()


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
            print(proc)
            response = chatbot_1.get_responses(proc)
            print(response)
            sent = send_message(response)
            print(sent)
            check_duplicate(proc, match_ids)
            time.sleep(1)
        except:
            print("Error getting message...maybe token expired")
            break


if __name__ == "__main__":
    # remember to run sms_auth_v3 before running this
    my_id = tinder_api_sms.get_self().get("_id")
    get_message_every_1_sec(my_id)

