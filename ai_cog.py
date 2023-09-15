import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import time
import random

load_dotenv()  # Load environment variables from .env file

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("AI Cog Loaded")
        self.API_URL = "https://api-inference.huggingface.co/models/MikeTsak/Corner"
        self.headers = {
            "Authorization": f"{os.getenv('API_HUGGINGFACE')}"
        }
    MAX_RETRIES = 10  # Maximum number of retries

    def query(self, payload):
        for _ in range(self.MAX_RETRIES):
            data = {
                "inputs": payload["inputs"],
                "parameters": {
                    "return_full_text": False,
                    "temperature": 0.8,  # Adjust based on desired randomness
                    "top_k": 50,  # Adjust to get diverse results
                    "top_p": 0.95,  # Adjust to get probable results
                    "temperature": 0.8,  # Adjust based on desired randomness
                },
                "options": {
                    "use_cache": True,
                    "wait_for_model": True
                }
            }
            #Σκονακι --> https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task

            response = requests.post(self.API_URL, headers=self.headers, json=data)
            response_data = response.json()
            
            if 'error' in response_data and 'loading' in response_data.get('error', ''):
                # If the model is loading, sleep for 1 second and retry
                time.sleep(1)
            else:
                # Otherwise, return the response (be it a successful one or another kind of error)
                print(response_data)
                return response_data


    # Event listener for messages
    @commands.Cog.listener()
    async def on_message(self, message):
        # Return if the message was sent by the bot
        if message.author == self.bot.user:
            return

        # If it's a DM or the bot was mentioned or a random number is 24
        if isinstance(message.channel, discord.DMChannel) or self.bot.user in message.mentions or random.randint(1, 800) == 24:
            # Remove the mention if there's any and pass the rest as payload
            content_without_mention = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            print('message received:', content_without_mention)
            await message.channel.typing()
            output = self.query({
                "inputs": content_without_mention,
            })

            # Check the output format and send the right response
            if 'error' in output:
                await message.channel.send(output['error'])
            elif isinstance(output, list) and 'generated_text' in output[0]:
                answer = output[0]['generated_text'].strip()
                await message.channel.send(answer)
            else:
                await message.channel.send("An unknown error occurred.")


def setup(bot):
    bot.add_cog(AICog(bot))
