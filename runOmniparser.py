import requests
import base64
import os

# The API endpoint URL
API_URL = "http://localhost:7860/process_image"

def main():
    # Prompt the user for an image name located in the 'input' folder
    image_name = input("Enter the input image filename (located in 'input' folder): ")

    # Construct the image path
    image_path = os.path.join("input", image_name)

    # Check if file exists
    if not os.path.isfile(image_path):
        print(f"File {image_path} does not exist.")
        return

    # Open the image file in binary mode
    with open(image_path, "rb") as f:
        files = {"image_file": (image_name, f, "image/png")}

        # Send POST request to the /process_image endpoint
        response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Just print the raw returned data for now
        print("Parsed Content List:", data.get("parsed_content_list", []))
        print("Label Coordinates:", data.get("label_coordinates", {}))

        # If you still want to print or save the image, you can:
        b64_image = data.get("image", None)
        if b64_image:
            output_filename = os.path.splitext(image_name)[0] + "_labeled.png"
            output_path = os.path.join("output", output_filename)
            image_data = base64.b64decode(b64_image)
            with open(output_path, "wb") as out_file:
                out_file.write(image_data)
            print(f"Labeled image saved to {output_path}")
        else:
            print("No labeled image returned in the response.")
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)


if __name__ == "__main__":
    main()
