# Aadhar Card Verification System

## Overview

This Python program verifies the authenticity of Aadhar cards using the Google Vision API. It includes two main functions:

1. **Extract Text**: Extracts text from a list of image paths.
2. **Classify Aadhar**: Classifies whether the extracted text corresponds to a valid Aadhar card.

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies:

  ```bash
  pip install -r requirements.txt


## Set up the Google Vision API

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service/account/key.json"
```

### Usage

#### 1. Extract Text from Images

```python
from main import extract_text

# Define a list of image paths
image_paths = ["path/to/image1.jpg", "http://example.com/image2.jpg", "path/to/image3.png"]

# Extract text from the images
extracted_texts = extract_text(image_paths)

print("Extracted Texts:", extracted_texts)
```

#### 2. Classify Aadhar Data

```python
from your_module import classify_aadhar

# Classify the extracted text
result = classify_aadhar(extracted_texts)

print("Classification:", result)
```

#### Note:

- Ensure the Google Vision API key is correctly set up and accessible.
- Customize the functions based on your specific use case and directory structure.