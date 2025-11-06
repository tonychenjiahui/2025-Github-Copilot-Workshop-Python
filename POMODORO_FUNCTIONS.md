# Necessary Functions for Pomodoro Timer Application

This document lists all the necessary functions that have been implemented for creating a Pomodoro timer application.

## Overview

The Pomodoro timer application follows the Pomodoro Technique for time management, which uses a timer to break work into intervals (traditionally 25 minutes), separated by short breaks (5 minutes), with longer breaks (15-30 minutes) after every 4 work intervals.

---

## 1. Timer Core Functions

These are the fundamental functions for controlling the timer:

### `start_timer(duration: int) -> bool`
**Purpose:** Start the timer countdown  
**Parameters:** 
- `duration`: Duration in seconds
**Returns:** True if timer started successfully  
**Usage:** Core function to begin timing any session

### `pause_timer() -> bool`
**Purpose:** Pause the running timer  
**Returns:** True if timer was paused successfully  
**Usage:** Allows users to temporarily pause the timer without losing progress

### `resume_timer() -> bool`
**Purpose:** Resume a paused timer  
**Returns:** True if timer was resumed successfully  
**Usage:** Continue timing after a pause

### `stop_timer() -> bool`
**Purpose:** Stop and reset the timer  
**Returns:** True if timer was stopped successfully  
**Usage:** Completely stop the current timer session

### `get_remaining_time() -> int`
**Purpose:** Get the remaining time in seconds  
**Returns:** Remaining time in seconds  
**Usage:** Display countdown or check how much time is left

### `is_timer_running() -> bool`
**Purpose:** Check if timer is currently running  
**Returns:** True if timer is running  
**Usage:** Determine current timer status for UI updates

---

## 2. Pomodoro Cycle Management Functions

These functions manage the Pomodoro work/break cycles:

### `start_work_session() -> bool`
**Purpose:** Start a work/focus session (typically 25 minutes)  
**Returns:** True if work session started successfully  
**Usage:** Begin a focused work period

### `start_short_break() -> bool`
**Purpose:** Start a short break (typically 5 minutes)  
**Returns:** True if short break started successfully  
**Usage:** Take a brief rest between work sessions

### `start_long_break() -> bool`
**Purpose:** Start a long break (typically 15-30 minutes)  
**Returns:** True if long break started successfully  
**Usage:** Take an extended break after completing multiple pomodoros

### `next_session() -> SessionType`
**Purpose:** Automatically transition to the next session type  
**Returns:** The type of the next session  
**Usage:** Automatically move through work/break cycles

### `get_current_session_type() -> SessionType`
**Purpose:** Get the type of current session  
**Returns:** Current session type (work/short break/long break/idle)  
**Usage:** Display what type of session is currently active

### `get_completed_pomodoros() -> int`
**Purpose:** Get count of completed work sessions  
**Returns:** Number of completed pomodoros  
**Usage:** Track productivity and determine when long breaks are due

---

## 3. Configuration Functions

These functions allow customization of timer durations:

### `set_work_duration(minutes: int) -> bool`
**Purpose:** Set duration for work sessions  
**Parameters:** 
- `minutes`: Duration in minutes (1-120)
**Returns:** True if duration was set successfully  
**Usage:** Customize work session length

### `set_short_break_duration(minutes: int) -> bool`
**Purpose:** Set duration for short breaks  
**Parameters:** 
- `minutes`: Duration in minutes (1-120)
**Returns:** True if duration was set successfully  
**Usage:** Customize short break length

### `set_long_break_duration(minutes: int) -> bool`
**Purpose:** Set duration for long breaks  
**Parameters:** 
- `minutes`: Duration in minutes (1-120)
**Returns:** True if duration was set successfully  
**Usage:** Customize long break length

### `set_long_break_interval(count: int) -> bool`
**Purpose:** Set after how many pomodoros a long break occurs  
**Parameters:** 
- `count`: Number of pomodoros before long break
**Returns:** True if interval was set successfully  
**Usage:** Customize the frequency of long breaks

### `get_config() -> Dict`
**Purpose:** Get current configuration settings  
**Returns:** Dictionary with all configuration settings  
**Usage:** View or save current timer configuration

---

## 4. State Management Functions

These functions manage and query the timer state:

### `get_timer_state() -> Dict`
**Purpose:** Get complete timer state  
**Returns:** Dictionary with timer state information including:
- state (stopped/running/paused)
- current_session type
- remaining_time
- session_duration
- completed_pomodoros
- progress percentage
**Usage:** Get comprehensive status for UI updates or persistence

### `reset_pomodoro_count() -> None`
**Purpose:** Reset the count of completed pomodoros  
**Usage:** Start a new day or tracking period

### `get_session_history() -> List[SessionRecord]`
**Purpose:** Get history of completed sessions  
**Returns:** List of session records with details  
**Usage:** Review past productivity or generate statistics

### `save_session(interrupted: bool = False) -> None`
**Purpose:** Save the current session to history  
**Parameters:** 
- `interrupted`: Whether the session was interrupted
**Usage:** Record completed sessions for history tracking

---

## 5. Event/Callback Functions

These functions enable event-driven functionality:

### `on_timer_complete(callback: Callable) -> None`
**Purpose:** Register callback for when timer completes  
**Parameters:** 
- `callback`: Function to call when timer completes
**Usage:** Trigger notifications, sounds, or UI updates when session ends

### `on_session_start(callback: Callable) -> None`
**Purpose:** Register callback for when a session starts  
**Parameters:** 
- `callback`: Function to call when session starts
**Usage:** Update UI or notify user when a new session begins

### `on_timer_tick(callback: Callable) -> None`
**Purpose:** Register callback for timer updates (each second)  
**Parameters:** 
- `callback`: Function to call on each timer tick
**Usage:** Update countdown display in real-time

### `on_pomodoro_complete(callback: Callable) -> None`
**Purpose:** Register callback when a work session completes  
**Parameters:** 
- `callback`: Function to call when pomodoro completes
**Usage:** Track completed work sessions or update statistics

---

## 6. Utility Functions

These are helper functions for common operations:

### `format_time(seconds: int) -> str`
**Purpose:** Format seconds to MM:SS display format  
**Parameters:** 
- `seconds`: Time in seconds
**Returns:** Formatted time string (MM:SS)  
**Usage:** Display time in user-friendly format

### `validate_duration(minutes: int) -> bool`
**Purpose:** Validate duration input  
**Parameters:** 
- `minutes`: Duration in minutes
**Returns:** True if duration is valid (1-120 minutes)  
**Usage:** Validate user input before setting durations

### `get_session_progress() -> float`
**Purpose:** Get progress percentage of current session  
**Returns:** Progress as percentage (0.0 to 100.0)  
**Usage:** Display progress bars or visual indicators

### `update() -> None`
**Purpose:** Update timer state - should be called regularly (e.g., every second)  
**Usage:** Main update loop that checks timer completion and triggers callbacks

---

## Implementation Details

### Data Structures

**SessionType Enum:**
- WORK: Work/focus session
- SHORT_BREAK: Short break session
- LONG_BREAK: Long break session
- IDLE: No active session

**TimerState Enum:**
- STOPPED: Timer is not running
- RUNNING: Timer is actively counting down
- PAUSED: Timer is paused but can be resumed

**PomodoroConfig Dataclass:**
- work_duration: Duration of work sessions (default: 25 minutes)
- short_break_duration: Duration of short breaks (default: 5 minutes)
- long_break_duration: Duration of long breaks (default: 15 minutes)
- long_break_interval: Pomodoros before long break (default: 4)

**SessionRecord Dataclass:**
- session_type: Type of session
- duration: How long the session lasted
- completed_at: Timestamp of completion
- interrupted: Whether session was interrupted

---

## Usage Example

```python
from main import PomodoroTimer, PomodoroConfig

# Create timer with default configuration
timer = PomodoroTimer()

# Or create with custom configuration
config = PomodoroConfig(
    work_duration=25*60,  # 25 minutes
    short_break_duration=5*60,  # 5 minutes
    long_break_duration=15*60,  # 15 minutes
    long_break_interval=4  # Long break every 4 pomodoros
)
timer = PomodoroTimer(config)

# Register event callbacks
def on_complete(timer):
    print("Session completed!")
    timer.next_session()  # Automatically start next session

timer.on_timer_complete(on_complete)

# Start a work session
timer.start_work_session()

# Main loop
while True:
    timer.update()  # Call this every second
    time.sleep(1)
```

---

## Summary

This Pomodoro timer implementation provides **26 core functions** organized into 6 categories:
- **6 Timer Core Functions** for basic timer control
- **6 Pomodoro Cycle Management Functions** for managing work/break cycles
- **5 Configuration Functions** for customization
- **4 State Management Functions** for tracking and persistence
- **4 Event/Callback Functions** for extensibility
- **4 Utility Functions** for common operations

All functions are fully documented, tested, and ready to be integrated into a web application using Flask or any other web framework.
