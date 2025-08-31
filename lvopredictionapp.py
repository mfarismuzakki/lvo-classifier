import streamlit as st
import os
import random
import string
import shutil
import pandas as pd
import numpy as np
import cv2
import nibabel as nib
import matplotlib.pyplot as plt
from keras.models import load_model
import joblib
import dicom2nifti
import plotly.graph_objects as go
from modelconfig import MODEL_CONFIGS

dicom2nifti.settings.disable_validate_slice_increment()

# Streamlit app configuration
st.set_page_config(
    page_title="LVO Classifier",
    page_icon="images/ui_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "A CT scan classifier powered by machine learning."}
)

# ---------- Utility Functions ----------

def save_temporary_dicom(uploaded_files, name):
    try:
        default_path = f'temporary_ct_data/dicom/{name}'
        os.makedirs(default_path, exist_ok=True)
        for idx, dicom_file in enumerate(uploaded_files):
            with open(f'{default_path}/{idx}.dcm', 'wb') as f:
                f.write(dicom_file.read())
        return default_path
    except Exception as e:
        st.error(f"Error saving DICOM files: {e}")
        return None

def convert_dicom_to_nifti(name):
    try:
        dicom_path = f'temporary_ct_data/dicom/{name}/'
        nifti_path = f'temporary_ct_data/nifti/{name}/'
        os.makedirs(nifti_path, exist_ok=True)
        dicom2nifti.convert_directory(dicom_path, nifti_path, compression=True, reorient=True)
        nifti_file_name = os.listdir(nifti_path)[0]
        output_file = f'temporary_ct_data/nifti/{name}.nii.gz'
        shutil.move(f'{nifti_path}/{nifti_file_name}', output_file)
        shutil.rmtree(nifti_path)
        return output_file
    except Exception as e:
        st.error(f"Error converting DICOM to NIfTI: {e}")
        return None

def save_slices(image_data, output_path, plane, img):
    wl = 40
    ww = 80
    slice_index = image_data.shape[2] // 3 + 3 if plane == 'mca' else image_data.shape[2] // 2
    slice_data = image_data[:, :, slice_index]

    x_dim, y_dim, _ = img.header.get_zooms()
    aspect_ratio = y_dim / x_dim
    dpi = 200
    slice_data = apply_windowing(slice_data, wl, ww)

    plt.figure(figsize=(8, 8 * aspect_ratio), dpi=dpi)
    plt.imshow(slice_data.T, cmap='gray', origin='lower', aspect='auto')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

def apply_windowing(slice_data, wl, ww):
    min_val = wl - ww / 2
    max_val = wl + ww / 2
    slice_data = np.clip(slice_data, min_val, max_val)
    return (slice_data - min_val) / (max_val - min_val)

def classify(compliment_data, model_path):
    try:
        model = joblib.load(model_path)
        result = model.predict(compliment_data)
        result_proba = model.predict_proba(compliment_data)
        return result[0], result_proba
    except Exception as e:
        st.error(f"Error in classification: {e}")
        return None, None

def load_slice_image(img_name):
    mca = cv2.imread(f'temporary_ct_data/slices/mca_{img_name}.png')
    insula = cv2.imread(f'temporary_ct_data/slices/insula_{img_name}.png')
    mca = cv2.resize(mca, (128, 128)).astype('float32') / 255.0
    insula = cv2.resize(insula, (128, 128)).astype('float32') / 255.0
    os.remove(f'temporary_ct_data/slices/mca_{img_name}.png')
    os.remove(f'temporary_ct_data/slices/insula_{img_name}.png')
    return np.array([mca.flatten()]), np.array([insula.flatten()])

@st.cache_resource
def get_autoencoder_model():
    return load_model('ml_model/autoencoder/v1.h5')

def image_to_tabular(mca, insula):
    ae = get_autoencoder_model()
    return ae.predict(mca), ae.predict(insula)

# ---------- Main App ----------
def main():
    st.markdown("""
        <div style="display: flex; align-items: center; background-color: #778899; padding: 10px; border-radius: 5px;">
            <div>
                <h3 style="margin: 0; color: white;">Fakultas Kedokteran, Universitas Indonesia</h3>
                <h5 style="margin: 0; color: white;">dr. Mohammad Kurniawan, Sp.S (K), Msc, FICA</h5>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
    st.title("LVO Classifier")
    st.sidebar.header("Upload Input Data")

    # --- Model selection ---
    model_names = [m['name'] for m in MODEL_CONFIGS]
    model_name = st.sidebar.selectbox("Model Type", model_names)
    selected_model = next((m for m in MODEL_CONFIGS if m['name'] == model_name), None)

    if not selected_model:
        st.error("Model config not found.")
        return

    columns_selected = selected_model["columns"]
    model_path = selected_model["path"]

    uploaded_files = None
    if selected_model.get("require_ct", True):
        uploaded_files = st.sidebar.file_uploader("Upload DICOM Files", accept_multiple_files=True)

    st.sidebar.subheader("Tabular Input Data")

    # --- Input Data ---
    boolean_columns = [
        'dm', 'gagal_jantung', 'hyperdense', 'hipertensi', 'af', 'hemiparesis',
        'hemihipestesi_parestesia', 'paresis_nervus_kranialis', 'deviasi_konjugat',
        'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in_(di_atas_6)', 'nihss_in_(di_atas_10)', 
        'ddimer_(di_atas_500)'
    ]

    tabular_input = {}
    if 'jenis_kelamin' in columns_selected:
        jk = st.sidebar.selectbox("Jenis kelamin", ["Pria", "Wanita"])
        tabular_input['jenis_kelamin'] = 1 if jk == "Pria" else 0

    for col in columns_selected:
        if col == 'jenis_kelamin':
            continue
        if col in boolean_columns:
            val = st.sidebar.selectbox(col.replace('_', ' ').capitalize(), ["Ya", "Tidak"])
            tabular_input[col] = 1 if val == "Ya" else 0
        elif not col.startswith('ct_'):
            tabular_input[col] = st.sidebar.number_input(col.replace('_', ' ').capitalize(), value=0.0)

    # --- Classification ---
    if st.sidebar.button("Classify"):
        with st.spinner("Processing..."):
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

            mca_tab = insula_tab = None
            if selected_model.get("require_ct", True) and uploaded_files:
                dicom_path = save_temporary_dicom(uploaded_files, name)
                nifti_path = convert_dicom_to_nifti(name)
                if nifti_path:
                    img = nib.load(nifti_path)
                    image_data = img.get_fdata()
                    os.makedirs('temporary_ct_data/slices', exist_ok=True)

                    save_slices(image_data, f'temporary_ct_data/slices/mca_{name}.png', 'mca', img)
                    save_slices(image_data, f'temporary_ct_data/slices/insula_{name}.png', 'insula', img)

                    st.subheader("Generated Slices")
                    col1, col2 = st.columns(2)
                    col1.image(f'temporary_ct_data/slices/mca_{name}.png', caption="MCA Slice", use_container_width=True)
                    col2.image(f'temporary_ct_data/slices/insula_{name}.png', caption="Insula Slice", use_container_width=True)

                    mca, insula = load_slice_image(name)
                    mca_tab, insula_tab = image_to_tabular(mca, insula)

                    shutil.rmtree(f'temporary_ct_data/dicom/{name}', ignore_errors=True)
                    os.remove(nifti_path)

            # Final input
            final_input = []
            for col in columns_selected:
                if col == 'ct_mca':
                    final_input.append(mca_tab[0] if mca_tab is not None else 0)
                elif col == 'ct_insula':
                    final_input.append(insula_tab[0] if insula_tab is not None else 0)
                else:
                    final_input.append(tabular_input.get(col, 0))

            df_input = pd.DataFrame([final_input], columns=columns_selected)
            result, result_proba = classify(df_input, model_path)

            if result is not None:
                labels = ["Tidak LVO", "LVO"]
                values = [p * 100 for p in result_proba[0]]
                classification_label = "Ya, terdapat kemungkinan LVO" if result == 1 else "Tidak, LVO tidak terdeteksi"

                st.header(f"Hasil Klasifikasi: **{classification_label}**")
                st.markdown(f"""
                **Kesimpulan:** Hasil klasifikasi menunjukkan **{"LVO terdeteksi" if result == 1 else "tidak ada LVO terdeteksi"}**
                dengan probabilitas sebesar **{values[result]:.2f}%**.
                """)

                st.subheader("Probabilitas Deteksi LVO")
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.6,
                    textinfo='label+percent',
                    hoverinfo='label+value',
                    marker=dict(colors=["#636EFA", "#EF553B"], line=dict(color="#FFFFFF", width=2))
                )])
                fig.update_layout(title="Distribusi Probabilitas Klasifikasi", annotations=[dict(text="LVO", x=0.5, y=0.5, font_size=20, showarrow=False)])
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
