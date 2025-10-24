#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Point d'entrée de l'application
Pour Replit deployment avec gunicorn
"""

from backend.app import app

if __name__ == "__main__":
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
