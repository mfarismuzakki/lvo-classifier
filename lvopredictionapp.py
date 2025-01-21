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
import gdown

# Streamlit app configuration
st.set_page_config(
    page_title="LVO Classifier",
    page_icon="images/ui_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "A CT scan classifier powered by machine learning."}
)

# Utility functions
def save_temporary_dicom(uploaded_files, name):
    """Save uploaded DICOM files temporarily."""
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
    """Convert DICOM files to NIfTI format."""
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

    if plane == 'mca':
        # Geser slice index MCA ke atas
        slice_index = image_data.shape[2] // 3 + 3  # Menambahkan 5 slice ke atas
        slice_data = image_data[:, :, slice_index]
    elif plane == 'insula':
        slice_index = image_data.shape[2] // 2
        slice_data = image_data[:, :, slice_index]

    # Calculate the aspect ratio to balance the dimensions
    x_dim, y_dim, _ = img.header.get_zooms()
    aspect_ratio = y_dim / x_dim

    # Increase the dpi to improve the resolution
    dpi = 200

    slice_data = apply_windowing(slice_data, wl, ww)

    print(output_path)

    # Create a new figure with a balanced aspect ratio and higher dpi
    plt.figure(figsize=(8, 8 * aspect_ratio), dpi=dpi)
    plt.imshow(slice_data.T, cmap='gray', origin='lower', aspect='auto')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

def apply_windowing(slice_data, wl, ww):
    """Apply window level and width to the slice."""
    min_val = wl - ww / 2
    max_val = wl + ww / 2
    slice_data = np.clip(slice_data, min_val, max_val)
    return (slice_data - min_val) / (max_val - min_val)

def classify(compliment_data, model_path):
    """Classify the input data."""
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
    mca = cv2.resize(mca, (128, 128))
    mca = mca.astype('float32')
    mca = (mca / 255.0).flatten()

    insula = cv2.imread(f'temporary_ct_data/slices/insula_{img_name}.png')
    insula = cv2.resize(insula, (128, 128))
    insula = insula.astype('float32')
    insula = (insula / 255.0).flatten()

    os.remove(f'temporary_ct_data/slices/mca_{img_name}.png')
    os.remove(f'temporary_ct_data/slices/insula_{img_name}.png')

    return np.array([mca]), np.array([insula])

def image_to_tabular(mca, insula):

    ae_load_model = load_model('ml_model/autoencoder/v1.h5')
    mca = ae_load_model.predict(mca)
    insula = ae_load_model.predict(insula)

    return mca, insula

# Streamlit UI
def main():

    # logo_path = "images/fkui_logo.png"
    # st.image(logo_path, use_container_width=True)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; background-color: #778899; padding: 10px; border-radius: 5px;">
            <div>
                <h3 style="margin: 0; color: white;">Fakultas Kedokteran, Universitas Indonesia</h3>
                <h5 style="margin: 0; color: white;">dr. Mohammad Kurniawan, Sp.S (K), Msc, FICA</h5>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("LVO Classifier")
    st.sidebar.header("Upload Input Data")

    # Pilihan tipe model
    model_type = st.sidebar.selectbox("Model Type", ["All Data", "Selected Column"])
    uploaded_files = st.sidebar.file_uploader("Upload DICOM Files", accept_multiple_files=True) if model_type == "All Data" else None

    st.sidebar.subheader("Tabular Input Data")

    # Daftar kolom
    columns_all = ['jenis_kelamin', 'usia', 'dm', 'gagal_jantung', 'hipertensi', 'af', 
                   'hemiparesis', 'hemihipestesi_parestesia', 'paresis_nervus_kranialis', 
                   'deviasi_konjugat', 'afasia', 'nihss_in', 'ddimer', 'gcs_code', 
                   'Interpretasi_cta', 'hyperdense', 'insullar_ribbon']
    columns_selected = ['hemiparesis', 'nihss_in', 'hyperdense', 'insullar_ribbon']

    # Pilih kolom berdasarkan tipe model
    selected_columns = columns_all if model_type == "All Data" else columns_selected

    # Kolom boolean untuk "Ya"/"Tidak"
    boolean_columns = ['dm', 'gagal_jantung', 'hipertensi', 'af', 'hemiparesis', 
                       'hemihipestesi_parestesia', 'paresis_nervus_kranialis', 
                       'deviasi_konjugat', 'afasia', 'hyperdense', 'insullar_ribbon', 
                       'gcs_code', 'Interpretasi_cta']

    # Input jenis_kelamin
    if 'jenis_kelamin' in selected_columns:
        jenis_kelamin = st.sidebar.selectbox("Jenis kelamin", options=["Pria", "Wanita"])

    # Input kolom boolean
    boolean_inputs = {}
    for col in boolean_columns:
        if col in selected_columns:
            boolean_inputs[col] = st.sidebar.selectbox(col.replace('_', ' ').capitalize(), options=["Ya", "Tidak"])

    # Input kolom numerik
    numerical_columns = [col for col in selected_columns if col not in boolean_columns + ['jenis_kelamin']]
    numerical_inputs = {col: st.sidebar.number_input(col.replace('_', ' ').capitalize(), value=0.0) for col in numerical_columns}

    # Gabungkan semua input
    tabular_input = {**numerical_inputs}
    if 'jenis_kelamin' in selected_columns:
        tabular_input['jenis_kelamin'] = 1 if jenis_kelamin == "Pria" else 0
    for col, value in boolean_inputs.items():
        tabular_input[col] = 1 if value == "Ya" else 0

    # Pastikan kolom input sesuai dengan urutan di columns_all atau columns_selected
    final_input = []
    for col in (columns_all if model_type == "All Data" else columns_selected):
        if col in tabular_input:
            final_input.append(tabular_input[col])
        else:
            # Jika kolom tidak diisi, beri nilai default (0 atau nilai lain yang sesuai)
            final_input.append(0)

    # Tombol untuk klasifikasi
    if st.sidebar.button("Classify"):
        with st.spinner("Processing..."):
            random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            dicom_path = nifti_path = None

            # Jika tipe model adalah "All Data" dan file DICOM diunggah
            if model_type == "All Data" and uploaded_files:
                dicom_path = save_temporary_dicom(uploaded_files, random_name)
                if dicom_path:
                    nifti_path = convert_dicom_to_nifti(random_name)
                if nifti_path:
                    img = nib.load(nifti_path)
                    image_data = img.get_fdata()

                    if not os.path.exists('temporary_ct_data/slices'):
                        os.makedirs('temporary_ct_data/slices')

                    # Simpan slice MCA dan insula
                    save_slices(image_data, f'temporary_ct_data/slices/mca_{random_name}.png', 'mca', img)
                    save_slices(image_data, f'temporary_ct_data/slices/insula_{random_name}.png', 'insula', img)

                    st.subheader("Generated Slices")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(f'temporary_ct_data/slices/mca_{random_name}.png', caption="MCA Slice", use_container_width=True)
                    with col2:
                        st.image(f'temporary_ct_data/slices/insula_{random_name}.png', caption="Insula Slice", use_container_width=True)

                    mca, insula = load_slice_image(random_name)
                    mca_tab, insula_tab = image_to_tabular(mca, insula)

                    columns_all.append('ct_mca')
                    columns_all.append('ct_insula')
                    final_input.append(mca_tab)
                    final_input.append(insula_tab)

                    shutil.rmtree(f'temporary_ct_data/dicom/{random_name}')
                    os.remove(nifti_path)

            # Pilih model berdasarkan tipe
            model_path = 'ml_model/random_forest/random_forest_all_column.sav' if model_type == "All Data" else 'ml_model/mlp/mlp_selected_column.sav'
            compliment_data = pd.DataFrame([final_input], columns=columns_all if model_type == "All Data" else columns_selected)
            result, result_proba = classify(compliment_data, model_path)

            if result is not None:
                labels = ["Tidak LVO", "LVO"]
                values = [p * 100 for p in result_proba[0]]

                classification_label = "Ya, terdapat kemungkinan LVO" if result == 1 else "Tidak, LVO tidak terdeteksi"

                # Menampilkan kesimpulan utama
                st.header(f"Hasil Klasifikasi: **{classification_label}**")
                
                # Menambahkan deskripsi kesimpulan
                if result == 1:
                    st.markdown(f"""
                    **Kesimpulan:** Hasil klasifikasi menunjukkan **LVO terdeteksi** dengan probabilitas sebesar **{values[1]:.2f}%**.
                    """)
                else:
                    st.markdown(f"""
                    **Kesimpulan:** Hasil klasifikasi menunjukkan **tidak ada LVO terdeteksi** dengan probabilitas sebesar **{values[0]:.2f}%**.
                    """)

                # Tampilkan probabilitas klasifikasi
                st.subheader("Probabilitas Deteksi LVO")
                if result_proba is not None:
                    # Data untuk donut chart
                    # Membuat donut chart dengan Plotly
                    fig = go.Figure(data=[go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.6,  # Membuat pie chart menjadi donut
                        textinfo='label+percent',
                        hoverinfo='label+value',
                        marker=dict(colors=["#636EFA", "#EF553B"], line=dict(color="#FFFFFF", width=2))
                    )])

                    fig.update_layout(
                        title="Distribusi Probabilitas Klasifikasi",
                        annotations=[dict(
                            text="LVO",
                            x=0.5,
                            y=0.5,
                            font_size=20,
                            showarrow=False
                        )]
                    )

                    # Render chart di Streamlit
                    st.plotly_chart(fig, use_container_width=True)
                    
if __name__ == "__main__":
    main()
