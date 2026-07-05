import os
import shutil

artifacts = {
    "gradient": r"C:\Users\HP\.gemini\antigravity\brain\0043f60d-2ec1-4ef2-89e2-e44923ec85c2\gradient_1780007396442.png",
    "sunset":   r"C:\Users\HP\.gemini\antigravity\brain\0043f60d-2ec1-4ef2-89e2-e44923ec85c2\sunset_1780007415000.png",
    "forest":   r"C:\Users\HP\.gemini\antigravity\brain\0043f60d-2ec1-4ef2-89e2-e44923ec85c2\forest_1780007541971.png",
}

images_dir = os.path.join(os.path.dirname(__file__), "assets", "images")
os.makedirs(images_dir, exist_ok=True)

for name, src in artifacts.items():
    dest = os.path.join(images_dir, f"{name}.jpg")
    if os.path.exists(src):
        shutil.copy(src, dest)
        print(f"[OK] Copied {name} -> {dest}")
    else:
        print(f"[MISSING] Source not found: {src}")

# Remove obsolete procedural generator if present
generator = os.path.join(os.path.dirname(__file__), "core", "image_generator.py")
if os.path.exists(generator):
    os.remove(generator)
    print("[OK] Removed obsolete core/image_generator.py")

print("\nSetup complete — run: python main.py")
