import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os
import re

class HTMLEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python HTML Editor")
        self.root.geometry("800x600")

        # Initial theme settings
        self.dark_mode = True
        self.dark_bg_color = "#1e1e1e"
        self.dark_text_fg_color = "#ffffff"
        self.dark_tag_color = "#569CD6"
        self.dark_string_color = "#CE9178"

        self.light_bg_color = "#ffffff"
        self.light_text_fg_color = "#000000"
        self.light_tag_color = "#0000ff"
        self.light_string_color = "#a31515"

        # Text area for HTML editing
        self.text_area = tk.Text(self.root, wrap='word', font=('Consolas', 12), bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        self.text_area.pack(fill='both', expand=True)

        # Configure tags for syntax highlighting
        self.text_area.tag_configure("tag", foreground=self.dark_tag_color)
        self.text_area.tag_configure("string", foreground=self.dark_string_color)

        # Frame for buttons
        self.button_frame = tk.Frame(self.root, bg=self.dark_bg_color)
        self.button_frame.pack(fill='x')

        # Save button
        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_file, bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        self.save_button.pack(side='left', padx=5, pady=5)

        # Preview button
        self.preview_button = tk.Button(self.button_frame, text="Preview", command=self.preview_html, bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        self.preview_button.pack(side='left', padx=5, pady=5)

        # Dark/Light mode switch button
        self.mode_button_text = tk.StringVar()
        self.mode_button_text.set("Switch to Light Mode")
        self.mode_button = tk.Button(self.button_frame, textvariable=self.mode_button_text, command=self.toggle_mode, bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        self.mode_button.pack(side='right', padx=5, pady=5)

        # Status bar for line/column and file type info
        self.status_bar = tk.Label(self.root, text="Line: 1 | Column: 0 | UTF-8 HTML", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Highlight tags when typing
        self.text_area.bind("<KeyRelease>", self.update_status)
        self.text_area.bind("<ButtonRelease-1>", self.update_status)

    def toggle_mode(self):
        # Toggle between dark and light mode
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.text_area.config(bg=self.dark_bg_color, fg=self.dark_text_fg_color)
            self.save_button.config(bg=self.dark_bg_color, fg=self.dark_text_fg_color)
            self.preview_button.config(bg=self.dark_bg_color, fg=self.dark_text_fg_color)
            self.mode_button_text.set("Switch to Light Mode")
            self.status_bar.config(bg=self.dark_bg_color, fg=self.dark_text_fg_color)
            self.text_area.tag_configure("tag", foreground=self.dark_tag_color)
            self.text_area.tag_configure("string", foreground=self.dark_string_color)
        else:
            self.text_area.config(bg=self.light_bg_color, fg=self.light_text_fg_color)
            self.save_button.config(bg=self.light_bg_color, fg=self.light_text_fg_color)
            self.preview_button.config(bg=self.light_bg_color, fg=self.light_text_fg_color)
            self.mode_button_text.set("Switch to Dark Mode")
            self.status_bar.config(bg=self.light_bg_color, fg=self.light_text_fg_color)
            self.text_area.tag_configure("tag", foreground=self.light_tag_color)
            self.text_area.tag_configure("string", foreground=self.light_string_color)

        # Re-highlight tags based on the new mode
        self.highlight_tags()

    def update_status(self, event=None):
        # Update the status bar with current line and column
        cursor_pos = self.text_area.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        line_num = int(line)
        col_num = int(col) + 1  # Convert to 1-based index

        file_type = "UTF-8 HTML"
        if self.dark_mode:
            self.status_bar.config(text=f"Line: {line_num} | Column: {col_num} | {file_type}", bg=self.dark_bg_color, fg=self.dark_text_fg_color)
        else:
            self.status_bar.config(text=f"Line: {line_num} | Column: {col_num} | {file_type}", bg=self.light_bg_color, fg=self.light_text_fg_color)

    def highlight_tags(self, event=None):
        # Get all the text from the text area
        text = self.text_area.get("1.0", tk.END)

        # Use regular expressions to find and tag HTML tags
        tag_pattern = r"<(/?)(\w+)"
        string_pattern = r'"([^"]*)"'

        self.text_area.tag_remove("tag", "1.0", tk.END)
        self.text_area.tag_remove("string", "1.0", tk.END)

        for match in re.finditer(tag_pattern, text):
            start_index = match.start()
            end_index = match.end()
            is_close_tag = match.group(1) == "/"
            tag_name = match.group(2)

            if is_close_tag:
                self.text_area.tag_add("tag", f"1.{start_index}", f"1.{end_index}")
            else:
                self.text_area.tag_add("tag", f"1.{start_index}", f"1.{end_index}")

        for match in re.finditer(string_pattern, text):
            start_index = match.start(1) + 1
            end_index = match.end(1) - 1

            self.text_area.tag_add("string", f"1.{start_index}", f"1.{end_index}")

    def save_file(self):
        # Get file path to save the HTML content
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            # Save the content of the text area to the file
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get("1.0", tk.END))
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def preview_html(self):
        # Save the HTML content to a temporary file and open it in the default web browser
        try:
            with open("temp_preview.html", 'w', encoding='utf-8') as file:
                file.write(self.text_area.get("1.0", tk.END))
            webbrowser.open_new_tab("temp_preview.html")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview HTML: {e}")

# Create the main window
root = tk.Tk()
root.configure(bg="#1e1e1e")
app = HTMLEditor(root)
root.mainloop()
