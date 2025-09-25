# 🔹 HTTP/3 Overview

HTTP/3 is the **third major version** of HTTP.

* Standardized in **2022**.
* Built on **QUIC** (Quick UDP Internet Connections) instead of TCP.

👉 It’s already supported by Chrome, Firefox, Edge, and most CDNs (Cloudflare, AWS CloudFront, etc.).

---

## 🔹 Key Differences Between HTTP/2 and HTTP/3

### 1. **Transport Protocol**

* **HTTP/2** runs over **TCP**.
* **HTTP/3** runs over **QUIC (UDP-based)**.

Why?

* TCP has problems with **head-of-line blocking**: if one packet is lost, everything waits until it’s retransmitted.
* QUIC solves this by handling streams independently — one lost packet doesn’t block others.

---

### 2. **Multiplexing with Streams**

* HTTP/2 multiplexes streams, but still suffers from TCP’s blocking.
* HTTP/3’s QUIC streams are **independent** → no blocking, faster recovery.

---

### 3. **Built-in Security**

* QUIC includes **TLS 1.3** by default.
* In HTTP/2, TLS was layered on top of TCP.
* In HTTP/3, encryption is baked into the protocol → faster handshakes.

---

### 4. **Connection Migration**

* With TCP (HTTP/2), if your IP changes (e.g., switching from WiFi to mobile data), the connection resets.
* With QUIC (HTTP/3), connections are bound to a **connection ID**, not the IP → seamless migration.

Example:

* Video call continues without disruption when switching networks.

---

### 5. **Performance in Real World**

* Faster page loads on mobile networks.
* Lower latency for streaming, gaming, and APIs.
* Already widely used by **Google, YouTube, Facebook, and Cloudflare**.

---

## 🔹 Quick Comparison Table

| Feature              | HTTP/1.1                       | HTTP/2          | HTTP/3 (QUIC)          |
| -------------------- | ------------------------------ | --------------- | ---------------------- |
| Protocol             | Text over TCP                  | Binary over TCP | Binary over QUIC (UDP) |
| Multiplexing         | ❌ (one request per connection) | ✅               | ✅ (no TCP blocking)    |
| Header Compression   | ❌                              | ✅ (HPACK)       | ✅ (QPACK)              |
| Security             | Optional TLS                   | Mostly TLS      | Always TLS 1.3         |
| Connection Migration | ❌                              | ❌               | ✅                      |

---

## 🔹 Why It Matters for APIs & gRPC

* gRPC already supports **HTTP/2**, and experimental support for **HTTP/3** is coming.
* With HTTP/3, **API calls will be faster and more resilient**, especially in mobile/cloud-native environments.

---

✅ Summary:

* **HTTP/2** = Binary + Multiplexed + Faster than HTTP/1.1.
* **HTTP/3** = QUIC + Stream independence + Seamless connection migration + Built-in TLS 1.3.

---

👉 Since you’re learning APIs, do you want me to show you **how to run a gRPC service over HTTP/3 (QUIC)** in your lab, or first practice normal HTTP/2-based gRPC?
