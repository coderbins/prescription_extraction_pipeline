# prescription_extraction_pipeline

End-to-end pipeline to extract structured data from handwritten medical prescriptions using Google Gemini 2.0 and Streamlit for UI.

---

## Pipeline Overview

The pipeline processes handwritten medical prescriptions and extracts structured data in Markdown format. It supports both single image uploads and batch processing of images in a zip file.

### Flowchart

```plaintext
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  User Uploads     | ----> |  Preprocessing    | ----> |  Structured Data  |
|  Image(s)         |       |  (Validation,     |       |  Extraction       |
|                   |       |  Loading)         |       |  Using Gemini LLM |
+-------------------+       +-------------------+       +-------------------+
        |                                                       |
        |                                                       v
        +------------------------------------------------>  Markdown Output
```

---

## Pipeline Steps

### 1. User Uploads Image(s)
   - Single Image Mode: Users can upload a single prescription image in `.jpg`, `.jpeg`, or `.png` format.
   - Dataset Mode: Users can upload a zip file containing multiple prescription images.

### 2. Preprocessing
   - Validation: Ensures the uploaded files are valid image formats.
   - Loading: Images are loaded into memory using OpenCV for further processing.
   - Flattening (Dataset Mode): If a zip file is uploaded, the directory structure is flattened, and all valid images are extracted.

### 3. Structured Data Extraction
   - The loaded image(s) are passed to the `extract_structured_data` function in `src/model.py`.
   - The function uses the Google Gemini 2.0 API to analyze the image and extract structured data, such as:
     - Patient information
     - Prescribed drugs
     - Dosage
     - Frequency
     - Duration
     - Special instructions
   - The extracted data is returned in Markdown format.

### 4. Output
   - The extracted data is displayed in the Streamlit app as Markdown.
   - For batch processing, results for each image are displayed sequentially.

---

## Setup

1. Create a Virtual Environment:
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set Up Environment Variables:
   - Create a `.env` file in the root directory:
     ```bash
     touch .env
     ```
   - Add your `GEMINI_API_KEY` to the `.env` file:
     ```
     GEMINI_API_KEY="your_api_key_here"
     ```

4. Run the Streamlit App:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Notes
- Ensure your `.env` file is not shared publicly to protect your API key.
- The pipeline supports both single image uploads and batch processing of images in a zip file.

---

## Files

- `streamlit_app.py`: Streamlit UI for file upload and dataset processing.
- `src/preprocess.py`: Image preprocessing functions (e.g., loading images).
- `src/model.py`: Gemini API client and logic for extracting structured data.
- `src/__init__.py`: Empty file to mark the `src` directory as a package.
- `requirements.txt`: List of dependencies for the project.
- `.env`: Environment variables file containing the `GEMINI_API_KEY`.

---

## Features

- Single Image Mode: Upload a single prescription image for processing.
- Dataset Mode: Upload a zip file containing multiple prescription images for batch processing.
- Preprocessing: Basic image loading and validation.
- Structured Data Extraction: Uses Google Gemini 2.0 to extract and format prescription details in Markdown.

---

## Limitations

- Ensure the uploaded images are in `.jpg`, `.jpeg`, or `.png` format.
