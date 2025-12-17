---
id: "005"
title: "Fix useAuth context boundary error"
stage: "red"
date: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-backend-auth"
branch: "002-backend-auth"
user: "user"
command: "/sp.resolveerror"
labels: ["bug-fix", "react-context", "auth", "docusaurus", "render-boundary"]
links:
  spec: "specs/002-backend-auth/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/docusaurus/src/components/AuthenticatedRagChatbot.js"
  - "frontend/docusaurus/src/pages/index.js"
  - "frontend/docusaurus/src/components/TextbookToolbar.js"
  - "frontend/docusaurus/src/components/TextbookLayout.js"
  - "frontend/docusaurus/docusaurus.config.js"
tests: []
---

## PROMPT_TEXT
Runtime error:
"useAuth must be used within an AuthProvider" persists
despite AuthProvider wrapping global layout.

## CONTEXT
- Docusaurus creates multiple React render roots
- BrowserOnly, MDX, and client-only components
  do NOT inherit context from Layout
- RagChatbot is rendered in a separate tree

## RESPONSE_TEXT
Successfully resolved the "useAuth must be used within an AuthProvider" error by addressing Docusaurus-specific render boundary issues.

### Root Cause Analysis:
- Docusaurus creates multiple React render roots
- AuthProvider wrapped in global Root component doesn't reach all render trees
- RagChatbot components in different contexts lacked auth context

### Changes Made:
1. Created AuthenticatedRagChatbot wrapper component that ensures AuthProvider context
2. Updated all RagChatbot usages to use AuthenticatedRagChatbot:
   - index.js (homepage)
   - TextbookToolbar.js
   - TextbookLayout.js
3. Removed Root.js and clientModules approach (not needed with component wrapping)
4. Each RagChatbot instance now has its own AuthProvider context

### Key Technical Details:
- AuthenticatedRagChatbot: Higher-order component that wraps RagChatbot with AuthProvider
- Component-level context wrapping ensures provider-consumer pairing
- Removed global Root approach that didn't work with Docusaurus render boundaries
- No duplicate providers within same render tree (each wrapper is in separate tree)

## OUTCOME
The RagChatbot component now has access to authentication context in all render trees, resolving the context error while respecting Docusaurus render boundaries.

## EVALUATION
- Error resolved: useAuth hook now works in all RagChatbot instances
- Docusaurus render boundaries respected: Each context is in appropriate render tree
- No breaking changes: Existing functionality preserved
- Proper React context patterns: Provider-consumer pairs maintained