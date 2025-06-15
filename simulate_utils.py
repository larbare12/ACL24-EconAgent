import sys
import numpy as np
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import seaborn as sns
import re
import os
import multiprocessing
import scipy

save_path = './'

brackets = list(np.array([0, 97, 394.75, 842, 1607.25, 2041, 5103])*100/12)
quantiles = [0, 0.25, 0.5, 0.75, 1.0]

from datetime import datetime
world_start_time = datetime.strptime('2001.01', '%Y.%m')

prompt_cost_1k, completion_cost_1k = 0.001, 0.002

def prettify_document(document: str) -> str:
    # Remove sequences of whitespace characters (including newlines)
    cleaned = re.sub(r'\s+', ' ', document).strip()
    return cleaned


def get_multiple_completion(dialogs, num_cpus=15, temperature=0, max_tokens=100,reflection=0):
    from functools import partial
    if reflection==0:
        get_completion_partial = partial(get_completion, temperature=temperature, max_tokens=max_tokens)
    else:
        get_completion_partial = partial(get_reflection, temperature=temperature, max_tokens=max_tokens)
    with multiprocessing.Pool(processes=num_cpus) as pool:
        results = pool.map(get_completion_partial, dialogs)
    total_cost = sum([cost for _, cost in results])
    return [response for response, _ in results], total_cost

def get_completion(dialogs, temperature=1, max_tokens=100,model='deepseek-chat'):
    from openai import OpenAI
    import time
    client = OpenAI(api_key="sk-14271b0e74f34691a70ee509c7eda4ca", base_url="https://api.deepseek.com")
    max_retries = 20
    for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=dialogs,
                temperature=temperature,
                max_tokens=max_tokens,
                model=model,
                response_format={
                    'type': 'json_object'
                }
            )
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            this_cost = prompt_tokens/1000*prompt_cost_1k + completion_tokens/1000*completion_cost_1k
            return response.choices[0].message.content, this_cost
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(6)
            else:
                print(f"An error of type {type(e).__name__} occurred: {e}")
                return "Error"

def get_reflection(dialogs, temperature=1, max_tokens=100,model='deepseek-chat'):
    from openai import OpenAI
    import time
    client = OpenAI(api_key="sk-14271b0e74f34691a70ee509c7eda4ca", base_url="https://api.deepseek.com")
    max_retries = 20
    for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=dialogs,
                temperature=temperature,
                max_tokens=max_tokens,
                model=model
            )
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            this_cost = prompt_tokens/1000*prompt_cost_1k + completion_tokens/1000*completion_cost_1k
            return response.choices[0].message.content, this_cost
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(6)
            else:
                print(f"An error of type {type(e).__name__} occurred: {e}")
                return "Error"

def format_numbers(numbers):
    return '[' + ', '.join('{:.2f}'.format(num) for num in numbers) + ']'

def format_percentages(numbers):
    return '[' + ', '.join('{:.2%}'.format(num) for num in numbers) + ']'
