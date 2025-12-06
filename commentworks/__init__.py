"""
CommentWorks: Privacy-first local AI for analyzing open-ended survey comments.

Detect themes, assign tags, and understand feedback without sending data to the cloud.
"""

from .core import detect_themes, assign_themes

__version__ = "0.1.0-alpha"
__all__ = ["detect_themes", "assign_themes"]
