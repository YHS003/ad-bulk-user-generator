# Active Directory Bulk User Generator

A Python Tkinter-based GUI application for generating bulk Active Directory user creation commands using `dsadd user`.

The tool simplifies the process of creating multiple AD users by generating a ready-to-run `.bat` file with customizable user attributes and account settings.

---

## Features

### User Configuration

* Create multiple users at once
* Dynamic user table generation
* Generate bulk `dsadd user` commands

### Organizational Structure

* Fixed OU for all users
* Per-user OU configuration
* Fixed Domain Components (DC)
* Per-user DC configuration

### User Attributes

* Common Name (CN)
* First Name
* Last Name
* Email Address
* Telephone Number
* Password

### Account Options

* Must Change Password at Next Logon
* Password Never Expires
* Account Disabled

### Export & Preview

* Preview generated commands before export
* Save commands as a `.bat` file
* Status bar notifications

---

## Technologies Used

* Python 3
* Tkinter GUI Framework

No third-party libraries are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ad-bulk-user-generator.git
cd ad-bulk-user-generator
```

Run the application:

```bash
python main.py
```

---

## Usage

### Step 1

Enter the number of users you want to create.

### Step 2

Choose whether:

* OU is fixed for all users
* DC values are fixed for all users

### Step 3

Generate the user table.

### Step 4

Fill in user information.

### Step 5

Click **Preview Commands** to review generated commands.

### Step 6

Click **Generate BAT** and save the batch file.

### Step 7

Run the generated `.bat` file on a Windows Server with Active Directory tools installed.

---

## Example Output

```bat
dsadd user "cn=Ahmed,ou=Employees,dc=company,dc=local" -fn "Ahmed" -ln "Ali" -email "ahmed@company.local" -tel "01012345678" -pwd "P@ssw0rd" -mustchpwd yes

dsadd user "cn=Sara,ou=Employees,dc=company,dc=local" -fn "Sara" -ln "Mohamed" -pwd "P@ssw0rd" -pwdneverexpires yes
```

---

## Project Structure

```text
AD-Bulk-User-Generator/
│
├── main.py
├── README.md
└── screenshots/
```

---

## Future Improvements

* CSV Import
* Excel Import/Export
* Dark Mode
* User Templates
* PowerShell Export Support
* Active Directory Integration
* Search and Edit Existing Users
* User Validation Rules

---

## Author

**Yehya Hamdy Shehata**

* Computer Engineering Student
* Cybersecurity Enthusiast
* Python Developer

GitHub: https://github.com/YOUR_USERNAME

---

## License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this software.
