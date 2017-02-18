from mailchimp3 import MailChimp
import requests
import json
import logging
import ConfigParser
from slackipycore import invite, AlreadyInvited, AlreadyInTeam, InvalidInviteeEmail, InvalidAuthToken, APIRequestError
import os

# start configuration parser
parser = ConfigParser.ConfigParser()
parser.read("main.conf")

# reading variables
logger_level = parser.get('logging', 'logger_level', raw = True)
handler_level = parser.get('logging', 'handler_level', raw = True)
log_format = parser.get('logging', 'log_format', raw = True)
log_file = parser.get('logging', 'log_file')

mc_user = parser.get('mailchimp', 'mc_user')
mc_token = parser.get('mailchimp', 'mc_token')
mc_id = parser.get('mailchimp', 'mc_id')

slack_token = parser.get('slack', 'slack_token')
slack_id = parser.get('slack', 'slack_id')

# set logger logging level
logger = logging.getLogger(__name__)
logger.setLevel(eval(logger_level))

# set handler logging level
handler = logging.FileHandler(log_file)
handler.setLevel(eval(handler_level))

# create a logging format
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

mc_client = MailChimp(mc_user, mc_token)

try:
    mc_members = mc_client.lists.members.all(mc_id, get_all=False, fields="members.email_address,members.timestamp_signup")
except requests.exceptions.ConnectionError as e:
    logger.error(repr(e))
    exit(1)

mc_members_dict = json.loads(json.dumps(mc_members))

for mc_member in mc_members_dict['members'][1:]:

    ea = mc_member['email_address']

    try:
        invite(slack_id, slack_token, ea)
    except AlreadyInvited as e :
        logger.info(repr(e) + " : " + ea)

    except AlreadyInTeam as e:
        logger.info(repr(e) + " : " + ea)

    except InvalidInviteeEmail as e:
        logger.error(repr(e) + " : " + ea)

    except InvalidAuthToken as e:
        logger.error(repr(e) + " : " + ea)

    except APIRequestError as e:
        logger.error(repr(e) + " : " + ea)
