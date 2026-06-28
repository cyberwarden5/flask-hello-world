# 🚀 Tool Titan API Platform
[**tooltitan.vercel.app**](https://tooltitan.vercel.app)

**Tool Titan** is a modern, high-performance SaaS developer platform and REST API suite designed for fast account automation, artificial intelligence queries, and utility tools.

---

## ✨ Available API Endpoints & Features

### 🛠️ Active & Automation APIs

#### 1. **Seedr Account Checker**
- **Endpoint**: `/seedr`
- **Method**: `GET`
- **Parameter**: `combo` (`email:password`)
- **Description**: Validates Seedr.cc account credentials and fetches live storage telemetry, tier details, and location data.

#### 2. **Crunchyroll Account Checker**
- **Endpoint**: `/crunchyroll`
- **Method**: `GET`
- **Parameter**: `combo` (`email:password`)
- **Description**: Verifies Crunchyroll accounts, checks active membership plans, renewal dates, and trial indicators.

#### 3. **Blackbox AI Chat**
- **Endpoint**: `/blackbox`
- **Method**: `GET`
- **Parameters**: `prompt`, `system_prompt` (optional), `web_access` (optional), `stream` (optional)
- **Description**: Connects directly to Blackbox AI model for natural language processing and technical queries.

#### 4. **AI Image Generator**
- **Endpoint**: `/image`
- **Method**: `GET`
- **Parameter**: `prompt`
- **Description**: Generates high-fidelity visual assets on demand via cloud synthesis.

---

### ⏳ Upcoming APIs (Coming Soon - Q3 2026)

#### 5. **Hotmail Checker API**
- **Endpoint**: `/hotmail`
- **Method**: `GET`
- **Description**: Automated verification engine for Hotmail & Outlook mailboxes.

#### 6. **CyberGhost VPN API**
- **Endpoint**: `/cyberghost`
- **Method**: `GET`
- **Description**: High-speed CyberGhost VPN account validation and device limit telemetry.

#### 7. **Weather API**
- **Endpoint**: `/weather`
- **Method**: `GET`
- **Description**: Real-time global meteorological weather forecast and climate REST endpoint.

#### 8. **NFToken Generator API**
- **Endpoint**: `/nftoken`
- **Method**: `GET`
- **Description**: Converts Netflix session cookies into instant one-click login token URLs.

---

## 📖 Standard Response Format

All API responses are formatted in pretty-printed JSON:

```json
{
    "status": "success",
    "http_code": 200,
    "response": "Data payload here",
    "dev": "@Aftabkabir"
}
```

---

## 🛠️ Tech Stack & Local Setup

- **Backend**: Python 3.8+, Flask, Cloudscraper, Requests
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism design system), JavaScript (ES6+), Lucide Icons
- **Deployment**: Vercel Serverless Server Engine (`vercel.json`)

### Running Locally
```bash
# Clone the repository
git clone https://github.com/aftabkabirr/flask-hello-world.git

# Install requirements
pip install -r requirements.txt

# Run local development server
python api/index.py
```

---

## 👨‍💻 Developer & Contact Info
- **Developer**: Aftab Kabir (`@Aftabkabir`)
- **Telegram**: [@aftab_kabirr](https://t.me/aftab_kabirr)
- **GitHub**: [@aftabkabirr](https://github.com/aftabkabirr)

© 2025 Tool Titan API Tools. All Rights Reserved.
