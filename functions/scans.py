import streamlit as st
from PIL import Image
import numpy as np
import json
from tensorflow import keras

@st.cache_resource(show_spinner=False)
def get_brain_model():
    try:
        model = keras.models.load_model("models/pkl/tumor.h5")
        with open("models/pkl/tumor_class_names.json") as f:
            class_names = json.load(f)
        return model, class_names
    except Exception as e:
        st.error(f"Failed to load brain tumor model or class names. Error: {e}")
        return None, None

def preprocess_brain_image(image, target_size=(224, 224)):
    image = image.resize(target_size)
    img_array = np.array(image) # / 255.0
    if img_array.ndim == 2:
        img_array = np.stack([img_array]*3, axis=-1)
    img_array = img_array[..., :3]  # Ensure 3 channels
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)

def show():
    st.title("Medical Scans")
    st.markdown("Learn about different medical imaging techniques available.")
    
    scan_types = {
        "Brain Tumor Scan": {
            "description": "MRI scans to detect abnormal growths in the brain.",
            "details": "Magnetic Resonance Imaging (MRI) is used to create detailed images of the brain, helping identify tumors, their size, and location. Early detection is critical for effective treatment."
        },
        "Lung Scan": {
            "description": "CT scans to assess lung health and detect abnormalities.",
            "details": "Computed Tomography (CT) scans provide cross-sectional images of the lungs, useful for diagnosing conditions like lung cancer, infections, or chronic obstructive pulmonary disease (COPD)."
        },
        "Cataract Scan": {
            "description": "Eye imaging to diagnose cataracts.",
            "details": "Specialized imaging techniques, such as slit-lamp exams and optical coherence tomography (OCT), help detect clouding of the eye's lens, guiding surgical or non-surgical interventions."
        }
    }
    
    tabs = st.tabs(list(scan_types.keys()))
    
    for idx, (scan_name, scan_info) in enumerate(scan_types.items()):
        with tabs[idx]:
            st.subheader(scan_name)
            st.write(f"**Description**: {scan_info['description']}")
            st.markdown(f"**Details**: {scan_info['details']}")
            if scan_name == "Brain Tumor Scan":
                st.markdown("---")
                st.markdown("#### Upload a Brain MRI Scan for AI Analysis")
                uploaded_scan = st.file_uploader(
                    "Upload MRI Image (PNG, JPG, JPEG)",
                    type=["png", "jpg", "jpeg"],
                    key="brain_mri_upload"
                )
                if uploaded_scan is not None:
                    try:
                        image = Image.open(uploaded_scan).convert("RGB")
                        model, class_names = get_brain_model()
                        if model is None or class_names is None:
                            return
                        img_array = preprocess_brain_image(image)
                        preds = model.predict(img_array)
                        pred_class = np.argmax(preds, axis=1)[0]
                        label = class_names[pred_class]
                        st.success(f"Inference Result: {label}")
                    except Exception as e:
                        st.error(f"Could not process the scan. Please ensure it is a valid MRI image. Error: {e}")
            if st.button("Learn More", key=f"learn_{scan_name}"):
                st.info("More detailed resources coming soon!")
