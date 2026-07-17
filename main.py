import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from ai_engine import SmartAIEngine

# =========================================================================
# THEME DEFINITIONS (Light, Dark, Moderate) - dark theme text is light
# =========================================================================
THEMES = {
    "Light": {
        "bg_main": "#FEF9F0",
        "bg_sidebar": "#FFFFFF",
        "bg_card": "#FFFFFF",
        "header": "#2D3E50",
        "accent": "#E67E22",
        "accent_dark": "#D35400",
        "secondary": "#3498DB",
        "danger": "#E74C3C",
        "text_primary": "#2C3E50",
        "text_secondary": "#7F8C8D",
        "border": "#E8E8E8",
        "hover": "#FDF2E9",
        "shadow": "#D5D8DC",
        "user_bubble": "#E67E22",
        "ai_bubble": "#34495E",
        "chat_bg": "#2C3E50",
        "chat_header": "#1A252F",
        "chat_entry_bg": "#34495E",
        "chat_entry_fg": "white",
        "listbox_bg": "#FAFAFA",
        "textbox_bg": "#FFFFFF",
        "entry_fg": "#2C3E50",
        "combobox_fg": "#2C3E50",
        "combobox_listbox_bg": "#FFFFFF",
        "combobox_listbox_fg": "#2C3E50"
    },
    "Dark": {
        "bg_main": "#1E1E2E",
        "bg_sidebar": "#2D2D3D",
        "bg_card": "#2D2D3D",
        "header": "#0F0F1A",
        "accent": "#F39C12",
        "accent_dark": "#E67E22",
        "secondary": "#3498DB",
        "danger": "#E74C3C",
        "text_primary": "#F0F0F0",      # Light text on dark background
        "text_secondary": "#B0B0C0",
        "border": "#3D3D4D",
        "hover": "#3D3D4D",
        "shadow": "#1A1A2A",
        "user_bubble": "#F39C12",
        "ai_bubble": "#3D3D5C",
        "chat_bg": "#1E1E2E",
        "chat_header": "#0F0F1A",
        "chat_entry_bg": "#2D2D3D",
        "chat_entry_fg": "white",
        "listbox_bg": "#2D2D3D",
        "textbox_bg": "#2D2D3D",
        "entry_fg": "#F0F0F0",
        "combobox_fg": "#F0F0F0",
        "combobox_listbox_bg": "#2D2D3D",
        "combobox_listbox_fg": "#F0F0F0"
    },
    "Moderate": {
        "bg_main": "#F0F4F8",
        "bg_sidebar": "#FFFFFF",
        "bg_card": "#FFFFFF",
        "header": "#1F4A5C",
        "accent": "#5D9B9B",
        "accent_dark": "#4A7C7C",
        "secondary": "#6C8B9E",
        "danger": "#C97B84",
        "text_primary": "#2E3B3B",
        "text_secondary": "#6A7E8A",
        "border": "#CFDDE6",
        "hover": "#E6F0F5",
        "shadow": "#BCCCD9",
        "user_bubble": "#5D9B9B",
        "ai_bubble": "#2E4A5C",
        "chat_bg": "#EAF0F5",
        "chat_header": "#1F4A5C",
        "chat_entry_bg": "#FFFFFF",
        "chat_entry_fg": "#2E3B3B",
        "listbox_bg": "#FAFAFA",
        "textbox_bg": "#FFFFFF",
        "entry_fg": "#2E3B3B",
        "combobox_fg": "#2E3B3B",
        "combobox_listbox_bg": "#FFFFFF",
        "combobox_listbox_fg": "#2E3B3B"
    }
}

# =========================================================================
# DSA DEFINITIONS
# =========================================================================
class StepsNode:
    def __init__(self, step_text):
        self.step_text = step_text
        self.next = None

class RequestQueue:
    def __init__(self):
        self.container = deque()
    def enqueue(self, task_name):
        self.container.append(task_name)
    def dequeue(self):
        return self.container.popleft() if self.container else None
    def get_all(self):
        return list(self.container)

class NavigationStack:
    def __init__(self):
        self.items = []
    def push(self, recipe_dict):
        if not self.items or self.items[-1]["name"] != recipe_dict["name"]:
            self.items.append(recipe_dict)
    def pop(self):
        return self.items.pop() if len(self.items) > 1 else None

# =========================================================================
# MAIN APPLICATION
# =========================================================================
class ModernRecipeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DISH DASH 🍛")
        self.root.geometry("1150x880")
        
        self.ai = SmartAIEngine()
        self.nav_stack = NavigationStack()
        self.req_queue = RequestQueue()
        
        self.current_recipe_node = None
        self.current_step_index = 1
        
        # Fonts (cross-platform)
        self.default_font = ("Helvetica", 10)
        self.bold_font = ("Helvetica", 10, "bold")
        self.title_font = ("Helvetica", 16, "bold")
        self.heading_font = ("Helvetica", 11, "bold")
        
        self.current_theme = "Light"
        self.theme_vars = THEMES[self.current_theme]
        
        self._apply_theme()
        self._setup_styles()
        self._create_layout()
        self._log_system_request("System Core Application Started")
    
    def _apply_theme(self):
        self.root.configure(bg=self.theme_vars["bg_main"])
    
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure base styles
        style.configure("Card.TFrame", background=self.theme_vars["bg_card"], relief="flat", borderwidth=0)
        style.configure("Sidebar.TFrame", background=self.theme_vars["bg_sidebar"], relief="flat")
        style.configure("Header.TFrame", background=self.theme_vars["header"])
        
        # Button styles
        style.configure("Accent.TButton", background=self.theme_vars["accent"], foreground="white",
                        borderwidth=0, focusthickness=0, padding=(14, 8), font=self.bold_font)
        style.map("Accent.TButton", background=[("active", self.theme_vars["accent_dark"])])
        
        style.configure("Secondary.TButton", background=self.theme_vars["secondary"], foreground="white",
                        borderwidth=0, padding=(14, 8), font=self.bold_font)
        style.map("Secondary.TButton", background=[("active", "#2980B9")])
        
        style.configure("Danger.TButton", background=self.theme_vars["danger"], foreground="white",
                        borderwidth=0, padding=(14, 8), font=self.bold_font)
        style.map("Danger.TButton", background=[("active", "#C0392B")])
        
        # Combobox style - entry field
        style.configure("TCombobox", fieldbackground=self.theme_vars["bg_card"],
                        background=self.theme_vars["bg_card"], foreground=self.theme_vars["combobox_fg"],
                        borderwidth=1, relief="solid", padding=6, font=self.default_font)
        
        # Combobox dropdown listbox style (for dark theme)
        style.map("TCombobox", 
                  fieldbackground=[("readonly", self.theme_vars["bg_card"])],
                  foreground=[("readonly", self.theme_vars["combobox_fg"])],
                  selectbackground=[("readonly", self.theme_vars["accent"])],
                  selectforeground=[("readonly", "white")])
        
        # Entry style
        style.configure("TEntry", fieldbackground=self.theme_vars["bg_card"],
                        foreground=self.theme_vars["entry_fg"], borderwidth=1, relief="solid",
                        padding=6, font=self.default_font)
        
        # Label styles
        style.configure("Title.TLabel", font=self.title_font, foreground=self.theme_vars["text_primary"])
        style.configure("Heading.TLabel", font=self.heading_font, foreground=self.theme_vars["text_primary"])
        style.configure("Muted.TLabel", foreground=self.theme_vars["text_secondary"])
        
        # Additional fix for combobox dropdown list - configure the listbox that appears
        self.root.option_add("*TCombobox*Listbox.background", self.theme_vars["combobox_listbox_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", self.theme_vars["combobox_listbox_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.theme_vars["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "white")
    
    def _create_layout(self):
        self.header_frame = tk.Frame(self.root, bg=self.theme_vars["header"], height=65)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        
        title_label = tk.Label(self.header_frame, text="🍛  DISH DASH 🍛",
                               fg="white", bg=self.theme_vars["header"], font=self.title_font)
        title_label.pack(side="left", padx=24, pady=18)
        
        subtitle = tk.Label(self.header_frame, text="Smart Recipe Recommendation System",
                            fg="#BDC3C7", bg=self.theme_vars["header"], font=self.default_font)
        subtitle.pack(side="left", padx=(5,0))
        
        theme_frame = tk.Frame(self.header_frame, bg=self.theme_vars["header"])
        theme_frame.pack(side="right", padx=20)
        tk.Label(theme_frame, text="Theme:", bg=self.theme_vars["header"], fg="white", font=self.default_font).pack(side="left")
        self.theme_combo = ttk.Combobox(theme_frame, values=["Light", "Dark", "Moderate"], state="readonly", width=10)
        self.theme_combo.set(self.current_theme)
        self.theme_combo.pack(side="left", padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self._change_theme)
        
        self.main_container = tk.Frame(self.root, bg=self.theme_vars["bg_main"])
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(16, 20))
        
        self.sidebar_shadow = tk.Frame(self.main_container, bg=self.theme_vars["shadow"], bd=0)
        self.sidebar_shadow.pack(side="left", fill="y", padx=(0, 16))
        self.sidebar = tk.Frame(self.sidebar_shadow, bg=self.theme_vars["bg_sidebar"], bd=0, highlightthickness=0)
        self.sidebar.pack(fill="both", expand=True, padx=(0,2), pady=2)
        
        content_bg = tk.Frame(self.main_container, bg=self.theme_vars["bg_main"])
        content_bg.pack(side="right", fill="both", expand=True)
        self.content_container = tk.Frame(content_bg, bg=self.theme_vars["bg_main"])
        self.content_container.pack(fill="both", expand=True)
        
        self.tab_browse = tk.Frame(self.content_container, bg=self.theme_vars["bg_main"])
        self.tab_ai = tk.Frame(self.content_container, bg=self.theme_vars["bg_main"])
        self.tab_book = tk.Frame(self.content_container, bg=self.theme_vars["bg_main"])
        self.tab_help = tk.Frame(self.content_container, bg=self.theme_vars["bg_main"])
        for tf in [self.tab_browse, self.tab_ai, self.tab_book, self.tab_help]:
            tf.pack(fill="both", expand=True)
            tf.pack_forget()
        
        self._build_browse_tab()
        self._build_ai_tab()
        self._build_book_tab()
        self._build_help_tab()
        
        nav_buttons = [
            ("🔍  BROWSE", self.tab_browse),
            ("⚡  FIND MY DISH", self.tab_ai),
            ("📖  MY BOOK", self.tab_book),
            ("💬  DASH ASSISTANT", self.tab_help)
        ]
        
        self.tab_buttons = {}
        self.current_tab = None
        
        for text, tab in nav_buttons:
            btn = tk.Button(self.sidebar, text=text, bg=self.theme_vars["bg_sidebar"], fg=self.theme_vars["text_primary"],
                            font=self.bold_font, bd=0, anchor="w", padx=20, pady=14,
                            cursor="hand2", activebackground=self.theme_vars["hover"], activeforeground=self.theme_vars["accent"])
            btn.pack(fill="x", padx=12, pady=6)
            btn.config(command=lambda t=tab, b=btn: self._switch_tab(t, b))
            self.tab_buttons[tab] = btn
        
        self._switch_tab(self.tab_browse, self.tab_buttons[self.tab_browse])
        
        self.queue_bar = tk.Frame(self.root, bg=self.theme_vars["header"], height=38)
        self.queue_bar.pack(side="bottom", fill="x")
        self.queue_bar.pack_propagate(False)
        self.lbl_queue_status = tk.Label(self.queue_bar, text="[FIFO Queue]: System ready",
                                         bg=self.theme_vars["header"], fg="#BDC3C7", font=self.default_font)
        self.lbl_queue_status.pack(side="left", padx=20, pady=8)
    
    def _change_theme(self, event):
        new_theme = self.theme_combo.get()
        if new_theme == self.current_theme:
            return
        self.current_theme = new_theme
        self.theme_vars = THEMES[self.current_theme]
        self._apply_theme()
        self._setup_styles()
        self._rebuild_ui()
    
    def _rebuild_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._create_layout()
    
    def _switch_tab(self, tab_frame, button):
        for tf in [self.tab_browse, self.tab_ai, self.tab_book, self.tab_help]:
            tf.pack_forget()
        for btn in self.tab_buttons.values():
            btn.config(bg=self.theme_vars["bg_sidebar"], fg=self.theme_vars["text_primary"])
        tab_frame.pack(fill="both", expand=True)
        button.config(bg=self.theme_vars["hover"], fg=self.theme_vars["accent"])
        self.current_tab = tab_frame
    
    def _log_system_request(self, task_description):
        self.req_queue.enqueue(task_description)
        self.lbl_queue_status.config(text=f"🔄 [FIFO Queue] → {task_description}")
    
    def get_visual_for_item(self, item_name):
        visual_map = {
            "whisk":"🌀","spoon":"🥄","fork":"🍴","knife":"🔪","plate":"🍽️","bowl":"🥣","spatula":"🍳",
            "broccoli":"🥦","chicken":"🍗","potato":"🥔","milk":"🥛","egg":"🥚","tea":"🍵","herb":"🌿",
            "butter":"🧈","sushi":"🍣","burger":"🍔","pizza":"🍕","boba":"🧋","carrot":"🥕","tomato":"🍅",
            "cheese":"🧀","bread":"🍞","rice":"🍚","noodle":"🍜","fish":"🐟","meat":"🥩","fruit":"🍎",
            "vegetable":"🥬","soup":"🥣","salad":"🥗","pasta":"🍝","taco":"🌮","burrito":"🌯","ice cream":"🍦",
            "cake":"🍰","cookie":"🍪","chocolate":"🍫","candy":"🍬"
        }
        name = item_name.lower()
        for key, emoji in visual_map.items():
            if key in name:
                return emoji
        return "🍴"
    
    # -------------------- TAB 1: BROWSE --------------------
    def _build_browse_tab(self):
        left_card = tk.Frame(self.tab_browse, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"])
        left_card.pack(side="left", fill="y", padx=(0, 16), pady=12)
        left_card.pack_propagate(False)
        left_card.config(width=280)
        
        tk.Label(left_card, text="Cuisine", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"]).pack(anchor="w", padx=16, pady=(16, 4))
        self.cb_cuisine = ttk.Combobox(left_card, values=list(self.ai.recipe_database.keys()), state="readonly")
        self.cb_cuisine.pack(fill="x", padx=16, pady=4)
        self.cb_cuisine.bind("<<ComboboxSelected>>", self._browse_cuisine_selected)
        
        tk.Label(left_card, text="Meal Type", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"]).pack(anchor="w", padx=16, pady=(12, 4))
        self.cb_meal = ttk.Combobox(left_card, state="readonly")
        self.cb_meal.pack(fill="x", padx=16, pady=4)
        self.cb_meal.bind("<<ComboboxSelected>>", self._browse_meal_selected)
        
        tk.Label(left_card, text="Recipes", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"]).pack(anchor="w", padx=16, pady=(12, 4))
        self.lb_recipes = tk.Listbox(left_card, bg=self.theme_vars["listbox_bg"],
                                     fg=self.theme_vars["text_primary"], font=self.default_font,
                                     bd=0, highlightthickness=1, highlightbackground=self.theme_vars["border"],
                                     selectbackground=self.theme_vars["accent"], selectforeground="white")
        self.lb_recipes.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.lb_recipes.bind("<<ListboxSelect>>", self._browse_show_recipe)
        
        right_card = tk.Frame(self.tab_browse, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"])
        right_card.pack(side="right", fill="both", expand=True, pady=12)
        
        self.txt_display = tk.Text(right_card, wrap="word", bg=self.theme_vars["textbox_bg"], fg=self.theme_vars["text_primary"],
                                   font=self.default_font, bd=0, highlightthickness=0,
                                   padx=20, pady=20)
        self.txt_display.pack(fill="both", expand=True)
        
        step_bar = tk.Frame(right_card, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"], height=50)
        step_bar.pack(side="bottom", fill="x")
        step_bar.pack_propagate(False)
        
        tk.Label(step_bar, text="Linked List Stepper:", font=self.bold_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["accent"]).pack(side="left", padx=16)
        self.lbl_step_display = tk.Label(step_bar, text="Select a recipe to view steps", bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_secondary"], font=self.default_font)
        self.lbl_step_display.pack(side="left", fill="x", expand=True, padx=10)
        
        self.btn_next_step = tk.Button(step_bar, text="Next Step →", bg=self.theme_vars["accent"], fg="white",
                                       font=self.bold_font, bd=0, cursor="hand2", padx=16, pady=6,
                                       state="disabled", command=self._traverse_next_linked_step)
        self.btn_next_step.pack(side="right", padx=16, pady=8)
    
    def _browse_cuisine_selected(self, event):
        c = self.cb_cuisine.get()
        if c in self.ai.recipe_database:
            self.cb_meal['values'] = list(self.ai.recipe_database[c].keys())
            self.cb_meal.set('')
            self.lb_recipes.delete(0, tk.END)
    
    def _browse_meal_selected(self, event):
        c = self.cb_cuisine.get()
        m = self.cb_meal.get()
        self.lb_recipes.delete(0, tk.END)
        if c in self.ai.recipe_database and m in self.ai.recipe_database[c]:
            for r in self.ai.recipe_database[c][m]:
                self.lb_recipes.insert(tk.END, r["name"])
    
    def _browse_show_recipe(self, event):
        sel = self.lb_recipes.curselection()
        if not sel: return
        name = self.lb_recipes.get(sel[0])
        recipe = self.ai.hash_table.get(name.lower())
        if recipe:
            self.nav_stack.push(recipe)
            self._render_recipe_view(recipe)
    
    def _render_recipe_view(self, recipe):
        self._log_system_request(f"Viewing: {recipe['name']}")
        self.txt_display.delete("1.0", tk.END)
        mascot = self.get_visual_for_item(recipe["name"])
        data = f"{mascot}{mascot} {recipe['name'].upper()} {mascot}{mascot}\n"
        data += f"⏱️ Time: {recipe['time']} mins\n"
        data += "━"*55 + "\n\n🛒 Ingredients:\n"
        for ing in recipe['ingredients']:
            data += f"  {self.get_visual_for_item(ing)} {ing}\n"
        data += "\n📖 Steps:\n"
        for i, step in enumerate(recipe['steps'], 1):
            data += f"  [{i}] {step}\n"
        self.txt_display.insert(tk.END, data)
        
        head = None
        cur = None
        for step in recipe['steps']:
            node = StepsNode(step)
            if not head:
                head = node
                cur = head
            else:
                cur.next = node
                cur = cur.next
        self.current_recipe_node = head
        self.current_step_index = 1
        if head:
            self.lbl_step_display.config(text=f"Step 1: {head.step_text}", fg=self.theme_vars["text_primary"])
            self.btn_next_step.config(state="normal")
        else:
            self.lbl_step_display.config(text="No steps available")
    
    def _traverse_next_linked_step(self):
        if self.current_recipe_node and self.current_recipe_node.next:
            self.current_recipe_node = self.current_recipe_node.next
            self.current_step_index += 1
            self.lbl_step_display.config(text=f"Step {self.current_step_index}: {self.current_recipe_node.step_text}")
        else:
            self.btn_next_step.config(state="disabled")
            self.lbl_step_display.config(text="🏁 End of instructions – enjoy your meal!", fg=self.theme_vars["accent"])
    
    # -------------------- TAB 2: AI PIPELINE --------------------
    def _build_ai_tab(self):
        control_card = tk.Frame(self.tab_ai, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"])
        control_card.pack(side="top", fill="x", padx=16, pady=16)
        
        row1 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        row1.pack(fill="x", padx=20, pady=10)
        tk.Label(row1, text="Cuisine:", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], width=12, anchor="w").pack(side="left")
        self.cb_ai_cuisine = ttk.Combobox(row1, values=list(self.ai.recipe_database.keys()), state="readonly", width=32)
        self.cb_ai_cuisine.pack(side="left", padx=5)
        self.cb_ai_cuisine.bind("<<ComboboxSelected>>", self._ai_pipeline_cuisine_selected)
        
        self.row2 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        tk.Label(self.row2, text="Meal Type:", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], width=12, anchor="w").pack(side="left")
        self.cb_ai_meal = ttk.Combobox(self.row2, state="readonly", width=32)
        self.cb_ai_meal.pack(side="left", padx=5)
        self.cb_ai_meal.bind("<<ComboboxSelected>>", self._ai_pipeline_meal_selected)
        
        self.row3 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        tk.Label(self.row3, text="Mode:", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], width=12, anchor="w").pack(side="left")
        self.cb_ai_mode = ttk.Combobox(self.row3, values=["Time Only", "Staples Only", "Both"], state="readonly", width=30)
        self.cb_ai_mode.pack(side="left", padx=5)
        self.cb_ai_mode.bind("<<ComboboxSelected>>", self._ai_pipeline_mode_chosen)
        
        self.row4 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        tk.Label(self.row4, text="Max Time (min):", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], width=12, anchor="w").pack(side="left")
        self.sl_ai_time = tk.Scale(self.row4, from_=5, to=120, orient="horizontal", bg=self.theme_vars["bg_card"],
                                   troughcolor=self.theme_vars["border"], highlightthickness=0, length=220)
        self.sl_ai_time.set(45)
        self.sl_ai_time.pack(side="left", padx=5)
        
        self.row5 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        tk.Label(self.row5, text="Ingredients :", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], width=12, anchor="w").pack(side="left")
        self.ent_ai_ings = ttk.Entry(self.row5, width=40)
        self.ent_ai_ings.pack(side="left", padx=5, fill="x", expand=True)
        
        self.row6 = tk.Frame(control_card, bg=self.theme_vars["bg_card"])
        self.btn_ai_pipeline_run = tk.Button(self.row6, text="⚡ GENERATE RANKED RECIPES", bg=self.theme_vars["accent"], fg="white",
                                             font=self.bold_font, bd=0, cursor="hand2", padx=24, pady=8,
                                             command=self._execute_pipeline_ai_search)
        self.btn_ai_pipeline_run.pack(anchor="e", pady=8)
        
        self.row2.pack_forget()
        self.row3.pack_forget()
        self.row4.pack_forget()
        self.row5.pack_forget()
        self.row6.pack_forget()
        
        self.txt_ai_out = tk.Text(self.tab_ai, wrap="word", bg=self.theme_vars["textbox_bg"], fg=self.theme_vars["text_primary"],
                                  font=self.default_font, bd=0, highlightthickness=1, highlightbackground=self.theme_vars["border"],
                                  padx=16, pady=16)
        self.txt_ai_out.pack(fill="both", expand=True, padx=16, pady=(0,16))
    
    def _ai_pipeline_cuisine_selected(self, event):
        c = self.cb_ai_cuisine.get()
        self.cb_ai_meal['values'] = list(self.ai.recipe_database[c].keys())
        self.cb_ai_meal.set('')
        self.row2.pack(fill="x", padx=20, pady=6)
        self.row3.pack_forget()
        self.row4.pack_forget()
        self.row5.pack_forget()
        self.row6.pack_forget()
    
    def _ai_pipeline_meal_selected(self, event):
        self.cb_ai_mode.set('')
        self.row3.pack(fill="x", padx=20, pady=6)
        self.row4.pack_forget()
        self.row5.pack_forget()
        self.row6.pack_forget()
    
    def _ai_pipeline_mode_chosen(self, event):
        mode = self.cb_ai_mode.get()
        self.row4.pack_forget()
        self.row5.pack_forget()
        if mode == "Time Only":
            self.row4.pack(fill="x", padx=20, pady=6)
        elif mode == "Staples Only":
            self.row5.pack(fill="x", padx=20, pady=6)
        elif mode == "Both":
            self.row4.pack(fill="x", padx=20, pady=6)
            self.row5.pack(fill="x", padx=20, pady=6)
        self.row6.pack(fill="x", padx=20, pady=6)
    
    def _execute_pipeline_ai_search(self):
        cuisine = self.cb_ai_cuisine.get()
        meal = self.cb_ai_meal.get()
        mode = self.cb_ai_mode.get()
        max_time = self.sl_ai_time.get()
        staples = [i.strip() for i in self.ent_ai_ings.get().split(",") if i.strip()]
        matches = self.ai.recommend_pipeline(cuisine, meal, mode, max_time, staples)
        self.txt_ai_out.delete("1.0", tk.END)
        if not matches:
            self.txt_ai_out.insert(tk.END, "❌ No recipes found matching your criteria.")
            return
        self.txt_ai_out.insert(tk.END, f"🎯 TOP RECOMMENDATIONS ({mode})\n\n")
        for r in matches:
            self.txt_ai_out.insert(tk.END, f"{self.get_visual_for_item(r['name'])} {r['name']} — {r['time']} mins\n")
            self.txt_ai_out.insert(tk.END, f"   Ingredients: {', '.join(r['ingredients'])}\n\n")
    
    # -------------------- TAB 3: PERSONAL BOOK --------------------
    def _build_book_tab(self):
        left_card = tk.Frame(self.tab_book, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"])
        left_card.pack(side="left", fill="y", padx=(16,8), pady=16)
        left_card.pack_propagate(False)
        left_card.config(width=260)
        
        tk.Label(left_card, text="📘 Your Custom Recipes", font=self.title_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["accent"]).pack(pady=(12,8))
        self.custom_listbox = tk.Listbox(left_card, bg=self.theme_vars["listbox_bg"],
                                         fg=self.theme_vars["text_primary"], font=self.default_font,
                                         selectbackground=self.theme_vars["accent"], selectforeground="white",
                                         bd=0, highlightthickness=0)
        self.custom_listbox.pack(fill="both", expand=True, padx=12, pady=(0,12))
        self.custom_listbox.bind("<<ListboxSelect>>", self._on_custom_select)
        
        right_card = tk.Frame(self.tab_book, bg=self.theme_vars["bg_card"], highlightthickness=1, highlightbackground=self.theme_vars["border"])
        right_card.pack(side="right", fill="both", expand=True, padx=(8,16), pady=16)
        
        tk.Label(right_card, text="✏️ Recipe Editor", font=self.title_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"]).pack(pady=(16,8))
        
        form = tk.Frame(right_card, bg=self.theme_vars["bg_card"])
        form.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(form, text="Recipe Name", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], anchor="w").pack(fill="x", pady=(8,2))
        self.ent_name = ttk.Entry(form)
        self.ent_name.pack(fill="x", pady=2)
        
        tk.Label(form, text="Ingredients (comma separated, include quantities)", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], anchor="w").pack(fill="x", pady=(8,2))
        self.ent_ings = ttk.Entry(form)
        self.ent_ings.pack(fill="x", pady=2)
        
        tk.Label(form, text="Time (minutes)", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], anchor="w").pack(fill="x", pady=(8,2))
        self.ent_time = ttk.Entry(form)
        self.ent_time.pack(fill="x", pady=2)
        
        tk.Label(form, text="Steps (one per line)", font=self.heading_font, bg=self.theme_vars["bg_card"], fg=self.theme_vars["text_primary"], anchor="w").pack(fill="x", pady=(8,2))
        self.txt_steps = tk.Text(form, height=5, font=self.default_font, bd=1, relief="solid", highlightbackground=self.theme_vars["border"],
                                 bg=self.theme_vars["textbox_bg"], fg=self.theme_vars["text_primary"])
        self.txt_steps.pack(fill="both", expand=True, pady=5)
        
        btn_frame = tk.Frame(form, bg=self.theme_vars["bg_card"])
        btn_frame.pack(fill="x", pady=16)
        
        self.btn_add = tk.Button(btn_frame, text="➕ Add New", bg=self.theme_vars["accent"], fg="white", font=self.bold_font,
                                 bd=0, cursor="hand2", padx=16, pady=6, command=self._add_recipe)
        self.btn_add.pack(side="left", padx=5)
        
        self.btn_update = tk.Button(btn_frame, text="✏️ Update", bg=self.theme_vars["secondary"], fg="white", font=self.bold_font,
                                    bd=0, cursor="hand2", padx=16, pady=6, command=self._update_recipe, state="disabled")
        self.btn_update.pack(side="left", padx=5)
        
        self.btn_delete = tk.Button(btn_frame, text="🗑️ Delete", bg=self.theme_vars["danger"], fg="white", font=self.bold_font,
                                    bd=0, cursor="hand2", padx=16, pady=6, command=self._delete_recipe, state="disabled")
        self.btn_delete.pack(side="left", padx=5)
        
        self.btn_clear = tk.Button(btn_frame, text="Clear Form", bg=self.theme_vars["text_secondary"], fg="white", font=self.bold_font,
                                   bd=0, cursor="hand2", padx=16, pady=6, command=self._clear_form)
        self.btn_clear.pack(side="right", padx=5)
        
        self._refresh_custom_list()
    
    def _refresh_custom_list(self):
        self.custom_listbox.delete(0, tk.END)
        custom_recipes = self.ai.recipe_database.get("Personal", {}).get("Custom", [])
        for r in custom_recipes:
            self.custom_listbox.insert(tk.END, r["name"])
        if self.custom_listbox.size() == 0:
            self.btn_update.config(state="disabled")
            self.btn_delete.config(state="disabled")
    
    def _on_custom_select(self, event):
        sel = self.custom_listbox.curselection()
        if not sel:
            return
        name = self.custom_listbox.get(sel[0])
        recipe = self.ai.hash_table.get(name.lower())
        if recipe:
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, recipe["name"])
            self.ent_ings.delete(0, tk.END)
            self.ent_ings.insert(0, ", ".join(recipe["ingredients"]))
            self.ent_time.delete(0, tk.END)
            self.ent_time.insert(0, str(recipe["time"]))
            self.txt_steps.delete("1.0", tk.END)
            self.txt_steps.insert("1.0", "\n".join(recipe["steps"]))
            self.btn_update.config(state="normal")
            self.btn_delete.config(state="normal")
    
    def _clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_ings.delete(0, tk.END)
        self.ent_time.delete(0, tk.END)
        self.txt_steps.delete("1.0", tk.END)
        self.custom_listbox.selection_clear(0, tk.END)
        self.btn_update.config(state="disabled")
        self.btn_delete.config(state="disabled")
    
    def _get_form_recipe(self):
        name = self.ent_name.get().strip()
        ings = self.ent_ings.get().strip()
        time_str = self.ent_time.get().strip()
        steps = self.txt_steps.get("1.0", tk.END).strip()
        if not name or not ings or not time_str or not steps:
            messagebox.showerror("Error", "All fields are required.")
            return None
        try:
            time_val = int(time_str)
        except:
            messagebox.showerror("Error", "Time must be an integer.")
            return None
        ing_list = [i.strip() for i in ings.split(",") if i.strip()]
        step_list = [s.strip() for s in steps.split("\n") if s.strip()]
        return {"name": name, "ingredients": ing_list, "time": time_val, "steps": step_list}
    
    def _add_recipe(self):
        recipe = self._get_form_recipe()
        if not recipe:
            return
        try:
            self.ai.add_custom_recipe(recipe, "Personal", "Custom")
            messagebox.showinfo("Success", f"Added '{recipe['name']}'")
            self._refresh_custom_list()
            self._clear_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _update_recipe(self):
        sel = self.custom_listbox.curselection()
        if not sel:
            return
        old_name = self.custom_listbox.get(sel[0])
        new_recipe = self._get_form_recipe()
        if not new_recipe:
            return
        try:
            self.ai.update_custom_recipe(old_name, new_recipe, "Personal", "Custom")
            messagebox.showinfo("Success", f"Updated '{old_name}' → '{new_recipe['name']}'")
            self._refresh_custom_list()
            self._clear_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _delete_recipe(self):
        sel = self.custom_listbox.curselection()
        if not sel:
            return
        name = self.custom_listbox.get(sel[0])
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            try:
                self.ai.delete_custom_recipe(name, "Personal", "Custom")
                messagebox.showinfo("Deleted", f"'{name}' removed")
                self._refresh_custom_list()
                self._clear_form()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    # -------------------- TAB 4: CHAT ASSISTANT --------------------
    def _build_help_tab(self):
        chat_container = tk.Frame(self.tab_help, bg=self.theme_vars["chat_bg"])
        chat_container.pack(fill="both", expand=True)
        
        header = tk.Frame(chat_container, bg=self.theme_vars["chat_header"], height=50)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="💬 ChefAI Expert Chat", fg="white", bg=self.theme_vars["chat_header"], font=self.bold_font).pack(side="left", padx=20)
        
        self.chat_log = tk.Text(chat_container, bg=self.theme_vars["chat_bg"], bd=0, highlightthickness=0,
                                font=self.default_font, wrap="word", padx=12, pady=12)
        self.chat_log.pack(fill="both", expand=True)
        
        self.chat_log.tag_configure("user", justify="right", foreground="white", background=self.theme_vars["user_bubble"],
                                    lmargin1=180, lmargin2=180, rmargin=20, spacing3=8, spacing1=8,
                                    font=self.default_font)
        self.chat_log.tag_configure("ai", justify="left", foreground="#F1F5F9", background=self.theme_vars["ai_bubble"],
                                    lmargin1=20, lmargin2=20, rmargin=180, spacing3=8, spacing1=8,
                                    font=self.default_font)
        self.chat_log.config(state="disabled")
        
        input_frame = tk.Frame(chat_container, bg=self.theme_vars["chat_header"], height=70)
        input_frame.pack(side="bottom", fill="x")
        input_frame.pack_propagate(False)
        
        self.entry_query = tk.Entry(input_frame, bg=self.theme_vars["chat_entry_bg"], fg=self.theme_vars["chat_entry_fg"], insertbackground=self.theme_vars["chat_entry_fg"],
                                    font=self.default_font, bd=0, highlightthickness=1, highlightbackground="#5D6D7E")
        self.entry_query.pack(side="left", fill="x", expand=True, padx=(20,10), pady=16)
        self.entry_query.insert(0, "my custard got burnt while cooking")
        self.entry_query.bind("<Return>", lambda e: self._send_chat())
        
        send_btn = tk.Button(input_frame, text="Send", bg=self.theme_vars["accent"], fg="white", font=self.bold_font,
                             bd=0, cursor="hand2", padx=20, pady=8, command=self._send_chat)
        send_btn.pack(side="right", padx=(0,20), pady=16)
        
        self._append_chat("ChefAI: 🍳 Hello! Describe any cooking issue (burnt, salty, runny, etc.)", "ai")
    
    def _append_chat(self, text, sender):
        self.chat_log.config(state="normal")
        if sender == "user":
            self.chat_log.insert(tk.END, f"  {text}\n\n", "user")
        else:
            self.chat_log.insert(tk.END, f"  {text}\n\n", "ai")
        self.chat_log.config(state="disabled")
        self.chat_log.see(tk.END)
    
    def _send_chat(self):
        query = self.entry_query.get().strip()
        if not query:
            return
        self._append_chat(f"You: {query}", "user")
        response = self.ai.troubleshoot(query)
        self._append_chat(f"ChefAI: {response}", "ai")
        self.entry_query.delete(0, tk.END)

# =========================================================================
# RUN APPLICATION
# =========================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRecipeGUI(root)
    root.mainloop()