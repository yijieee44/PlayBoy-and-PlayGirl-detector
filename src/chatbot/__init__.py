import dialogflow
import os
from google.api_core.exceptions import InvalidArgument


class Chatbot:

    def __init__(self):
        self.DIALOGFLOW_PROJECT_ID = 'ml-project-cwly'
        self.DIALOGFLOW_LANGUAGE_CODE = 'en-US'
        self.GOOGLE_APPLICATION_CREDENTIALS = 'credential.json'
        self.credential_path = 'src/cred/credential.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credential_path

    def get_response(self, tester_id, input_text):
        SESSION_ID = tester_id
        text_to_be_analyzed = input_text
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        # print("Query text:", response.query_result.query_text)
        # print("Detected intent:", response.query_result.intent.display_name)
        # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        # print("Fulfillment text:", response.query_result.fulfillment_text)

        return response.query_result.fulfillment_text

    def get_responses(self, dict_):
        new_dict = dict_
        for tester in dict_:
            if dict_[tester] != "":
                new_dict[tester] = self.get_response(tester, dict_[tester])
        return new_dict