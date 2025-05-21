import requests
import base64
import mimetypes
import os
import time


def gemini_ocr(image_path, api_key, max_retries=3, timeout=30):
    if not os.path.exists(image_path):
        return f"❌ Error: File not found at {image_path}"

    try:

        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type not in ['image/png', 'image/jpeg']:
            return "❌ Error: Only PNG/JPEG images supported"


        with open(image_path, 'rb') as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}

        # Precision-focused instruction prompt
        system_prompt = """Extract text EXACTLY as shown:
- Preserve ALL characters, case, and spacing
- Include numbers, symbols (×÷°), and prices
- Skip non-text elements and explanations
- Output format examples:
  "ACDC CLIMP 23.99"
  "177×BC"
  "ERR-04"
  "88:88\""""

        payload = {
            "contents": [{
                "parts": [
                    {"inlineData": {"mimeType": mime_type, "data": image_base64}},
                    {"text": system_prompt}
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topP": 0.3,
                "maxOutputTokens": 200
            }
        }
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=timeout)
                response.raise_for_status()

                # Parse response
                content = response.json()['candidates'][0]['content']['parts'][0]['text']

                # Clean and format output
                cleaned = ' '.join(content.strip().split())
                return cleaned

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limited
                    wait_time = 2 ** (attempt + 1)
                    time.sleep(wait_time)
                    continue
                return f"❌ API Error {response.status_code}: {response.text}"

            except (KeyError, IndexError):
                return "✅ No text found in image"

    except Exception as e:
        return f"❌ Processing error: {str(e)}"


if __name__ == "__main__":
    image_path = "C:/Users/Rohan/Downloads/capchas (2).jpeg"
    api_key = "AIzaSyBi4EHiGT1gWWVdiS2ctEhzPd2dm8EJb4A"

    result = gemini_ocr(image_path, api_key)

    print("\n=== OCR RESULT ===")
    print(result)
    print("==================")