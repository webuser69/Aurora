import re
import webbrowser
import subprocess
import platform

# Detect if running locally on Windows
IS_WINDOWS = platform.system() == "Windows"

# Websites
sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "reddit": "https://www.reddit.com",
    "linkedin": "https://www.linkedin.com",
    "stackoverflow": "https://stackoverflow.com",
    "github": "https://github.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "wikipedia": "https://www.wikipedia.org",
    "whatsapp": "https://web.whatsapp.com",
    "openai": "https://www.openai.com",
    "zoom": "https://zoom.us",
    "spotify": "https://open.spotify.com",
    "canva": "https://www.canva.com",
    "chatgpt": "https://chat.openai.com"
}

# Apps (Windows only)
apps = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "command prompt": "cmd",
    "chrome": "chrome",
    "file explorer": "explorer",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "task manager": "taskmgr",
    "snipping tool": "snippingtool",
    "settings": "ms-settings:",
    "windows security": "windowsdefender:"
}

# Closing apps (Windows only)
app_close = {
    "notepad": "notepad.exe",
    "calculator": "ApplicationFrameHost.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "chrome": "chrome.exe",
    "file explorer": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "task manager": "taskmgr.exe",
    "snipping tool": "snippingtool.exe",
    "settings": "SystemSettings.exe",
    "windows security": "SecurityHealthSystray.exe"
}

# ---------------- UTILITY ---------------- #
def _match(user, collection):
    """Find items from collection that appear in user input"""
    return [item for item in collection if re.search(rf"\b{re.escape(item)}\b", user)]

# ---------------- OPEN WEBSITES ---------------- #
def open_web(user):
    matched = _match(user, sites)
    if not matched:
        return None
    
    response = []
    for site in matched:
        site_info = {"message": f"Opening {site.capitalize()}...", "url": sites[site]}
        response.append(site_info)
    return response

# ---------------- OPEN APPS ---------------- #
def open_app(user):
    matched = _match(user, apps)
    if not matched: 
        return None

    if not IS_WINDOWS:
        return "Opening system apps is not supported online. Please use a local version."

    responses = []
    for app in matched:
        try:
            subprocess.Popen(apps[app])
            responses.append(f"Opening {app.capitalize()}...")
        except Exception:
            responses.append(f"Failed to open {app.capitalize()}.")
    return " ".join(responses)

# ---------------- CLOSE APPS ---------------- #
def close_app(user):
    matched = _match(user, app_close)
    if not matched: 
        return None

    if not IS_WINDOWS:
        return "Closing system apps is not supported online. Please use a local version."

    responses = []
    for app in matched:
        try:
            subprocess.run(["taskkill", "/f", "/im", app_close[app]],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            responses.append(f"Closed {app.capitalize()}.")
        except Exception:
            responses.append(f"Failed to close {app.capitalize()}.")
    return " ".join(responses)
