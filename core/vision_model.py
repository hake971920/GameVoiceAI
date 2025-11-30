import base64
from io import BytesIO
from typing import Optional
from PIL import Image
from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

class VisionModel:
    def __init__(self):
        """
        Initialize Vision Model Client.
        """
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        self.model_name = MODEL_NAME
        print(f"Initialized VisionModel with model: {self.model_name}")

    def _encode_image(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string.
        """
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def analyze_image(self, image: Image.Image, prompt: str = "What is happening in this image?") -> str:
        """
        Analyze the image using the vision model.
        :param image: PIL Image object.
        :param prompt: Text prompt for the model.
        :return: Model's response text.
        """
        base64_image = self._encode_image(image)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    # Simple test (requires API Key)
    if not OPENAI_API_KEY:
        print("Please set OPENAI_API_KEY in .env file to test VisionModel.")
    else:
        try:
            # Create a dummy image for testing if capture fails or just use a solid color
            img = Image.new('RGB', (100, 100), color = 'red')
            
            model = VisionModel()
            print("Analyzing test image...")
            result = model.analyze_image(img, "What color is this image?")
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
