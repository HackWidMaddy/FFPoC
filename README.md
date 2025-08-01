# FFPoC - Firefox Service Worker Exploit Proof of Concept

## 🚨 Overview

FFPoC is a **proof-of-concept exploit** demonstrating how a **malicious service worker** can be used to persistently hijack a user's browser session, exfiltrate sensitive data, and serve malicious content even after the victim leaves the attacker's website. The PoC targets **Firefox's handling of service workers**, showcasing how they can be abused for persistent and covert access.

## 🧠 Concept

This PoC demonstrates the following attack flow:

1. **Victim visits a malicious website** where a rogue service worker is registered.
2. The **service worker persists** in the browser, gaining control over fetch events for all subsequent navigations in that origin scope.
3. The attacker uses the service worker to:

   * Intercept and modify network requests
   * Exfiltrate sensitive data
   * Maintain persistence even after tab close
4. A simple Python HTTP server simulates both attacker and victim environments.

## 📁 Project Structure

```
FFPoC-main/
├── attacker/
│   ├── index.html         # Malicious landing page that registers the service worker
│   ├── sw.js              # Malicious service worker code
│   └── server.py          # Simple HTTP server to host attacker's content
├── victim/
│   ├── index.html         # Simulated victim website
│   └── server.py          # HTTP server hosting a legitimate-looking site
```

## 🧪 Setup and Run

### Prerequisites

* Python 3.x
* Firefox browser

### Step-by-Step Instructions

1. **Run attacker server**:

```bash
cd attacker
python3 server.py
```

2. **Run victim server**:

```bash
cd victim
python3 server.py
```

3. **In Firefox**, visit the attacker's site (typically `http://localhost:8000`).
4. Observe that the service worker remains active and can now monitor or manipulate future requests even on different tabs under the same origin.

## ⚠️ Disclaimer

This repository is intended **strictly for educational and research purposes**. The exploit demonstrates a security concern regarding service worker persistence and abuse. Do not deploy this code on any system you do not own or have explicit permission to test.

## 📚 References

* [Mozilla Service Worker API Docs](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
* [OWASP Service Worker Security](https://owasp.org/www-community/attacks/Service_Worker_Security)

---
