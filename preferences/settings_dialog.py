import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

class SettingsDialog:
    def __init__(self, parent, preference_manager):
        self.parent = parent
        self.pref_manager = preference_manager
        self.temp_preferences = {}  # Temporary storage for changes
        self.widgets = {}  # Keep track of widgets for updates
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Copy current preferences to temporary storage
        self._copy_preferences()
        
        # Build the interface
        self._build_ui()
        
        # Center the dialog
        self._center_window()
    
    def _copy_preferences(self):
        """Copy current preferences to temporary storage."""
        import copy
        self.temp_preferences = copy.deepcopy(self.pref_manager.preferences)
    
    def _center_window(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        
        # Get dialog dimensions
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Get parent position and dimensions
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate centered position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def _build_ui(self):
        """Build the settings dialog UI."""
        # Create main container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create tabs for each category
        self.tabs = {}
        for category in self.pref_manager.schema:
            # Create frame for tab
            tab_frame = ttk.Frame(self.notebook)
            self.tabs[category] = tab_frame
            
            # Add tab to notebook with properly formatted name
            tab_label = category.replace('_', ' ').title()
            self.notebook.add(tab_frame, text=tab_label)
            
            # Create scrollable frame for tab content
            canvas = tk.Canvas(tab_frame, highlightthickness=0)
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Grid canvas and scrollbar
            canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            # Configure grid weights
            tab_frame.grid_rowconfigure(0, weight=1)
            tab_frame.grid_columnconfigure(0, weight=1)
            
            # Build preference controls for this category
            self._build_category_controls(scrollable_frame, category)
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Add buttons
        ttk.Button(
            button_frame,
            text="OK",
            command=self._on_ok
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Apply",
            command=self._on_apply
        ).pack(side=tk.RIGHT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._on_reset
        ).pack(side=tk.LEFT)
    
    def _build_category_controls(self, parent, category: str):
        """Build controls for a preference category."""
        prefs = self.pref_manager.schema[category]
        
        for row, (key, spec) in enumerate(prefs.items()):
            # Create frame for this preference
            pref_frame = ttk.LabelFrame(
                parent,
                text=spec['label'],
                padding="10"
            )
            pref_frame.grid(
                row=row,
                column=0,
                sticky=(tk.W, tk.E),
                padx=10,
                pady=5
            )
            pref_frame.grid_columnconfigure(0, weight=1)
            
            # Add description
            if spec.get('description'):
                desc_label = ttk.Label(
                    pref_frame,
                    text=spec['description'],
                    wraplength=400,
                    foreground='gray'
                )
                desc_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
            
            # Create appropriate control based on type
            control_row = 1 if spec.get('description') else 0
            
            if spec['type'] == 'boolean':
                var = tk.BooleanVar(value=self.temp_preferences[category][key])
                control = ttk.Checkbutton(
                    pref_frame,
                    variable=var,
                    command=lambda c=category, k=key, v=var: self._on_change(c, k, v.get())
                )
                control.grid(row=control_row, column=0, sticky=tk.W)
                self.widgets[f"{category}.{key}"] = var
                
            elif spec['type'] == 'choice':
                var = tk.StringVar(value=self.temp_preferences[category][key])
                control = ttk.Combobox(
                    pref_frame,
                    textvariable=var,
                    values=spec['options'],
                    state='readonly',
                    width=20
                )
                control.bind(
                    '<<ComboboxSelected>>',
                    lambda e, c=category, k=key, v=var: self._on_change(c, k, v.get())
                )
                control.grid(row=control_row, column=0, sticky=tk.W)
                self.widgets[f"{category}.{key}"] = var
                
            elif spec['type'] == 'integer':
                frame = ttk.Frame(pref_frame)
                frame.grid(row=control_row, column=0, sticky=tk.W)
                
                var = tk.IntVar(value=self.temp_preferences[category][key])
                
                # Create spinbox
                spinbox = ttk.Spinbox(
                    frame,
                    from_=spec.get('min', 0),
                    to=spec.get('max', 100),
                    textvariable=var,
                    width=10,
                    command=lambda c=category, k=key, v=var: self._on_change(c, k, v.get())
                )
                spinbox.pack(side=tk.LEFT)
                
                # Add unit label if specified
                if 'unit' in spec:
                    ttk.Label(frame, text=spec['unit']).pack(side=tk.LEFT, padx=(5, 0))
                
                self.widgets[f"{category}.{key}"] = var
                
            elif spec['type'] == 'string':
                var = tk.StringVar(value=self.temp_preferences[category][key])
                control = ttk.Entry(
                    pref_frame,
                    textvariable=var,
                    width=30
                )
                control.bind(
                    '<FocusOut>',
                    lambda e, c=category, k=key, v=var: self._on_change(c, k, v.get())
                )
                control.bind(
                    '<Return>',
                    lambda e, c=category, k=key, v=var: self._on_change(c, k, v.get())
                )
                control.grid(row=control_row, column=0, sticky=(tk.W, tk.E))
                self.widgets[f"{category}.{key}"] = var
    
    def _on_change(self, category: str, key: str, value: Any):
        """Handle preference change."""
        self.temp_preferences[category][key] = value
    
    def _validate_all(self) -> bool:
        """Validate all temporary preferences."""
        for category, prefs in self.temp_preferences.items():
            for key, value in prefs.items():
                spec = self.pref_manager.schema[category][key]
                if not self.pref_manager._validate_value(value, spec):
                    messagebox.showerror(
                        "Validation Error",
                        f"Invalid value for {spec['label']}: {value}"
                    )
                    return False
        return True
    
    def _apply_changes(self):
        """Apply temporary preferences to the preference manager."""
        if not self._validate_all():
            return False
        
        # Apply each preference
        for category, prefs in self.temp_preferences.items():
            for key, value in prefs.items():
                current_value = self.pref_manager.get(category, key)
                if current_value != value:
                    self.pref_manager.set(category, key, value)
        
        return True
    
    def _on_ok(self):
        """Handle OK button click."""
        if self._apply_changes():
            self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button click."""
        self.dialog.destroy()
    
    def _on_apply(self):
        """Handle Apply button click."""
        if self._apply_changes():
            messagebox.showinfo("Settings", "Settings applied successfully!")
            # Update temporary preferences with current values
            self._copy_preferences()
    
    def _on_reset(self):
        """Handle Reset to Defaults button click."""
        result = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?"
        )
        
        if result:
            # Reset in preference manager
            self.pref_manager.reset_to_defaults()
            
            # Update temporary preferences
            self._copy_preferences()
            
            # Update all widgets
            for category in self.pref_manager.schema:
                for key in self.pref_manager.schema[category]:
                    widget_key = f"{category}.{key}"
                    if widget_key in self.widgets:
                        value = self.temp_preferences[category][key]
                        self.widgets[widget_key].set(value)
            
            messagebox.showinfo("Settings", "Settings reset to defaults!")
