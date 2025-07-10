MODEL_CONFIGS = [
    # {
    #     "name": "Model 1 (Acc 94%)",
    #     "path": "ml_model/lda/lda_v1.sav",
    #     "columns": [
    #         'jenis_kelamin', 'usia', 'dm', 'gagal_jantung', 'hipertensi',
    #         'af', 'hemiparesis', 'hemihipestesi_parestesia', 'paresis_nervus_kranialis',
    #         'deviasi_konjugat', 'afasia', 'nihss_in_(di_atas_6)', 'ddimer', 'at', 'hct', 'fibrinogen',
    #         'leukosit', 'neutrofil', 'limfosit', 'nc', 'lc', 'nlr', 'gds', 'gdp',
    #         'hba1c', 'hyperdense', 'insullar_ribbon', 'gcs_code_(kesadaran_menurun)',
    #         'ct_mca', 'ct_insula'
    #     ]
    # },
    # {
    #     "name": "Model 2 (Acc 90%)",
    #     "path": "ml_model/lda/lda_v1.1.sav",
    #     "columns": [
    #         'nihss_in_(di_atas_6)', 'insullar_ribbon', 'hemiparesis',
    #         'deviasi_konjugat', 'gcs_code_(kesadaran_menurun)', 'afasia',
    #         'ct_mca', 'ct_insula'
    #     ]
    # },
    {
        "name": "Model 1 RF (Acc 93.55%)",
        "path": "ml_model/random_forest/random_forest_1.sav",
        "require_ct": True,
        "columns": [
            'usia', 'jenis_kelamin', 'dm',
            'gagal_jantung', 'hipertensi', 'af', 'hemiparesis',
            'hemihipestesi_parestesia', 'paresis_nervus_kranialis',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ddimer', 'hct', 'at', 'hyperdense', 'insullar_ribbon',
            'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Model 2 RF (Acc 83.87%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_2.sav",
        "columns": [
            'usia', 'jenis_kelamin', 'dm',
            'gagal_jantung', 'hipertensi', 'af', 'hemiparesis',
            'hemihipestesi_parestesia', 'paresis_nervus_kranialis',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in',
            'ddimer', 'hct', 'at', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Model 7 RF (Acc 74.19%)",
        "require_ct": True,
        "path": "ml_model/random_forest/random_forest_7.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in_(di_atas_10)',
            'at', 'hct', 'ct_mca', 'ct_insula'
        ]
    },
    {
        "name": "Model 8b RF (Acc 80.65%)",
        "require_ct": False,
        "path": "ml_model/random_forest/random_forest_8b.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)'
        ]
    },
    {
        "name": "Model 9 RF (Acc 64.52%)",
        "require_ct": False,
        "path": "ml_model/random_forest/random_forest_9.sav",
        "columns": [
            'hemiparesis', 'hemihipestesi_parestesia',
            'deviasi_konjugat', 'afasia', 'gcs_code_(kesadaran_menurun)', 'nihss_in_(di_atas_10)'
        ]
    },
    
]