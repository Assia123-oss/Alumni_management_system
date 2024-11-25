from .models import Alumni
from .schemas import AlumniCreate, AlumniUpdate, Alumni
from .services import AlumniService
from .routes import router

__all__ = [
    'Alumni',
    'AlumniCreate',
    'AlumniUpdate',
    'AlumniService',
    'router'
]