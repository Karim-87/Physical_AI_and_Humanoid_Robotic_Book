<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial creation)
- Modified principles: All principles added (new project)
- Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
- Removed sections: None
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity
Content and implementation must be simple and minimal; Features should be essential and focused; Start with the minimum viable solution and expand only when necessary.

### II. Accuracy
All technical content must be factually correct and verified; Code examples must be tested and functional; Information accuracy is prioritized over comprehensiveness.

### III. Minimalism
Keep the codebase lightweight and efficient; Minimize dependencies and external requirements; Focus on core functionality without unnecessary complexity.

### IV. Fast Builds
Ensure rapid build times for the Docusaurus textbook; Optimize compilation and deployment processes; Prioritize developer experience with quick iteration cycles.

### V. Free-tier Architecture
Design all infrastructure components to work within free-tier constraints; No heavy GPU usage or expensive resources; Lightweight embeddings and cost-effective solutions.

### VI. RAG-Only Knowledge Source
The RAG chatbot must answer questions exclusively from book text content; No external knowledge sources allowed; Maintain strict boundaries between book content and AI responses.

## Additional Constraints

### Technical Constraints
- No heavy GPU usage for processing or inference
- Minimal embeddings to stay within free-tier limits
- Docusaurus-based UI for textbook presentation
- RAG system using Qdrant + Neon + FastAPI stack
- Free-tier friendly architecture throughout

### Content Constraints
- 6 short chapters covering core topics:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Clean, professional presentation suitable for educational use

## Development Workflow

### Implementation Requirements
- All features must be testable and verified
- Code changes require validation of both functionality and performance
- Changes to textbook content must maintain educational quality
- RAG system updates must preserve accuracy and response quality

### Quality Gates
- All components must work within free-tier constraints
- Build times must remain under acceptable limits
- Content accuracy must be verified before merging
- Performance benchmarks must be met for deployment

## Governance

This constitution serves as the authoritative guide for all project decisions. All development activities must align with these principles. Changes to this constitution require explicit approval and documentation of the reasoning. All team members are responsible for upholding these standards and ensuring compliance with the defined constraints and workflows.

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10
