from settings import *
from hermes.pushover import *

title = "message"
message = "test message"

token = PUSHOVER_APP_TOKEN
user = PUSHOVER_USER_KEY

general_notification = Pushover(token=token)
general_notification.user(user)
message = general_notification.msg(
    message
    )
message.set("title", title)

general_notification.send(message)

critical_notification = Pushover(token=token)
critical_notification.user(user)
message = critical_notification.msg(
    "This is a test message for a critical alert."
    )
message.set("title", "Test Critical Alert")
message.set("priority", "2")
message.set("expire", "2")
message.set("retry", "120")
message.set("sound", "spacealarm")

critical_notification.send(message)
