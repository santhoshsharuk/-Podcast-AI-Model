import os
import subprocess
import random
import time
import difflib
import json
import math
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pydub import AudioSegment
import google.generativeai as genai
from dotenv import load_dotenv

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
# IMPORTANT: Change this secret key for any real-world deployment
app.secret_key = 'a_very_secret_key_for_session_management_change_me'

# --- CORE CONFIGURATION ---
MODEL_FOLDER = "model"
OUTPUT_FOLDER = os.path.join("static", "output")
HISTORY_FILE = "history.json" # File to store podcast metadata

# Ensure required directories exist on startup
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)


# --- HISTORY HELPER FUNCTIONS ---

def load_history():
    """Loads the podcast history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return [] # Return empty list if file is corrupted, empty, or not found

def save_history_entry(new_entry):
    """Saves a new podcast entry to the history file."""
    history = load_history()
    history.insert(0, new_entry) # Insert new entry at the beginning
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


# --- GENERAL HELPER FUNCTIONS ---

def get_available_voices():
    """Scans the model folder and returns a list of .onnx voice files."""
    if not os.path.isdir(MODEL_FOLDER): return []
    return sorted([f for f in os.listdir(MODEL_FOLDER) if f.endswith('.onnx')])

def get_speakers_from_script(script_text):
    """Parses the script to find unique speaker names."""
    speakers = set()
    for line in script_text.strip().split('\n'):
        if ":" in line:
            speaker = line.split(":", 1)[0].strip()
            if speaker: speakers.add(speaker)
    return sorted(list(speakers))


# --- CORE LOGIC: SCRIPT & AUDIO GENERATION ---

def generate_podcast_script(topic, duration_minutes):
    """Generates a podcast script using the Gemini API."""
    print("Connecting to Gemini API...")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        target_word_count = int(float(duration_minutes) * 150)
    except (ValueError, TypeError):
        target_word_count = 150 # Default to 1 minute

    prompt = f"""
    You are a helpful assistant that writes engaging podcast scripts.
    Your task is to generate a podcast script on the topic: "{topic}".
    The script's total length should be approximately {target_word_count} words.
    The script must be a conversation between two distinct speakers, 'Host' and 'Expert'.

    RULES:
    1. Format each line exactly as "SPEAKER: Dialogue". For example, "Host: Welcome to the show."
    2. Do not include any other text, explanations, or markdown formatting like ```.
    3. The conversation must be natural, informative, and flow well.
    4. The script must start with 'Host'.
    """
    try:
        response = model.generate_content(prompt, request_options={"timeout": 120})
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None

def assemble_podcast_audio(script_text, voice_mapping, output_filename):
    """Converts a script text into a final MP3 file using the selected voices."""
    print(f"Starting audio assembly for {output_filename} with voices: {voice_mapping}")
    final_podcast = AudioSegment.silent(duration=1000)
    temp_file_path = os.path.join(OUTPUT_FOLDER, "_temp_line.wav")
    
    try:
        script_lines = script_text.strip().split('\n')
        for line_num, line in enumerate(script_lines):
            line = line.strip()
            if not line or ":" not in line: continue

            speaker, text = line.split(":", 1)
            speaker = speaker.strip()
            text_to_speak = text.strip().replace('"', '\\"')

            if speaker in voice_mapping:
                print(f"  - Line {line_num+1}: Generating audio for {speaker}...")
                voice_model_filename = voice_mapping[speaker]
                full_voice_path = os.path.join(MODEL_FOLDER, voice_model_filename)
                
                command = f'echo "{text_to_speak}" | piper.exe --model "{full_voice_path}" --output_file "{temp_file_path}"'
                subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                
                line_audio = AudioSegment.from_wav(temp_file_path)
                final_podcast += line_audio + AudioSegment.silent(duration=random.randint(600, 1200))
        
        final_output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        final_podcast.export(final_output_path, format="mp3", bitrate="192k")
        return True
    except Exception as e:
        print(f"An error occurred during audio assembly: {e}")
        return False
    finally:
        if os.path.exists(temp_file_path): os.remove(temp_file_path)

# --- FLASK ROUTES ---

@app.route('/')
def dashboard():
    """Page 1: The new dashboard homepage."""
    history = load_history()
    
    total_podcasts = len(history)
    total_duration_minutes = sum(float(entry.get('duration', 0)) for entry in history if str(entry.get('duration', 0)).replace('.', '', 1).isdigit())
    
    if total_duration_minutes > 0:
        hours, minutes = divmod(total_duration_minutes, 60)
        formatted_duration = f"{int(hours)}h {round(minutes)}m" if hours > 0 else f"{round(minutes)}m"
    else: formatted_duration = "0m"

    last_creation_date = "Never"
    if history:
        last_creation_date = datetime.fromisoformat(history[0]['creation_date']).strftime('%b %d, %Y')

    return render_template('dashboard.html',
                           total_podcasts=total_podcasts,
                           formatted_duration=formatted_duration,
                           last_creation_date=last_creation_date,
                           recent_podcasts=history[:3])

@app.route('/create')
def create_new_route():
    """Page 2: The form to create a new podcast."""
    return render_template('create.html')

@app.route('/history')
def history_page():
    """Displays the full history of generated podcasts."""
    return render_template('history.html', history=load_history())

@app.route('/edit_script', methods=['POST'])
def edit_script_route():
    """Step 1 of creation: Generate and show the script for editing."""
    session.clear()
    session['topic'] = request.form['topic']
    session['duration'] = request.form['duration']
    
    script = generate_podcast_script(session['topic'], session['duration'])
    if not script:
        flash("Error: Could not generate a script from the AI. Please try again later.")
        return redirect(url_for('create_new_route'))
    
    session['original_script'] = script
    return render_template('edit_script.html', original_script=script, topic=session['topic'])

@app.route('/review_script', methods=['POST'])
def review_script_route():
    """Step 2 of creation: Show a diff of the original vs. edited script."""
    original_script = request.form['original_script']
    edited_script = request.form['edited_script']
    
    d = difflib.HtmlDiff(wrapcolumn=80)
    diff_table = d.make_table(original_script.splitlines(), edited_script.splitlines(), fromdesc='Original AI Script', todesc='Your Edited Version')
    
    session['edited_script'] = edited_script
    return render_template('review_script.html', diff_table=diff_table, edited_script=edited_script)

@app.route('/select_voices', methods=['POST'])
def select_voices_route():
    """Step 3 of creation: Let the user assign voices to speakers."""
    final_script = request.form['final_script']
    session['final_script'] = final_script
    
    speakers = get_speakers_from_script(final_script)
    available_voices = get_available_voices()
    
    if not available_voices:
        flash("CRITICAL ERROR: No voice models (.onnx files) found in the 'model' folder.")
        return redirect(url_for('create_new_route'))
    if not speakers:
        flash("Warning: No speakers (e.g., 'Host:') were detected in your script. Please edit the script to include speakers.")
        return render_template('edit_script.html', original_script=final_script, topic=session.get('topic'))

    return render_template('select_voices.html', speakers=speakers, available_voices=available_voices, final_script=final_script)

@app.route('/process_audio', methods=['POST'])
def process_audio_route():
    """Step 4 of creation: Assemble the audio and save to history."""
    final_script = request.form['final_script']
    
    user_voice_mapping = {sp: request.form.get(f'voice_for_{sp}') for sp in get_speakers_from_script(final_script)}
            
    timestamp = int(time.time())
    output_filename = f"podcast_{timestamp}.mp3"
    
    success = assemble_podcast_audio(final_script, user_voice_mapping, output_filename)
    
    if not success:
        flash("A critical error occurred during audio generation. Please check the console logs for details.")
        return redirect(url_for('create_new_route'))
        
    new_history_entry = {
        "filename": output_filename,
        "topic": session.get('topic', 'N/A'),
        "duration": session.get('duration', 'N/A'),
        "creation_date": datetime.now().isoformat(),
        "script": final_script
    }
    save_history_entry(new_history_entry)
    
    session['display_script'] = final_script
    return redirect(url_for('success', filename=output_filename, topic=session.get('topic', 'your podcast')))

@app.route('/success')
def success():
    """Final page: The result page with audio player and script."""
    filename = request.args.get('filename')
    topic = request.args.get('topic')
    script = session.get('display_script', 'Script not available.')
    
    if not filename: return redirect(url_for('dashboard'))

    return render_template('success.html', filename=filename, topic=topic, script=script)


if __name__ == '__main__':
    app.run(debug=True)