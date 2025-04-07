from flask import Flask, request, jsonify, send_file, session
from roboflow import Roboflow
from flask_cors import CORS
from PIL import Image
import numpy as np
import base64
import json
import cv2
from io import BytesIO
from huggingface_hub import InferenceClient
import google.generativeai as genai
from inference_sdk import InferenceHTTPClient

# Initialize Clients
CLIENT = InferenceHTTPClient(api_url="https://classify.roboflow.com", api_key="KQSYBMVR3uU9mYfiP6ER")
hf_client = InferenceClient(api_key="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")
genai.configure(api_key="AIzaSyAzRlbHISAwL7ytMoSb4M9VOxn9cFDlGhU")
genai_model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

def prophenta_Vision_Llama_v1(image=None, text_query=None, conversation=None):
    if not conversation:
        conversation = []

    if image:
        image_data = image.read()
        img = Image.open(BytesIO(image_data))
        mime_type =  img.format.lower()
        if mime_type is None:
            return "Unsupported image format."
        base64_image = base64.b64encode(image_data).decode('utf-8')
        image_url = f"data:image/{mime_type};base64,{base64_image}"
        
        conversation.append({
            "role": "user",
            "content": [
                {"type": "text", "text": text_query},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        })
        
        response = hf_client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct",
            messages=conversation,
            max_tokens=500,
        )
        return response.choices[0].message["content"]

    elif text_query:
        conversation.append({
            "name": "AI-Powered Multi-Modal Chatbot for Skin Disease Diagnosis",
            "context": "medical",
            "role": "user",
            "input": text_query + " Provide a professional yet simple response as a doctor would."
        })
        
        response = genai_model.generate_content(contents=[{"text": str(conversation)}])
        return response.text

    return "Please provide either an image or a text query."

@app.route('/bot', methods=['POST'])
def interact_with_bot():
    user_input = request.form.get('text')
    response = prophenta_Vision_Llama_v1(text_query=user_input, conversation=session.get('conversation', []))
    return jsonify({'response': response})

@app.route('/botimg', methods=['POST'])
def interact_with_bot_img():
    user_input = request.form.get('text')
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"error": "No image file provided"}), 400

    image_bytes = image_file.read()
    image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Perform inference
    detections = CLIENT.infer(image_np, model_id="skin-disease-classification-opfbn/2")
    
    # Debugging output
    print("Detections Response:", detections)

    if not detections or 'predictions' not in detections:
        return jsonify({"error": "No detections found"}), 400

    predictions_dict = detections['predictions']
    if not isinstance(predictions_dict, dict) or not predictions_dict:
        return jsonify({"error": "Invalid predictions format"}), 400

    # Extract the class with highest confidence
    best_class = max(predictions_dict, key=lambda k: predictions_dict[k]['confidence'])
    best_confidence = predictions_dict[best_class]['confidence'] * 100

    # Draw prediction text on the image (no bounding box data available in response)
    label = f"{best_class} ({best_confidence:.2f}%)"
    cv2.putText(image_np, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Convert processed image to Base64
    _, encoded_image = cv2.imencode(".jpg", image_np)
    predicted_image_base64 = base64.b64encode(encoded_image).decode('utf-8')

    prompt = (
        f"Detected Condition: {best_class} ({best_confidence:.2f}% confidence).\n\n"
        "Explain this condition, including causes, symptoms, treatments, and preventive measures."
    )

    result = prophenta_Vision_Llama_v1(text_query=prompt)

    return jsonify({
        "image_data": predicted_image_base64,
        "class_name": best_class,
        "accuracy": best_confidence                                                             ,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
