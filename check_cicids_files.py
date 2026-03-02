"""
Check what CICIDS files you have and their contents
"""
from pathlib import Path
import pandas as pd

data_dir = Path('data/raw')

print("🔍 Checking CICIDS2017 files...")
print("="*60)

csv_files = list(data_dir.glob('*.csv'))

if len(csv_files) == 0:
    print("❌ No CSV files found in data/raw/")
    exit(1)

print(f"Found {len(csv_files)} CSV file(s):\n")

for filepath in sorted(csv_files):
    print(f"📄 {filepath.name}")
    print("   " + "-"*56)
    
    try:
        # Load just first 1000 rows to check
        df = pd.read_csv(filepath, nrows=1000)
        
        # Check for label column
        label_col = None
        for col in df.columns:
            if 'label' in col.lower():
                label_col = col
                break
        
        if label_col:
            print(f"   Size: {filepath.stat().st_size / (1024**2):.1f} MB")
            
            # Load full label column only
            df_full = pd.read_csv(filepath, usecols=[label_col])
            total_rows = len(df_full)
            
            print(f"   Rows: {total_rows:,}")
            print(f"   Label column: '{label_col}'")
            print(f"   Labels:")
            
            label_counts = df_full[label_col].value_counts()
            for label, count in label_counts.items():
                pct = count / total_rows * 100
                print(f"      {label}: {count:,} ({pct:.1f}%)")
        else:
            print("   ⚠️  No label column found")
        
        print()
        
    except Exception as e:
        print(f"   ❌ Error loading: {e}")
        print()

print("="*60)
print("\n💡 Recommendation:")
print("Use files that contain both BENIGN and attack labels")
print("Good choices:")
print("  - Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
print("  - Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv")
print("  - Any file with multiple label types")