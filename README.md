# 🔐 File Sharing System – Backend (Django + MySQL)

A secure backend system that allows **Ops users to upload files** and **Client users to securely download them** via an encrypted URL. This project was built as part of a backend assignment using Django REST Framework.

---

## 🚀 Features

- 🔐 **User Roles**: Separate authentication and permissions for `Ops` and `Client`
- 📤 **File Upload (Ops)**: Upload `.docx`, `.pptx`, `.xlsx` securely
- 🔗 **Encrypted URL Generation**: Signup returns a secure download URL (Fernet-encrypted)
- 📩 **Email Verification (Mocked)**: Email verification link is printed to console
- 🧾 **Token-based Authentication**: All APIs protected with DRF token auth
- 📁 **List & Download Files (Client)**: Clients can list and securely download files
- 🎯 **Download Specific File**: Option to download a file by ID

---

## 🧑‍💻 Tech Stack

- **Backend**: Django 5, Django REST Framework
- **Auth**: TokenAuthentication (`rest_framework.authtoken`)
- **Database**: MySQL
- **Security**: Fernet encryption (`cryptography`)
- **Email**: Mocked with Django console backend
- **Others**: Python Decouple, DRF Browsable API

---

## 📁 Project Structure

