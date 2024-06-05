import ast
import json
import os
import re

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Example function to call Llama3 API and format the response
def call_llama3_api(prompt):
    api_url = "http://localhost:11434/api/generate"  # Replace with actual Llama3 API URL
    headers = {
        # "Authorization": "Bearer YOUR_LLAMA3_API_KEY",  # Replace with your Llama3 API key
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3",  # Replace with the model name, e.g., "llama3", "llama3-turbo", "llama3-eco
        "prompt": prompt,
        "stream": False,
        # "max_tokens": 150  # Adjust as necessary
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    # return response.json()["choices"][0]["text"]
    return response.json().get("response", [])


# Function to generate recommendations using Llama3 and format them as a list of dictionaries
def ai_generate_recommendations(detailed_data, title_length=10, description_length=25):
    prompt = f"""
    - CLTV: £{detailed_data['cltv']:.2f}
    - Average Customer Lifespan: {detailed_data['avg_customer_lifespan']:.2f} years
    - Total Revenue: £{detailed_data['total_revenue']:.2f}
    - Number of Purchases: {detailed_data['num_purchases']}
    - Number of Customers: {detailed_data['num_customers']}
    - Average Purchase Value (APV): £{detailed_data['apv']:.2f}
    - Average Purchase Frequency Rate (APFR): {detailed_data['apfr']:.2f}
    - Customer Value (CV): £{detailed_data['cv']:.2f}
    - Customer Acquisition Cost (CAC): £{detailed_data['cac']:.2f}

    As an expert in Business Administration, Marketing, Finance, Data Science, or Computer Science, your task is to provide meaningful insights and recommendations based on the computed provided data. 
    Please analyze the provided data and provide top 7 insights with insightful suggestions (including data values) tailored to each of these domains. Your recommendations should be specific, actionable, and relevant to the context of the data provided. Consider various aspects such as strategic decisions, optimization opportunities, potential risks, and innovative approaches. Use your expertise to provide well-rounded advice that can drive better outcomes and add significant value.

    Return the recommendations as a JSON list of dictionaries, where each dictionary contains the following keys:
    - "title": a string with a maximum of {title_length} words
    - "description": a string with a maximum of {description_length} words
    - "metrics": a string describing the specific metrics relevant to the insights

    You are allwed to reference the detailed_data values in your insights. Ensure that the recommendations are relevant, actionable, and tailored to the specific context of the data provided. Your recommendations should demonstrate your expertise in the field and provide valuable insights for improving business performance.

    Do NOT include any other information in the response apart from the JSON list of insights dictionaries in a clean Python format.
    Extremely important: DO NOT add any text before and after the Python list of dictionaries.
    """
    llama3_response = call_llama3_api(prompt)
    with open(os.path.join(BASE_DIR, 'ai', 'llama3_response.txt'), 'w') as f:
        f.write(llama3_response)
    try:
        recommendations_list = ast.literal_eval(llama3_response)
    except ValueError:
        print("Error: Unable to parse the response from Llama3.")
        recommendations_list = []
    except SyntaxError:
        print("Error: Syntax error while parsing the response from Llama3.")
        recommendations_list = []
    return recommendations_list


def check_llama3_state():
    response = requests.get('http://localhost:11434')
    if response.status_code == 200:
        return True
    else:
        return False

def main():
    # Example detailed data
    detailed_data = {
        "cltv": 1000,
        "avg_customer_lifespan": 3,
        "total_revenue": 50000,
        "num_purchases": 100,
        "num_customers": 50,
        "apv": 500,
        "apfr": 2,
        "cv": 1000,
        "cac": 200
    }
    recommendations = ai_generate_recommendations(detailed_data)

    print(recommendations)
    print(type(recommendations))



if __name__ == "__main__":
    main()
    # response = requests.get('http://localhost:11434')
    # print(response.status_code)
    # print(response.text)