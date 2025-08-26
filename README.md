<div align="center">

  <img src="https://path-to-your-logo-or-banner.png" alt="Podcast AI Banner" width="800"/>

  <h1>🎙️ Podcast AI</h1>

  <p>
    <strong>Generate professional, studio-quality podcasts from text scripts using high-performance AI voice models.</strong>
  </p>

  <p>
    <a href="https://github.com/santhoshsharuk/podcast-ai/blob/main/LICENSE">
      <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg">
    </a>
    <a href="https://www.python.org/">
      <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8+-blue.svg">
    </a>
    <a href="https://github.com/santhoshsharuk/podcast-ai/releases">
      <img alt="GitHub release" src="https://img.shields.io/github/v/release/santhoshsharuk/podcast-ai">
    </a>
    <a href="https://github.com/santhoshsharuk/podcast-ai/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/santhoshsharuk/podcast-ai">
    </a>
    <a href="https://github.com/santhoshsharuk/podcast-ai/stargazers">
      <img alt="Stars" src="https://img.shields.io/github/stars/santhoshsharuk/podcast-ai">
    </a>
  </p>
</div>

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
- [🎧 Example Output](#-example-output)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#-prerequisites)
  - [Installation & Setup](#-installation--setup)
- [▶️ Usage](#️-usage)
  - [Basic Usage](#-basic-usage)
  - [Advanced Usage](#-advanced-usage)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [📧 Contact](#-contact)

---

## 🤖 About The Project

**Podcast AI** is an open-source tool designed to automate audio content creation. It leverages the power of **Piper TTS**, a fast and high-quality neural text-to-speech system, with efficient **ONNX** models to transform plain text scripts into engaging, ready-to-publish podcasts.

Whether you're a content creator looking to streamline your workflow or a developer interested in AI-powered audio generation, this project provides a solid foundation.

---

## ✨ Key Features

- ✅ **High-Fidelity Speech Synthesis**: Generates natural-sounding speech from text using state-of-the-art models.
- ✅ **Fast & Efficient**: Built on Piper TTS and ONNX Runtime for rapid, local inference without relying on cloud APIs.
- ✅ **Customizable Voices**: Easily switch between different voice models by providing the corresponding `.onnx` and `.json` files.
- ✅ **Audio Assembly**: Seamlessly combines generated speech segments, intro/outro music, and sound effects.
- ✅ **Cross-Platform**: Runs on any system with Python, including Windows, macOS, and Linux.
- ✅ **Fully Open-Source**: Free to use, modify, and distribute under the MIT License.

---

## 🎧 Example Output

Listen to a sample podcast generated with this tool:

➡️ **[Listen to `final_podcast.mp3`](./final_podcast.mp3)**

The audio was generated from a simple script like this:

```txt
(intro_music)
Welcome to AI Spotlight, the show where we explore the latest breakthroughs in artificial intelligence.
(transition_sound)
Today, we're discussing generative models. These models can create brand new content, from text and images to music and even code. It's a revolution in creativity.
(outro_music)
```

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` and `venv` (usually included with Python)
- `git` for cloning the repository

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/santhoshsharuk/podcast-ai.git
    cd podcast-ai
    ```

2.  **Download Core Dependencies & Voice Models**
    Large files like the Piper engine and voice models are hosted on GitHub Releases to keep the repository lightweight.

    - Go to the [**Releases Page**](../../releases).
    - Download the latest `piper.zip` and the desired voice model (e.g., `voice-en-us-amy-medium.zip`).
    - Extract them into the project directory.

3.  **Organize Your Files**
    Create a `voices` directory and place your model files inside. Your project structure should look like this:

    ```tree
    .
    ├── assemble_podcast.py
    ├── script.txt
    ├── voices/
    │   └── en_US-amy-medium/
    │       ├── en_US-amy-medium.onnx
    │       └── en_US-amy-medium.onnx.json
    ├── piper/
    │   ├── piper
    │   └── ... (other piper files)
    ```

4.  **Create a Virtual Environment & Install Requirements**
    It's best practice to use a virtual environment to manage dependencies.

    ```bash
    # Create and activate the virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

    # Install the required Python packages
    pip install -r requirements.txt
    ```

You are now ready to generate your first podcast!

---

## ▶️ Usage

The main script `assemble_podcast.py` reads your `script.txt`, generates audio for each line, and combines them into a final file.

### Basic Usage

Simply run the script with Python:

```bash
python assemble_podcast.py
```

This will:
- Read `script.txt`.
- Use the default voice model found in the `voices/` directory.
- Output the final audio to `final_podcast.mp3`.
- Play a success sound upon completion.

### Advanced Usage

You can customize the behavior using command-line arguments for greater flexibility.

```bash
python assemble_podcast.py \
  --script my_new_episode.txt \
  --voice voices/en_GB-alan-medium \
  --output episode_01.wav \
  --no-sound
```

**Available Arguments:**

| Argument        | Shorthand | Description                                           | Default                        |
| --------------- | --------- | ----------------------------------------------------- | ------------------------------ |
| `--script`      | `-s`      | Path to the input script file.                        | `script.txt`                   |
| `--voice`       | `-v`      | Path to the voice model directory.                    | First directory in `voices/`   |
| `--output`      | `-o`      | Path for the final output audio file.                 | `final_podcast.mp3`            |
| `--no-sound`    |           | Disable the success sound upon completion.            | N/A (flag)                     |

---

## 📂 Project Structure

```tree
.
├── .gitignore              # Files to ignore for Git
├── assemble_podcast.py     # Main script to generate the podcast
├── LICENSE                 # Project license file
├── README.md               # You are here!
├── requirements.txt        # Python package dependencies
├── script.txt              # Default input text script
├── final_podcast.mp3       # Example output file
├── assets/                 # (Optional) For sounds like intros, outros
│   └── success.wav
├── piper/                  # Piper TTS engine (from releases)
└── voices/                 # Directory for voice models
    └── en_US-amy-medium/
        ├── en_US-amy-medium.onnx
        └── en_US-amy-medium.onnx.json
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  **Fork** the Project (🍴)
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a **Pull Request** (🚀)

Please open an issue first to discuss any major changes you would like to make.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

---

## 📧 Contact

**Santhosh Sharuk**

[![Gmail](https://img.shields.io/badge/Gmail-santhoshsharuk16@gmail.com-red?style=for-the-badge&logo=gmail)](mailto:santhoshsharuk16@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-santhoshsharuk-black?style=for-the-badge&logo=github)](https://github.com/santhoshsharuk)

<div align="center">

---
*Generated by Podcast AI - Where words find their voice.*

</div>
