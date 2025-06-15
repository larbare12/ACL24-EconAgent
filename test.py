messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]

# from openai import OpenAI
#
# client = OpenAI(api_key="sk-14271b0e74f34691a70ee509c7eda4ca", base_url="https://api.deepseek.com")
#
# # Round 1

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages
# )
#
# messages.append(response.choices[0].message)
# print(f"Messages Round 1: {messages}")

# from openai import OpenAI
# client = OpenAI(api_key="sk-14271b0e74f34691a70ee509c7eda4ca", base_url="https://api.deepseek.com")
#
# response = client.chat.completions.create(
#     messages=messages,
#     temperature=1,
#     max_tokens=100,
#     model='deepseek-chat'
# )
# prompt_tokens = response.usage.prompt_tokens
# completion_tokens = response.usage.completion_tokens
# this_cost = prompt_tokens/1000*0.1 + completion_tokens/1000*0.2
# print(response.choices[0].message.content, this_cost)
# #

import pickle

f = open(r'data/gpt-3-noperception-reflection-1-3agents-4months/env_4.pkl','rb')  # pickle_data_path为.pickle文件的路径；
info = pickle.load(f)
print(info)

f.close()  # 别忘记close pickle文件