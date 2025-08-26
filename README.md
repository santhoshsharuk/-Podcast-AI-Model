
```markdown
# 🎙️ Podcast AI Model

An open-source **AI Podcast Generator** powered by [Piper TTS](https://github.com/rhasspy/piper) and **ONNX Runtime**.  
This project allows anyone to convert text into natural-sounding podcasts using multiple pre-trained voice models.  

✅ Open Source (MIT License)  
✅ Multiple English voices (US & UK)  
✅ Simple Python script to assemble podcasts  
✅ Cross-platform (Windows, Linux, macOS with ONNX support)  

---

## 🚀 Features
- 🎤 **Text-to-Speech** – Convert `script.txt` into podcast-ready audio.  
- 🌍 **Multiple Voices** – Includes US & UK voices (`Joe`, `Lessac`, `Southern English Female`).  
- 📝 **Simple Workflow** – Edit `script.txt` → Run Python script → Get `final_podcast.mp3`.  
- 🎧 **Clean Audio** – Optimized with ONNX Runtime for performance.  
- 🔊 **Notification Sound** – Plays `success.wav` when podcast generation is done.  

---

## 📂 Project Structure
```

podcast-ai-model/
│── assemble\_podcast.py           # Main Python script
│── script.txt                    # Input text file
│── final\_podcast.mp3             # Example generated podcast
│── success.wav                   # Notification sound
│── models/                       # Voice models
│   ├── en\_GB-southern\_english\_female-low\.onnx
│   ├── en\_GB-southern\_english\_female-low\.onnx.json
│   ├── en\_US-joe-medium.onnx
│   ├── en\_US-joe-medium.onnx.json
│   ├── en\_US-lessac-medium.onnx
│   ├── en\_US-lessac-medium.onnx.json
│── bin/                          # Executables and dependencies
│   ├── piper.exe
│   ├── espeak-ng.dll
│   ├── piper\_phonemize.dll
│   ├── onnxruntime.dll
│   ├── onnxruntime\_providers\_shared.dll
│   ├── libtashkeel\_model.ort
│── LICENSE                       # MIT License (Santhosh Sharuk)
│── README.md                     # Documentation
│── requirements.txt              # Python dependencies

````

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/santhoshsharuk/podcast-ai-model.git
cd podcast-ai-model
````

Install Python dependencies:

```bash
pip install -r requirements.txt
```

*(ONNX Runtime and Piper executables are already included in `/bin`.)*

---

## 🛠️ Usage

1. Edit the text you want to convert inside `script.txt`.
2. Run the podcast assembly script:

```bash
python assemble_podcast.py
```

3. The generated podcast will be saved as `final_podcast.mp3`.
4. Once complete, you’ll hear the `success.wav` notification sound.

---

## 🎤 Available Voices

| Model File                               | Voice               |
| ---------------------------------------- | ------------------- |
| `en_US-joe-medium.onnx`                  | US English – Joe    |
| `en_US-lessac-medium.onnx`               | US English – Lessac |
| `en_GB-southern_english_female-low.onnx` | UK English – Female |

You can switch voices by editing `assemble_podcast.py` and selecting the desired model.

---

## 📂 Example

**Input (`script.txt`):**

```
Welcome to our very first AI-generated podcast.
This podcast was created using open-source tools.
Stay tuned for more episodes powered by AI!
```

**Output (`final_podcast.mp3`):**
🎧 Natural-sounding podcast audio file.

---

## 🤝 Contributing

Pull requests are welcome!
If you’d like to add new voices, improve audio processing, or add new features, please open an issue or submit a PR.

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

**© 2025 Santhosh Sharuk**

---

## 📊 Badges

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

---

```

---

🔥 This README will make your repo look **professional like Piper** and clear for anyone who wants to use it.  

Do you also want me to **write the first version of `assemble_podcast.py`** that:  
- Reads `script.txt`  
- Uses Piper model (`.onnx`)  
- Outputs `final_podcast.mp3`  
So you can push it along with this README?
```
