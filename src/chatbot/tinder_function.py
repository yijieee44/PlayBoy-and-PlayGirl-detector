import time
import os
from src.chatbot import tinder_api_sms
from src import chatbot
from src.model.model import clean_msg


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
                    individual_messages = individual_messages + " " + str(message['message'])
            processed_messages[first["match_id"]] = individual_messages
    return processed_messages, match_ids


def check_duplicate(proc, match_id):
    for id in match_id:
        try:
            message = proc[id]
            message = clean_msg(message)
            message = " " + message
            ospath = os.getcwd()
            ospath = ospath.replace("\\", "/")
            ospath = ospath.split("/chatbot")[0]
            filename = ospath + "/src/replies/" + id + ".txt"
            file = open(filename, "r")
            if message not in file:
                file.close()
                file = open(filename, "a")
                file.write(message)
                file.close()
        except FileNotFoundError:
            file = open(filename, "w+")
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
            check_duplicate(proc, match_ids)
            print(proc)
            response = chatbot_1.get_responses(proc)
            print(response)
            sent = send_message(response)
            print(sent)
            time.sleep(1)
        except:
            print("Error getting message...maybe token expired")
            break

