"""
Script to move existing models to models/ directory and 
prepare the directory structure
"""
from pathlib import Path
import shutil

# Create models directory
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# Model files to move
model_files = [
    "autoencoder.keras",
    "encoder.keras",
    "autoencoder_scaler.pkl",
    "ae_threshold.npy"
]

moved = []
missing = []

for file_name in model_files:
    source = Path(file_name)
    dest = models_dir / file_name
    
    if source.exists() and source != dest:
        shutil.move(str(source), str(dest))
        moved.append(file_name)
        print(f"✓ Moved {file_name} to models/")
    elif dest.exists():
        print(f"✓ {file_name} already in models/")
    else:
        missing.append(file_name)
        print(f"✗ {file_name} not found")

print("\n" + "=" * 60)
print("SETUP COMPLETE")
print("=" * 60)

if moved:
    print(f"\nMoved {len(moved)} files to models/")

if missing:
    print(f"\n⚠️  Missing {len(missing)} model files:")
    for f in missing:
        print(f"   - {f}")
    print("\nRun training scripts to generate missing models:")
    print("   python 3_train.py")
else:
    print("\n✓ All model files are ready!")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Test the API:")
print("   python api/main.py")
print()
print("2. Run monitoring dashboard:")
print("   streamlit run monitoring/dashboard.py")
print()
print("3. Or use Docker:")
print("   docker-compose up")
print("=" * 60)
