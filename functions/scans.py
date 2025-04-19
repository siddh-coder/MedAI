import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

@st.cache_resource(show_spinner=False)
def get_brain_model():
    try:
        processor = AutoImageProcessor.from_pretrained("jayanta/vit-base-patch16-224-in21k-face-recognition")
        model = AutoModelForImageClassification.from_pretrained("jayanta/vit-base-patch16-224-in21k-face-recognition")
        return processor, model
    except Exception as e:
        st.error(f"Failed to load model and processor. Error: {e}")
        return None, None

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
                        processor, model = get_brain_model()
                        if processor is None or model is None:
                            continue
                        inputs = processor(images=image, return_tensors="pt")
                        with torch.no_grad():
                            outputs = model(**inputs)
                            logits = outputs.logits
                            predicted_class_idx = logits.argmax(-1).item()
                            label = model.config.id2label[predicted_class_idx]
                        st.success(f"Inference Result: {label}")
                    except Exception as e:
                        st.error(f"Could not process the scan. Please ensure it is a valid MRI image. Error: {e}")
            if st.button("Learn More", key=f"learn_{scan_name}"):
                st.info("More detailed resources coming soon!")
