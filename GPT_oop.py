import openai
openai.api_key = "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"
model_id = 'gpt-3.5-turbo'

class GPT: # still trying to make it
    def __init__(self):
        self.user_input = None
        self.role = "user"
        self.message_history = []
    def generate_response(self, role="user"):
        if len(self.message_history) >= 5:
            self.message_history.pop(0)
        self.user_input = input('User:')
        self.message_history.append({'role': 'system', 'content': 'You are a helpful assistant.'})
        self.message_history.append({'role': self.role, 'content': f"{self.user_input}"})

        array_exit = ["", "Bye ChatGPT", "Bye ChatGPT", "bye", "bye chat", "bye", "see you"]
        if self.user_input in array_exit:
            return None
        
        completion = openai.ChatCompletion.create(
            model=model_id,
            messages=self.message_history
        )
        response = completion.choices[0].message['content'].strip()
        #print(response)
        self.message_history.append({'role': "assistant", 'content': f"{response}"})
        return response    

if __name__ == "__main__":
    gpt = GPT()
    conversation = gpt.generate_response(role="user")