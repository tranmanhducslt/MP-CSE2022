import openai
openai.api_key = "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"
model_id = 'ft:gpt-3.5-turbo-0613:personal::82xXgYyF'

class GPT: # still trying to make it
    def __init__(self):
        self.user_input = None
        self.role = "User"
        self.prompt = None
        self.conversation = None
    def generate_response(user_input, role="user"):
        message_history.append({'role': 'system', 'content': 'You are a helpful assistant.'})
        message_history.append({"role": self.role, "content": f"{self.user_input}"})

        array_exit = ["", "Bye ChatGPT", "Bye ChatGPT", "bye", "bye chat", "bye", "see you"]
        if self.user_input in array_exit:
            return None
        
        completion = openai.ChatCompletion.create(
            model=model_id,
            messages=message_history
        )
        response = completion.choices[0].message.content
        print(completion.choices[0].message.content.strip())
        message_history.append({"role": "assistant", "content": f"{response}"})
        return response

    message_history = []

    while True:
        gpt = GPT()
        gpt.prompt = input('User:')
        gpt.conversation = generate_response(gpt.prompt, role="user")
        if gpt.conversation is None:
            break