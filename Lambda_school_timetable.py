from __future__ import print_function

import time
import json
import boto3


def save_to_bucket(user_id, user_data):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('YOUR_BUCKET_ID')
    bucket.put_object(
        ContentType='application/json',
        Key=user_id,
        Body=json.dumps(user_data)
    )


def load_from_bucket(user_id):
    s3 = boto3.client('s3')
    try:
        data = s3.get_object(Bucket='YOUR_BUCKET_ID', Key=user_id)
        return json.loads(data['Body'].read())
    except:
        return {}


SKILL_NAME = "School Timetable"
HELP_MESSAGE = "School Timetable will tell you your lessons for the current day or the next. Would you like to set it up?"
HELP_REPROMPT = "What can I help you with?"
LAUNCH_MESSAGE = "School timetable can tell you what lessons you have, but first you must tell me your lessons for the week. You can say, tell school timetable to set Monday to Maths, Physics, and English"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "School timetable cannot help with that. You can say 'What are my lessons today' or 'Tell school timetable to set Wednesday to English, Mathematics and Chemistry. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'


def lambda_handler(event, context):
    """  App entry point  """

    if (event['session']['application']['applicationId'] != "YOUR_AMAZON_SKILL_APP_ID"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']
    intent = request['intent']
    # process the intents
    if intent_name == "Today":
        return get_today(intent, session)
    elif intent_name == "Tomorrow":
        return get_tomorrow(intent, session)
    elif intent_name == "SetMonday":
        return set_monday(intent, session )
    elif intent_name == "SetTuesday":
        return set_tuesday(intent, session)
    elif intent_name == "SetWednesday":
        return set_wednesday(intent, session)
    elif intent_name == "SetThursday":
        return set_thursday(intent, session)
    elif intent_name == "SetFriday":
        return set_friday(intent, session)
    elif intent_name == "SetSaturday":
        return set_saturday(intent, session)
    elif intent_name == "SetSunday":
        return set_sunday(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else
        return get_help_response()


days = [
    ['Mon', "monday"], 
    ["Tue", "tuesday"], 
    ["Wed", "wednesday"],
    ["Thu", "thursday"],
    ["Fri", "friday"],
    ["Sat", "saturday"],
    ["Sun", "sunday"]]

def get_today(intent, session):
    localtime = time.asctime( time.localtime(time.time()) )
    timetable = load_from_bucket(session["user"]["userId"])
    for i in range(len(days)):
        day = days[i][0]
        if day in localtime:
            if days[i][1] in timetable:
                speechOutput = "Your lessons for today are " + timetable[days[i][1]]
                break
            else:
                speechOutput = "There are no lessons set for today."
                break
    cardcontent = speechOutput
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))


def get_tomorrow(intent, session):
    localtime = time.asctime( time.localtime(time.time()) )
    timetable = load_from_bucket(session["user"]["userId"])
    for i in range(len(days)):
        day = days[i][0]
        if day in localtime:
            if day != "Sun":
                i = i + 1
                if days[i][1] in timetable:
                    speechOutput = "Your lessons for tomorrow are " + timetable[days[i][1]]
                else:
                    speechOutput = "You have no lessons set for tomorrow"
            else:
                i = i - 6
                if days[i][1] in timetable:
                    speechOutput = "Your lessons for tomorrow are " + timetable[days[i][1]]
                else:
                    speechOutput = "You have no lessons set for tomorrow"
    cardcontent = speechOutput
    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))


# return response(speech_response(speech_output, False)) Allow user to reply 

def set_monday(intent, session):

    timetable = load_from_bucket(session["user"]["userId"])
    timetable["monday"] = intent['slots']['Monday']['value']
    save_to_bucket(session["user"]["userId"], timetable)
    speechOutput = "I have set Monday to " + timetable["monday"]
    cardcontent = speechOutput

    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def set_tuesday(intent, session):
    timetable = load_from_bucket(session["user"]["userId"])
    timetable["tuesday"] = intent['slots']['Tuesday']['value']
    save_to_bucket(session["user"]["userId"], timetable)
    speechOutput = "I have set Tuesday to " + timetable["tuesday"]
    cardcontent = speechOutput

    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def set_wednesday(intent, session):
    timetable = load_from_bucket(session["user"]["userId"])
    timetable["wednesday"] = intent['slots']['Wednesday']['value']
    save_to_bucket(session["user"]["userId"], timetable)
    speechOutput = "I have set Wednesday to " + timetable["wednesday"]
    cardcontent = speechOutput


    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def set_thursday(intent, session):
    timetable = load_from_bucket(session["user"]["userId"])
    timetable["thursday"] = intent['slots']['Thursday']['value']
    save_to_bucket(session["user"]["userId"], timetable)
    speechOutput = "I have set Thursday to " + timetable["thursday"]
    cardcontent = speechOutput

    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def set_friday(intent, session):
    timetable = load_from_bucket(session["user"]["userId"])
    timetable["friday"] = intent['slots']['Friday']['value']
    save_to_bucket(session["user"]["userId"], timetable)
    speechOutput = "I have set Friday to " + timetable["friday"]
    cardcontent = speechOutput


    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def set_saturday(intent, session):
    timetable = load_from_bucket(session['user']['userId'])
    timetable["saturday"] = intent['slots']['Saturday']['value']
    save_to_bucket(session["user"]['userId'], timetable)
    speechOutput = "I have set Saturday to " + timetable["saturday"]
    cardcontent = speechOutput


    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))


def set_sunday(intent, session):
    timetable = load_from_bucket(session['user']['userId'])
    timetable["sunday"] = intent['slots']['Sunday']['value']
    save_to_bucket(session["user"]['userId'], timetable)
    speechOutput = "I have set Sunday to " + timetable["sunday"]
    cardcontent = speechOutput


    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))

def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response(request, session):
    """ get and return the help string  """
    timetable = load_from_bucket(session["user"]["userId"])
    if timetable == {}:
        speech_message = LAUNCH_MESSAGE
        return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
    else:
        return get_today(request, session)

def get_stop_response():
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """

def on_session_ended():
    """ called on session ends """

def on_launch(request, session):
    """ called on Launch, we reply with a launch message  """

    return get_launch_response(request, session)


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def dialog_response(endsession):
    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }

def speech_response_with_card(title, output, cardcontent, endsession):
    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }
