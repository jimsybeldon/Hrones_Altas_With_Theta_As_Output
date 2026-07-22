![alt text](image.png)

usda_nutrient_tracker/
│
├── data/
│   ├── input/
│   │   └── food_log_template.xlsx      # where you’ll enter your daily foods
│   └── output/
│       └── daily_nutrient_report.xlsx  # auto-generated reports
│
├── src/
│   ├── __init__.py
│   ├── main.py                         # main entry point (run this)
│   ├── config.py                       # holds API key, constants
│   ├── usda_api.py                     # handles USDA API calls
│   ├── processing.py                   # does nutrient calculations & DRI comparison
│   ├── excel_writer.py                 # builds styled Excel output
│
├── tests/
│   └── test_usda_api.py                # optional: verify that API calls work
│
├── requirements.txt                    # Python package dependencies
└── README.md                           # documentation
