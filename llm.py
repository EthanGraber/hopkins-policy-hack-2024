from time import sleep
from litellm import completion

def generate_notification_with_examples(examples):

    prompt = f"""
    Generate a short, personalized, notification message that reminds the user to do their physical therapy.

    Here's a list of examples that have worked well for this user in the past:
    <examples>
    {examples}
    </examples>

    Respond only with the notification content. Include no other text in your response.
    """

    response = completion(
        model="ollama/llama3.2:1b-text-q5_K_M", 
        messages=[{ "content": prompt,"role": "user"}], 
        api_base="http://localhost:11434",
        stream=False
    )

    return response.complete_response