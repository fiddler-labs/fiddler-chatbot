# Cursor Rules for Rapid Development

## Rules Files

- **ai_assistant.mdc**: Guidelines for Cursor
- **README.md**: Documentation of the rules system and philosophy
- **tool_diagram_assistant.mdc**: Specialized rules for diagram generation and concept visualization

## Updating Rules

When updating these rules:

- Keep changes focused and specific
- Avoid contradictory guidelines
- Test the effectiveness of rules after changes
- Document new patterns in appropriate rule files

## Maintainer Notes

When updating these rules:

- Keep them focused on rapid delivery
- Prioritize working functionality over perfect structure
- Make changes only when they speed up development
- Remember: done is better than perfect!
- Maintain consistent markdown formatting using bullet points by default

## Architecture Diagrams

The project should create three key Mermaid diagrams that document the architecture:

- **System Architecture Diagram** (docs/diagram-system_architecture.md): Shows components, modules, and their relationships
- **Integration Sequence Diagram** (docs/diagram-integration_sequence.md): Illustrates the interaction flow between components
- **Data Model ER Diagram** (docs/diagram-data_model_entity_rels.md): Represents data models and their relationships

When making significant changes to the codebase, ensure these diagrams are updated to reflect the current architecture.
These can be updated by invoking the tool_diagram_assistant.mdc
