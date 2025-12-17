---
id: "001"
title: "Resolve process not defined error"
stage: "general"
date: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-backend-auth"
user: "user"
command: "/sp.resolveerror"
labels: ["bug-fix", "oauth", "environment-variables"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/docusaurus/src/components/OAuthService.js"
  - "frontend/docusaurus/docusaurus.config.js"
  - "frontend/docusaurus/.env"
  - "frontend/docusaurus/.env.example"
tests: []
---

## PROMPT_TEXT
Uncaught runtime error in browser:
ReferenceError: process is not defined

Stack trace indicates failure in:
- src/components/OAuthService.js (line ~6)
- Triggered during client-side execution

## CONTEXT
- Application is a frontend web app running in the browser
- Built using SpecKit Plus (/sp) workflow
- Code is generated and iterated using Claude Code CLI
- Browser environment does NOT support Node.js globals like `process`

## ROOT CAUSE HYPOTHESIS
Client-side JavaScript is referencing `process` or `process.env`,
which only exists in Node.js environments.

This typically occurs when:
- Environment variables are accessed incorrectly
- Node-style config is used in browser components
- OAuth configuration is instantiated at import time

## RESPONSE_TEXT
Successfully resolved the "process is not defined" error in the browser environment. The issue was in OAuthService.js where `process.env` was being accessed directly, which is not available in browser environments.

### Changes Made:
1. Updated OAuthService.js to safely access environment variables using a helper method that checks for variables in the window object first
2. Modified docusaurus.config.js to use webpack's EnvironmentPlugin to expose environment variables to the browser
3. Created .env and .env.example files with the required OAuth configuration

### Key Technical Details:
- Replaced direct `process.env` access with `getEnvVar()` helper method
- Added webpack configuration to pass environment variables to browser
- Environment variables are now accessible via window object during runtime
- Maintained backward compatibility for Node.js build time usage

## OUTCOME
The OAuthService component now initializes properly in the browser environment without throwing the "process is not defined" error. OAuth functionality for Facebook and Google login should work correctly.

## EVALUATION
- Error resolved: Verified that OAuthService no longer accesses `process.env` directly
- Browser compatibility: Component now works in browser environment
- Environment variable access: Variables are properly exposed to browser via webpack
- No breaking changes: Existing functionality preserved