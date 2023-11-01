import openai
openai.api_key = "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"
model_id = 'ft:gpt-3.5-turbo-0613:personal::82xXgYyF'

class GPT: # still trying to make it
    def __init__(self):
        self.user_input = None
        self.role = "User"
        self.message_history = {}
    def generate_response(self, role="user"):
        if len(self.message_history) >= 5:
            self.message_history.pop(0)
        self.user_input = input('User:')
        self.message_history.append({'role': 'system', 'content': 'You are a helpful assistant.'})
        self.message_history.append({"role": self.role, "content": f"{self.user_input}"})

        array_exit = ["", "Bye ChatGPT", "Bye ChatGPT", "bye", "bye chat", "bye", "see you"]
        if self.user_input in array_exit or not self.user_input:
            return None
        
        completion = openai.ChatCompletion.create(
            model=model_id,
            messages=self.message_history
        )
        response = completion.choices[0].message['content'].strip()
        print(response)
        self.message_history.append({"role": "assistant", "content": f"{response}"})
        return response    

    while True:
        gpt = GPT()
        gpt.conversation = generate_response(gpt.generate_response, role="user")
        if gpt.conversation is None:
            break