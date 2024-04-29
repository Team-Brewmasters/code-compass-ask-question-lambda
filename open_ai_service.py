from openai import OpenAI

# Set up your OpenAI API credentials
api_key = "sk-proj-RRkKlGDUEXpvF6EyyWyRT3BlbkFJJCovL0rU94pzUcogHxlg"

def call_chatgpt(prompt, files):
    
    client = OpenAI(api_key=api_key)

    # client.api_key = api_key


    # Call the OpenAI ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": '''You are a master engineer designed to analyze a repository and answer questions about that repository. The repo info will be given below.'''}, 
                  {"role": "system", "content": '''Respond in the format of a JSON object with the following structure:{

    "answer": "The answer to the question (Please respond in markdown format and make it as detailed as possible)",
    "confidence": "Your confidence level in the answer (High, Medium, Low)"
}'''}, 
      {"role": "system", "content": str(files)},
        {"role": "user", "content": str(prompt)}],
    )

 
    # Extract the generated response from the API response
    generated_response = response.choices[0].message.content

    return generated_response
