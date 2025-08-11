
import openai
import requests
from PIL import Image
import io
import os
from typing import Optional
from dotenv import load_dotenv


class oldOpenAI:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('openai_key')
        self.max_size_mb = 4.0

    def variation(self, image_url):
        try:
            # Process the image
            output_file = self.process_image_for_openai(image_url, "tmp.png")
            print(f"Image ready for OpenAI API: {output_file}")

            # Verify file size
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"Final file size: {file_size:.2f} MB")

            # Simon new key 2025

            response = openai.Image.create_variation(
                image=open("tmp.png", "rb"),  # must be a square PNG < 4 MB
                n=3,  # number of variations (1–10)
                size="1024x1024"  # options: "256x256", "512x512", "1024x1024"
            )

            URLs = []
            for i, data in enumerate(response["data"]):
                URLs.append(data["url"])

            os.remove('tmp.png')
            return URLs


        except Exception as e:
            print(f"Error: {e}")


    def process_image_for_openai(self, image_url, output_path = "processed_image.png"):
        try:
            response = requests.get(image_url, stream=True, timeout=30)
            response.raise_for_status()

            # Load image from response content
            image_data = io.BytesIO(response.content)
            image = Image.open(image_data)


            # Convert to RGB if necessary (handles RGBA, P, etc.)
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')

            # Start with high quality
            quality = 95

            # Try to save and check file size
            while quality > 10:
                # Save to memory buffer first to check size
                buffer = io.BytesIO()
                image.save(buffer, format='PNG', optimize=True)
                file_size_mb = len(buffer.getvalue()) / (1024 * 1024)

                print(f"File size at quality {quality}: {file_size_mb:.2f} MB")

                if file_size_mb <= self.max_size_mb:
                    # Size is acceptable, save to file
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    print(f"Image saved to: {output_path} ({file_size_mb:.2f} MB)")
                    return output_path

                # If still too large, resize the image
                if file_size_mb > self.max_size_mb * 2:  # Significantly oversized
                    # Reduce dimensions
                    new_width = int(image.width * 0.8)
                    new_height = int(image.height * 0.8)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Resized to: {image.size}")
                else:
                    # Just reduce quality
                    quality -= 10

            # If we get here, we couldn't get under the size limit
            # Save the smallest version we achieved
            buffer = io.BytesIO()
            image.save(buffer, format='PNG', optimize=True)
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())

            final_size_mb = len(buffer.getvalue()) / (1024 * 1024)
            print(f"Warning: Could not reduce below {self.max_size_mb}MB. Final size: {final_size_mb:.2f} MB")
            return output_path

        except requests.RequestException as e:
            raise Exception(f"Failed to download image: {e}")
        except Exception as e:
            raise Exception(f"Failed to process image: {e}")








