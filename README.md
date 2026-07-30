# Security-First Personal Portfolio & Verification Portal

A lightweight, modern web portfolio and bot-protected verification gateway built with **FastAPI**, **Jinja2**, and **ALTCHA**. Features a responsive glassmorphism UI, strict security headers, and rate limiting.

---

## ✨ Features

* **Proof-of-Work CAPTCHA:** Integrated [ALTCHA](https://altcha.org/) challenge to block automated bots without intrusive image puzzles.
* **Security Hardening:** Strictly configured Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), and anti-clickjacking headers.
* **Rate Limiting:** IP-based endpoint limiting powered by `slowapi`.
* **Glassmorphic UI:** Modern, responsive CSS design with dynamic blurring and custom mobile breakpoint rules.
* **Custom Error Handling:** Dedicated Jinja2 templates for session expiration and custom 404 pages.

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
Make sure you have Python 3.10+ installed.

### 2. Clone the Repository
git clone [https://github.com/evanpopp/work_site.git](https://github.com/evanpopp/work_site.git)
cd work_site

### 3. Set Up Environment Variables
cp .env.example .env
sudo nano .env
ALTCHA_HMAC_KEY=your_random_secret_string_here

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Run the Application
uvicorn app:app --host 127.0.0.1 --port 8001

---

## 🛠️ Built With & Acknowledgements

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Templating:** [Jinja2](https://jinja2.palletsprojects.com/)
* **Security & Bot Protection:** [ALTCHA](https://altcha.org/) & [SlowAPI](https://github.com/laurents/slowapi)
* **Styling:** Custom CSS (Glassmorphism)

### AI Assistance Disclosure
I used **Google Gemini** as an AI pair-programmer throughout the development of this project. AI assistance was utilized for:
* Refining backend FastAPI middleware and security header configurations.
* Troubleshooting rate-limiting (`slowapi`) and Content Security Policy (CSP) worker integration.
* Optimizing responsive CSS layout behavior and cross-browser styling.

*All AI-suggested code was reviewed, tested, and integrated by me (a human).*

---

## License
MIT License

Copyright (a) 2026 Evan Popp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.