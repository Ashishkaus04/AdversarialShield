# AdversarialShield

A comprehensive evaluation framework for adversarial robustness in network intrusion detection systems.

## Project Overview

Machine learning-based security systems are vulnerable to adversarial attacks. This project:
1. Implements multiple adversarial attacks (FGSM, PGD, data poisoning)
2. Evaluates defense mechanisms (adversarial training, feature squeezing, ensemble)
3. Provides explainability using SHAP
4. Benchmarks all attack-defense combinations

## Setup
```bash
# Clone repository
git clone <your-repo-url>
cd AdversarialShield

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download dataset
# See data/README.md for instructions
```

## Project Structure
```
AdversarialShield/
├── data/               # Dataset files
├── models/             # Model implementations
├── explainability/     # SHAP integration
├── dashboard/          # Streamlit UI
├── notebooks/          # Jupyter notebooks
└── docs/              # Documentation
```

## Current Status

- [x] Day 1: Project setup and data exploration
- [ ] Day 2-3: Data preprocessing
- [ ] Week 2: Base classifier training
- [ ] Week 3-4: Attack implementation
- [ ] Week 5-7: Defense implementation
- [ ] Week 8: Benchmarking

## Author

Ashish Kaushik


## License

MIT