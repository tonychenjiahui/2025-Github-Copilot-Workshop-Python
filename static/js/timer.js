// Pomodoro Timer Logic
class PomodoroTimer {
    constructor() {
        this.config = {
            workDuration: 25 * 60,
            shortBreakDuration: 5 * 60,
            longBreakDuration: 15 * 60
        };
        
        this.state = {
            currentMode: 'work',
            timeRemaining: this.config.workDuration,
            isRunning: false,
            sessionCount: 1,
            timerInterval: null
        };
        
        this.elements = {
            timeDisplay: document.getElementById('timeDisplay'),
            startBtn: document.getElementById('startBtn'),
            pauseBtn: document.getElementById('pauseBtn'),
            resetBtn: document.getElementById('resetBtn'),
            sessionCount: document.getElementById('sessionCount'),
            currentMode: document.getElementById('currentMode'),
            modeBtns: document.querySelectorAll('.mode-btn')
        };
        
        this.init();
    }
    
    init() {
        // Load configuration from server
        this.loadConfig();
        
        // Set up event listeners
        this.elements.startBtn.addEventListener('click', () => this.start());
        this.elements.pauseBtn.addEventListener('click', () => this.pause());
        this.elements.resetBtn.addEventListener('click', () => this.reset());
        
        this.elements.modeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                this.changeMode(mode);
            });
        });
        
        // Update display
        this.updateDisplay();
    }
    
    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            if (response.ok) {
                this.config = await response.json();
                this.state.timeRemaining = this.config.workDuration;
                this.updateDisplay();
            }
        } catch (error) {
            console.error('Failed to load config:', error);
        }
    }
    
    start() {
        if (!this.state.isRunning) {
            this.state.isRunning = true;
            this.elements.startBtn.classList.add('hidden');
            this.elements.pauseBtn.classList.remove('hidden');
            
            this.state.timerInterval = setInterval(() => {
                this.tick();
            }, 1000);
        }
    }
    
    pause() {
        if (this.state.isRunning) {
            this.state.isRunning = false;
            this.elements.startBtn.classList.remove('hidden');
            this.elements.pauseBtn.classList.add('hidden');
            
            if (this.state.timerInterval) {
                clearInterval(this.state.timerInterval);
                this.state.timerInterval = null;
            }
        }
    }
    
    reset() {
        this.pause();
        
        // Reset time based on current mode
        switch (this.state.currentMode) {
            case 'work':
                this.state.timeRemaining = this.config.workDuration;
                break;
            case 'shortBreak':
                this.state.timeRemaining = this.config.shortBreakDuration;
                break;
            case 'longBreak':
                this.state.timeRemaining = this.config.longBreakDuration;
                break;
        }
        
        this.updateDisplay();
    }
    
    tick() {
        if (this.state.timeRemaining > 0) {
            this.state.timeRemaining--;
            this.updateDisplay();
        } else {
            // Timer completed
            this.pause();
            this.playNotificationSound();
            this.handleSessionComplete();
        }
    }
    
    handleSessionComplete() {
        // Store current mode before switching
        const completedMode = this.state.currentMode;
        
        // Auto-switch mode after completion
        if (this.state.currentMode === 'work') {
            if (this.state.sessionCount % 4 === 0) {
                this.changeMode('longBreak');
            } else {
                this.changeMode('shortBreak');
            }
            this.state.sessionCount++;
        } else {
            this.changeMode('work');
        }
        
        this.updateSessionCount();
        
        // Show notification with correct mode
        this.showNotification(completedMode);
    }
    
    changeMode(mode) {
        this.pause();
        this.state.currentMode = mode;
        
        // Update active button
        this.elements.modeBtns.forEach(btn => {
            if (btn.dataset.mode === mode) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Set time based on mode
        switch (mode) {
            case 'work':
                this.state.timeRemaining = this.config.workDuration;
                this.elements.currentMode.textContent = 'Work';
                break;
            case 'shortBreak':
                this.state.timeRemaining = this.config.shortBreakDuration;
                this.elements.currentMode.textContent = 'Short Break';
                break;
            case 'longBreak':
                this.state.timeRemaining = this.config.longBreakDuration;
                this.elements.currentMode.textContent = 'Long Break';
                break;
        }
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.state.timeRemaining / 60);
        const seconds = this.state.timeRemaining % 60;
        
        this.elements.timeDisplay.textContent = 
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
    
    updateSessionCount() {
        this.elements.sessionCount.textContent = this.state.sessionCount;
    }
    
    playNotificationSound() {
        // Create a simple beep sound using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.log('Could not play sound:', error);
        }
    }
    
    showNotification(completedMode) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const modeText = completedMode === 'work' ? 'Work session' : 'Break';
            new Notification('Pomodoro Timer', {
                body: `${modeText} completed!`
            });
        }
    }
}

// Request notification permission on load
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
