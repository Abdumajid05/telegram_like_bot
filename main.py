import requests
import os



import time

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/'
        self.last_update_id = None
        self.like = 0
        self.dislike = 0
        

    def get_updates(self):
        """
        Fetches updates from the Telegram API.
        :return: JSON response containing updates.
        """
        url = self.api_url + 'getUpdates'
        params = {'timeout': 100, 'offset': self.last_update_id}
        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, chat_id, text):
        """
        Sends a message to the specified chat.
        :param chat_id: ID of the chat where the message will be sent.
        :param text: Text of the message to send.
        """
        url = self.api_url + 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        requests.get(url, params=params)
    # def send_photo(self, chat_id, photo_url):
    #     """
    #     Sends a photo to the specified chat.
    #     :param chat_id: ID of the chat where the photo will be sent.
    #     :param photo_url: URL of the photo to send.
    #     """
        
    #     url = self.api_url +'sendPhoto'
    #     params = {'chat_id': chat_id, 'photo': photo_url}
    #     requests.get(url, params=params)

    def handle_updates(self, updates):
        """
        Handles the incoming updates by processing each message and sending a response.
        :param updates: JSON response containing updates.
        """
        if 'result' in updates:
            for update in updates['result']:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    text = update['message']['text']
                    
                    # Respond to the received message
                    if text == '👍':
                        self.like += 1
                    if text == '👎':
                        self.dislike += 1
                    t = f'Total likes: {self.like}\nTotal dislikes: {self.dislike}'
                    self.send_message(chat_id,t)
                    # Update last_update_id to prevent reprocessing the same messages
                    self.last_update_id = update['update_id'] + 1

    def run(self):
        """
        Runs the bot, continuously fetching updates and handling them.
        """
        while True:
            updates = self.get_updates()
            self.handle_updates(updates)
            time.sleep(0.1)

if __name__ == '__main__':
    # Replace with your bot's token
    TOKEN = os.environ['TOKEN'] 

    
    bot = TelegramBot(TOKEN)
    bot.run()
