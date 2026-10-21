## Cross-device web previews

When delivering an application for review on another device, use the `tailscale-preview` skill if it is installed and Tailscale is available. Supply the verified private HTTPS URL rather than only `localhost`. Do not expose applications without authorization, disrupt existing Serve configurations, or use Tailscale Funnel automatically. Clearly state what connectivity was actually tested.
