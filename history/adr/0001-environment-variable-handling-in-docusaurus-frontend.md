# ADR-0001: Environment Variable Handling in Docusaurus Frontend

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-17
- **Feature:** 002-backend-auth
- **Context:** Need to securely handle OAuth configuration and API endpoints in a Docusaurus-based frontend that runs in the browser environment where Node.js `process.env` is not available.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Environment Variable Access: Use webpack's EnvironmentPlugin to expose required environment variables to the browser
- Safe Access Pattern: Implement helper method to safely access environment variables with browser/node compatibility
- Configuration: Use .env files for local development with proper example files for documentation
- Components: OAuthService.js, docusaurus.config.js, and associated frontend components

## Consequences

### Positive

- Browser compatibility: Components work correctly in browser without "process is not defined" errors
- Security: Environment variables are injected at build time, not stored in source control
- Maintainability: Clear pattern for accessing environment variables in frontend components
- Development experience: Consistent configuration approach across frontend and backend

### Negative

- Build-time dependency: Environment variables must be available during build process
- Configuration complexity: Requires both .env files and webpack configuration
- Potential exposure: Environment variables are bundled into client-side code (limited to public-facing OAuth IDs)

## Alternatives Considered

Alternative A: API endpoint for configuration - Fetch configuration from backend at runtime
- Pros: More secure for sensitive data, dynamic configuration possible
- Cons: Additional network request, doesn't solve OAuth redirect issues, more complex

Alternative B: Hardcoded configuration - Store values directly in code
- Pros: Simple implementation
- Cons: Security risk, no flexibility, version control issues

Alternative C: Runtime injection via HTML meta tags - Inject values through HTML template
- Pros: Secure at build time, no process.env dependency
- Cons: More complex setup, requires server-side template modification

## References

- Feature Spec: specs/002-backend-auth/spec.md
- Implementation Plan: specs/002-backend-auth/plan.md
- Related ADRs: None
- Evaluator Evidence: history/prompts/general/001-resolve-process-not-defined-error.general.prompt.md
