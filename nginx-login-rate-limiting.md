# Nginx Login Rate Limiting Best Practices

## Overview

Rate limiting login endpoints is critical for protecting against brute-force attacks. This document covers the best practices for implementing login rate limiting in nginx, specifically which HTTP methods to limit.

## Key Decision: Which Methods to Rate Limit?

### Recommendation: All Methods EXCEPT GET

```nginx
map $request_method $login_limit_key {
    GET     "";                      # Empty key = no rate limit
    default $binary_remote_addr;     # Rate limit all other methods
}
limit_req_zone $login_limit_key zone=login:10m rate=5r/m;
```

### Rationale

| Method | Purpose | Should Rate Limit? |
|--------|---------|-------------------|
| **GET** | Display login form | No - safe, improves UX |
| **POST** | Submit credentials | Yes - primary attack vector |
| **PUT** | Potential auth attempt | Yes - defense in depth |
| **PATCH** | Potential auth attempt | Yes - defense in depth |
| **DELETE** | Unusual but possible | Yes - defense in depth |

**Why not POST-only?**
- POST-only works but is less defensive
- Future app changes might introduce alternative auth methods
- Non-standard clients might use PUT/PATCH
- Negligible overhead to limit all non-GET methods

**Why exclude GET?**
- GET only displays the login form (no credential transmission)
- Users should be able to refresh the login page freely
- Rate limiting GET would hurt UX without security benefit

## Implementation

### NixOS Configuration

```nix
services.nginx = {
  appendHttpConfig = ''
    # Standard rate limiting zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req_status 429;  # Return 429 instead of 503

    # Login endpoint rate limiting - all methods EXCEPT GET
    map $request_method $login_limit_key {
      GET     "";
      default $binary_remote_addr;
    }
    limit_req_zone $login_limit_key zone=login:10m rate=5r/m;
  '';

  virtualHosts."app.example.com" = {
    locations."/login" = {
      proxyPass = "http://127.0.0.1:8080";
      extraConfig = ''
        # Nginx locations are mutually exclusive - this location won't inherit
        # rate limits from "/". We need both zones here.
        # See: https://nginx.org/en/docs/http/ngx_http_core_module.html#location
        limit_req zone=login burst=3 nodelay;  # Strict for POST/PUT/PATCH/DELETE
        limit_req zone=api burst=20 nodelay;   # Standard limit for GET
        limit_conn conn_limit 5;
      '';
    };
  };
};
```

### Important: Location Mutual Exclusivity

Nginx locations are **mutually exclusive**. When a request matches `/login`, it does NOT inherit rate limits from the `/` location. This means login endpoints need their own complete rate limiting configuration.

From the [nginx documentation](https://nginx.org/en/docs/http/ngx_http_core_module.html#location):
> "To find location matching a given request, nginx first checks locations defined using the prefix strings... the location with the longest matching prefix is selected and remembered. Then regular expressions are checked..."

Once a location is selected, only that location's directives apply.

### Key Configuration Options

| Option | Value | Purpose |
|--------|-------|---------|
| `rate=5r/m` | 5 requests/minute | Strict limit for login attempts |
| `burst=3` | 3 extra requests | Small buffer for legitimate retries |
| `nodelay` | Immediate rejection | Don't queue excess requests |
| `limit_req_status 429` | HTTP 429 | Proper "Too Many Requests" response |

## Identifying the Correct Login Endpoint

**Critical**: Rate limit the actual authentication endpoint, not just the login page URL.

| Application | Login Endpoint | Notes |
|-------------|---------------|-------|
| **Umami** | `/api/auth/login` | Next.js API route |
| **GlitchTip** | `/login` | Django form POST |
| **Django apps** | `/login` or `/accounts/login/` | Check django-allauth config |
| **FastAPI** | `/api/auth/login` or `/token` | Depends on implementation |
| **Uptime Kuma** | WebSocket | Cannot rate limit with nginx |

### How to Verify

Test each potential endpoint:

```bash
# Test which methods are accepted
for method in GET POST PUT PATCH; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X $method https://app.example.com/login)
  echo "$method: HTTP $code"
done
```

- `401/403` = Valid endpoint (bad credentials / CSRF)
- `405` = Method not allowed
- `404` = Endpoint doesn't exist

## Defense in Depth

Rate limiting should be combined with other protections:

### 1. fail2ban Integration

fail2ban monitors nginx logs and bans IPs that trigger too many rate limit errors:

```nix
services.fail2ban.jails.nginx-limit-req = ''
  enabled = true
  port = http,https
  backend = systemd
  journalmatch = _SYSTEMD_UNIT=nginx.service + _COMM=nginx
  maxretry = 5
  bantime = 1h
'';
```

### 2. Two-Factor Authentication (2FA)

Even if rate limiting is bypassed, 2FA prevents unauthorized access:
- Umami: Supports TOTP
- GlitchTip: Supports TOTP
- Uptime Kuma: Supports TOTP (essential since WebSocket auth can't be rate limited)

### 3. Connection Limiting

Limit concurrent connections per IP on login endpoints:

```nginx
limit_conn conn_limit 5;
```

## Testing Rate Limits

### Verify Rate Limiting Works

```bash
# Should see 401/403 for first ~4 requests, then 429
for i in {1..8}; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    https://app.example.com/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"test"}')
  echo "Request $i: HTTP $code"
done
```

Expected output:
```
Request 1: HTTP 401
Request 2: HTTP 401
Request 3: HTTP 401
Request 4: HTTP 401
Request 5: HTTP 429
Request 6: HTTP 429
...
```

### Verify GET is Not Limited

```bash
# Should never see 429
for i in {1..10}; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X GET https://app.example.com/login)
  echo "GET $i: HTTP $code"
done
```

### Reset Rate Limits (for testing)

```bash
# Restart nginx to clear rate limit zones
sudo systemctl restart nginx

# Unban from fail2ban if needed
sudo fail2ban-client set nginx-limit-req unbanip <IP>
```

## Special Cases

### WebSocket Authentication (Uptime Kuma)

Some applications use WebSocket for authentication (e.g., Uptime Kuma uses Socket.io). nginx HTTP rate limiting cannot protect these endpoints.

**Mitigations:**
- Enable 2FA (essential)
- Use connection limiting (`limit_conn`)
- Strong passwords
- fail2ban monitoring (if app logs failed attempts)

### API Token Authentication

For APIs using bearer tokens instead of username/password:
- Rate limit the token generation endpoint
- Consider shorter token lifetimes
- Implement token rotation

## References

- [Rate limiting: another way I guard against brute-force logins](https://ethitter.com/2016/05/rate-limiting-another-way-i-guard-against-brute-force-logins/)
- [NGINX Rate Limiting - Community Blog](https://blog.nginx.org/blog/rate-limiting-nginx)
- [Nginx brute force protection](https://bobcares.com/blog/nginx-brute-force-protection/)
- [Umami Authentication API](https://umami.is/docs/api/authentication)

## Changelog

- **2026-01-05**: Initial version based on implementation for analytics.test001.nl and errors.test001.nl
