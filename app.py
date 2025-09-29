import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import time

# Set page config for a compact, centered layout
st.set_page_config(page_title="Healthcare Image Encryption", layout="centered", page_icon="🏥")

# Custom CSS for vibrant, polished UI
st.markdown("""
<style>
    .main {background: linear-gradient(to bottom, #d9e6ff, #ffffff); padding: 8px; font-family: 'Arial', sans-serif;}
    .stButton>button {background: linear-gradient(to right, #1a73e8, #4285f4); color: white; border: none; border-radius: 12px; font-size: 16px; padding: 10px 20px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.2);}
    .stButton>button:hover {transform: translateY(-2px); background: linear-gradient(to right, #1557b0, #357abd); box-shadow: 0 4px 8px rgba(0,0,0,0.3);}
    .stSlider label {font-size: 14px; color: #1a3c6e; font-weight: bold; margin-bottom: 5px;}
    .stFileUploader label {font-size: 14px; color: #1a3c6e; font-weight: bold; margin-bottom: 5px;}
    .stImage img {border: 3px solid #1a73e8 !important; border-radius: 10px; max-height: 200px; box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important; margin: 5px auto; display: block;}
    .header {text-align: center; color: #1a3c6e; font-size: 30px; font-weight: bold; margin: 8px 0;}
    .subheader {text-align: center; color: #344))^4e57; font-size: 16px; margin-bottom: 10px;}
    .project-text {text-align: center; color: #333; font-size: 14px; margin: 8px 0; background: #f8f9fa; padding: 10px; border-radius: 8px;}
    .status-bar {text-align: center; color: #2ba847; font-size: 14px; font-weight: bold; margin: 8px 0; background: #e6ffe6; padding: 5px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

def generate_chaotic_sequence(x0, r, length):
    sequence = []
    x = x0
    for _ in range(length):
        x = r * x * (1 - x)
        sequence.append(int((x * 256) % 256))
    return np.array(sequence, dtype=np.uint8)

# Header
st.markdown("<div class='header'>Chaos-Based Image Encryption for Healthcare</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Securely encrypt and decrypt medical images using chaotic sequences</div>", unsafe_allow_html=True)

# Project Details
st.markdown("<div class='project-text'>"
            "<b>Project:</b> Chaos-Based Image Encryption for Healthcare Imaging<br>"
            "<b>Group 1:</b> Sanyam Garg, Divyansh Bhushan, Aman Kumar, Manmohan Kumar, Vishal Kumar<br>"
            "<b>Submitted to:</b> Dr. Kakali Chatterjee, Assistant Professor, NIT Patna"
            "</div>", unsafe_allow_html=True)

# Status bar
if 'status' not in st.session_state:
    st.session_state['status'] = "Ready to Encrypt"
st.markdown(f"<div class='status-bar'>{st.session_state['status']}</div>", unsafe_allow_html=True)

# Input and Actions layout
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose Grayscale Image (e.g., MRI)", type=["jpg", "png"], help="Upload a grayscale MRI image.")
with col2:
    st.subheader("Encryption Keys")
    key_x0 = st.slider("Secret Key X0", min_value=0.0, max_value=1.0, value=0.5, step=0.01, help="Initial value (0 to 1).")
    key_r = st.slider("Secret Key R", min_value=3.5, max_value=4.0, value=3.99, step=0.01, help="Control parameter (3.5 to 4.0).")

# Centered action buttons
st.markdown("<div style='text-align: center; margin: 10px 0;'>", unsafe_allow_html=True)
encrypt_button = st.button("Encrypt Image", key="encrypt", help="Encrypt the uploaded image.")
decrypt_button = st.button("Decrypt Image", key="decrypt", help="Decrypt using the provided keys.")
st.markdown("</div>", unsafe_allow_html=True)

# Process image
if uploaded_file:
    with st.spinner("Processing image..."):
        st.session_state['status'] = "Processing Image..."
        img = np.array(Image.open(uploaded_file).convert('L'))
        height, width = img.shape
        total_pixels = height * width
        flat_img = img.flatten()
        chaotic_seq = generate_chaotic_sequence(key_x0, key_r, total_pixels)
        sort_indices = np.argsort(chaotic_seq)
        
        # Original image
        st.subheader("Original Image")
        st.image(img, caption="Uploaded MRI Image", use_container_width=False, width=200)
        st.session_state['status'] = "Image Loaded"

    if encrypt_button:
        with st.spinner("Encrypting..."):
            st.session_state['status'] = "Encrypting Image..."
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            encrypted_flat = flat_img[sort_indices]
            encrypted_flat = np.bitwise_xor(encrypted_flat, chaotic_seq)
            encrypted_img = encrypted_flat.reshape((height, width)).astype(np.uint8)
            st.session_state['encrypted_flat'] = encrypted_flat
            st.session_state['sort_indices'] = sort_indices
            st.session_state['encrypted_img'] = encrypted_img
            st.session_state['status'] = "Encryption Complete"
            st.success("Encryption complete! Image is secure.")

    if decrypt_button and 'encrypted_flat' in st.session_state:
        with st.spinner("Decrypting..."):
            st.session_state['status'] = "Decrypting Image..."
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            encrypted_flat = st.session_state['encrypted_flat']
            sort_indices = st.session_state['sort_indices']
            chaotic_seq_dec = generate_chaotic_sequence(key_x0, key_r, total_pixels)
            decrypted_flat = np.bitwise_xor(encrypted_flat, chaotic_seq_dec)
            inverse_indices = np.argsort(sort_indices)
            decrypted_flat = decrypted_flat[inverse_indices]
            decrypted_img = decrypted_flat.reshape((height, width)).astype(np.uint8)
            st.session_state['decrypted_img'] = decrypted_img
            st.session_state['status'] = "Decryption Complete"
            st.success("Decryption complete! Verify the image matches the original.")

    # Side-by-side encrypted and decrypted images
    if 'encrypted_img' in st.session_state or 'decrypted_img' in st.session_state:
        st.subheader("Results")
        col_enc, col_dec = st.columns([1, 1])
        with col_enc:
            if 'encrypted_img' in st.session_state:
                st.image(st.session_state['encrypted_img'], caption="Encrypted Image", use_container_width=False, width=200)
                buf = io.BytesIO()
                Image.fromarray(st.session_state['encrypted_img']).save(buf, format="PNG")
                st.download_button("Download Encrypted Image", buf.getvalue(), "encrypted.png", key="download_encrypt")
        with col_dec:
            if 'decrypted_img' in st.session_state:
                st.image(st.session_state['decrypted_img'], caption="Decrypted Image", use_container_width=False, width=200)
                buf = io.BytesIO()
                Image.fromarray(st.session_state['decrypted_img']).save(buf, format="PNG")
                st.download_button("Download Decrypted Image", buf.getvalue(), "decrypted.png", key="download_decrypt")