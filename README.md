# Dyslexia | aixelsyD  Real-Time Text Reversal API
is software that re-orients lettering for people that see letters different, so they can read.

Welcome to the Dyslexia Real-Time Text Reversal API! This software is designed to help individuals with dyslexia read text more easily by reversing the letters in real-time. The API processes images of text, enhances them for better clarity, and uses Tesseract OCR to detect and reverse the text, making it more accessible for dyslexic readers.

<img style="align:center;border-radius:13px;max-width:800px;width:600px;" src="tesseract.jpeg"/>

Python 3.11 in use, for more into visit -> https://python.org



## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Real-Time Text Reversal**: Processes images and reverses text for easier reading.
- **Image Enhancement**: Converts images to grayscale and enhances them for better clarity.
- **Custom Temporary Directory**: Uses a custom temporary directory for file handling.
- **User-Friendly API**: Simple API endpoints for easy integration with other applications.

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/dyslexia-text-reversal-api.git
    cd dyslexia-text-reversal-api
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Tesseract**:
    - On Ubuntu:
      ```bash
      sudo apt-get install tesseract-ocr
      ```
    - On macOS using Homebrew:
      ```bash
      brew install tesseract
      ```

4. **Update Tesseract Path**:
    - Ensure the Tesseract executable path is correctly set in the code:
      ```python
      pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path if necessary
      ```

## Usage
1. **Run the Application**:
    ```bash
    python app.py
    ```

2. **Access the API**:
    - Open your browser and navigate to `http://127.0.0.1:5000/` to see the welcome page.

## API Endpoints
### `POST /process_image`
Processes an uploaded image and returns the reversed text.

- **Request**:
  - `image`: The image file to be processed.

- **Response**:
  - JSON object containing the reversed text and other metadata.

- **Example**:
    ```bash
    curl -X POST -F "image=@path/to/your/image.png" http://.0.0.1:5000/process_image
    ```

### `GET /`
Displays the welcome page with additional information about the API.

## Contributing
We welcome contributions from the community! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch to your fork.
4. Open a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using the Dyslexia Real-Time Text Reversal API! If you have any questions or need further assistance, feel free to open an issue on GitHub. Happy coding!
