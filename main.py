"""
AD Bulk User Generator
Author: Yehya Hamdy Shehata (SCRonin)
Version: 1.0

Description:
A Tkinter-based GUI tool that generates dsadd user commands for bulk
Active Directory user creation and exports them to a .bat file.

Features:
- Fixed or per-user OU configuration
- Fixed or per-user DC configuration
- Optional user attributes:
    * First Name
    * Last Name
    * Email
    * Telephone Number
- Custom password support
- Must Change Password at Next Logon
- Password Never Expires
- Account Disabled
- Command Preview
- Save-As dialog
- Dynamic user table

Requirements:
- Python 3.x
- Tkinter (included with standard Python on Windows)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ADBulkUserGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AD Bulk User Generator")
        self.root.geometry("1200x700")

        self.rows = []

        config = ttk.LabelFrame(root, text="Configuration")
        config.pack(fill="x", padx=10, pady=10)

        ttk.Label(config, text="Number of Users").grid(row=0, column=0, padx=5, pady=5)
        self.num_users = ttk.Entry(config, width=10)
        self.num_users.grid(row=0, column=1)

        self.fixed_ou = tk.BooleanVar()
        self.fixed_dc = tk.BooleanVar()

        ttk.Checkbutton(config, text="Fixed OU", variable=self.fixed_ou).grid(row=1, column=0, sticky="w")
        self.ou_entry = ttk.Entry(config, width=20)
        self.ou_entry.grid(row=1, column=1)

        ttk.Checkbutton(config, text="Fixed DC", variable=self.fixed_dc).grid(row=2, column=0, sticky="w")

        self.dc1_entry = ttk.Entry(config, width=15)
        self.dc1_entry.grid(row=2, column=1)

        self.dc2_entry = ttk.Entry(config, width=15)
        self.dc2_entry.grid(row=2, column=2)

        ttk.Button(config, text="Create Table", command=self.create_table).grid(row=0, column=5, padx=20)

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        actions = ttk.Frame(root)
        actions.pack(fill="x", padx=10, pady=10)

        ttk.Button(actions, text="Preview Commands", command=self.preview).pack(side="left", padx=5)
        ttk.Button(actions, text="Generate BAT", command=self.generate_bat).pack(side="left", padx=5)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status, relief="sunken").pack(fill="x", side="bottom")

    def create_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.rows = []

        try:
            count = int(self.num_users.get())
            if count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")
            return

        headers = [
            "CN", "First Name", "Last Name", "Email",
            "Phone", "Password", "Must Change",
            "Pwd Never Expires", "Disabled"
        ]

        if not self.fixed_ou.get():
            headers.append("OU")

        if not self.fixed_dc.get():
            headers.extend(["DC1", "DC2"])

        for c, h in enumerate(headers):
            ttk.Label(self.table_frame, text=h).grid(row=0, column=c, padx=3, pady=3)

        for r in range(1, count + 1):
            row = {}

            col = 0
            for key in ["cn", "fn", "ln", "email", "phone", "pwd"]:
                e = ttk.Entry(self.table_frame, width=15)
                e.grid(row=r, column=col, padx=2, pady=2)
                row[key] = e
                col += 1

            row["must"] = tk.BooleanVar()
            ttk.Checkbutton(self.table_frame, variable=row["must"]).grid(row=r, column=col)
            col += 1

            row["never"] = tk.BooleanVar()
            ttk.Checkbutton(self.table_frame, variable=row["never"]).grid(row=r, column=col)
            col += 1

            row["disabled"] = tk.BooleanVar()
            ttk.Checkbutton(self.table_frame, variable=row["disabled"]).grid(row=r, column=col)
            col += 1

            if not self.fixed_ou.get():
                e = ttk.Entry(self.table_frame, width=15)
                e.grid(row=r, column=col)
                row["ou"] = e
                col += 1

            if not self.fixed_dc.get():
                e1 = ttk.Entry(self.table_frame, width=10)
                e1.grid(row=r, column=col)
                row["dc1"] = e1
                col += 1

                e2 = ttk.Entry(self.table_frame, width=10)
                e2.grid(row=r, column=col)
                row["dc2"] = e2

            self.rows.append(row)

        self.status.set(f"{count} user rows created")

    def build_commands(self):
        commands = []

        for row in self.rows:
            cn = row["cn"].get().strip()

            if not cn:
                continue

            ou = self.ou_entry.get().strip() if self.fixed_ou.get() else row["ou"].get().strip()
            dc1 = self.dc1_entry.get().strip() if self.fixed_dc.get() else row["dc1"].get().strip()
            dc2 = self.dc2_entry.get().strip() if self.fixed_dc.get() else row["dc2"].get().strip()

            cmd = f'dsadd user "cn={cn},ou={ou},dc={dc1},dc={dc2}"'

            if row["fn"].get():
                cmd += f' -fn "{row["fn"].get()}"'

            if row["ln"].get():
                cmd += f' -ln "{row["ln"].get()}"'

            if row["email"].get():
                cmd += f' -email "{row["email"].get()}"'

            if row["phone"].get():
                cmd += f' -tel "{row["phone"].get()}"'

            password = row["pwd"].get().strip() or "P@ssw0rd"
            cmd += f' -pwd "{password}"'

            if row["must"].get():
                cmd += " -mustchpwd yes"

            if row["never"].get():
                cmd += " -pwdneverexpires yes"

            if row["disabled"].get():
                cmd += " -disabled yes"

            commands.append(cmd)

        return commands

    def preview(self):
        commands = self.build_commands()

        win = tk.Toplevel(self.root)
        win.title("Command Preview")

        txt = tk.Text(win)
        txt.pack(fill="both", expand=True)

        txt.insert("1.0", "\n".join(commands))

    def generate_bat(self):
        commands = self.build_commands()

        if not commands:
            messagebox.showerror("Error", "No commands generated.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".bat",
            filetypes=[("Batch Files", "*.bat")]
        )

        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(commands))

        self.status.set(f"Saved: {file_path}")
        messagebox.showinfo("Success", "BAT file generated successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ADBulkUserGenerator(root)
    root.mainloop()

