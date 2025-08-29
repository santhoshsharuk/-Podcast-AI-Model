# Model Files

⚠️ **Important:** The model files (`.onnx`, `.json`) are **not stored in this repository** because they are large in size.  

## How to use
1. Go to the [Releases section](../../releases) of this repository.  
2. Download the required `.onnx` model and its corresponding `.json` file.  
3. Place them inside this `model/` folder.  

📂 model/
┣ 📄 your_model.onnx
┣ 📄 your_model.json
┗ 📄 README.md


## Notes
- Do **not** commit `.onnx` or `.json` files directly into git.  
- The `.gitignore` ensures large model files are ignored.  
- If you update models, upload them as **Release assets** on GitHub.  
