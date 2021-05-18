import tinder_api_sms

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
                    individual_messages = individual_messages + " " + str(message['message'])
            processed_messages.append(individual_messages)
    return processed_messages, ids, match_ids


if __name__ == "__main__":
    my_id = tinder_api_sms.get_self().get("_id")
    matches = tinder_api_sms.all_matches()
    matches_info = matches.get('data').get('matches')
    messages_all = []
    for match in matches_info:
        messages_all.append(match.get('messages'))
    proc, ids, match_ids = process_messages(messages_all, my_id)
    print(proc)
    print(ids)
    print(match_ids)