@echo off
start cmd /k "python -m http.server 8080"
start cmd /k "python core/server.py"