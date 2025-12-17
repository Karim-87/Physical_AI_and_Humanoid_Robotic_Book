---
id: "004"
title: "Fix useAuth context error"
stage: "red"
date: "2025-12-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-backend-auth"
branch: "002-backend-auth"
user: "user"
command: "/sp.resolveerror"
labels: ["bug-fix", "react-context", "auth", "docusaurus"]
links:
  spec: "specs/002-backend-auth/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/docusaurus/src/components/Root.js"
  - "frontend/docusaurus/docusaurus.config.js"
tests: []
---

## PROMPT_TEXT
Runtime error:
"useAuth must be used within an AuthProvider"

## CONTEXT
- React frontend (Docusaurus)
- AuthProvider defines React Context
- useAuth hook throws if context is undefined
- RagChatbot uses useAuth but is rendered outside provider

## RESPONSE_TEXT
Successfully resolved the "useAuth must be used within an AuthProvider" error by implementing the proper React Context pattern for Docusaurus applications.

### Changes Made:
1. Created a Root.js component that wraps all children with AuthProvider
2. Updated docusaurus.config.js to use the Root component via clientModules

### Key Technical Details:
- Root.js: Simple component that wraps children with AuthProvider
- docusaurus.config.js: Added clientModules configuration to register Root component
- AuthProvider context is now available throughout the entire app tree
- No changes needed to useAuth hook or RagChatbot component

### Implementation:
- Created frontend/docusaurus/src/components/Root.js
- Added require.resolve('./src/components/Root.js') to clientModules in config
- AuthProvider now wraps the entire application ensuring context availability

## OUTCOME
The RagChatbot component can now access the authentication context via useAuth hook without throwing an error. The AuthProvider context is available throughout the entire component tree.

## EVALUATION
- Error resolved: useAuth hook now works properly throughout the app
- Context availability: AuthProvider wraps entire application
- No breaking changes: Existing functionality preserved
- Docusaurus best practice: Used proper clientModules approach for global providers