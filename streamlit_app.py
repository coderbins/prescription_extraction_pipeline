import os
import zipfile
import streamlit as st
import cv2
from PIL import Image
from src.preprocess import load_image, list_images
from src.model import extract_structured_data
import shutil  # Add this import for deleting directories

# App Title
st.title("🧾 Handwritten Prescription Extraction Pipeline")

# Initialize session state variables
if "raw_md" not in st.session_state:
    st.session_state.raw_md = None
if "dataset_results" not in st.session_state:
    st.session_state.dataset_results = []

# Function to cleanup temporary files and folders
def cleanup_temp_files():
    """Delete temporary files and folders."""
    temp_files = ["temp.zip", "temp.jpg", "temp.png", "temp.jpeg", "temp_dataset.zip"]
    temp_folders = ["temp_dataset", "images"]

    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

    for folder in temp_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

# Choose Upload Mode
upload_mode = st.radio("Choose upload mode", ["Single Image", "Dataset (Zip File)"])

if upload_mode == "Single Image":
    # Upload Single Image
    image_file = st.file_uploader("Upload Prescription Image", type=["jpg", "png", "jpeg"])
    if image_file:
        # Cleanup temporary files before saving the uploaded file
        cleanup_temp_files()

        file_ext = os.path.splitext(image_file.name)[1]
        img_path = f"temp{file_ext}"
        with open(img_path, "wb") as f:
            f.write(image_file.getbuffer())
        st.success("Image uploaded successfully!")

        # Display Image
        img = load_image(img_path)
        if img is None:
            st.error("Error loading image. The file may be unsupported or corrupted.")
        else:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                st.image(img_pil, caption="Uploaded Image", use_container_width=True)

                # Extract Information
                if st.button("Extract Information"):
                    with st.spinner("Processing image..."):
                        st.session_state.raw_md = extract_structured_data(img_path)
                    st.markdown(st.session_state.raw_md, unsafe_allow_html=True, help=None)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

elif upload_mode == "Dataset (Zip File)":
    # Upload Dataset
    dataset_file = st.file_uploader("Upload Dataset (Zip File)", type=["zip"])
    if dataset_file:
        # Cleanup temporary files before saving the uploaded file
        cleanup_temp_files()

        dataset_path = "temp_dataset"
        with open("temp_dataset.zip", "wb") as f:
            f.write(dataset_file.getbuffer())
        try:
            # Extract the zip file
            with zipfile.ZipFile("temp_dataset.zip", "r") as zip_ref:
                zip_ref.extractall(dataset_path)
            st.success("Dataset uploaded and extracted successfully!")
        except zipfile.BadZipFile:
            st.error("The uploaded file is not a valid zip file. Please upload a valid zip file.")
            st.stop()

        # Flatten the directory structure
        flattened_images_path = os.path.join(dataset_path, "images")
        os.makedirs(flattened_images_path, exist_ok=True)
        for root, _, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):  # Only move image files
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(flattened_images_path, file)

                    # Handle duplicate filenames
                    if os.path.exists(dst_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(dst_path):
                            dst_path = os.path.join(flattened_images_path, f"{base}_{counter}{ext}")
                            counter += 1

                    os.rename(src_path, dst_path)

        # Ensure there are images in the flattened folder
        images = list_images(flattened_images_path)
        if not images:
            st.error("No valid images found in the uploaded dataset.")
            st.stop()

        # Extract Information
        if st.button("Extract Information"):
            with st.spinner("Processing dataset..."):
                st.session_state.dataset_results = []
                for img_path in images:
                    img = load_image(img_path)
                    if img is None:
                        st.warning(f"Skipping invalid or corrupted image: {os.path.basename(img_path)}")
                        continue

                    try:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img_pil = Image.fromarray(img_rgb)
                        st.image(img_pil, caption=f"Processing: {os.path.basename(img_path)}", use_container_width=True)

                        raw_md = extract_structured_data(img_path)
                        st.markdown(raw_md, unsafe_allow_html=False, help=None)
                        st.session_state.dataset_results.append((img_path, raw_md))
                    except Exception as e:
                        st.warning(f"An error occurred while processing {os.path.basename(img_path)}: {e}")
