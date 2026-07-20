# Ticket: Optional discrete GPU for Cromwell Ollama (Thelio Mira)

**Status:** Proposed  
**Priority:** unset
**Context:** Hardware diagnosis 2026-07-09 — sawtooth-ai has empty PCIe slots; only Raphael iGPU (2 GiB). CPU path is correct today but caps interactive + cron latency.

## Scope (decision + install, not code-first)

- [ ] Choose NVIDIA vs AMD dGPU for Ollama (compose wiring differs: CUDA vs ROCm image)  
- [ ] Install card in Thelio Mira empty slot  
- [ ] Update `compose.yml` ollama service devices / image tag  
- [ ] Re-benchmark tool-bearing agent turns; raise model size if desired (e.g. 8b)  
- [ ] Document in `ecosystem/deployment/README.md`  

## Out of scope

- Trying to use Raphael iGPU for production LLM  

## Related

- `docs/session-reports/2026-07-09-1410-cromwell-cpu-tuning-and-watchdog.md`  
- `docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
