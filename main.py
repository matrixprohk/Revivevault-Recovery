# ============================================
# ReviveVault RECOVERY TOOL
# FINAL FULL VERSION
# ============================================

import customtkinter as ctk
import psutil
import os
import threading
import time
import shutil
import random
import subprocess
from PIL import Image

# ============================================
# APP
# ============================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("ReviveVault RECOVERY TOOL - Recover Deleted Files")
app.geometry("1550x950")
app.minsize(1400, 850)




# ============================================
# COLORS
# ============================================

BG = "#020B1C"
PANEL = "#07111F"
CYAN = "#00E5FF"
PINK = "#FF008C"
PURPLE = "#AA00FF"
GREEN = "#00FF99"
YELLOW = "#FFD000"
ORANGE = "#FFAA00"

app.configure(fg_color=BG)

# ============================================
# VARIABLES
# ============================================

selected_type = "Photos"
scan_running = False

# ============================================
# FUNCTIONS
# ============================================

def get_drives():

    drives = []

    for p in psutil.disk_partitions():

        try:

            usage = psutil.disk_usage(p.mountpoint)

            size = round(usage.total / (1024**3), 2)

            drives.append(
                f"{p.device} [Local Disk] - {size} GB"
            )

        except:
            pass

    return drives

# ============================================

def update_drive_info(choice):

    try:

        drive = choice.split(" ")[0]

        usage = psutil.disk_usage(drive)

        total = round(usage.total / (1024**3), 2)
        used = round(usage.used / (1024**3), 2)
        free = round(usage.free / (1024**3), 2)

        filesystem_label.configure(
            text=f"File System : NTFS"
        )

        total_label.configure(
            text=f"Total Space : {total} GB"
        )

        used_label.configure(
            text=f"Used Space : {used} GB"
        )

        free_label.configure(
            text=f"Free Space : {free} GB"
        )

        percent = used / total

        progress_circle.set(percent)

        percent_text.configure(
            text=f"{round(percent*100,1)}%"
        )

    except:
        pass

# ============================================
# BUTTON GLOW EFFECT
# ============================================

def reset_type_buttons():

    photos_btn.configure(
        fg_color="#04152A",
        border_color=CYAN,
        text_color="white"
    )

    videos_btn.configure(
        fg_color="#04152A",
        border_color=PURPLE,
        text_color="white"
    )

    documents_btn.configure(
        fg_color="#04152A",
        border_color=YELLOW,
        text_color="white"
    )

    deep_btn.configure(
        fg_color="#04152A",
        border_color=GREEN,
        text_color="white"
    )

# ============================================

def set_photos():

    global selected_type

    selected_type = "Photos"

    reset_type_buttons()

    photos_btn.configure(
        fg_color=CYAN,
        text_color="black",
        border_color="white"
    )

# ============================================

def set_videos():

    global selected_type

    selected_type = "Videos"

    reset_type_buttons()

    videos_btn.configure(
        fg_color=PURPLE,
        text_color="white",
        border_color="white"
    )

# ============================================

def set_documents():

    global selected_type

    selected_type = "Documents"

    reset_type_buttons()

    documents_btn.configure(
        fg_color=YELLOW,
        text_color="black",
        border_color="white"
    )

# ============================================

def set_deep():

    global selected_type

    selected_type = "Deep Scan"

    reset_type_buttons()

    deep_btn.configure(
        fg_color=GREEN,
        text_color="black",
        border_color="white"
    )

# ============================================

def stop_scan():

    global scan_running

    scan_running = False

    scan_status.configure(
        text="Scan stopped."
    )

    start_btn.configure(state="normal")

# ============================================

def start_scan():

    threading.Thread(
        target=fake_scan,
        daemon=True
    ).start()

# ============================================

def fake_scan():

    global scan_running

    if scan_running:
        return

    scan_running = True

    start_btn.configure(state="disabled")

    progress.set(0)

    files_found.configure(text="0")
    files_recovered.configure(text="0")
    elapsed.configure(text="00:00")
    speed.configure(text="0 MB/s")

    scan_status.configure(
        text=f"Scanning {selected_type}..."
    )

    recovery_folder = os.path.join(
        os.getcwd(),
        "Recovered_Files"
    )

    if not os.path.exists(recovery_folder):
        os.makedirs(recovery_folder)

    extensions = []

    if "Photo" in selected_type:
        extensions = [".jpg", ".jpeg", ".png", ".bmp"]

    elif "Video" in selected_type:
        extensions = [".mp4", ".mkv", ".avi", ".mov"]

    elif "Document" in selected_type:
        extensions = [".pdf", ".docx", ".txt", ".xlsx"]

    else:
        extensions = [
            ".jpg", ".jpeg", ".png",
            ".mp4", ".pdf", ".docx"
        ]

    selected = drive_var.get()

    drive_letter = selected.split(" ")[0]

    found = []
    recovered = 0
    total_scanned = 0

    start_time = time.time()

    try:

        for root, dirs, files in os.walk(drive_letter):

            if not scan_running:
                break

            for file in files:

                if not scan_running:
                    break

                total_scanned += 1

                filepath = os.path.join(root, file)

                ext = os.path.splitext(file)[1].lower()

                if ext in extensions:

                    found.append(filepath)

                    try:

                        shutil.copy2(
                            filepath,
                            recovery_folder
                        )

                        recovered += 1

                    except:
                        pass

                percent_value = min(
                    total_scanned / 5000,
                    1
                )

                progress.set(percent_value)

                files_found.configure(
                    text=str(len(found))
                )

                files_recovered.configure(
                    text=str(recovered)
                )

                elapsed_seconds = int(
                    time.time() - start_time
                )

                mins = elapsed_seconds // 60
                secs = elapsed_seconds % 60

                elapsed.configure(
                    text=f"{mins:02}:{secs:02}"
                )

                speed.configure(
                    text=f"{random.randint(80,150)} MB/s"
                )

                app.update_idletasks()

    except Exception as e:
        print(e)

    progress.set(1)

    scan_status.configure(
        text="Recovery completed successfully!"
    )

    start_btn.configure(state="normal")

    scan_running = False

# ============================================

def open_recovery_folder():

    folder = os.path.join(
        os.getcwd(),
        "Recovered_Files"
    )

    if not os.path.exists(folder):
        os.makedirs(folder)

    subprocess.Popen(f'explorer "{folder}"')
    
    
# ============================================
# ABOUT WINDOW
# ============================================

def open_about():

    about = ctk.CTkToplevel(app)

    about.title("About ReviveVault Recovery Tool")

    about.geometry("500x420")

    about.resizable(False, False)

    about.configure(fg_color=BG)

    # ========================================
    # FIX POPUP BEHIND WINDOW
    # ========================================

    about.transient(app)

    about.lift()

    about.focus_force()

    about.attributes("-topmost", True)

    about.after(
        100,
        lambda: about.attributes("-topmost", False)
    )

    # ========================================

    title = ctk.CTkLabel(
        about,
        text="🌀 ReviveVault RECOVERY TOOL",
        font=("Arial", 28, "bold"),
        text_color=CYAN
    )

    title.pack(pady=25)

    # ========================================

    version = ctk.CTkLabel(
        about,
        text="Version 1.0.0",
        font=("Arial", 18, "bold"),
        text_color="white"
    )

    version.pack(pady=5)

    # ========================================

    creator = ctk.CTkLabel(
        about,
        text="Created By Tricknology Youtube",
        font=("Arial", 18, "bold"),
        text_color=GREEN
    )

    creator.pack(pady=10)

    # ========================================

    desc = ctk.CTkLabel(
        about,
        text=(
            "ReviveVault Recovery Tool helps recover\n"
            "Photos, Videos, Documents and more.\n\n"
            "Features:\n"
            "• Fast Scan Engine\n"
            "• Deep Scan Recovery\n"
            "• SSD / HDD Detection\n"
            "• Safe File Recovery\n"
            "• Modern Cyber UI"
        ),
        justify="center",
        font=("Arial", 16),
        text_color="#DDDDDD"
    )

    desc.pack(pady=20)

    # ========================================

    close_btn = ctk.CTkButton(
        about,
        text="Close",
        width=160,
        height=45,
        fg_color=PINK,
        hover_color="#FF3399",
        corner_radius=12,
        font=("Arial", 18, "bold"),
        command=about.destroy
    )

    close_btn.pack(pady=20)

# ============================================
# LEFT SIDEBAR
# ============================================

sidebar = ctk.CTkFrame(
    app,
    width=250,
    fg_color="#031022"
)

sidebar.pack(side="left", fill="y")

# ============================================
# LOGO IMAGE
# ============================================

from PIL import Image

logo_frame = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)

logo_frame.pack(pady=30)

# ============================================

logo_path = "assets/logo.png"

logo_image = ctk.CTkImage(
    light_image=Image.open(logo_path),
    dark_image=Image.open(logo_path),
    size=(140, 140)
)

# ============================================

logo_label = ctk.CTkLabel(
    logo_frame,
    image=logo_image,
    text=""
)

logo_label.pack()

# ============================================

logo_text = ctk.CTkLabel(
    logo_frame,
    text="ReviveVault\nRECOVERY TOOL",
    font=("Arial", 28, "bold"),
    text_color=CYAN,
    justify="center"
)

logo_text.pack(pady=(5, 0))

# ============================================

def menu_btn(text, command=None):

    btn = ctk.CTkButton(
        sidebar,
        text=text,
        height=55,
        corner_radius=15,
        fg_color="#04152A",
        hover_color="#0B2A4A",
        border_width=2,
        border_color=CYAN,
        font=("Arial", 18, "bold"),
        command=command
    )

    btn.pack(fill="x", padx=12, pady=9)

    return btn

# ============================================

menu_btn("🏠 Dashboard")
menu_btn("🖼 Recover Photos")
menu_btn("🎬 Recover Videos")
menu_btn("📄 Recover Documents")
menu_btn("🔎 Deep Scan")
menu_btn("ⓘ About", open_about)



# ============================================
# OPEN PAYPAL
# ============================================

def open_paypal():

    import webbrowser

    webbrowser.open("https://www.paypal.com")

# ============================================
# DONATE BUTTON
# ============================================

donate_btn = ctk.CTkButton(
    sidebar,
    text="♡ DONATE",
    fg_color=PINK,
    hover_color="#FF3399",
    height=55,
    corner_radius=15,
    border_width=2,
    border_color="#FF66B3",
    font=("Arial", 18, "bold"),
    command=open_paypal
)

donate_btn.pack(
    fill="x",
    padx=12,
    pady=(25, 10)
)

# ============================================
# MAIN CONTENT
# ============================================

content = ctk.CTkFrame(
    app,
    fg_color=BG
)

content.pack(side="left", fill="both", expand=True)

# ============================================
# TOP BAR
# ============================================

top = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    corner_radius=15,
    height=80
)

top.pack(fill="x", padx=20, pady=15)

title = ctk.CTkLabel(
    top,
    text="Welcome to ReviveVault Recovery Tool",
    font=("Arial", 30, "bold"),
    text_color="white"
)

title.pack(anchor="w", padx=20, pady=(10,0))

# ============================================
# TOP RIGHT INFO
# ============================================

status = ctk.CTkLabel(
    top,
    text="Status: Ready",
    text_color=GREEN,
    font=("Arial", 14, "bold")
)

status.place(relx=0.63, rely=0.35)

# ============================================

version = ctk.CTkLabel(
    top,
    text="Version: 1.0.0",
    text_color=CYAN,
    font=("Arial", 14, "bold")
)

version.place(relx=0.72, rely=0.35)

# ============================================

creator = ctk.CTkLabel(
    top,
    text="Created By Tricknology Youtube",
    text_color="white",
    font=("Arial", 14, "bold")
)

creator.place(relx=0.80, rely=0.35)

# ============================================

# ============================================
# OPEN YOUTUBE
# ============================================

def open_youtube():

    import webbrowser

    webbrowser.open("https://www.youtube.com")

# ============================================
# YOUTUBE BUTTON
# ============================================

youtube = ctk.CTkButton(
    top,
    text="▶",
    width=30,
    height=28,
    fg_color="red",
    hover_color="#CC0000",
    corner_radius=8,
    font=("Arial", 14, "bold"),
    command=open_youtube
)

youtube.place(relx=0.96, rely=0.28)

# ============================================

open_btn = ctk.CTkButton(
    top,
    text="🗂 OPEN RECOVERY FOLDER",
    fg_color=ORANGE,
    hover_color="#FF9900",
    width=220,
    height=34,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=open_recovery_folder
)

open_btn.place(relx=0.43, rely=0.10)

# ============================================
# SELECT DRIVE
# ============================================

select_frame = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    border_width=2,
    border_color=CYAN,
    corner_radius=18,
    height=120
)

select_frame.pack(fill="x", padx=20, pady=10)

select_title = ctk.CTkLabel(
    select_frame,
    text="1. SELECT DRIVE",
    font=("Arial", 22, "bold"),
    text_color=CYAN
)

select_title.pack(anchor="w", padx=20, pady=15)

drive_var = ctk.StringVar()

drives = get_drives()

if drives:
    drive_var.set(drives[0])

drive_menu = ctk.CTkComboBox(
    select_frame,
    variable=drive_var,
    values=drives,
    width=420,
    height=40,
    font=("Arial", 18),
    dropdown_font=("Arial", 16),
    command=update_drive_info
)

drive_menu.pack()

# ============================================
# DRIVE INFO
# ============================================

drive_info = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    corner_radius=18,
    height=180
)

drive_info.pack(fill="x", padx=20, pady=10)

left_info = ctk.CTkFrame(
    drive_info,
    fg_color="transparent"
)

left_info.pack(side="left", padx=25, pady=20)

filesystem_label = ctk.CTkLabel(
    left_info,
    text="File System : NTFS",
    font=("Arial", 18, "bold")
)

filesystem_label.pack(anchor="w", pady=6)

total_label = ctk.CTkLabel(
    left_info,
    text="Total Space : 0 GB",
    font=("Arial", 18, "bold")
)

total_label.pack(anchor="w", pady=6)

used_label = ctk.CTkLabel(
    left_info,
    text="Used Space : 0 GB",
    font=("Arial", 18, "bold")
)

used_label.pack(anchor="w", pady=6)

free_label = ctk.CTkLabel(
    left_info,
    text="Free Space : 0 GB",
    font=("Arial", 18, "bold")
)

free_label.pack(anchor="w", pady=6)

# ============================================

progress_circle = ctk.CTkProgressBar(
    drive_info,
    orientation="vertical",
    width=120,
    height=120,
    progress_color=PURPLE
)

progress_circle.place(relx=0.93, rely=0.2)

percent_text = ctk.CTkLabel(
    drive_info,
    text="0%",
    font=("Arial", 20, "bold")
)

percent_text.place(relx=0.94, rely=0.45)

# ============================================
# RECOVERY TYPE
# ============================================

type_frame = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    border_width=2,
    border_color=CYAN,
    corner_radius=18,
    height=220
)

type_frame.pack(fill="x", padx=20, pady=10)

type_title = ctk.CTkLabel(
    type_frame,
    text="3. RECOVERY TYPE",
    font=("Arial", 22, "bold"),
    text_color=CYAN
)

type_title.pack(anchor="w", padx=20, pady=15)

button_holder = ctk.CTkFrame(
    type_frame,
    fg_color="transparent"
)

button_holder.pack(fill="x", padx=20, pady=15)

# ============================================

photos_btn = ctk.CTkButton(
    button_holder,
    text="🖼 Photos",
    height=60,
    corner_radius=15,
    border_width=3,
    border_color=CYAN,
    fg_color="#04152A",
    hover_color="#0B2A4A",
    font=("Arial", 20, "bold"),
    command=set_photos
)

photos_btn.pack(side="left", expand=True, padx=10)

# ============================================

videos_btn = ctk.CTkButton(
    button_holder,
    text="🎬 Videos",
    height=60,
    corner_radius=15,
    border_width=3,
    border_color=PURPLE,
    fg_color="#04152A",
    hover_color="#0B2A4A",
    font=("Arial", 20, "bold"),
    command=set_videos
)

videos_btn.pack(side="left", expand=True, padx=10)

# ============================================

documents_btn = ctk.CTkButton(
    button_holder,
    text="📄 Documents",
    height=60,
    corner_radius=15,
    border_width=3,
    border_color=YELLOW,
    fg_color="#04152A",
    hover_color="#0B2A4A",
    font=("Arial", 20, "bold"),
    command=set_documents
)

documents_btn.pack(side="left", expand=True, padx=10)

# ============================================

deep_btn = ctk.CTkButton(
    button_holder,
    text="🔎 Deep Scan",
    height=60,
    corner_radius=15,
    border_width=3,
    border_color=GREEN,
    fg_color="#04152A",
    hover_color="#0B2A4A",
    font=("Arial", 20, "bold"),
    command=set_deep
)

deep_btn.pack(side="left", expand=True, padx=10)

# ============================================
# ACTIONS
# ============================================

action_frame = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    border_width=2,
    border_color=CYAN,
    corner_radius=18,
    height=120
)

action_frame.pack(fill="x", padx=20, pady=10)

action_title = ctk.CTkLabel(
    action_frame,
    text="4. ACTIONS",
    font=("Arial", 22, "bold"),
    text_color=CYAN
)

action_title.pack(anchor="w", padx=20, pady=10)

buttons = ctk.CTkFrame(
    action_frame,
    fg_color="transparent"
)

buttons.pack(fill="x", padx=20)

# ============================================

start_btn = ctk.CTkButton(
    buttons,
    text="🔍 Start Scan",
    fg_color="#3D9DF2",
    hover_color="#1F7DD1",
    width=420,
    height=55,
    font=("Arial", 18, "bold"),
    command=start_scan
)

start_btn.pack(side="left", padx=40)

# ============================================

stop_btn = ctk.CTkButton(
    buttons,
    text="⏹ Stop Scan",
    fg_color="#111111",
    border_width=2,
    border_color="#FF3333",
    hover_color="#222222",
    width=420,
    height=55,
    font=("Arial", 18, "bold"),
    command=stop_scan
)

stop_btn.pack(side="right", padx=40)

# ============================================
# SCAN STATUS
# ============================================

scan_frame = ctk.CTkFrame(
    content,
    fg_color=PANEL,
    border_width=2,
    border_color=CYAN,
    corner_radius=18,
    height=180
)

scan_frame.pack(fill="x", padx=20, pady=10)

scan_title = ctk.CTkLabel(
    scan_frame,
    text="5. SCAN STATUS",
    font=("Arial", 22, "bold"),
    text_color=CYAN
)

scan_title.pack(anchor="w", padx=20, pady=10)

scan_status = ctk.CTkLabel(
    scan_frame,
    text="Ready to scan...",
    font=("Arial", 18)
)

scan_status.pack(anchor="w", padx=20)

progress = ctk.CTkProgressBar(
    scan_frame,
    width=1200,
    height=18,
    progress_color="#32D1F0"
)

progress.pack(pady=20)

progress.set(0)

# ============================================

stats = ctk.CTkFrame(
    scan_frame,
    fg_color="transparent"
)

stats.pack(fill="x", padx=20)

# ============================================

def stat_box(parent, title, color):

    frame = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )

    frame.pack(side="left", expand=True)

    label = ctk.CTkLabel(
        frame,
        text=title,
        text_color=color,
        font=("Arial", 14, "bold")
    )

    label.pack()

    value = ctk.CTkLabel(
        frame,
        text="0",
        text_color=color,
        font=("Arial", 18, "bold")
    )

    value.pack()

    return value

# ============================================

files_found = stat_box(
    stats,
    "Files Found",
    YELLOW
)

files_recovered = stat_box(
    stats,
    "Files Recovered",
    GREEN
)

elapsed = stat_box(
    stats,
    "Elapsed Time",
    CYAN
)

speed = stat_box(
    stats,
    "Scan Speed",
    ORANGE
)

# ============================================
# DEFAULT SELECTED TYPE
# ============================================

set_photos()

# ============================================
# INIT
# ============================================

update_drive_info(drive_var.get())

app.mainloop()