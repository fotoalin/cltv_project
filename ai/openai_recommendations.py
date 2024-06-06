import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def call_openai_api(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # model="gpt-3.5-turbo",
        model="gpt-3.5-turbo-1106",
        # model="gpt-4o",
    )
    # return response.choices[0].message.content
    return response.choices[0].message.content


def ai_generate_recommendations(detailed_data, title_length=10, description_length=25):
    prompt = f"""
As an expert in Business Administration, Marketing, Finance, Data Science, or Computer Science, your task is to provide meaningful insights and recommendations based on the computed provided data. 
Please analyze the provided data and provide top 7 insights with insightful suggestions (including data values) tailored to each of these domains. Your recommendations should be specific, actionable, and relevant to the context of the data provided. Consider various aspects such as strategic decisions, optimization opportunities, potential risks, and innovative approaches. Use your expertise to provide well-rounded advice that can drive better outcomes and add significant value.

CLTV: £{detailed_data['cltv']:.2f}
Average Customer Lifespan: {detailed_data['avg_customer_lifespan']:.2f} years
Total Revenue: £{detailed_data['total_revenue']:.2f}
Number of Purchases: {detailed_data['num_purchases']}
Number of Customers: {detailed_data['num_customers']}
Average Purchase Value (APV): £{detailed_data['apv']:.2f}
Average Purchase Frequency Rate (APFR): {detailed_data['apfr']:.2f}
Customer Value (CV): £{detailed_data['cv']:.2f}
Customer Acquisition Cost (CAC): £{detailed_data['cac']:.2f}

Return the recommendations as a JSON list of dictionaries, where each dictionary contains the following keys:
- "title": a string with a maximum of {title_length} words
- "description": a string with a maximum of {description_length} words
- "metrics": a string describing the specific metrics relevant to the insights

You are allwed to reference the detailed_data values in your insights. Ensure that the recommendations are relevant, actionable, and tailored to the specific context of the data provided. Your recommendations should demonstrate your expertise in the field and provide valuable insights for improving business performance.

Do NOT include any other information in the response apart from the JSON list of insights dictionaries in a clean Python format.
Extremely important: DO NOT add any text before and after the Python list of dictionaries.
    """
    openai_response = call_openai_api(prompt)
    with open(os.path.join(BASE_DIR, 'ai', 'openai_response.txt'), 'w') as f:
        f.write(openai_response)
    try:
        recommendations_list = json.loads(openai_response)
    except ValueError:
        print("Error: Unable to parse the response from OpenAI.")
        recommendations_list = []
    return recommendations_list

def main():
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
