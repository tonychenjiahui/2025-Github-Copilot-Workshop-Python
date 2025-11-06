"""
Pomodoro Timer Application
A timer application following the Pomodoro Technique for time management.

Necessary Functions for Pomodoro Timer Application:
=====================================================

1. Timer Core Functions:
   - start_timer(): Start the timer countdown
   - pause_timer(): Pause the running timer
   - resume_timer(): Resume a paused timer
   - stop_timer(): Stop and reset the timer
   - get_remaining_time(): Get the remaining time in seconds
   - is_timer_running(): Check if timer is currently running

2. Pomodoro Cycle Management Functions:
   - start_work_session(): Start a work/focus session (typically 25 minutes)
   - start_short_break(): Start a short break (typically 5 minutes)
   - start_long_break(): Start a long break (typically 15-30 minutes)
   - next_session(): Automatically transition to the next session type
   - get_current_session_type(): Get the type of current session (work/short break/long break)
   - get_completed_pomodoros(): Get count of completed work sessions

3. Configuration Functions:
   - set_work_duration(minutes): Set duration for work sessions
   - set_short_break_duration(minutes): Set duration for short breaks
   - set_long_break_duration(minutes): Set duration for long breaks
   - set_long_break_interval(count): Set after how many pomodoros a long break occurs
   - get_config(): Get current configuration settings

4. State Management Functions:
   - get_timer_state(): Get complete timer state (running/paused/stopped)
   - reset_pomodoro_count(): Reset the count of completed pomodoros
   - get_session_history(): Get history of completed sessions
   - save_session(): Save the current session to history

5. Event/Callback Functions:
   - on_timer_complete(callback): Register callback for when timer completes
   - on_session_start(callback): Register callback for when a session starts
   - on_timer_tick(callback): Register callback for timer updates (each second)
   - on_pomodoro_complete(callback): Register callback when a work session completes

6. Utility Functions:
   - format_time(seconds): Format seconds to MM:SS display format
   - validate_duration(minutes): Validate duration input
   - get_session_progress(): Get progress percentage of current session
"""

import time
from enum import Enum
from typing import Callable, Optional, List, Dict
from dataclasses import dataclass, field


class SessionType(Enum):
    """Types of Pomodoro sessions"""
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    IDLE = "idle"


class TimerState(Enum):
    """States of the timer"""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


@dataclass
class PomodoroConfig:
    """Configuration for Pomodoro timer"""
    work_duration: int = 25 * 60  # 25 minutes in seconds
    short_break_duration: int = 5 * 60  # 5 minutes in seconds
    long_break_duration: int = 15 * 60  # 15 minutes in seconds
    long_break_interval: int = 4  # Long break after 4 pomodoros


@dataclass
class SessionRecord:
    """Record of a completed session"""
    session_type: SessionType
    duration: int
    completed_at: float
    interrupted: bool = False


class PomodoroTimer:
    """Main Pomodoro Timer class implementing all necessary functions"""
    
    def __init__(self, config: Optional[PomodoroConfig] = None):
        self.config = config or PomodoroConfig()
        self._state = TimerState.STOPPED
        self._current_session = SessionType.IDLE
        self._remaining_time = 0
        self._session_duration = 0
        self._start_time = 0
        self._pause_time = 0
        self._completed_pomodoros = 0
        self._session_history: List[SessionRecord] = []
        
        # Event callbacks
        self._on_timer_complete_callbacks: List[Callable] = []
        self._on_session_start_callbacks: List[Callable] = []
        self._on_timer_tick_callbacks: List[Callable] = []
        self._on_pomodoro_complete_callbacks: List[Callable] = []
    
    # ===== 1. Timer Core Functions =====
    
    def start_timer(self, duration: int) -> bool:
        """
        Start the timer countdown
        
        Args:
            duration: Duration in seconds
            
        Returns:
            True if timer started successfully
        """
        if duration <= 0:
            return False
        
        self._state = TimerState.RUNNING
        self._remaining_time = duration
        self._session_duration = duration
        self._start_time = time.time()
        self._pause_time = 0
        return True
    
    def pause_timer(self) -> bool:
        """
        Pause the running timer
        
        Returns:
            True if timer was paused successfully
        """
        if self._state != TimerState.RUNNING:
            return False
        
        self._state = TimerState.PAUSED
        self._pause_time = time.time()
        return True
    
    def resume_timer(self) -> bool:
        """
        Resume a paused timer
        
        Returns:
            True if timer was resumed successfully
        """
        if self._state != TimerState.PAUSED:
            return False
        
        self._state = TimerState.RUNNING
        # Adjust start time to account for pause duration
        pause_duration = time.time() - self._pause_time
        self._start_time += pause_duration
        self._pause_time = 0
        return True
    
    def stop_timer(self) -> bool:
        """
        Stop and reset the timer
        
        Returns:
            True if timer was stopped successfully
        """
        self._state = TimerState.STOPPED
        self._remaining_time = 0
        self._session_duration = 0
        self._start_time = 0
        self._pause_time = 0
        return True
    
    def get_remaining_time(self) -> int:
        """
        Get the remaining time in seconds
        
        Returns:
            Remaining time in seconds
        """
        if self._state == TimerState.RUNNING:
            elapsed = time.time() - self._start_time
            remaining = self._session_duration - elapsed
            return max(0, int(remaining))
        elif self._state == TimerState.PAUSED:
            elapsed = self._pause_time - self._start_time
            remaining = self._session_duration - elapsed
            return max(0, int(remaining))
        else:
            return 0
    
    def is_timer_running(self) -> bool:
        """
        Check if timer is currently running
        
        Returns:
            True if timer is running
        """
        return self._state == TimerState.RUNNING
    
    # ===== 2. Pomodoro Cycle Management Functions =====
    
    def start_work_session(self) -> bool:
        """
        Start a work/focus session (typically 25 minutes)
        
        Returns:
            True if work session started successfully
        """
        self._current_session = SessionType.WORK
        started = self.start_timer(self.config.work_duration)
        if started:
            self._trigger_session_start_callbacks()
        return started
    
    def start_short_break(self) -> bool:
        """
        Start a short break (typically 5 minutes)
        
        Returns:
            True if short break started successfully
        """
        self._current_session = SessionType.SHORT_BREAK
        started = self.start_timer(self.config.short_break_duration)
        if started:
            self._trigger_session_start_callbacks()
        return started
    
    def start_long_break(self) -> bool:
        """
        Start a long break (typically 15-30 minutes)
        
        Returns:
            True if long break started successfully
        """
        self._current_session = SessionType.LONG_BREAK
        started = self.start_timer(self.config.long_break_duration)
        if started:
            self._trigger_session_start_callbacks()
        return started
    
    def next_session(self) -> SessionType:
        """
        Automatically transition to the next session type
        
        Returns:
            The type of the next session
        """
        # Save current session if it was completed
        if self._state == TimerState.RUNNING or self._state == TimerState.PAUSED:
            self.save_session(interrupted=False)
        
        if self._current_session == SessionType.WORK:
            self._completed_pomodoros += 1
            self._trigger_pomodoro_complete_callbacks()
            
            # Determine if long break or short break
            if self._completed_pomodoros % self.config.long_break_interval == 0:
                self.start_long_break()
                return SessionType.LONG_BREAK
            else:
                self.start_short_break()
                return SessionType.SHORT_BREAK
        else:
            # After any break, start work session
            self.start_work_session()
            return SessionType.WORK
    
    def get_current_session_type(self) -> SessionType:
        """
        Get the type of current session
        
        Returns:
            Current session type
        """
        return self._current_session
    
    def get_completed_pomodoros(self) -> int:
        """
        Get count of completed work sessions
        
        Returns:
            Number of completed pomodoros
        """
        return self._completed_pomodoros
    
    # ===== 3. Configuration Functions =====
    
    def set_work_duration(self, minutes: int) -> bool:
        """
        Set duration for work sessions
        
        Args:
            minutes: Duration in minutes
            
        Returns:
            True if duration was set successfully
        """
        if not self.validate_duration(minutes):
            return False
        self.config.work_duration = minutes * 60
        return True
    
    def set_short_break_duration(self, minutes: int) -> bool:
        """
        Set duration for short breaks
        
        Args:
            minutes: Duration in minutes
            
        Returns:
            True if duration was set successfully
        """
        if not self.validate_duration(minutes):
            return False
        self.config.short_break_duration = minutes * 60
        return True
    
    def set_long_break_duration(self, minutes: int) -> bool:
        """
        Set duration for long breaks
        
        Args:
            minutes: Duration in minutes
            
        Returns:
            True if duration was set successfully
        """
        if not self.validate_duration(minutes):
            return False
        self.config.long_break_duration = minutes * 60
        return True
    
    def set_long_break_interval(self, count: int) -> bool:
        """
        Set after how many pomodoros a long break occurs
        
        Args:
            count: Number of pomodoros before long break
            
        Returns:
            True if interval was set successfully
        """
        if count <= 0:
            return False
        self.config.long_break_interval = count
        return True
    
    def get_config(self) -> Dict:
        """
        Get current configuration settings
        
        Returns:
            Dictionary with configuration settings
        """
        return {
            'work_duration': self.config.work_duration // 60,
            'short_break_duration': self.config.short_break_duration // 60,
            'long_break_duration': self.config.long_break_duration // 60,
            'long_break_interval': self.config.long_break_interval
        }
    
    # ===== 4. State Management Functions =====
    
    def get_timer_state(self) -> Dict:
        """
        Get complete timer state
        
        Returns:
            Dictionary with timer state information
        """
        return {
            'state': self._state.value,
            'current_session': self._current_session.value,
            'remaining_time': self.get_remaining_time(),
            'session_duration': self._session_duration,
            'completed_pomodoros': self._completed_pomodoros,
            'progress': self.get_session_progress()
        }
    
    def reset_pomodoro_count(self) -> None:
        """Reset the count of completed pomodoros"""
        self._completed_pomodoros = 0
    
    def get_session_history(self) -> List[SessionRecord]:
        """
        Get history of completed sessions
        
        Returns:
            List of session records
        """
        return self._session_history.copy()
    
    def save_session(self, interrupted: bool = False) -> None:
        """
        Save the current session to history
        
        Args:
            interrupted: Whether the session was interrupted
        """
        if self._current_session != SessionType.IDLE:
            record = SessionRecord(
                session_type=self._current_session,
                duration=self._session_duration,
                completed_at=time.time(),
                interrupted=interrupted
            )
            self._session_history.append(record)
    
    # ===== 5. Event/Callback Functions =====
    
    def on_timer_complete(self, callback: Callable) -> None:
        """
        Register callback for when timer completes
        
        Args:
            callback: Function to call when timer completes
        """
        if callback not in self._on_timer_complete_callbacks:
            self._on_timer_complete_callbacks.append(callback)
    
    def on_session_start(self, callback: Callable) -> None:
        """
        Register callback for when a session starts
        
        Args:
            callback: Function to call when session starts
        """
        if callback not in self._on_session_start_callbacks:
            self._on_session_start_callbacks.append(callback)
    
    def on_timer_tick(self, callback: Callable) -> None:
        """
        Register callback for timer updates (each second)
        
        Args:
            callback: Function to call on each timer tick
        """
        if callback not in self._on_timer_tick_callbacks:
            self._on_timer_tick_callbacks.append(callback)
    
    def on_pomodoro_complete(self, callback: Callable) -> None:
        """
        Register callback when a work session completes
        
        Args:
            callback: Function to call when pomodoro completes
        """
        if callback not in self._on_pomodoro_complete_callbacks:
            self._on_pomodoro_complete_callbacks.append(callback)
    
    def _trigger_timer_complete_callbacks(self) -> None:
        """Trigger all timer complete callbacks"""
        for callback in self._on_timer_complete_callbacks:
            callback(self)
    
    def _trigger_session_start_callbacks(self) -> None:
        """Trigger all session start callbacks"""
        for callback in self._on_session_start_callbacks:
            callback(self)
    
    def _trigger_timer_tick_callbacks(self) -> None:
        """Trigger all timer tick callbacks"""
        for callback in self._on_timer_tick_callbacks:
            callback(self)
    
    def _trigger_pomodoro_complete_callbacks(self) -> None:
        """Trigger all pomodoro complete callbacks"""
        for callback in self._on_pomodoro_complete_callbacks:
            callback(self)
    
    # ===== 6. Utility Functions =====
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """
        Format seconds to MM:SS display format
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string (MM:SS)
        """
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def validate_duration(minutes: int) -> bool:
        """
        Validate duration input
        
        Args:
            minutes: Duration in minutes
            
        Returns:
            True if duration is valid
        """
        return 1 <= minutes <= 120  # Between 1 and 120 minutes
    
    def get_session_progress(self) -> float:
        """
        Get progress percentage of current session
        
        Returns:
            Progress as percentage (0.0 to 100.0)
        """
        if self._session_duration == 0:
            return 0.0
        
        remaining = self.get_remaining_time()
        elapsed = self._session_duration - remaining
        return (elapsed / self._session_duration) * 100.0
    
    def update(self) -> None:
        """
        Update timer state - should be called regularly (e.g., every second)
        This checks if timer has completed and triggers appropriate callbacks
        """
        if self._state == TimerState.RUNNING:
            remaining = self.get_remaining_time()
            
            # Trigger tick callbacks
            self._trigger_timer_tick_callbacks()
            
            # Check if timer completed
            if remaining <= 0:
                self._trigger_timer_complete_callbacks()
                self.save_session(interrupted=False)
                self.stop_timer()


# Example usage and demonstration
if __name__ == "__main__":
    print("=== Pomodoro Timer Application ===\n")
    print("Necessary Functions Implemented:\n")
    print("1. Timer Core Functions:")
    print("   - start_timer(), pause_timer(), resume_timer(), stop_timer()")
    print("   - get_remaining_time(), is_timer_running()\n")
    
    print("2. Pomodoro Cycle Management:")
    print("   - start_work_session(), start_short_break(), start_long_break()")
    print("   - next_session(), get_current_session_type(), get_completed_pomodoros()\n")
    
    print("3. Configuration Functions:")
    print("   - set_work_duration(), set_short_break_duration(), set_long_break_duration()")
    print("   - set_long_break_interval(), get_config()\n")
    
    print("4. State Management:")
    print("   - get_timer_state(), reset_pomodoro_count()")
    print("   - get_session_history(), save_session()\n")
    
    print("5. Event/Callback Functions:")
    print("   - on_timer_complete(), on_session_start()")
    print("   - on_timer_tick(), on_pomodoro_complete()\n")
    
    print("6. Utility Functions:")
    print("   - format_time(), validate_duration(), get_session_progress()\n")
    
    print("=" * 50)
    print("\nDemo: Quick timer test (5 seconds work session)\n")
    
    # Create timer with custom short duration for demo
    config = PomodoroConfig()
    config.work_duration = 5  # 5 seconds for demo
    timer = PomodoroTimer(config)
    
    # Register callbacks
    def on_start(t):
        print(f"✓ Session started: {t.get_current_session_type().value}")
    
    def on_complete(t):
        print("✓ Timer completed!")
    
    def on_tick(t):
        remaining = t.get_remaining_time()
        formatted = PomodoroTimer.format_time(remaining)
        progress = t.get_session_progress()
        print(f"  Time remaining: {formatted} ({progress:.1f}% complete)")
    
    timer.on_session_start(on_start)
    timer.on_timer_complete(on_complete)
    timer.on_timer_tick(on_tick)
    
    # Start work session
    timer.start_work_session()
    
    # Run for 5 seconds
    for _ in range(6):
        timer.update()
        time.sleep(1)
    
    print(f"\nFinal state: {timer.get_timer_state()}")
    print(f"Config: {timer.get_config()}")
