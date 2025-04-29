import cohere
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # You can set to DEBUG for more detailed logs
ch = logging.StreamHandler()  # Stream to console or set a FileHandler to log to a file
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Replace with your actual Cohere API Key
COHERE_API_KEY = "ydluXmReKq7KOBFId4w4YAL2IlgAGUj5cGXyq8dW"

# Set up Cohere API client
cohere_client = cohere.Client(COHERE_API_KEY)

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            # Log the incoming request
            logger.info(f"Received POST request: {request.body}")

            # Parse the request body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            # Check if the message is empty or invalid
            if not user_message:
                logger.warning("Received empty message")
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            # Call Cohere API to generate a response
            logger.info(f"Sending message to Cohere API: {user_message}")
            response = cohere_client.generate(
                model='command-xlarge',  # Update to a valid model ID
                prompt=user_message,
                max_tokens=150
            )

            # Extract the AI's reply
            ai_message = response.generations[0].text.strip()

            # Log the response from Cohere
            logger.info(f"Cohere API response: {ai_message}")

            # Return the AI response
            return JsonResponse({"reply": ai_message})

        except cohere.errors.NotFoundError as e:
            # Log the specific error for a missing model
            logger.error(f"Cohere model not found error: {str(e)}")
            return JsonResponse({"error": "The specified model was not found. Please check the model ID."}, status=404)

        except json.JSONDecodeError:
            # Log JSON parsing error
            logger.error("Invalid JSON format in the request body")
            return JsonResponse({"error": "Invalid JSON format in the request body"}, status=400)

        except Exception as e:
            # Log any unexpected errors
            logger.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    else:
        # Return error for non-POST requests
        logger.warning("Received non-POST request")
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
