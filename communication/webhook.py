import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from config import WEBHOOK_PUBLIC_ID, WEBHOOK_PUBLIC_TOKEN, WEBHOOK_PRIVATE_ID, WEBHOOK_PRIVATE_TOKEN

def send_public_message(content):
    webhook = Webhook.partial(WEBHOOK_PUBLIC_ID, WEBHOOK_PUBLIC_TOKEN,\
     adapter=RequestsWebhookAdapter())

    webhook.send(content)

def send_private_message(content):
    webhook = Webhook.partial(WEBHOOK_PRIVATE_ID, WEBHOOK_PRIVATE_TOKEN,\
     adapter=RequestsWebhookAdapter())

    webhook.send(content)
