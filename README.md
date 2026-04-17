```markdown
# 🤖 JARVIS - AI Personal Assistant

A powerful, modular AI personal assistant with voice activation, futuristic HUD interface, and intelligent automation capabilities. Inspired by Iron Man's JARVIS, built with Python.

---

## ✨ Features

### 🎯 Core Capabilities

- **Voice Activation**: Hands-free operation with speech recognition
- **Text Mode**: Silent CLI operation for quiet environments
- **Futuristic HUD**: Sci-Fi inspired PyQt6 graphical interface
- **Modular Skills**: Plugin-based architecture for easy extension
- **Wake Word Detection**: Responds to "Jarvis" or direct commands
- **Cross-Platform**: Works on macOS (primary) and Windows

### 🛠️ Built-in Skills

| Skill | Description | Commands |
|-------|-------------|----------|
| **System** | Volume, apps, power controls | "Set volume to 50", "Open Safari", "Shutdown" |
| **Weather** | Current weather & 5-day forecast | "What's the weather in Tokyo?" |
| **Web** | Google search, YouTube, news | "Search for Python tutorials", "Open YouTube" |
| **Email** | Check unread, read recent emails | "Check my emails", "Get recent messages" |
| **Files** | Create, read, write, delete files | "Create a file named notes.txt" |
| **Memory** | Persistent storage of information | "Remember my password is 1234" |
| **DateTime** | Time, date, timers | "What time is it?", "Set a timer for 5 minutes" |
| **Text** | File summarization with AI | "Summarize the document on my desktop" |
| **Screenshots** | Full screen and region capture | "Take a screenshot" |
| **Camera** | Photo capture and live view | "Take a photo", "Start camera" |
| **Vision** | AI image analysis | "Analyze this image" |
| **Detection** | YOLOv8 object detection | "Detect objects from camera" |
| **Gemini** | Google Gemini AI integration | "Ask Gemini about space" |
| **WhatsApp** | Send messages via web | "Send WhatsApp to +1234567890" |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- macOS (primary) or Windows
- Microphone (for voice mode)
- Internet connection

### Installation

```bash
# Clone the repository
git clone https://github.com/devikiran-04/Jarvis-The-AI-Assistant.git
cd Jarvis-The-AI-Assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running JARVIS

```bash
# Start with GUI
python jarvis.py

# Start in voice mode
python jarvis.py --voice

# Start in text mode (CLI)
python jarvis.py --text
```

---

## 🎮 Usage

### Voice Commands

Simply say "Jarvis" followed by your command:

- *"Jarvis, what's the weather in New York?"*
- *"Jarvis, open Safari"*
- *"Jarvis, set a timer for 10 minutes"*
- *"Jarvis, take a screenshot"*
- *"Jarvis, remember my meeting is at 3 PM"*

### Text Commands (CLI Mode)

Type commands directly when running in text mode:

```
> weather in London
> open chrome
> create file notes.txt
> check emails
```

### GUI Interface

The futuristic HUD provides:
- **Visual Feedback**: Animated response indicators
- **Command History**: Scrollable log of interactions
- **Status Panel**: System status and active processes
- **Quick Actions**: Clickable buttons for common tasks

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    JARVIS Core                           │
│              (Command Parser & Router)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    ▼                 ▼                 ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Voice  │    │   GUI   │    │   CLI   │
│ Module  │    │ (PyQt6) │    │  Mode   │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    ▼
           ┌─────────────┐
           │ Skill Router │
           └──────┬──────┘
                  │
    ┌─────────────┼─────────────┬─────────────┐
    ▼             ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ System │  │  Web   │  │ Vision │  │  AI    │
│ Skills │  │ Skills │  │ Skills │  │ Skills │
└────────┘  └────────┘  └────────┘  └────────┘
```

---

## 📁 Project Structure

```
Jarvis-The-AI-Assistant/
│
├── jarvis.py              # Main entry point
├── requirements.txt       # Python dependencies
├── config.yaml           # Configuration file
├── README.md             # This file
│
├── core/                 # Core modules
│   ├── __init__.py
│   ├── assistant.py      # Main assistant class
│   ├── command_parser.py # Natural language parser
│   ├── speech.py         # Text-to-speech & recognition
│   └── memory.py         # Persistent storage
│
├── gui/                  # PyQt6 interface
│   ├── __init__.py
│   ├── main_window.py    # HUD interface
│   ├── widgets.py        # Custom UI components
│   └── styles.py         # QSS themes
│
├── skills/               # Skill modules
│   ├── __init__.py
│   ├── system.py         # System control
│   ├── weather.py        # Weather API
│   ├── web.py            # Web search & browsing
│   ├── email_client.py   # Email integration
│   ├── files.py          # File operations
│   ├── vision.py         # Camera & image analysis
│   ├── ai_gemini.py      # Google Gemini integration
│   └── whatsapp.py       # WhatsApp automation
│
├── utils/                # Utilities
│   ├── __init__.py
│   ├── helpers.py
│   └── constants.py
│
└── assets/               # Resources
    ├── sounds/           # Audio files
    ├── images/           # Icons & backgrounds
    └── models/           # ML models (YOLOv8, etc.)
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize JARVIS:

```yaml
assistant:
  name: "Jarvis"
  voice: "en-US"  # or "en-GB", "en-AU"
  wake_word: "Jarvis"
  response_speed: "normal"  # "slow", "normal", "fast"

api_keys:
  openweather: "your_openweather_api_key"
  gemini: "your_google_gemini_api_key"
  email:
    smtp_server: "smtp.gmail.com"
    username: "your_email@gmail.com"
    password: "your_app_password"

preferences:
  default_browser: "Safari"  # or "Chrome", "Firefox"
  screenshot_path: "~/Desktop/Screenshots"
  camera_save_path: "~/Desktop/Photos"
```

---

## 🔧 Skills Development

Create custom skills easily:

```python
from skills.base import Skill

class MySkill(Skill):
    def __init__(self):
        super().__init__("MySkill")
    
    def can_handle(self, command: str) -> bool:
        return "my command" in command.lower()
    
    def handle(self, command: str):
        # Your skill logic here
        return "Skill executed successfully!"
```

Register in `skills/__init__.py`:

```python
from .my_skill import MySkill

SKILL_REGISTRY = [
    # ... existing skills
    MySkill(),
]
```

---

## 🛡️ Privacy & Security

- **Local Processing**: Voice recognition happens locally
- **No Data Collection**: Your commands stay on your device
- **Encrypted Memory**: Sensitive data is encrypted at rest
- **API Key Security**: Keys stored in local config only

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Microphone not detected | Check system permissions in Settings > Privacy > Microphone |
| Speech not recognized | Speak clearly, reduce background noise |
| GUI not loading | Ensure PyQt6 is installed: `pip install PyQt6` |
| Camera access denied | Grant camera permission in System Preferences |
| Slow response | Check internet connection, reduce active skills |

---

## 🗺️ Roadmap

- [ ] Home automation integration (Smart home control)
- [ ] Calendar management (Google Calendar, Outlook)
- [ ] Music control (Spotify, Apple Music)
- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Mobile companion app
- [ ] Cloud sync for memory

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingSkill`)
3. Commit your changes (`git commit -m 'Add amazing skill'`)
4. Push to the branch (`git push origin feature/AmazingSkill`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by Iron Man's JARVIS from Marvel
- Speech recognition powered by [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- Text-to-speech by [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- GUI built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- AI capabilities via [Google Gemini](https://ai.google.dev/)

---

**Built with ❤️ by [Devi Kiran](https://github.com/devikiran-04)**

> *"I am JARVIS, your personal AI assistant. How may I help you today?"*

⭐ Star this repository if you find it helpful!
```
