"""Embodiment layer — the body senses and muscles of SPEACE."""

from speace_core.cellular_brain.embodiment.cyber_physical_sensor_array import (
    CyberPhysicalSensorArray,
)
from speace_core.cellular_brain.embodiment.embodied_action_actuator import (
    EmbodiedActionActuator,
)
from speace_core.cellular_brain.embodiment.physical_environment_model import (
    PhysicalEnvironmentModel,
)
from speace_core.cellular_brain.embodiment.embodiment_monitor import (
    EmbodimentMonitor,
)

__all__ = [
    "CyberPhysicalSensorArray",
    "EmbodiedActionActuator",
    "PhysicalEnvironmentModel",
    "EmbodimentMonitor",
]
