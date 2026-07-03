# 🗑️ Node Modules & Vendor Project Purger

A smart, interactive CLI tool built in Python to safely scan your workspaces, calculate exact directory sizes, and recursively delete target dependency folders (`node_modules` and `vendor`).

### ✨ Features
* **Smart Context Filters:** Only targets `node_modules` or `vendor` if a matching `package.json` or `composer.json` is anchored next to it.
* **System Guardrails:** Automatically skips system paths, hidden folders, and cloud sync directories (like iCloud Drive) to prevent accidental data loss or unwanted background downloads.
* **Size Calculation:** Tells you exactly how much disk space each folder is consuming (and how much you'll save) before you wipe anything.
* **Interactive Toggling:** Full multi-select checkbox menu featuring instant select-all capabilities via terminal shortcuts.

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
Open your terminal and clone this repository to a secure location on your machine (e.g., your home folder):

```bash
git clone [https://github.com/YOUR_USERNAME/repo-name.git](https://github.com/YOUR_USERNAME/repo-name.git) ~/deps-purger
cd ~/deps-purger
```

### 2. Install Requirements
Make sure you have the required interactive prompt engine installed globally (or in your preferred environment):

```bash
pip install -r requirements.txt
```
*(Note: Depending on your OS, you might need to use `pip3`).*

---

## 🎮 How to Use (Interactive Controls)

Once running, navigate the prompt using the following keyboard shortcuts:
* **`Arrow Keys` / `J or K`**: Navigate up and down the folder list.
* **`Spacebar`**: Select or deselect a specific folder.
* **`a`**: **Toggle / Select ALL items** at once.
* **`i`**: Invert your current selection.
* **`Enter`**: Proceed to the final confirmation step.

---

## ⚙️ Setting Up a Global Shortcut (Run from Anywhere)

To run this tool inside any of your workspace directories without typing the full path every time, configure a simple global alias.

### For macOS & Linux (`zsh` or `bash`)

1. Open your profile configuration file in an editor (usually `.zshrc` for modern macOS or `.bashrc` for Linux):
   ```bash
   nano ~/.zshrc
   ```
2. Scroll to the bottom and paste the following line (adjusting the path to wherever you cloned the folder):
   ```bash
   alias purge-deps="python3 ~/deps-purger/cleaner.py"
   ```
3. Save and close the file (`Ctrl+O`, `Enter`, then `Ctrl+X`).
4. Reload your terminal settings to apply the change:
   ```bash
   source ~/.zshrc
   ```

### For Windows (PowerShell Profile)

1. Open your PowerShell profile configuration:
   ```powershell
   notepad $PROFILE
   ```
2. Paste the following function snippet inside the file (adjusting the path to your cloned folder):
   ```powershell
   function purge-deps {
       python C:\project-purger\cleaner.py
   }
   ```
3. Save the file and restart your PowerShell window.

---

## 🏃‍♀️ Running the Tool Globally

Now, whenever you want to free up massive amounts of storage space, simply open your terminal, **navigate to your workspace or project root folder**, and run:

```bash
purge-deps
```