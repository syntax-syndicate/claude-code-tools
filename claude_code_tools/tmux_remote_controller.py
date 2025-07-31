#!/usr/bin/env python3
"""
Remote Tmux Controller - Stub implementation
This is a minimal stub to prevent import errors when tmux-cli is used outside tmux.
"""

import subprocess
from typing import Optional, List, Dict


class RemoteTmuxController:
    """Stub implementation of RemoteTmuxController to prevent import errors."""
    
    def __init__(self, session_name: str = "remote-cli-session"):
        """Initialize with session name."""
        self.session_name = session_name
        print(f"Warning: RemoteTmuxController is not fully implemented.")
        print(f"Remote mode functionality is currently unavailable.")
        print(f"Please use tmux-cli from inside a tmux session for full functionality.")
    
    def list_panes(self) -> List[Dict[str, str]]:
        """Return empty list."""
        return []
    
    def launch_cli(self, command: str, name: Optional[str] = None) -> Optional[str]:
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def send_keys(self, text: str, pane_id: Optional[str] = None, enter: bool = True,
                  delay_enter: bool = True):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def capture_pane(self, pane_id: Optional[str] = None, lines: Optional[int] = None) -> str:
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def wait_for_idle(self, pane_id: Optional[str] = None, idle_time: float = 2.0,
                     check_interval: float = 0.5, timeout: Optional[int] = None) -> bool:
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def send_interrupt(self, pane_id: Optional[str] = None):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def send_escape(self, pane_id: Optional[str] = None):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def kill_window(self, window_id: Optional[str] = None):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def attach_session(self):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def cleanup_session(self):
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def list_windows(self) -> List[Dict[str, str]]:
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")
    
    def _resolve_pane_id(self, pane: Optional[str]) -> Optional[str]:
        """Not implemented."""
        raise NotImplementedError("Remote mode is not available. Please use tmux-cli from inside tmux.")