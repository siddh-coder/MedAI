import streamlit as st

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
            if st.button("Learn More", key=f"learn_{scan_name}"):
                st.info("More detailed resources coming soon!")
