# Enhanced NeuralShield Models Package
# This package contains all the enhanced threat detection models

__version__ = "2.0.0"
__author__ = "NeuralShield Team"

# Try to import full modules first, fallback to simplified versions
try:
    from .signature_detector import SignatureDetector
    from .file_analyzer import FileAnalyzer
    from .behavioral_analyzer import BehavioralAnalyzer
    from .encrypted_detector import EncryptedThreatDetector
    from .social_engineering_detector import SocialEngineeringDetector
    from .ensemble_detector import EnhancedThreatDetector
    FULL_MODULES_AVAILABLE = True
except ImportError:
    # Fallback to simplified modules
    from .signature_detector_simple import SignatureDetector
    from .file_analyzer_simple import FileAnalyzer
    from .behavioral_analyzer_simple import BehavioralAnalyzer
    from .encrypted_detector_simple import EncryptedThreatDetector
    from .social_engineering_detector_simple import SocialEngineeringDetector
    from .ensemble_detector_simple import EnhancedThreatDetector
    FULL_MODULES_AVAILABLE = False

__all__ = [
    'SignatureDetector',
    'FileAnalyzer', 
    'BehavioralAnalyzer',
    'EncryptedThreatDetector',
    'SocialEngineeringDetector',
    'EnhancedThreatDetector',
    'FULL_MODULES_AVAILABLE'
]
