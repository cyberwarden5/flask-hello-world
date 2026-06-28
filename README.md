
# Tool Titan API 🌟  
[**tooltitan.vercel.app**](https://tooltitan.vercel.app)  

**Tool Titan** is a powerful and feature-packed API that allows you to:  
- ✅ **Check Seedr Account**: Validate Seedr account credentials and fetch account details.  
- ✅ **Verify Crunchyroll Accounts**: Test Crunchyroll combos for validity and retrieve subscription details.  
- 🤖 **Chat with Blackbox AI**: Experience AI-powered chat for advanced, intelligent conversations.  
- 🎨 **Generate Stunning Images**: Create AI-generated images based on your prompts.  

---

## 🚀 Features  

### 1. **Seedr Account Combo Checker**  
Easily validate Seedr account credentials and retrieve the following:  
- Premium status  
- Storage information (in GB)  
- Package type  
- Account country  

### 2. **Crunchyroll Account Checker**  
Check if Crunchyroll accounts are valid and get:  
- Email verification status  
- Account creation date  
- Subscription details (type, currency, amount, free trial, etc.)  

### 3. **Blackbox AI Chat**  
Interact with Blackbox AI for:  
- Intelligent conversations  
- Creative responses  
- Insights and assistance  

### 4. **Image Generation with Blackbox AI**  
Generate beautiful images by simply providing a text prompt. Perfect for:  
- Creative projects  
- Visualization  
- Artistic inspiration  

---

## 📖 How to Use  

### **Base URL**  
All requests should be made to the base URL:  
`https://tooltitan.vercel.app`

### **Endpoints**  

#### 1. **Check Seedr Account**  
**Endpoint**: `/seedr`  
**Method**: `GET`  
**Query Parameter**:  
- `combo`: `email:password`  

**Example Request**:  
```
https://tooltitan.vercel.app/seedr?combo=email@example.com:password123
```

#### 2. **Check Crunchyroll Account**  
**Endpoint**: `/crunchy`  
**Method**: `GET`  
**Query Parameter**:  
- `combo`: `email:password`  

**Example Request**:  
```
https://tooltitan.vercel.app/crunchy?combo=email@example.com:password123
```

#### 3. **Chat with Blackbox AI**  
**Endpoint**: `/blackbox`  
**Method**: `GET`  
**Query Parameters**:  
- `prompt`: Your chat input.  
- `system_prompt` (optional): Define system behavior (default: *"Don't Write Code unless Mentioned"*).  
- `web_access` (optional): Enable web access (`true`/`false`, default: `true`).  
- `stream` (optional): Enable streaming responses (`true`/`false`, default: `true`).  

**Example Request**:  
```
https://tooltitan.vercel.app/blackbox?prompt=Tell me about AI.
```

#### 4. **Generate AI Images**  
**Endpoint**: `/image`  
**Method**: `GET`  
**Query Parameter**:  
- `prompt`: Your image generation description.  

**Example Request**:  
```
https://tooltitan.vercel.app/image?prompt=Create a futuristic cityscape at sunset.
```

---

## 🛠️ Requirements  
- **Python** 3.8 or above  
- **Flask** framework installed (`pip install flask`)  
- **Requests** library (`pip install requests`)  
- **Cloudscraper** library (`pip install cloudscraper`)  

---

## 🤝 Contributions  
We welcome contributions! Feel free to submit pull requests or report issues.  

---

## 👨‍💻 Developer Info  
**Creator**: Aftab Kabir  
**GitHub**: [@aftabkabirr](https://github.com/aftabkabirr)  
**Contact**: [@aftab_kabirr](https://twitter.com/aftab_kabirr)  

---

**Enjoy using Tool Titan and make your workflow more powerful! 🚀**
