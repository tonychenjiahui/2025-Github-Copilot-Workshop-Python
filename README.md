# 2025 Github Copilot Workshop - Python

This repository contains a Pomodoro Timer web application built with Flask, HTML, CSS, and JavaScript.

## 🍅 Pomodoro Timer Web App

A clean and modern Pomodoro timer to help you stay focused and productive using the Pomodoro Technique.

### Features

- **Three Timer Modes**: Work (25 min), Short Break (5 min), Long Break (15 min)
- **Visual Timer Display**: Large, easy-to-read countdown timer
- **Session Tracking**: Keep track of completed work sessions
- **Browser Notifications**: Get notified when a session completes
- **Sound Alerts**: Audio notification at the end of each session
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-Mode Switching**: Automatically switches between work and break modes

### Architecture

#### Backend (Flask)
- **app.py**: Main Flask application with routes and API endpoints
  - `/`: Serves the main HTML page
  - `/api/config`: Returns timer configuration (work/break durations)

#### Frontend
- **templates/index.html**: Main HTML template with timer UI
- **static/css/style.css**: Responsive CSS styling with gradient background
- **static/js/timer.js**: JavaScript timer logic and UI interactions

### Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: CSS3 with modern features (flexbox, gradients, transitions)
- **State Management**: Client-side JavaScript class-based state

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/tonychenjiahui/2025-Github-Copilot-Workshop-Python.git
   cd 2025-Github-Copilot-Workshop-Python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Production mode (default)
   python app.py
   
   # Development mode with debug enabled
   FLASK_ENV=development python app.py
   ```

4. **Open in browser**
   Navigate to `http://localhost:5000`

### Usage

1. **Select a mode**: Choose between Work, Short Break, or Long Break
2. **Start the timer**: Click the "Start" button to begin the countdown
3. **Pause if needed**: Click "Pause" to temporarily stop the timer
4. **Reset**: Click "Reset" to restart the current mode's timer
5. **Stay focused**: Work until the timer completes, then take your break!

### Customization

You can customize timer durations by editing the configuration in `app.py`:

```python
WORK_DURATION = 25 * 60  # 25 minutes (in seconds)
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes
LONG_BREAK_DURATION = 15 * 60  # 15 minutes
```

### Project Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── timer.js      # Timer logic
├── point.py              # Point2D class example
├── deliverManager.py     # Delivery manager example
└── README.md             # This file
```

### Workshop Reference

ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0
