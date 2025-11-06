from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Pomodoro timer configuration (in seconds)
WORK_DURATION = 25 * 60  # 25 minutes
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes
LONG_BREAK_DURATION = 15 * 60  # 15 minutes

@app.route('/')
def index():
    """Render the main Pomodoro timer page"""
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get timer configuration"""
    return jsonify({
        'workDuration': WORK_DURATION,
        'shortBreakDuration': SHORT_BREAK_DURATION,
        'longBreakDuration': LONG_BREAK_DURATION
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
