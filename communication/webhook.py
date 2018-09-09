import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from config import WEBHOOK_ID, WEBHOOK_TOKEN

def send_message(content):
    webhook = Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN,\
     adapter=RequestsWebhookAdapter())

    webhook.send(content)
