foresight-rx/
│
├── README.md
├── requirements.txt
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
│
├── models/
│   ├── trained/
│   └── checkpoints/
│
├── src/
│   ├── monitoring/
│   │   ├── process_monitor.py
│   │   ├── file_monitor.py
│   │   └── system_metrics.py
│   │
│   ├── features/
│   │   ├── feature_extractor.py
│   │   └── entropy_calculator.py
│   │
│   ├── ai/
│   │   ├── autoencoder.py
│   │   ├── train.py
│   │   └── infer.py
│   │
│   ├── detection/
│   │   ├── threat_scorer.py
│   │   └── alert_manager.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── gpu_utils.py
│   │   └── helpers.py
│
├── dashboard/
│   ├── app.py
│   └── components/
│
├── simulator/
│   └── ransomware_simulator.py
│
├── scripts/
│   ├── collect_data.py
│   ├── train_model.sh
│   └── run_demo.sh
│
└── tests/
    └── test_pipeline.py