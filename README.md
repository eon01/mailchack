# Mailchack

Invite Mailchimp Subscribers To Slack

# How To

Check the configuration file ``` mail.conf ``` in order to configure: 

- The logger level: logger_level
- The logging handler level : handler_level
- The log format : log_format
- The file where logs will be stored: log_file
- Your mailchimp user : mc_user
- You mailchimp generated token : mc_token
- Your mailchimp list id: mc_id
- Your slack token : slack_token
- Your slack channel ID: slack_id

Then simply start: 

``` python main.py ```

It will invite all of your newsletter subscribers to your Slack team chat.
