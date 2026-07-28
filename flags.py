"""CloudBees Unify Feature Management integration for TaskFlow's backend.

Uses the official Python server-side SDK ("rox"). If ROX_SDK_KEY isn't set,
flags just use their default values below, so the app runs fine before
Module 5 (Feature Flags) of the workshop.

Reference:
https://docs.cloudbees.com/docs/cloudbees-unify/latest/feature-management/how-to-guides/install-server-side-sdks
"""

import os

from rox.server.rox_server import Rox
from rox.server.flags.rox_flag import RoxFlag
from rox.core.entities.rox_string import RoxString


class TaskFlowFlags:
    def __init__(self):
        # Boolean flag: show a reminder banner in the UI, driven from the backend.
        self.show_due_date_banner = RoxFlag(False)
        # String flag: priority label shown next to each task.
        self.task_priority_label = RoxString("medium", ["low", "medium", "high"])


flags = TaskFlowFlags()


def init_flags():
    """Register flags with Unify and connect using ROX_SDK_KEY if present."""
    Rox.register(flags)

    sdk_key = os.environ.get("ROX_SDK_KEY")
    if not sdk_key:
        print("ROX_SDK_KEY not set - using local default flag values.")
        return

    try:
        # Rox.setup() returns a Future-like object; .result() blocks until
        # the SDK has fetched its initial flag configuration.
        Rox.setup(sdk_key).result()
        print("Connected to CloudBees Unify Feature Management.")
    except Exception as exc:  # pragma: no cover - defensive, don't crash the app
        print(f"Feature flag setup failed, using defaults: {exc}")
