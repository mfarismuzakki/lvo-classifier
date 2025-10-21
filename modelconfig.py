# Placeholder configuration for input fields
FIELD_PLACEHOLDERS = {
    # 'usia': 'Tahun',
    # 'jenis_kelamin': 'Pilih jenis kelamin',
    # 'dm': 'Apakah pasien memiliki diabetes mellitus?',
    # 'gagal_jantung': 'Apakah pasien memiliki gagal jantung?',
    # 'hyperdense': 'Apakah terdapat tanda hyperdense?',
    # 'hipertensi': 'Apakah pasien memiliki hipertensi?',
    # 'af': 'Apakah pasien memiliki atrial fibrilasi?',
    # 'hemiparesis': 'Apakah terdapat hemiparesis?',
    # 'hemihipestesi_parestesia': 'Apakah terdapat hemihipestesi/parestesia?',
    # 'paresis_nervus_kranialis': 'Apakah terdapat paresis nervus kranialis?',
    # 'deviasi_konjugat': 'Apakah terdapat deviasi konjugat?',
    # 'afasia': 'Apakah terdapat afasia?',
    # 'gcs_code_(kesadaran_menurun)': 'Apakah kesadaran menurun?',
    # 'nihss_in': 'Masukkan nilai NIHSS (contoh: 8)',
    # 'nihss_in_(di_atas_6)': 'Apakah NIHSS di atas 6?',
    # 'nihss_in_(di_atas_10)': 'Apakah NIHSS di atas 10?',
    # 'ddimer_(di_atas_500)': 'Apakah D-Dimer di atas 500?',
    'hct': '%',
    'at': 'x 10^3/µL',
    # 'nlr': 'Masukkan nilai neutrophil-lymphocyte ratio (contoh: 3.5)',
    'nc': 'x 10^3/µL',
    # 'neutrofil': 'Masukkan nilai neutrofil (contoh: 75)',
    # 'leukosit': 'Masukkan nilai leukosit (contoh: 9500)',
    # 'ct_mca': 'Nilai CT MCA (otomatis dari gambar)',
    # 'ct_insula': 'Nilai CT Insula (otomatis dari gambar)'
}

MODEL_CONFIGS = [
    {
        "name": "Skema 1 RF (Acc 90.32%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_2b.sav",
        "columns": [
            'usia', 'jenis_kelamin', 'dm', 'gagal_jantung', 'hipertensi',
            'af', 'hemiparesis', 'hemihipestesi_parestesia',
            'paresis_nervus_kranialis', 'deviasi_konjugat', 'afasia',
            'gcs_code_(kesadaran_menurun)', 'nihss_in', 'ddimer_(di_atas_500)',
            'hct', 'at', 'nlr', 'nc', 'leukosit', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Skema 1 MLP (Acc 77.42%)",
        "require_ct": True,
        "path": "ml_model/mlp/mlp_2b.sav",
        "columns": [
            'usia', 'jenis_kelamin', 'dm', 'gagal_jantung', 'hipertensi',
            'af', 'hemiparesis', 'hemihipestesi_parestesia',
            'paresis_nervus_kranialis', 'deviasi_konjugat', 'afasia',
            'gcs_code_(kesadaran_menurun)', 'nihss_in', 'ddimer_(di_atas_500)',
            'hct', 'at', 'nlr', 'nc', 'leukosit', 'ct_mca', 'ct_insula'
        ]
    },

    {
        "name": "Skema 2 RF (Acc 87.10%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_4.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia', 'deviasi_konjugat',
            'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ddimer_(di_atas_500)', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Skema 2 MLP (Acc 74.19%)",
        "require_ct": True,
        "path": "ml_model/mlp/mlp_4.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia', 'deviasi_konjugat',
            'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'neutrofil', 'nlr', 'ct_mca', 'ct_insula'
        ]
    },

    {
        "name": "Skema 3 RF (Acc 83.87%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_4c.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'nlr', 'ct_mca', 'ct_insula'
        ]
    }
]