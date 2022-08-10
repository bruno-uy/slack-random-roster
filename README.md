# Random roster
AWS Lamda function for generating a random standup order with an option to return "the chosen" among the team (could serve as a moderator of the meeting).

To run this code as an AWS lambda function you need to:
1. Deploy the code from `lambda_function.py` into a new AWS lambda. You can follow these tutorials:
    - Code deployment: https://docs.amazonaws.cn/en_us/lambda/latest/dg/python-package.html
    - Layer for requirements: https://towardsaws.com/how-to-deploy-python-packages-for-aws-lambda-with-layers-acb70e75a3df
2. Add a Cloudwatch Events trigger from the lambda configuration console with your desired schedule.
3. Add a Slack webhook integration on your Slack account for the channel where you'd like the roster posted:
    - Create webhook: https://my.slack.com/services/new/incoming-webhook/
    - Nice step by step: https://medium.com/@neonforge/how-to-send-automated-slack-notifications-with-python-the-easy-way-ed1889f5a30
4. Create two environment variables in the lambda configuration.
    - `TEAM_ROSTER`: comma separated list of team members (no quotes needed).
    - `RENDER_CHOSEN`: set to `true` if you wanna render who is "the chosen" among the roster.
    - `SLACK_WEBHOOK_URL`: URL you received when you created the webhook integration on your Slack channel.