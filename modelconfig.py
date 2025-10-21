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