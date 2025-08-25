MODEL_CONFIGS = [
    {
        "name": "Complete RF (Acc 90.32%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_2.sav",
        "columns": [
            'usia', 'jenis_kelamin', 'dm', 'gagal_jantung', 'hipertensi',
            'af', 'hemiparesis', 'hemihipestesi_parestesia',
            'paresis_nervus_kranialis', 'deviasi_konjugat', 'afasia',
            'gcs_code_(kesadaran_menurun)', 'nihss_in', 'ddimer_(di_atas_500)',
            'hct', 'at', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Complete MLP (Acc 80.65%)",
        "require_ct": True,
        "path": "ml_model/mlp/mlp_2.sav",
        "columns": [
            'usia', 'jenis_kelamin', 'dm', 'gagal_jantung', 'hipertensi',
            'af', 'hemiparesis', 'hemihipestesi_parestesia',
            'paresis_nervus_kranialis', 'deviasi_konjugat', 'afasia',
            'gcs_code_(kesadaran_menurun)', 'nihss_in', 'ddimer_(di_atas_500)',
            'hct', 'at', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Selected Bivariat RF (Acc 87.10%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_4.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia', 'deviasi_konjugat',
            'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ddimer_(di_atas_500)', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Selected Bivariat MLP (Acc 74.19%)",
        "require_ct": True,
        "path": "ml_model/mlp/mlp_4.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia', 'deviasi_konjugat',
            'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ddimer_(di_atas_500)', 'ct_mca', 'ct_insula'
        ]
    },


    {
        "name": "Bivariate Tanpa D-dimer RF (Acc 80.65%)",
        "require_ct": False,
        "path": "ml_model/random_forest/random_forest_7b.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ct_mca', 'ct_insula'
        ]
    },

    {
        "name": "Bivariate Tanpa D-dimer MLP (Acc 83.87%)",
        "require_ct": False,
        "path": "ml_model/mlp/mlp_7b.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ct_mca', 'ct_insula'
        ]
    },

    {
        "name": "Pre Hospital RF (Acc 80.65%)",
        "require_ct": False,
        "path": "ml_model/random_forest/random_forest_8b.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)'
        ]
    },
    {
        "name": "Pre Hospital MLP (Acc 80.65%)",
        "require_ct": False,
        "path": "ml_model/mlp/mlp_8b.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)'
        ]
    },
]