"""
Verify that preprocessing completed successfully
"""
import numpy as np
import joblib
from pathlib import Path

print("🔍 Verifying preprocessing outputs...")
print("="*60)

# Check if all files exist
required_files = [
    'data/processed/X_train.npy',
    'data/processed/X_test.npy',
    'data/processed/y_train.npy',
    'data/processed/y_test.npy',
    'data/processed/scaler.pkl',
    'data/processed/feature_names.pkl',
    'data/processed/metadata.pkl',
]

all_exist = True
for filepath in required_files:
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    print(f"{status} {filepath}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n❌ Some files are missing. Re-run preprocessing notebook.")
    exit(1)

print("\n✓ All files exist")

# Load and verify data
print("\n📊 Loading data...")
X_train = np.load('data/processed/X_train.npy')
X_test = np.load('data/processed/X_test.npy')
y_train = np.load('data/processed/y_train.npy')
y_test = np.load('data/processed/y_test.npy')

print(f"✓ Training set: {X_train.shape}")
print(f"✓ Test set: {X_test.shape}")

# Load metadata
metadata = joblib.load('data/processed/metadata.pkl')
print(f"\n✓ Features: {metadata['n_features']}")
print(f"✓ Train samples: {metadata['n_train_samples']:,}")
print(f"✓ Test samples: {metadata['n_test_samples']:,}")

# Check data quality
print("\n🔍 Data quality checks:")

# 1. No NaN values
if np.isnan(X_train).any() or np.isnan(X_test).any():
    print("✗ Found NaN values!")
else:
    print("✓ No NaN values")

# 2. No infinity values
if np.isinf(X_train).any() or np.isinf(X_test).any():
    print("✗ Found infinity values!")
else:
    print("✓ No infinity values")

# 3. Proper scaling (mean ≈ 0, std ≈ 1)
mean = X_train.mean()
std = X_train.std()
print(f"✓ Training data - Mean: {mean:.6f}, Std: {std:.6f}")

if abs(mean) < 0.01 and abs(std - 1.0) < 0.1:
    print("✓ Data is properly scaled")
else:
    print("⚠️  Data scaling might be off")

# 4. Class balance
unique, counts = np.unique(y_train, return_counts=True)
print(f"\n✓ Training labels: {dict(zip(unique, counts))}")
print(f"  Class balance: {counts[0]/counts[1]:.2f}:1 (BENIGN:ATTACK)")

print("\n" + "="*60)
print("✅ PREPROCESSING VERIFICATION COMPLETE")
print("="*60)
print("\nYou're ready for Day 3: Training the baseline classifier!")