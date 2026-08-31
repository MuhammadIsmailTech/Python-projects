import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import csv
from PIL import Image, ImageTk
import datetime

# ==================== COLOR SCHEME ==================== #
COLORS = {
    "primary": "#4F46E5",
    "primary_dark": "#3730A3",
    "primary_light": "#818CF8",
    "accent": "#06B6D4",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg_dark": "#1E1B4B",
    "bg_medium": "#312E81",
    "bg_light": "#F8FAFC",
    "bg_white": "#FFFFFF",
    "text_dark": "#1E293B",
    "text_medium": "#475569",
    "text_light": "#94A3B8",
    "text_white": "#FFFFFF",
    "border": "#E2E8F0",
    "card_shadow": "#CBD5E1",
    "hover": "#EEF2FF",
    "table_header": "#4F46E5",
    "table_row_alt": "#F1F5F9",
    "input_bg": "#F8FAFC",
    "input_border": "#CBD5E1",
    "input_focus": "#818CF8",
    "scrollbar_bg": "#312E81",
    "scrollbar_trough": "#1E1B4B",
}

# ==================== ICONS (Unicode) ==================== #
ICONS = {
    "add": "➕", "search": "🔍", "update": "✏️", "delete": "🗑️",
    "show": "📋", "export": "📄", "total": "📊", "user": "👤",
    "lock": "🔒", "login": "🚀", "save": "💾", "clear": "🧹",
    "photo": "📷", "close": "✖", "dashboard": "🏠", "student": "🎓",
    "email": "📧", "phone": "📱", "book": "📚", "award": "🏆",
}


# ==================== DATABASE FUNCTION ==================== #
def db_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="mysql@9295",
        database="school1"
    )


# ==================== CUSTOM WIDGETS ==================== #
class ModernButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, bg=COLORS["primary"],
                 fg=COLORS["text_white"], font=("Segoe UI", 10, "bold"),
                 width=200, height=40, corner_radius=10, icon="", **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent.cget("bg") if parent.cget("bg") != "" else COLORS["bg_dark"],
                         highlightthickness=0, cursor="hand2", **kwargs)
        self.command, self.bg_color, self.fg_color = command, bg, fg
        self.hover_color = self._lighten_color(bg, 20)
        self.text, self.icon, self.corner_radius = text, icon, corner_radius
        self.font, self.width, self.height = font, width, height
        self.is_hovered = False
        self._draw_button()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _lighten_color(self, hex_color, percent):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = [min(255, int(c + (255 - c) * percent / 100)) for c in (r, g, b)]
        return f"#{r:02x}{g:02x}{b:02x}"

    def _darken_color(self, hex_color, percent):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = [max(0, int(c * (1 - percent / 100))) for c in (r, g, b)]
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius,y1, x2-radius,y1, x2,y1, x2,y1+radius,
                  x2,y2-radius, x2,y2, x2-radius,y2, x1+radius,y2,
                  x1,y2, x1,y2-radius, x1,y1+radius, x1,y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw_button(self):
        self.delete("all")
        color = self.hover_color if self.is_hovered else self.bg_color
        self._draw_rounded_rect(2, 2, self.width+2, self.height+2, self.corner_radius, 
                                fill=self._darken_color(self.bg_color, 15), outline="")
        self._draw_rounded_rect(0, 0, self.width, self.height, self.corner_radius, 
                                fill=color, outline="")
        display_text = f"{self.icon}  {self.text}" if self.icon else self.text
        self.create_text(self.width/2, self.height/2, text=display_text, 
                         fill=self.fg_color, font=self.font)

    def _on_enter(self, event): self.is_hovered = True; self._draw_button()
    def _on_leave(self, event): self.is_hovered = False; self._draw_button()
    def _on_click(self, event):
        if self.command: self.command()


class ModernEntry(tk.Frame):
    def __init__(self, parent, label="", icon="", placeholder="", **kwargs):
        super().__init__(parent, bg=COLORS["bg_white"])
        self.placeholder, self.has_placeholder = placeholder, False
        self.show_char = ""

        if label:
            tk.Label(self, text=label, font=("Segoe UI", 10, "bold"),
                     fg=COLORS["text_dark"], bg=COLORS["bg_white"], anchor="w").pack(fill="x", pady=(8, 2))

        self.entry_frame = tk.Frame(self, bg=COLORS["input_border"], padx=1, pady=1)
        self.entry_frame.pack(fill="x")

        if icon:
            tk.Label(self.entry_frame, text=icon, font=("Segoe UI", 12),
                     fg=COLORS["text_light"], bg=COLORS["input_bg"], width=3).pack(side="left", fill="y")

        entry_kwargs = {"font": ("Segoe UI", 11), "fg": COLORS["text_dark"], "bg": COLORS["input_bg"],
                        "relief": "flat", "insertbackground": COLORS["primary"], 
                        "selectbackground": COLORS["primary_light"]}
        
        # FIX 1: Extract 'show' character safely for passwords
        if "show" in kwargs:
            self.show_char = kwargs.pop("show")
        
        self.entry = tk.Entry(self.entry_frame, **entry_kwargs)
        self.entry.pack(side="left", fill="both", expand=True, ipady=8, padx=(5, 10))

        # FIX 1: Handle placeholder text securely
        if placeholder:
            # Temporarily remove '*' so the placeholder text is readable, not '********'
            if self.show_char:
                self.entry.config(show="")
            self.entry.insert(0, placeholder)
            self.entry.config(fg=COLORS["text_light"])
            self.has_placeholder = True
            self.entry.bind("<FocusIn>", self._on_focus_in)
            self.entry.bind("<FocusOut>", self._on_focus_out)
        else:
            self.entry.bind("<FocusIn>", lambda e: self.entry_frame.config(bg=COLORS["input_focus"]))
            self.entry.bind("<FocusOut>", lambda e: self.entry_frame.config(bg=COLORS["input_border"]))

    def _on_focus_in(self, event):
        if self.has_placeholder and self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS["text_dark"])
            # Restore the '*' mask once they start typing
            if self.show_char:
                self.entry.config(show=self.show_char)
            self.has_placeholder = False
        self.entry_frame.config(bg=COLORS["input_focus"])

    def _on_focus_out(self, event):
        if self.placeholder and self.entry.get() == "":
            # Remove '*' mask to show placeholder text again
            if self.show_char:
                self.entry.config(show="")
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=COLORS["text_light"])
            self.has_placeholder = True
        self.entry_frame.config(bg=COLORS["input_border"])

    def get(self):
        if self.has_placeholder and self.entry.get() == self.placeholder:
            return ""
        return self.entry.get()

    def delete(self, start, end):
        self.entry.delete(start, end)


class StatCard(tk.Frame):
    def __init__(self, parent, title="", value="", icon="", color=COLORS["primary"], **kwargs):
        super().__init__(parent, bg=COLORS["bg_white"], highlightthickness=0, **kwargs)
        self.config(padx=15, pady=15)
        icon_frame = tk.Frame(self, bg=color, width=50, height=50)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text=icon, font=("Segoe UI", 20), bg=color, fg=COLORS["text_white"]).place(relx=0.5, rely=0.5, anchor="center")
        self.value_label = tk.Label(self, text=value, font=("Segoe UI", 24, "bold"), fg=COLORS["text_dark"], bg=COLORS["bg_white"])
        self.value_label.pack(anchor="w", pady=(10, 0))
        tk.Label(self, text=title, font=("Segoe UI", 11), fg=COLORS["text_medium"], bg=COLORS["bg_white"]).pack(anchor="w")

    def set_value(self, text):
        self.value_label.config(text=text)


# ==================== LOGIN WINDOW ==================== #
class ModernLoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Student Management System - Login")
        self.window.geometry("500x600")
        self.window.configure(bg=COLORS["bg_light"])
        self.window.resizable(False, False)
        x = (self.window.winfo_screenwidth() // 2) - 250
        y = (self.window.winfo_screenheight() // 2) - 300
        self.window.geometry(f"500x600+{x}+{y}")
        self._build_ui()

    def _build_ui(self):
        main_frame = tk.Frame(self.window, bg=COLORS["bg_light"])
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        logo_frame = tk.Frame(main_frame, bg=COLORS["primary"], width=80, height=80)
        logo_frame.pack(pady=(20, 15))
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text=ICONS["student"], font=("Segoe UI", 36), bg=COLORS["primary"], fg=COLORS["text_white"]).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="Welcome Back", font=("Segoe UI", 26, "bold"), fg=COLORS["text_dark"], bg=COLORS["bg_light"]).pack(pady=(5, 0))
        tk.Label(main_frame, text="Sign in to continue to Student Management System", font=("Segoe UI", 11), fg=COLORS["text_medium"], bg=COLORS["bg_light"]).pack(pady=(5, 30))

        card = tk.Frame(main_frame, bg=COLORS["bg_white"], highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", pady=(0, 20), ipady=10)
        card_inner = tk.Frame(card, bg=COLORS["bg_white"])
        card_inner.pack(fill="x", padx=25, pady=20)

        self.user_entry = ModernEntry(card_inner, label="Username", icon=ICONS["user"], placeholder="Enter your username")
        self.user_entry.pack(fill="x", pady=(0, 10))

        self.pass_entry = ModernEntry(card_inner, label="Password", icon=ICONS["lock"], placeholder="Enter your password", show="*")
        self.pass_entry.pack(fill="x", pady=(0, 20))

        ModernButton(card_inner, text="Sign In", command=self.login, bg=COLORS["primary"], width=450, height=45, icon=ICONS["login"]).pack(pady=(5, 10))
        tk.Label(main_frame, text="© 2024 Student Management System", font=("Segoe UI", 9), fg=COLORS["text_light"], bg=COLORS["bg_light"]).pack(side="bottom", pady=10)

    def login(self):
        if self.user_entry.get() == "admin" and self.pass_entry.get() == "1234":
            self.window.destroy()
            root = tk.Tk()
            app = StudentSystem(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.\nPlease try again.")

    def run(self):
        self.window.mainloop()


# ==================== MODERN POPUP WINDOW ==================== #
class ModernPopup:
    def __init__(self, parent, title="", width=450, height=550, icon=""):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.window.configure(bg=COLORS["bg_light"])
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        header = tk.Frame(self.window, bg=COLORS["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f" {icon}  {title}", font=("Segoe UI", 14, "bold"), fg=COLORS["text_white"], bg=COLORS["primary"]).pack(side="left", padx=15)
        
        close_btn = tk.Label(header, text="✕", font=("Segoe UI", 14), fg=COLORS["text_white"], bg=COLORS["primary"], cursor="hand2")
        close_btn.pack(side="right", padx=15)
        close_btn.bind("<Button-1>", lambda e: self.window.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=COLORS["danger"]))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=COLORS["text_white"]))

        self.content = tk.Frame(self.window, bg=COLORS["bg_white"])
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

    def add_entry(self, label, icon="", row=0, placeholder=""):
        entry = ModernEntry(self.content, label=label, icon=icon, placeholder=placeholder)
        entry.grid(row=row, column=0, sticky="ew", pady=2)
        self.content.grid_columnconfigure(0, weight=1)
        return entry


# ==================== MAIN SYSTEM ==================== #
class StudentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg=COLORS["bg_light"])
        self.root.minsize(1100, 650)
        x = (self.root.winfo_screenwidth() // 2) - 650
        y = (self.root.winfo_screenheight() // 2) - 375
        self.root.geometry(f"1300x750+{x}+{y}")
        self._configure_styles()
        self._build_ui()
        self.show_all()
        self._update_stats()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Modern.Treeview", background=COLORS["bg_white"], foreground=COLORS["text_dark"],
                        fieldbackground=COLORS["bg_white"], font=("Segoe UI", 10), rowheight=40, borderwidth=0)
        style.configure("Modern.Treeview.Heading", background=COLORS["table_header"], foreground=COLORS["text_white"],
                        font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
        style.map("Modern.Treeview", background=[("selected", COLORS["primary_light"])], foreground=[("selected", COLORS["text_white"])])
        style.map("Modern.Treeview.Heading", background=[("active", COLORS["primary_dark"])])
        style.configure("Sidebar.Vertical.TScrollbar", background=COLORS["scrollbar_bg"], troughcolor=COLORS["scrollbar_trough"], arrowcolor=COLORS["text_white"], borderwidth=0)

    def _build_ui(self):
        # ==================== SIDEBAR ==================== #
        self.sidebar = tk.Frame(self.root, bg=COLORS["bg_dark"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # FIX 2: Pack footer FIRST so it stays strictly at the bottom
        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(side="bottom", fill="x")
        footer = tk.Frame(self.sidebar, bg=COLORS["bg_dark"], height=50)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        tk.Label(footer, text="👤  Admin", font=("Segoe UI", 10), fg=COLORS["text_light"], bg=COLORS["bg_dark"]).pack(side="left", padx=20, pady=15)
        tk.Label(footer, text="v2.0", font=("Segoe UI", 9), fg=COLORS["text_light"], bg=COLORS["bg_dark"]).pack(side="right", padx=20, pady=15)

        # Pack Logo SECOND at the top
        logo_container = tk.Frame(self.sidebar, bg=COLORS["primary"], height=70)
        logo_container.pack(fill="x")
        logo_container.pack_propagate(False)
        tk.Label(logo_container, text=f"{ICONS['student']}  SMS", font=("Segoe UI", 20, "bold"), fg=COLORS["text_white"], bg=COLORS["primary"]).pack(side="left", padx=20)

        # Pack Nav Label THIRD
        tk.Label(self.sidebar, text="NAVIGATION", font=("Segoe UI", 9, "bold"), fg=COLORS["text_light"], bg=COLORS["bg_dark"]).pack(anchor="w", padx=20, pady=(20, 10))

        # FIX 2: Pack Scroll Container LAST to take up remaining middle space
        scroll_container = tk.Frame(self.sidebar, bg=COLORS["bg_dark"])
        scroll_container.pack(fill="both", expand=True)

        self.sidebar_canvas = tk.Canvas(scroll_container, bg=COLORS["bg_dark"], highlightthickness=0, bd=0)
        self.sidebar_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.sidebar_canvas.yview, style="Sidebar.Vertical.TScrollbar")
        
        self.scrollable_sidebar = tk.Frame(self.sidebar_canvas, bg=COLORS["bg_dark"])
        self.scrollable_sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all")))
        
        self.sidebar_canvas.create_window((0, 0), window=self.scrollable_sidebar, anchor="nw", width=230)
        
        self.sidebar_scrollbar.pack(side="right", fill="y")
        self.sidebar_canvas.pack(side="left", fill="both", expand=True)

        # FIX 2: Bind mousewheel to the scrollable frame (not the canvas), so hovering over buttons keeps it active
        def _on_mousewheel(event):
            self.sidebar_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event):
            self.sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            self.sidebar_canvas.unbind_all("<MouseWheel>")

        self.scrollable_sidebar.bind("<Enter>", _bind_to_mousewheel)
        self.scrollable_sidebar.bind("<Leave>", _unbind_from_mousewheel)

        # Navigation Buttons
        nav_buttons = [
            (f"  {ICONS['dashboard']}    Dashboard", self._show_dashboard, COLORS["accent"]),
            (f"  {ICONS['add']}    Add Student", self.add_student, COLORS["success"]),
            (f"  {ICONS['search']}    Search Student", self.search_student, COLORS["primary_light"]),
            (f"  {ICONS['update']}    Update Student", self.update_student, COLORS["warning"]),
            (f"  {ICONS['delete']}    Delete Student", self.delete_student, COLORS["danger"]),
            (f"  {ICONS['show']}    Show All Students", self.show_all, COLORS["primary"]),
            (f"  {ICONS['export']}    Export to CSV", self.export_csv, COLORS["accent"]),
            (f"  {ICONS['total']}    Total Students", self.total_students, COLORS["success"]),
        ]

        for text, command, color in nav_buttons:
            btn_frame = tk.Frame(self.scrollable_sidebar, bg=COLORS["bg_dark"], cursor="hand2")
            btn_frame.pack(fill="x", padx=10, pady=2)
            indicator = tk.Frame(btn_frame, bg=color, width=4, height=0)
            indicator.place(x=0, y=5, relheight=0.8)
            label = tk.Label(btn_frame, text=text, font=("Segoe UI", 11), fg=COLORS["text_light"], bg=COLORS["bg_dark"], anchor="w", padx=15, pady=10)
            label.pack(fill="x")

            def make_hover_handlers(f, l, ind, cmd):
                def on_enter(e): f.config(bg=COLORS["bg_medium"]); l.config(fg=COLORS["text_white"]); ind.place(height=30)
                def on_leave(e): f.config(bg=COLORS["bg_dark"]); l.config(fg=COLORS["text_light"]); ind.place(height=0)
                def on_click(e): cmd()
                return on_enter, on_leave, on_click

            on_enter, on_leave, on_click = make_hover_handlers(btn_frame, label, indicator, command)
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", on_click)

        # ==================== MAIN CONTENT ==================== #
        self.main_content = tk.Frame(self.root, bg=COLORS["bg_light"])
        self.main_content.pack(side="right", fill="both", expand=True)

        top_bar = tk.Frame(self.main_content, bg=COLORS["bg_white"], height=65)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        tk.Label(top_bar, text="Student Management System", font=("Segoe UI", 16, "bold"), fg=COLORS["text_dark"], bg=COLORS["bg_white"]).pack(side="left", padx=25)
        
        self.time_label = tk.Label(top_bar, text=datetime.datetime.now().strftime("%A, %B %d, %Y"), font=("Segoe UI", 10), fg=COLORS["text_medium"], bg=COLORS["bg_white"])
        self.time_label.pack(side="right", padx=25)
        self._update_time()

        tk.Frame(self.main_content, bg=COLORS["border"], height=1).pack(fill="x")

        # Dashboard Stats
        self.stats_frame = tk.Frame(self.main_content, bg=COLORS["bg_light"])
        self.stats_frame.pack(fill="x", padx=25, pady=15)

        self.stat_total = StatCard(self.stats_frame, "Total Students", "0", ICONS["student"], COLORS["primary"])
        self.stat_total.grid(row=0, column=0, padx=(0, 15), sticky="nsew")
        self.stat_subjects = StatCard(self.stats_frame, "Subjects", "0", ICONS["book"], COLORS["accent"])
        self.stat_subjects.grid(row=0, column=1, padx=(0, 15), sticky="nsew")
        self.stat_grade_a = StatCard(self.stats_frame, "Grade A+", "0", ICONS["award"], COLORS["success"])
        self.stat_grade_a.grid(row=0, column=2, padx=(0, 15), sticky="nsew")
        self.stat_recent = StatCard(self.stats_frame, "Recent Added", "0", ICONS["add"], COLORS["warning"])
        self.stat_recent.grid(row=0, column=3, sticky="nsew")
        for i in range(4): self.stats_frame.grid_columnconfigure(i, weight=1)

        # Table Area
        table_card = tk.Frame(self.main_content, bg=COLORS["bg_white"], highlightthickness=1, highlightbackground=COLORS["border"])
        table_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        table_header = tk.Frame(table_card, bg=COLORS["bg_white"])
        table_header.pack(fill="x", padx=20, pady=(15, 10))
        tk.Label(table_header, text=f"{ICONS['show']}  Student Records", font=("Segoe UI", 13, "bold"), fg=COLORS["text_dark"], bg=COLORS["bg_white"]).pack(side="left")
        self.count_label = tk.Label(table_header, text="0 records", font=("Segoe UI", 10), fg=COLORS["text_medium"], bg=COLORS["bg_white"])
        self.count_label.pack(side="right")
        tk.Frame(table_card, bg=COLORS["border"], height=1).pack(fill="x", padx=20)

        tree_frame = tk.Frame(table_card, bg=COLORS["bg_white"])
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.table = ttk.Treeview(tree_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, style="Modern.Treeview",
                                  columns=("roll", "name", "fname", "sub", "grade", "email", "phone", "photo"), selectmode="browse")
        scroll_y.config(command=self.table.yview)
        scroll_x.config(command=self.table.xview)

        columns_config = {"roll": ("Roll No", 80), "name": ("Full Name", 150), "fname": ("Father's Name", 150), "sub": ("Subject", 120), "grade": ("Grade", 80), "email": ("Email", 180), "phone": ("Phone", 130), "photo": ("Photo Path", 150)}
        for col, (heading, width) in columns_config.items():
            self.table.heading(col, text=heading)
            self.table.column(col, width=width, minwidth=60, anchor="center")
        self.table["show"] = "headings"
        self.table.pack(fill="both", expand=True)
        self.table.tag_configure("oddrow", background=COLORS["table_row_alt"])
        self.table.tag_configure("evenrow", background=COLORS["bg_white"])

        # Status Bar
        self.status_bar = tk.Frame(self.main_content, bg=COLORS["bg_dark"], height=35)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        self.status_label = tk.Label(self.status_bar, text="  Ready", font=("Segoe UI", 9), fg=COLORS["text_light"], bg=COLORS["bg_dark"], anchor="w")
        self.status_label.pack(side="left", padx=10, fill="y")
        tk.Label(self.status_bar, text="Connected to Database  ", font=("Segoe UI", 9), fg=COLORS["success"], bg=COLORS["bg_dark"]).pack(side="right", padx=10)

    def _update_time(self):
        try:
            self.time_label.config(text=datetime.datetime.now().strftime("%A, %B %d, %Y  %I:%M %p"))
            self.root.after(60000, self._update_time)
        except: pass

    def _update_stats(self):
        try:
            con = db_connect(); cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM student"); total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(DISTINCT sub) FROM student"); subjects = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM student WHERE grade='A+'"); grade_a = cur.fetchone()[0]
            con.close()
            self.stat_total.set_value(str(total)); self.stat_subjects.set_value(str(subjects))
            self.stat_grade_a.set_value(str(grade_a)); self.stat_recent.set_value(str(min(total, 5)))
        except Exception as e: print(f"Stats error: {e}")

    def _set_status(self, message, color=COLORS["text_light"]): self.status_label.config(text=f"  {message}", fg=color)
    def _show_dashboard(self): self._update_stats(); self.show_all(); self._set_status("Dashboard loaded", COLORS["success"])

    # ==================== ADD STUDENT ==================== #
    def add_student(self):
        self._set_status("Opening Add Student form...")
        popup = ModernPopup(self.root, "Add New Student", 480, 620, ICONS["add"])
        entries = {}
        fields = [("Roll No", ICONS["student"], "Enter roll number"), ("Full Name", ICONS["user"], "Enter student name"), ("Father's Name", ICONS["user"], "Enter father's name"), ("Subject", ICONS["book"], "Enter subject"), ("Grade", ICONS["award"], "Enter grade (A+, A, B, C)"), ("Email", ICONS["email"], "Enter email address"), ("Phone", ICONS["phone"], "Enter phone number")]
        for i, (label, icon, placeholder) in enumerate(fields): entries[label] = popup.add_entry(label, icon, i, placeholder)

        photo_frame = tk.Frame(popup.content, bg=COLORS["bg_white"])
        photo_frame.grid(row=7, column=0, sticky="ew", pady=10)
        photo_path = {"value": ""}
        def upload_photo():
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
            if path: photo_path["value"] = path; photo_status.config(text="Photo selected ✓", fg=COLORS["success"])
        ModernButton(photo_frame, text="Upload Photo", command=upload_photo, bg=COLORS["accent"], width=200, height=38, icon=ICONS["photo"]).pack(side="left")
        photo_status = tk.Label(photo_frame, text="No photo selected", font=("Segoe UI", 9), fg=COLORS["text_light"], bg=COLORS["bg_white"])
        photo_status.pack(side="left", padx=15)

        def save():
            data = [entries[f].get() for f in entries.keys()]
            if "" in data: messagebox.showerror("Error", "Please fill all fields!", parent=popup.window); return
            try:
                con = db_connect(); cur = con.cursor()
                cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (*data, photo_path["value"]))
                con.commit(); con.close()
                messagebox.showinfo("Success", "Student added successfully!", parent=popup.window)
                popup.window.destroy(); self.show_all(); self._update_stats(); self._set_status("Student added successfully", COLORS["success"])
            except Exception as e: messagebox.showerror("Database Error", str(e), parent=popup.window)

        def clear():
            for e in entries.values(): e.delete(0, tk.END)
            photo_path["value"] = ""; photo_status.config(text="No photo selected", fg=COLORS["text_light"])

        btn_frame = tk.Frame(popup.content, bg=COLORS["bg_white"])
        btn_frame.grid(row=8, column=0, sticky="ew")
        ModernButton(btn_frame, text="Save Student", command=save, bg=COLORS["success"], width=200, height=40, icon=ICONS["save"]).pack(side="left", padx=(0, 10))
        ModernButton(btn_frame, text="Clear", command=clear, bg=COLORS["text_medium"], width=200, height=40, icon=ICONS["clear"]).pack(side="left")

    # ==================== SHOW ALL ==================== #
    def show_all(self):
        self._set_status("Loading students...")
        try:
            con = db_connect(); cur = con.cursor(); cur.execute("SELECT * FROM student"); rows = cur.fetchall()
            self.table.delete(*self.table.get_children())
            for i, r in enumerate(rows): self.table.insert("", "end", values=r, tags=("oddrow" if i % 2 == 0 else "evenrow",))
            con.close(); self.count_label.config(text=f"{len(rows)} records"); self._set_status(f"Loaded {len(rows)} student records", COLORS["success"])
        except Exception as e: messagebox.showerror("Error", str(e)); self._set_status("Error loading data", COLORS["danger"])

    # ==================== SEARCH STUDENT ==================== #
    def search_student(self):
        self._set_status("Opening search...")
        popup = ModernPopup(self.root, "Search Student", 400, 280, ICONS["search"])
        search_entry = popup.add_entry("Student Name", ICONS["search"], 0, "Enter name to search...")
        def search():
            name = search_entry.get()
            if not name: messagebox.showwarning("Warning", "Please enter a name!", parent=popup.window); return
            try:
                con = db_connect(); cur = con.cursor(); cur.execute("SELECT * FROM student WHERE name LIKE %s", ('%' + name + '%',)); rows = cur.fetchall()
                self.table.delete(*self.table.get_children())
                for i, r in enumerate(rows): self.table.insert("", "end", values=r, tags=("oddrow" if i % 2 == 0 else "evenrow",))
                con.close(); self.count_label.config(text=f"{len(rows)} records found"); popup.window.destroy()
                self._set_status(f"Found {len(rows)} students matching '{name}'", COLORS["success"])
                if len(rows) == 0: messagebox.showinfo("Search", "No students found!", parent=self.root)
            except Exception as e: messagebox.showerror("Error", str(e), parent=popup.window)
        ModernButton(popup.content, text="Search", command=search, bg=COLORS["primary"], width=380, height=42, icon=ICONS["search"]).grid(row=1, column=0, pady=20)

    # ==================== UPDATE STUDENT ==================== #
    def update_student(self):
        self._set_status("Opening update form...")
        popup = ModernPopup(self.root, "Update Student", 400, 350, ICONS["update"])
        roll_entry = popup.add_entry("Roll Number", ICONS["student"], 0, "Enter roll number")
        grade_entry = popup.add_entry("New Grade", ICONS["award"], 1, "Enter new grade")
        def update():
            roll, grade = roll_entry.get(), grade_entry.get()
            if not roll or not grade: messagebox.showwarning("Warning", "Please fill all fields!", parent=popup.window); return
            try:
                con = db_connect(); cur = con.cursor(); cur.execute("UPDATE student SET grade=%s WHERE rollNo=%s", (grade, roll))
                if cur.rowcount == 0: messagebox.showwarning("Not Found", "No student with that roll number!", parent=popup.window); con.close(); return
                con.commit(); con.close(); messagebox.showinfo("Success", "Student updated successfully!", parent=popup.window)
                popup.window.destroy(); self.show_all(); self._update_stats(); self._set_status("Student record updated", COLORS["success"])
            except Exception as e: messagebox.showerror("Error", str(e), parent=popup.window)
        ModernButton(popup.content, text="Update Record", command=update, bg=COLORS["warning"], width=380, height=42, icon=ICONS["update"]).grid(row=2, column=0, pady=20)

    # ==================== DELETE STUDENT ==================== #
    def delete_student(self):
        self._set_status("Opening delete form...")
        popup = ModernPopup(self.root, "Delete Student", 400, 300, ICONS["delete"])
        roll_entry = popup.add_entry("Roll Number", ICONS["student"], 0, "Enter roll number to delete")
        def delete():
            roll = roll_entry.get()
            if not roll: messagebox.showwarning("Warning", "Please enter a roll number!", parent=popup.window); return
            if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with Roll No: {roll}?", parent=popup.window): return
            try:
                con = db_connect(); cur = con.cursor(); cur.execute("DELETE FROM student WHERE rollNo=%s", (roll,))
                if cur.rowcount == 0: messagebox.showwarning("Not Found", "No student with that roll number!", parent=popup.window); con.close(); return
                con.commit(); con.close(); messagebox.showinfo("Deleted", "Student removed successfully!", parent=popup.window)
                popup.window.destroy(); self.show_all(); self._update_stats(); self._set_status("Student deleted", COLORS["warning"])
            except Exception as e: messagebox.showerror("Error", str(e), parent=popup.window)
        ModernButton(popup.content, text="Delete Student", command=delete, bg=COLORS["danger"], width=380, height=42, icon=ICONS["delete"]).grid(row=1, column=0, pady=20)

    # ==================== EXPORT CSV ==================== #
    def export_csv(self):
        self._set_status("Exporting to CSV...")
        try:
            con = db_connect(); cur = con.cursor(); cur.execute("SELECT * FROM student"); rows = cur.fetchall()
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="students.csv")
            if file_path:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f); writer.writerow(["Roll", "Name", "Father", "Subject", "Grade", "Email", "Phone", "Photo"]); writer.writerows(rows)
                messagebox.showinfo("Exported", f"Data exported to:\n{file_path}"); self._set_status("CSV exported successfully", COLORS["success"])
            else: self._set_status("Export cancelled", COLORS["text_light"])
            con.close()
        except Exception as e: messagebox.showerror("Error", str(e)); self._set_status("Export failed", COLORS["danger"])

    # ==================== TOTAL STUDENTS ==================== #
    def total_students(self):
        self._set_status("Calculating total students...")
        try:
            con = db_connect(); cur = con.cursor(); cur.execute("SELECT COUNT(*) FROM student"); total = cur.fetchone()[0]
            cur.execute("SELECT grade, COUNT(*) FROM student GROUP BY grade"); grade_dist = cur.fetchall(); con.close()
            popup = ModernPopup(self.root, "Student Statistics", 400, 400, ICONS["total"])
            tk.Label(popup.content, text=str(total), font=("Segoe UI", 48, "bold"), fg=COLORS["primary"], bg=COLORS["bg_white"]).pack(pady=(10, 0))
            tk.Label(popup.content, text="Total Students", font=("Segoe UI", 14), fg=COLORS["text_medium"], bg=COLORS["bg_white"]).pack(pady=(0, 20))
            tk.Frame(popup.content, bg=COLORS["border"], height=1).pack(fill="x", padx=20)
            tk.Label(popup.content, text="Grade Distribution", font=("Segoe UI", 12, "bold"), fg=COLORS["text_dark"], bg=COLORS["bg_white"]).pack(pady=(15, 10))
            for grade, count in grade_dist:
                row = tk.Frame(popup.content, bg=COLORS["bg_white"]); row.pack(fill="x", padx=30, pady=3)
                tk.Label(row, text=f"🏆  {grade}", font=("Segoe UI", 11), fg=COLORS["text_dark"], bg=COLORS["bg_white"]).pack(side="left")
                tk.Label(row, text=f"{count} students", font=("Segoe UI", 11), fg=COLORS["text_medium"], bg=COLORS["bg_white"]).pack(side="right")
            self._set_status(f"Total students: {total}", COLORS["success"])
        except Exception as e: messagebox.showerror("Error", str(e)); self._set_status("Error calculating total", COLORS["danger"])


if __name__ == "__main__":
    app = ModernLoginWindow()
    app.run()
