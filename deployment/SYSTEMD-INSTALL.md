# IBKR Client Portal Gateway — systemd --user installation

Optional: install CPGW as a systemd --user service so `run-ibkr-cpgw` can use systemctl commands and the CLI prefers managed lifecycle.

Also installs the CPGW Control Service (HTTP helper on 127.0.0.1:5500) for remote control from Fulfillment Desk / BG / Wv2.

## Install steps

1. **Copy the unit files:**

   ```bash
   mkdir -p ~/.config/systemd/user
   cp ~/sawtooth/ecosystem/deployment/ibkr-cpgw.service ~/.config/systemd/user/
   cp ~/sawtooth/ecosystem/deployment/cpgw-control.service ~/.config/systemd/user/
   ```

2. **Enable linger** (so the service persists after logout):

   ```bash
   loginctl enable-linger $USER
   ```

3. **Reload systemd and enable the services:**

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable ibkr-cpgw.service
   systemctl --user enable cpgw-control.service
   ```

4. **Verify installation:**

   ```bash
   ~/sawtooth/ecosystem/deployment/bin/run-ibkr-cpgw status
   ```

   You should see: `systemd:       enabled (status: inactive)`

5. **Start the services:**

   ```bash
   # Start CPGW
   ~/sawtooth/ecosystem/deployment/bin/run-ibkr-cpgw start
   
   # Start control service
   systemctl --user start cpgw-control.service
   ```

   Or directly via systemctl:

   ```bash
   systemctl --user start ibkr-cpgw.service
   systemctl --user start cpgw-control.service
   ```

## Usage after installation

Once installed and enabled, `run-ibkr-cpgw start`, `stop`, and `restart` will automatically use systemctl commands.

Check logs with:

```bash
# CPGW logs
journalctl --user -u ibkr-cpgw -f

# Control service logs
journalctl --user -u cpgw-control -f
```

Test the control service:

```bash
# Check status
curl http://127.0.0.1:5500/v1/cpgw/status

# From Docker (e.g. in BG/Wv2 console)
curl http://host.docker.internal:5500/v1/cpgw/status

# Restart (example)
curl -X POST http://127.0.0.1:5500/v1/cpgw/control \
  -H "Content-Type: application/json" \
  -d '{"action": "restart"}'
```

## Disable/uninstall

```bash
systemctl --user stop ibkr-cpgw.service cpgw-control.service
systemctl --user disable ibkr-cpgw.service cpgw-control.service
rm ~/.config/systemd/user/ibkr-cpgw.service
rm ~/.config/systemd/user/cpgw-control.service
systemctl --user daemon-reload
```

## Notes

- The unit files use `%h` to resolve to your home directory
- Assumes Winston estate is at `~/sawtooth/`
- Paper SSO still requires browser login after start/restart
- Keep-alive flag remains managed via `run-ibkr-cpgw keepalive on|off`
- Control service listens on **127.0.0.1:5500 only** (no external access)
- Control service has **no authentication** — relies on localhost-only binding
- No IBKR passwords stored or transmitted through the control service
