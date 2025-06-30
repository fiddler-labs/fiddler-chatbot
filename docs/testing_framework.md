# Testing Framework & Dev/Prod Separation Strategy

This framework would enable you to make changes, run automated tests, and get clear pass/fail feedback without human intervention, allowing tools like Cursor to iterate and refine the system autonomously until all tests pass.

- Dev and Prod environments currently mixed : Implement config-driven environment switching : Clean separation of development vs production data/settings
- GitHub Actions workflow for test automation : Immediate feedback on breaking changes

- Data Pipeline Testing
  - Corpus Generation Validation: Run end-to-end `data_generation.py` to ensure documentation processing, notebook conversion, and RSS crawling produce expected outputs

- Data Quality Checks:
  - Manually validate conversation memory, user feedback storage, and session persistence

