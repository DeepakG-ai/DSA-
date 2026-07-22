# The API Master Guide

## Practical Calling, Protocol Differences, the New QUERY Method, and Interview Preparation

This guide has four parts:

- **Part 1 — Calling APIs in practice.** How to actually make requests: API keys, Bearer tokens, Basic auth, OAuth2, sending JSON, sending PDFs and files with form data, downloading files, timeouts, retries. Every example in curl, Python, and JavaScript.
- **Part 2 — The new HTTP QUERY method (RFC 10008, June 2026).** The first new core method in decades — what it is and why it exists.
- **Part 3 — Deep differences: REST vs SSE vs WebSockets vs gRPC (plus GraphQL and Webhooks).** Comparison tables and how to choose.
- **Part 4 — Interview questions and answers.** Basic to advanced, including scenario questions and the traps interviewers set.

---

# PART 1 — CALLING APIs IN PRACTICE

Most tutorials teach you to BUILD APIs. This part teaches you to CALL them, which is what you actually do 90% of the time at work: calling Stripe, Razorpay, OpenAI, Google Maps, your own company's internal services.

## 1.1 The three tools you will use

| Tool | Where | When |
|------|-------|------|
| curl | Terminal | Quick tests, debugging, sharing reproducible examples with teammates |
| Python `requests` / `httpx` | Scripts and backends | Automation, backend-to-backend calls |
| JavaScript `fetch` | Browser and Node | Frontend apps |

Install once:

```bash
pip install requests            # classic, synchronous
pip install httpx               # modern, supports async
```

## 1.2 The simplest possible call

curl:

```bash
curl https://api.github.com/users/torvalds
```

Python:

```python
import requests

response = requests.get("https://api.github.com/users/torvalds")

print(response.status_code)      # 200
print(response.headers["Content-Type"])   # application/json
data = response.json()           # parses JSON body into a dict
print(data["name"])              # Linus Torvalds
```

JavaScript:

```javascript
const response = await fetch("https://api.github.com/users/torvalds");
console.log(response.status);          // 200
const data = await response.json();
console.log(data.name);
```

Three things you always work with: the **status code**, the **headers**, and the **body**.

## 1.3 Query parameters (filtering, searching)

Never build query strings by hand with string concatenation — the library encodes special characters correctly.

```bash
curl "https://api.example.com/products?category=phones&sort=-price&limit=20"
```

```python
params = {"category": "phones", "sort": "-price", "limit": 20}
response = requests.get("https://api.example.com/products", params=params)
# requests builds: /products?category=phones&sort=-price&limit=20
```

```javascript
const params = new URLSearchParams({category: "phones", sort: "-price", limit: 20});
const response = await fetch(`https://api.example.com/products?${params}`);
```

## 1.4 Authentication: the four common patterns

### Pattern 1 — API key in a header (most common for SaaS APIs)

Used by: OpenAI, Anthropic, Stripe, SendGrid, most weather/maps APIs.
You get a long random string from the provider's dashboard. Send it on EVERY request.

```bash
curl https://api.stripe.com/v1/charges \
  -H "Authorization: Bearer sk_test_51Abc..."

# Some providers use a custom header instead:
curl https://api.example.com/data \
  -H "X-API-Key: your-key-here"
```

```python
headers = {"Authorization": "Bearer sk_test_51Abc..."}
response = requests.get("https://api.stripe.com/v1/charges", headers=headers)
```

```javascript
const response = await fetch("https://api.stripe.com/v1/charges", {
  headers: { "Authorization": "Bearer sk_test_51Abc..." }
});
```

**Rules every professional follows:**
- Never hardcode keys in source code. Read from environment variables:
  ```python
  import os
  API_KEY = os.environ["STRIPE_API_KEY"]     # set in .env / shell, never committed
  ```
- Never put keys in the URL (`?api_key=...`) unless the provider forces it — URLs end up in logs, browser history, and proxies.
- Never call third-party APIs with secret keys from browser JavaScript — anyone can open DevTools and steal the key. Browser -> your backend -> third-party API.

### Pattern 2 — API key in query parameter (older/simpler APIs)

Used by: Google Maps, some weather APIs. Only use when the provider requires it.

```bash
curl "https://maps.googleapis.com/maps/api/geocode/json?address=Pune&key=YOUR_KEY"
```

### Pattern 3 — Basic Auth (username + password)

Older style; still used by Jenkins, Elasticsearch, many internal tools. The client sends `username:password` base64-encoded (which is encoding, NOT encryption — that is why HTTPS is mandatory).

```bash
curl -u admin:secret123 https://ci.example.com/api/jobs
```

```python
response = requests.get("https://ci.example.com/api/jobs",
                        auth=("admin", "secret123"))
```

```javascript
const response = await fetch("https://ci.example.com/api/jobs", {
  headers: { "Authorization": "Basic " + btoa("admin:secret123") }
});
```

### Pattern 4 — OAuth2 / JWT flow (login-based apps)

Used when the API acts on behalf of a USER (not just your app). Two-step dance:

Step 1 — exchange credentials for tokens:

```python
response = requests.post("https://api.example.com/auth/login",
                         json={"email": "ravi@example.com", "password": "..."})
tokens = response.json()
# {"access_token": "eyJ...", "refresh_token": "dGhp...", "expires_in": 900}
```

Step 2 — use the access token on every call:

```python
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
response = requests.get("https://api.example.com/orders", headers=headers)
```

Step 3 — when you get 401 (token expired), refresh and retry:

```python
if response.status_code == 401:
    r = requests.post("https://api.example.com/auth/refresh",
                      json={"refresh_token": tokens["refresh_token"]})
    tokens = r.json()
    headers["Authorization"] = f"Bearer {tokens['access_token']}"
    response = requests.get("https://api.example.com/orders", headers=headers)
```

## 1.5 Sending JSON (the everyday POST)

```bash
curl -X POST https://api.example.com/api/v1/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"restaurant_id": 42, "items": [{"id": 7, "qty": 2}]}'
```

```python
payload = {"restaurant_id": 42, "items": [{"id": 7, "qty": 2}]}
response = requests.post("https://api.example.com/api/v1/orders",
                         json=payload,          # json= sets Content-Type automatically
                         headers={"Authorization": f"Bearer {token}"})

if response.status_code == 201:
    order = response.json()
    print("Order placed:", order["order_id"])
else:
    print("Failed:", response.status_code, response.json())
```

```javascript
const response = await fetch("https://api.example.com/api/v1/orders", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({restaurant_id: 42, items: [{id: 7, qty: 2}]})
});
const order = await response.json();
```

Common beginner mistake in Python: `requests.post(url, data=payload)` sends FORM data, not JSON. Use `json=payload` for JSON.

## 1.6 Uploading files: PDFs, images, and multipart/form-data

This confuses everyone at first, so here is the full picture.

### What multipart/form-data is

JSON cannot carry raw binary bytes efficiently. When you upload a file, the request body is split into "parts" separated by a boundary string — one part per field, one part per file. This format is `multipart/form-data`. It is exactly what an HTML `<form>` with a file input produces.

Raw wire format (so you understand what the libraries build for you):

```
POST /api/v1/documents HTTP/1.1
Content-Type: multipart/form-data; boundary=----XYZ123

------XYZ123
Content-Disposition: form-data; name="title"

Invoice March 2026
------XYZ123
Content-Disposition: form-data; name="file"; filename="invoice.pdf"
Content-Type: application/pdf

%PDF-1.7 ...raw binary bytes of the PDF...
------XYZ123--
```

### Uploading a PDF with extra form fields

curl (`-F` = one form part; `@` = read from file):

```bash
curl -X POST https://api.example.com/api/v1/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "title=Invoice March 2026" \
  -F "category=finance" \
  -F "file=@/home/ravi/invoice.pdf;type=application/pdf"
```

Python:

```python
url = "https://api.example.com/api/v1/documents"
headers = {"Authorization": f"Bearer {token}"}
# CRITICAL: do NOT set Content-Type yourself here.
# requests generates it WITH the boundary string. If you set it manually,
# the boundary is missing and the server cannot parse the body.

with open("/home/ravi/invoice.pdf", "rb") as f:      # rb = read binary
    files = {
        "file": ("invoice.pdf", f, "application/pdf")
        #        (filename,     fileobj, content type)
    }
    data = {                                          # normal text fields
        "title": "Invoice March 2026",
        "category": "finance"
    }
    response = requests.post(url, headers=headers, files=files, data=data)

print(response.status_code, response.json())
```

JavaScript (browser — e.g., a file the user picked with `<input type="file">`):

```javascript
const fileInput = document.querySelector("#pdf-input");
const formData = new FormData();
formData.append("title", "Invoice March 2026");
formData.append("category", "finance");
formData.append("file", fileInput.files[0]);   // the PDF

const response = await fetch("https://api.example.com/api/v1/documents", {
  method: "POST",
  headers: { "Authorization": `Bearer ${token}` },
  // Do NOT set Content-Type — the browser adds it with the boundary.
  body: formData
});
```

### Uploading multiple files

```python
files = [
    ("files", ("invoice1.pdf", open("invoice1.pdf", "rb"), "application/pdf")),
    ("files", ("invoice2.pdf", open("invoice2.pdf", "rb"), "application/pdf")),
]
response = requests.post(url, headers=headers, files=files)
```

### The server side (FastAPI), so you see both halves

```python
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post("/api/v1/documents")
async def upload(title: str = Form(...),
                 category: str = Form(...),
                 file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDFs allowed"}
    content = await file.read()
    saved_path = save_to_storage(file.filename, content)   # pseudo: S3 etc.
    return {"title": title, "size_bytes": len(content), "path": saved_path}
```

### Alternative upload styles you will meet in the wild

1. **Raw body upload** — the file IS the whole body, no form fields:
   ```python
   with open("photo.jpg", "rb") as f:
       requests.put(url, data=f, headers={"Content-Type": "image/jpeg"})
   ```
2. **Presigned URL (the big-company pattern)** — your API returns a temporary
   S3 URL; the client uploads DIRECTLY to storage, bypassing your servers.
   This is how WhatsApp/Instagram scale media upload:
   ```python
   presigned = requests.post(api + "/uploads/presign",
                             json={"filename": "video.mp4"}, headers=headers).json()
   with open("video.mp4", "rb") as f:
       requests.put(presigned["url"], data=f)      # straight to S3
   requests.post(api + "/uploads/complete",
                 json={"upload_id": presigned["id"]}, headers=headers)
   ```
3. **Base64 in JSON** — file bytes encoded as text inside JSON. Simple but adds ~33% size; fine for small images, wrong for videos.

## 1.7 Downloading files

```python
# stream=True: do not load a 2 GB file into RAM at once
with requests.get("https://api.example.com/reports/annual.pdf",
                  headers=headers, stream=True) as r:
    r.raise_for_status()
    with open("annual.pdf", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
```

```bash
curl -H "Authorization: Bearer $TOKEN" -o annual.pdf \
     https://api.example.com/reports/annual.pdf
```

## 1.8 Production-grade calling: timeouts, retries, error handling

Copy this template — it is the difference between a script and professional code:

```python
import time
import requests

def call_api(method, url, *, headers=None, max_retries=3, **kwargs):
    """Call an API with timeout, retry on transient failures, and clear errors."""
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method, url,
                headers=headers,
                timeout=(3, 10),     # (connect timeout, read timeout) — ALWAYS set;
                **kwargs             # default is infinite and will hang your service
            )
        except requests.exceptions.Timeout:
            wait = 2 ** attempt      # 1s, 2s, 4s — exponential backoff
            time.sleep(wait)
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(2 ** attempt)
            continue

        if response.status_code == 429:                 # rate limited
            wait = int(response.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        if response.status_code >= 500:                 # server error: retry helps
            time.sleep(2 ** attempt)
            continue

        return response          # 2xx and 4xx come back to the caller;
                                 # 4xx means FIX THE REQUEST, retrying won't help

    raise RuntimeError(f"API failed after {max_retries} attempts: {url}")


resp = call_api("GET", "https://api.example.com/orders",
                headers={"Authorization": f"Bearer {token}"})
resp.raise_for_status()          # raises an exception on 4xx/5xx
orders = resp.json()
```

Rules encoded above, worth memorizing:
1. Always set a timeout. The default in most libraries is "wait forever."
2. Retry only what retrying can fix: timeouts, connection errors, 429, 5xx.
3. Never blindly retry a non-idempotent POST — you may create duplicates. Use idempotency keys (send header `Idempotency-Key: <uuid4>`).
4. Exponential backoff with jitter, so a thousand failing clients do not retry in sync and stampede the server.
5. Respect `Retry-After` on 429.

## 1.9 Consuming paginated APIs

```python
def fetch_all_products(base_url, headers):
    products, cursor = [], None
    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor
        page = requests.get(f"{base_url}/products", params=params,
                            headers=headers, timeout=10).json()
        products.extend(page["items"])
        cursor = page.get("next_cursor")
        if not cursor:
            return products
```

---

# PART 2 — THE NEW HTTP QUERY METHOD (RFC 10008)

You heard right: after decades of GET/POST/PUT/PATCH/DELETE, HTTP got a new core method. In June 2026 the IETF published RFC 10008 as a Proposed Standard, adding QUERY to the official HTTP Method Registry, registered as both safe and idempotent.

## 2.1 The problem it solves (first principles)

For complex read-only queries you always had two bad options:

**Option A — GET with a giant URL.**
```
GET /products?filters=%7B%22price%22%3A%7B%22lt%22... (2000 characters)
```
Problems: URLs have practical length limits (roughly 2,000–8,000 characters across browsers and proxies), structured data is ugly to URL-encode, and URLs leak into server logs, browser history, and bookmarks — bad if the query contains anything sensitive.

**Option B — POST with a JSON body** (what everyone actually does: `POST /search`).
Problem: POST throws away GET's guarantees. Caches, proxies, and clients cannot know a POST is read-only, so nothing caches it and nothing retries it safely. The semantics are lost.

## 2.2 What QUERY is

QUERY = the request semantics of GET + the request body of POST.

```
QUERY /products HTTP/1.1
Host: api.shop.com
Content-Type: application/json
Accept: application/json

{
  "filters": {"category": "phones", "price": {"lt": 50000}},
  "sort": [{"field": "rating", "order": "desc"}],
  "limit": 20
}
```

Properties, straight from the RFC:
- **Safe**: it never changes server state — declared at the protocol level, so any generic client, proxy, or cache can rely on it without reading your API docs.
- **Idempotent**: safe to retry automatically after a connection failure.
- **Cacheable**: responses can be cached, with the request body forming part of the cache key.
- The server can return a `Location` header pointing to a URI you can later GET to re-run the same query without resending the body — turning an expensive QUERY into a cheap cacheable GET.
- Discovery: servers advertise support via `Allow: GET, QUERY, OPTIONS, HEAD` and advertise accepted body formats via a new `Accept-Query` response header.
- In browsers, QUERY is not a CORS-safelisted method, so cross-origin JavaScript calls trigger a preflight OPTIONS request.

## 2.3 Comparison table (memorize this for interviews)

| Property | GET | POST | QUERY |
|----------|-----|------|-------|
| Request body | No (by convention) | Yes | Yes |
| Safe | Yes | No | Yes |
| Idempotent | Yes | No | Yes |
| Cacheable | Yes | Rarely/complicated | Yes (body in cache key) |
| Best for | Simple reads | Creation, actions | Complex read-only queries |

## 2.4 Calling it today

```bash
curl -X QUERY https://api.shop.com/products \
  -H "Content-Type: application/json" \
  -d '{"filters": {"category": "phones"}, "limit": 20}'
```

```python
# requests supports arbitrary methods:
response = requests.request("QUERY", "https://api.shop.com/products",
                            json={"filters": {"category": "phones"}, "limit": 20})
```

## 2.5 Adoption reality (say this in interviews to sound senior)

Being a Proposed Standard does not mean it works everywhere yet. Adoption depends on frameworks, proxies, CDNs, WAFs, and browsers adding support; OpenAPI 3.2 already supports describing QUERY endpoints. There are also fresh security considerations: WAF and CSRF rules written before June 2026 often list only GET/POST/PUT/PATCH/DELETE and may handle QUERY inconsistently, and caches must include the request body in the cache key or risk cache poisoning. Until your whole chain (CDN, load balancer, framework) handles QUERY deliberately, `POST /search` remains the pragmatic choice — but expect QUERY to become the standard answer for complex reads.

Interview one-liner: "QUERY (RFC 10008, June 2026) fills the historical gap between GET and POST: a safe, idempotent, cacheable method that carries a request body — ideal for complex filters and search."

---

# PART 3 — DEEP DIFFERENCES: REST vs SSE vs WEBSOCKETS vs gRPC (+ GraphQL, Webhooks)

## 3.1 The master comparison table

| Dimension | REST | SSE | WebSockets | gRPC |
|-----------|------|-----|------------|------|
| Communication model | Request -> response | Server -> client stream (one-way) | Full duplex (two-way, anytime) | RPC calls + all 4 streaming modes |
| Underlying protocol | HTTP/1.1 or HTTP/2 | HTTP (long-lived response) | Own protocol after HTTP Upgrade handshake | HTTP/2 |
| Data format | Usually JSON (text) | Text events (usually JSON) | Text or binary frames | Protobuf (binary) |
| Connection | New/reused per request; stateless | One persistent connection | One persistent connection; stateful | Persistent HTTP/2 channel, multiplexed |
| Who initiates messages | Client only | Client opens; then server only | Both sides | Both sides (in streaming modes) |
| Browser support | Native | Native (EventSource) | Native (WebSocket) | Not native (needs grpc-web + proxy) |
| Auto-reconnect | N/A | Built into browsers | You implement it | You configure it (channel policies) |
| Caching | Excellent (GET/QUERY) | No | No | No (by design; add your own) |
| Contract | Loose (OpenAPI optional) | Loose | None (you invent message format) | Strict (.proto, compile-time checked) |
| Human debuggable | Yes (curl) | Yes (curl works) | Harder (need ws tools) | Hardest (binary; grpcurl) |
| Load balancing | Trivial (stateless) | Moderate (long connections) | Hard (sticky state, needs pub/sub backbone) | Moderate (L7 balancing needed for HTTP/2) |
| Typical latency overhead per message | Highest (headers each request) | Low after connect | Lowest | Very low + fast serialization |
| Best at | CRUD, public APIs | Server push: notifications, streams of updates | Real-time bidirectional: chat, games, trading | Internal service-to-service, high RPS |

## 3.2 The differences that actually matter (explained, not just tabled)

**Direction of data flow** is the first filter:
- Client asks, server answers, done -> REST.
- Server needs to push, client mostly listens -> SSE.
- Both sides talk continuously -> WebSockets.
- Machine-to-machine function calls inside your infrastructure -> gRPC.

**State** is the second filter. REST is stateless: any server can answer any request, so scaling is "add more servers." SSE and WebSockets hold open connections in server memory: scaling now requires connection-aware load balancing and a pub/sub layer (Redis/Kafka) to route messages between servers. This single difference explains most of the operational cost gap.

**Contract strictness** is the third. REST + JSON fails at runtime when someone renames a field. gRPC's .proto fails at compile time. For 50 microservices maintained by 20 teams, compile-time failure is worth the tooling cost; for a public API consumed by unknown developers, JSON's flexibility and debuggability win.

**Efficiency**: one REST call carries ~200–800 bytes of headers. For a mobile app fetching a screen once, irrelevant. For services exchanging 50,000 messages/second, it is the whole game — hence gRPC (binary protobuf, header compression, multiplexed HTTP/2) internally.

## 3.3 SSE vs WebSockets — the classic interview face-off

They overlap (both push from server), so interviewers love this one.

| Question to ask yourself | If answer is... | Choose |
|--------------------------|-----------------|--------|
| Does the client need to SEND data on the same channel frequently? | No | SSE |
| | Yes | WebSockets |
| Do you want automatic reconnection for free? | Yes | SSE |
| Do you need binary data (audio, game state)? | Yes | WebSockets |
| Do you want it to pass through every proxy/firewall as plain HTTP? | Yes | SSE |
| Is sub-100ms two-way latency critical? | Yes | WebSockets |

Real mapping: ChatGPT-style token streaming, order tracking, live scores, notification feeds = SSE. Chat apps, multiplayer games, collaborative editing, trading terminals = WebSockets. A very common professional mistake is choosing WebSockets when SSE would do — you inherit reconnection logic, heartbeats, and sticky-session load balancing for nothing.

## 3.4 REST vs gRPC — the second classic

- Consumer is a browser or unknown third parties -> REST (native support, curl-able, cacheable).
- Consumer is your own services -> gRPC (typed contract, 5–10x less bandwidth, streaming built in).
- Standard industry answer: "REST at the edge, gRPC inside." The API gateway speaks REST/JSON to the world and gRPC to internal services.

## 3.5 GraphQL (one-paragraph literacy, because interviews ask)

GraphQL is an alternative to REST for the client-facing edge: one endpoint (`POST /graphql`), and the CLIENT specifies exactly which fields it wants in a query language. Solves REST's over-fetching (getting 40 fields when you need 3) and under-fetching (needing 4 REST calls to render one screen — GraphQL does it in 1). Costs: caching is harder (everything is POST — note that QUERY may improve this), server complexity is higher (N+1 query problem, needs dataloaders), and rate limiting is per-query-cost not per-request. Used by GitHub's public API, Facebook, Shopify. Interview answer for "REST vs GraphQL": "GraphQL when diverse clients (mobile/web/watch) need different shapes of the same data; REST when resources are stable and cacheability matters."

## 3.6 Webhooks (the reverse API)

A webhook is the server calling YOU: you register a URL, and the provider POSTs to it when an event happens. Razorpay calls `POST https://yourapp.com/webhooks/payment` when a payment settles — the opposite of you polling Razorpay. Rules: verify the signature header (anyone can POST to your public URL), respond 200 quickly and process asynchronously (queue it), and handle duplicate deliveries idempotently because providers retry. Webhooks vs SSE/WebSockets: webhooks are server-to-SERVER push (your backend has a public URL); SSE/WS are server-to-CLIENT push (browsers/apps cannot receive webhooks).

---

# PART 4 — INTERVIEW QUESTIONS AND ANSWERS

Organized by level. Answers are written the way strong candidates actually speak.

## 4.1 Basics (screening round)

**Q1. What is an API?**
A contract that lets two programs communicate: it defines what requests a server accepts and what responses it returns, hiding the implementation. Example: Swiggy's app renders whatever `GET /restaurants` returns without knowing anything about Swiggy's database.

**Q2. What is REST? What makes an API RESTful?**
An architectural style where everything is a resource identified by a URL, manipulated through standard HTTP methods, with stateless requests. RESTful in practice: nouns in URLs (`/orders/5`, not `/getOrder`), correct methods, correct status codes, stateless auth on each request, and cacheable reads.

**Q3. Difference between PUT and PATCH?**
PUT replaces the entire resource — you send the full object; missing fields are removed; it is idempotent. PATCH updates only the fields you send. Sending `{"name": "Ravi"}` via PUT wipes every other field; via PATCH it changes only the name.

**Q4. Difference between PUT and POST?**
POST creates a new member of a collection (`POST /orders` — server assigns the ID) and is not idempotent: two calls create two orders. PUT writes to a specific URI you name (`PUT /orders/5`) and is idempotent: repeating it yields the same final state.

**Q5. What do 401 and 403 mean, and how do they differ?**
401 Unauthorized: we don't know who you are — missing/invalid/expired credentials; fix by logging in or refreshing the token. 403 Forbidden: we know exactly who you are, and you're not allowed — a customer token calling an admin endpoint. 401 = authentication failed, 403 = authorization failed.

**Q6. What is the difference between authentication and authorization?**
Authentication = verifying identity (who are you) — login, tokens. Authorization = verifying permissions (what can you do) — roles, resource ownership. Airport analogy: passport check is authentication; the boarding pass deciding which gate you may enter is authorization.

**Q7. Why is HTTP called stateless, and why does it matter?**
The server retains nothing between requests; each request carries everything needed (including the auth token). It matters because any server in a fleet can serve any request — that is what makes horizontal scaling and simple load balancing possible.

**Q8. What is JSON and why do APIs use it?**
A lightweight text format for structured data (objects, arrays, strings, numbers, booleans, null). Used because it is human-readable, native to JavaScript, and supported by every language. Trade-off: as text it is bigger and slower to parse than binary formats like protobuf — which is why internal high-throughput systems use gRPC.

## 4.2 Intermediate (the round that filters most candidates)

**Q9. What are safe and idempotent methods? Why does idempotency matter?**
Safe = no state change on the server (GET, HEAD, OPTIONS, QUERY). Idempotent = repeating the request produces the same final state (GET, PUT, DELETE, QUERY — not POST, not usually PATCH). It matters because networks fail and clients/proxies retry: idempotent requests can be retried blindly; non-idempotent ones can cause duplicates (double payment). That distinction drives retry policy in every production client.

**Q10. A user clicks "Pay" twice and two orders are created. Fix it.**
Idempotency keys. The client generates a UUID per checkout attempt and sends it as `Idempotency-Key` on the POST. The server stores key -> response; on a duplicate key it returns the stored response instead of processing again. Stripe and Razorpay work exactly this way. Bonus: the frontend also disables the button, but the server-side key is the real guarantee — never trust the client.

**Q11. How does JWT authentication work end to end?**
Login: server verifies credentials and returns a signed JWT (header.payload.signature) containing user_id, roles, expiry — signed with the server's secret so it cannot be forged. Every request: client sends `Authorization: Bearer <jwt>`; the server verifies the signature and expiry locally, no DB lookup — which is why JWTs scale. Weakness: a stolen JWT works until expiry and stateless JWTs cannot be revoked; hence short-lived access tokens (15 min) plus rotating refresh tokens stored server-side (revocable), and optionally a Redis denylist for instant logout.

**Q12. Where would you store a JWT in a browser app?**
localStorage is readable by any JavaScript on the page, so an XSS bug leaks the token. Prefer an httpOnly, Secure, SameSite cookie — JavaScript cannot read it, mitigating XSS theft, at the cost of needing CSRF protection (SameSite + CSRF tokens). Strong answer: httpOnly cookie for the refresh token, access token held only in memory.

**Q13. Explain cursor vs offset pagination and when offset breaks.**
Offset (`?page=500&limit=20`) makes the DB scan and discard 10,000 rows — slow — and if rows are inserted between page loads, items shift and you see duplicates/misses. Cursor pagination returns an opaque pointer to the last item (`?cursor=abc`), letting the DB seek directly via an index — constant time, consistent under writes. Use offset only for small, mostly-static datasets; cursors for feeds and infinite scroll (how Twitter/Instagram feeds work).

**Q14. What is rate limiting and how would you implement it?**
Restricting requests per client per window (e.g., 100/min) to protect against abuse and overload; exceeding it returns 429 with Retry-After. Implementation: Redis, key `rate:{user_id}`, sliding-window counter or token-bucket; token bucket allows short bursts while capping average rate. Apply at the gateway so app servers never see the excess.

**Q15. What is CORS and why does the browser block your API call?**
Browsers enforce the same-origin policy: JavaScript on site A cannot read responses from domain B unless B opts in via CORS headers (`Access-Control-Allow-Origin`, etc.). For non-simple requests the browser sends a preflight OPTIONS first. Key insight interviewers probe: CORS is a browser-enforced protection for users; curl and server-to-server calls ignore it entirely — it is not server security.

**Q16. How do you version an API, and why?**
Because shipped mobile apps keep calling the old contract for months, breaking changes need a new version while the old one keeps running. URL versioning (`/api/v1/`) is most common and visible; header versioning (`Accept: application/vnd.api+json;version=2`) is cleaner but hidden. Also: additive changes (new optional fields) do not need a new version — design clients to ignore unknown fields.

**Q17. What's new in HTTP methods? (or: is GET getting an update?)**
RFC 10008, published June 2026, standardized QUERY: safe and idempotent like GET, but with a request body like POST, and cacheable with the body as part of the cache key. It solves the "complex search" dilemma where GET hits URL length/logging limits and POST loses cacheability and retry-safety. Adoption is early — frameworks, CDNs, and WAFs are still adding deliberate support — so `POST /search` remains common in production, but QUERY is the standards-track answer. Mentioning this signals you follow the field.

## 4.3 Advanced (senior/system-design rounds)

**Q18. REST vs gRPC — when and why?**
gRPC: binary protobuf over HTTP/2 with a compile-time contract and built-in streaming — 5–10x smaller payloads and much faster serialization; but browsers cannot call it natively and it is not curl-debuggable. Decision: REST (or GraphQL) at the public edge for compatibility and cacheability; gRPC between internal microservices for performance and type safety. Netflix/Uber pattern: gateway translates external REST to internal gRPC.

**Q19. SSE vs WebSockets vs polling for a live order-tracking feature?**
Polling: simplest, but wasteful and up to interval-seconds stale — acceptable fallback only. WebSockets: full duplex, but the client only listens here, so you would pay for stateful connections, custom reconnection, and sticky load balancing you don't need. SSE is the fit: one-way server push over plain HTTP, native browser auto-reconnect, proxy-friendly. Principle: choose the least powerful tool that meets the requirement — it is the cheapest to operate.

**Q20. How do WebSockets scale across multiple servers?**
The problem: user A is connected to server 1, user B to server 2; a message from A must reach B. Solution: a pub/sub backbone — servers publish messages to Redis Pub/Sub or Kafka, and every server subscribed to the relevant channel delivers to its local connections. Plus: connection-aware load balancing, heartbeats to reap dead connections, and a presence store (Redis) mapping user -> server. This added infrastructure is exactly why you avoid WebSockets when SSE suffices.

**Q21. Design the API for file upload at Instagram scale.**
Direct-through-API uploads make app servers shuffle gigabytes — waste. Use presigned URLs: (1) `POST /uploads/init` with filename/size/type returns a short-lived presigned S3 URL + upload_id; (2) client PUTs bytes directly to storage; (3) `POST /uploads/complete` triggers async processing (virus scan, transcode, thumbnails) via a queue; client learns completion via SSE/webhook/polling. For big files: multipart chunked upload with per-chunk retry. API servers never touch the bytes.

**Q22. A third-party API you depend on becomes slow. Protect your service.**
Timeouts first (never wait forever), retries with exponential backoff and jitter for transient failures only. Circuit breaker: after N consecutive failures, open the circuit and fail fast for a cooldown instead of piling threads onto a dying dependency; half-open to probe recovery. Bulkheads: cap concurrent calls to that dependency so it cannot exhaust your workers. Graceful degradation: serve cached/stale data or hide the widget. Keywords that score: timeout, retry+backoff+jitter, circuit breaker, bulkhead, fallback.

**Q23. How would you secure a public REST API? (checklist answer)**
HTTPS only; short-lived JWT auth + refresh rotation; authorization checks at the resource level (user can only read own orders — prevents IDOR/BOLA, the #1 API vulnerability); input validation via schemas; rate limiting per user and IP; no secrets or stack traces in responses; security headers; audit logging with trace IDs; secrets in env/vault, never code; and don't expose sequential integer IDs for sensitive resources — use UUIDs.

**Q24. What is HATEOAS? Is it used in practice?**
Hypermedia As The Engine Of Application State — responses include links to available next actions (`"links": {"cancel": "/orders/5/cancel"}`), so clients navigate the API like a website instead of hardcoding URLs. Honest answer interviewers respect: it is the highest level of the Richardson Maturity Model, but most real-world APIs stop at level 2 (resources + verbs + status codes) because generated SDKs and OpenAPI docs solve discoverability more practically.

**Q25. Explain what happens end-to-end when you call an API from your phone.**
DNS resolves api.example.com to an IP (via cached resolvers). TCP handshake, then TLS handshake (certificate verification, key exchange) — or QUIC over UDP if HTTP/3. The HTTP request hits a CDN/edge, then a load balancer, which picks an app server. Middleware runs: auth verification, rate limit, logging with a trace ID. Handler validates input, calls services/DB (possibly via gRPC), builds the response. Response travels back; client checks status, parses JSON, renders. Mentioning where caching can short-circuit (CDN for GET) and where failures occur (each hop needs a timeout) marks seniority.

## 4.4 Rapid-fire traps (one-line answers)

- **Can GET have a body?** Technically not forbidden, but servers/proxies may ignore or reject it — never rely on it. The correct tool for "read with a body" is now QUERY (RFC 10008).
- **Is PATCH idempotent?** Not guaranteed. `{"qty": 5}` is; an increment operation is not.
- **Is DELETE returning 404 on retry a violation of idempotency?** No — idempotency is about final server state, not identical responses.
- **Does HTTPS encrypt the URL?** Path and query are encrypted in transit, but URLs still land in server logs and browser history — so still no secrets in URLs.
- **Difference between 301 and 302?** Permanent vs temporary redirect; browsers/CDNs cache 301 aggressively.
- **What is a preflight request?** The browser's automatic OPTIONS call before non-simple cross-origin requests, asking the server which methods/headers are allowed.
- **Why JSON over XML?** Less verbose, maps directly to language data structures, native in JS. XML survives in enterprise/SOAP and document markup.
- **Status code for "logged in but not allowed"?** 403.
- **Status code for creating a resource?** 201 with a Location header.
- **What does Bearer mean in `Authorization: Bearer`?** "Whoever bears (holds) this token is granted access" — possession is proof, which is why tokens must be protected and short-lived.

---

# APPENDIX — HANDS-ON DRILL PLAN

Do these in order; each takes under an hour:

1. Call the free GitHub API with curl and Python: GET a user, list repos with query params, handle 404.
2. Get a free API key (e.g., a weather API) and call it with the key in a header from Python, reading the key from an environment variable.
3. Write the production `call_api` wrapper from section 1.8 and test it against an endpoint that returns 500 (use httpbin.org/status/500).
4. Build the FastAPI upload endpoint from section 1.6 and upload a real PDF to it with curl, Python, and a small HTML form.
5. Implement login -> access token -> call protected endpoint -> force expiry -> refresh -> retry.
6. Send a QUERY request with `requests.request("QUERY", ...)` to your own FastAPI app (add a route with `@app.api_route("/search", methods=["QUERY"])`) and see it work.
7. Answer every interview question in Part 4 out loud without reading the answer. Anything you stumble on, rebuild the example for it.

The interview questions test exactly what the drills build. Build first, then the answers become things you have seen, not things you memorized.
