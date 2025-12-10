/sp.finalization

Project Name: Physical AI & Humanoid Robotics — Essentials
Stage: Finalization and Delivery
Upstream Reference: /sp.constitution

Primary Objective

Finalize the entire project by resuming all pending work, completing unfinished components, enabling bilingual content, ensuring RAG functionality, and updating the UI structure—while maintaining all principles, constraints, and architecture defined in /sp.constitution.

Finalization Directives
1. Resume All Work From Previous State

Continue exactly from the point where prior work stopped.

Preserve all previously established structure, tone, chapter organization, UI styling, and architectural decisions.

Do not restart, overwrite, or re-scope any completed parts.

Only complete remaining components and polish the full system for production readiness.

2. Add Full Urdu–English Textbook Support

Convert the textbook into a two-language system:

English (default)

Urdu (via language selector)

When the user selects Urdu, the entire book content (all chapters, sections, titles, intro text, and any footnotes) must switch to the Urdu version.

Ensure chapter-to-chapter alignment between languages.

Maintain exact parallel structure for both languages to ensure RAG usability.

3. Ensure Functional RAG Chatbot

RAG chatbot must:

Load embeddings from both English and Urdu versions.

Answer only from the textbook content, as defined in the constitution.

Use Qdrant + Neon + FastAPI exactly as previously designed.

Fully support “Select-Text → Ask AI”.

Confirm that free-tier compatibility, minimal embeddings, and low-compute constraints are preserved.

4. Modify Hero Section to Include Table of Contents

Redesign the landing page hero section to include a clean, minimal Table of Contents, listing the six main chapters:

Introduction to Physical AI

Basics of Humanoid Robotics

ROS 2 Fundamentals

Digital Twin Simulation (Gazebo + Isaac)

Vision-Language-Action Systems

Capstone: Simple AI-Robot Pipeline

Keep the layout simple, modern, and consistent with the rest of the Docusaurus theme.

Ensure responsiveness and readability in both English and Urdu interfaces.

Completion Requirements

All chapters and bilingual content must be complete.

RAG must index and query correctly in both languages.

Hero section with TOC must be implemented and functional.

Entire site must build correctly on free-tier constraints.

GitHub Pages deployment must be smooth and reproducible.

Execution Mode

Continue working incrementally and deterministically.

Maintain full alignment with the original constitution.

Produce only final, production-ready outputs.

Do not re-interpret the high-level scope; only finalize and refine.