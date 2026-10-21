---
name: tailscale-preview
description: Publish and verify local web app previews privately over Tailscale Serve so users can review them from other authorized computers or mobile devices. Use when an agent needs to provide a review URL for a local development server, dashboard, prototype, or web application across devices.
compatibility: Requires a shell, Tailscale CLI, a connected tailnet, and an authorized local web service. Works on macOS and Linux with compatible Tailscale versions.
---

# Tailscale Preview

Provide a usable HTTPS review URL over the user's private Tailscale network rather than presenting `localhost` as the only review address.

## Boundaries

- Use **Tailscale Serve**, never Funnel, public reverse proxies, public tunnels, or firewall changes as substitutes without explicit authorization.
- Keep `localhost` for internal application communication and local testing. The rule concerns **links delivered to the user for cross-device review**.
- Only publish applications the user has authorized for remote review. If authorization for the specific application is unclear, ask before exposing it to the tailnet. Do not publish administrative interfaces, sensitive datasets, credentials, internal APIs, or production control panels by default.
- Tailnet access is not restricted to a single person by default; access depends on Tailscale policies and grants. Do not claim per-user restriction without checking it.
- Never alter ACLs, grants, device sharing, HTTPS settings, Funnel settings, or Tailscale identity automatically.
- Never reset an existing Serve configuration, overwrite another application's route, or shut down a preexisting service to make room for a preview. If there is a conflict, report it and request approval for the specific change.
- Do not install Tailscale, change permissions, or run privileged commands without authorization.
- Do not assume the agent can verify access from the user's actual phone. Report the scope of verification accurately.

## Workflow

### 1. Discover the local application

1. Identify the application root, startup command, target host, and local port from the existing project.
2. Confirm that the application is running and that its HTTP endpoint responds. Use an app-specific health route if known. Otherwise, test the home page.
3. Avoid changing a working app's listening interface to `0.0.0.0` solely for Tailscale Serve; a loopback-bound application is generally preferable.
4. Check whether the preview includes confidential information, debug endpoints, secrets, or administrative functionality. Stop and explain the exposure risk if so.

Example read-only verification (replace `3000` with the real port):

```sh
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:3000/
```

An HTTP error can be valid application behavior; inspect the response rather than treating every non-2xx result as a network failure.

### 2. Check prerequisites and configuration

```sh
command -v tailscale
tailscale version
tailscale status
tailscale serve status
```

- Check whether the device is connected to the correct tailnet.
- Inspect existing Serve assignments before any modification.
- Check whether the intended HTTPS route or port is already in use.
- If Serve is unavailable, not configured, or requires an interactive HTTPS setup, explain the exact blocker; ask authorization before changing device or tailnet settings.
- Consult the installed CLI help and current Tailscale documentation if version-specific syntax differs.

### 3. Start an authorized preview

If the application is authorized, the port is correct, and the chosen HTTPS route is free, use:

```sh
tailscale serve --bg 3000
```

Use the actual port, not the example. `--bg` makes the Serve assignment persistent until disabled; it does **not** keep the web application running. If persistent publication is not desired, use foreground operation managed by the current terminal/session instead.

Do not execute the example if a default HTTPS route is already occupied or if the resulting change could displace another route. Preserve existing routes and ask for authorization before choosing or altering a conflicting mapping.

### 4. Verify the delivered URL

```sh
tailscale serve status
```

1. Read the **actual** HTTPS URL from the Serve output. Never invent or construct a URL from an assumed hostname.
2. Check that the local application remains healthy.
3. Attempt an HTTPS request to the reported URL from the hosting machine, if networking permits. Note that success from the host is **not** proof that a second device can connect.
4. If another authorized tailnet device or remote test environment is available, verify the URL from there; otherwise explicitly mark cross-device verification as untested and ask the user to open the URL on the target device.
5. Do not claim success when the target app fails, Serve is unconfigured, or the HTTPS URL is inaccessible.

### 5. Deliver the result

Return a concise report containing:

- **Preview URL:** the actual HTTPS URL, only after obtaining it from Serve.
- **Host and application:** device and project, if known.
- **Exposure:** private to the tailnet subject to its access rules; never claim public internet access.
- **Persistence:** whether Serve runs in the background; explain that the application must also stay running.
- **Checks:** local HTTP, Serve configuration, HTTPS from host, HTTPS from a different device—each marked passed, failed, or not tested.
- **Cleanup:** the precise disable command matched to the Serve flags/routes used, and any limitations.

### 6. Clean up on request

Read the current Serve status and documentation first. Disable **only the mapping created for this preview** by reversing the original Serve invocation with its corresponding `off` command, retaining the relevant flags where required. For a simple default mapping started with `tailscale serve --bg 3000`, the documented shutdown form is typically:

```sh
tailscale serve off
```

Use this only after confirming it will not affect another publication. Never run `tailscale serve reset` as routine cleanup: it removes all Serve configuration for the device. If the preview shares a route or configuration with other services, stop and report the conflict instead of deleting it.

## Failure handling

- **Tailscale missing, disconnected, or inaccessible:** report the blocker; do not silently substitute public hosting.
- **Application not running:** first use the project's normal startup procedure when authorized, then retest.
- **Route conflict:** preserve existing routes; present the exact collision without overwriting anything.
- **HTTPS setup or certificate unavailable:** do not disable security checks or force insecure public exposure.
- **Host works but phone fails:** inspect tailnet connectivity, access policies, DNS resolution, device status, and app lifetime without weakening permissions.
- **No shell/remote access:** give commands and instructions only. Do not claim deployment or verification occurred.

## Reference

- Tailscale Serve CLI: https://tailscale.com/docs/reference/tailscale-cli/serve
- Tailscale Serve examples: https://tailscale.com/docs/reference/examples/serve
- Agent Skills format: https://agentskills.io/specification
