# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, with project-friendly semantic versions.

## [0.5.0-dev] - 2026-03-11

### Planned

- add local draft review heuristics
- detect explanation-heavy writing, weak hooks, repetitive transitions, and overly neat chapter closure
- surface review results through files and later through the GUI

### Added

- local review heuristics for explanation-heavy writing, repeated transitions, overly neat closure, weak hooks, and overly even pacing
- review report generation into the `reviews/` directory
- GUI entry for selecting a draft and generating a local review report

### Changed

- bumped local development version to `0.5.0.dev0`
- started the next isolated development branch after releasing `v0.4.0`

## [0.4.0] - 2026-03-11

### Planned

- build chapter pipeline on top of the new planning engine
- generate next-chapter cards from volume and plot-unit context
- add chapter progress tracking and recent event recap

### Added

- current chapter card generation based on current volume and plot unit
- current chapter writing prompt generation
- recent progress file generation
- chapter progress updates with chapter summary, hook, and word count
- GUI actions for refreshing chapter pipeline and advancing one chapter

### Changed

- promoted the chapter pipeline to the first stable `v0.4.0` release

## [0.3.0] - 2026-03-11

### Planned

- refine planning engine for different target word ranges
- improve chapter-count, volume-count, and plot-unit allocation
- prepare stronger story-planning profiles for projects under 100 wan words

### Added

- stronger planning profiles with payoff cadence and foreshadow cadence
- dynamic volume-role templates for opening, middle, truth, and finale phases
- real plot-unit generation instead of static unit placeholders
- new tests covering plot-unit continuity and scaling across target word ranges
- prompt pack generation for director, unit planner, chapter card, writer, and reviewer roles
- prompt shortcuts surfaced in the GUI dashboard

### Changed

- promoted the planning engine and prompt pack to the first stable `v0.3.0` release
- replaced the simple volume-count heuristic with a profile-driven estimation model
- updated project overview, volume outline, and plot-unit rendering to use the new planning data
- project initialization now writes reusable prompt files into the `prompts/` directory

## [0.2.0] - 2026-03-11

### Added

- desktop GUI entry based on Tkinter for the v0.2.0 prototype
- project initialization flow that creates a novel workspace and seed documents
- configurable target word planning for 1-1000 wan words, optimized first for projects under 100 wan words
- initial state model and template generation logic
- minimal automated test covering project initialization
- existing project loading flow in the GUI
- dashboard summary and volume overview for created or loaded projects
- project document shortcuts in the dashboard
- visible Git branch and tag status in the release panel

### Changed

- updated requirements, tasks, architecture, and project plan to reflect the GUI-first direction
- promoted the GUI prototype to the first stable `v0.2.0` release

## [0.1.1] - 2026-03-11

### Added

- remote repository alignment for the new project baseline
- merged previous remote history into the current repository lineage
- cleaned old repository-specific files from the working tree

### Changed

- bumped project version from `0.1.0` to `0.1.1`
- set current repository state to the new planning-first Shuangwen Pipeline project

## [0.1.0] - 2026-03-11

### Added

- initial repository skeleton
- project plan
- requirements document
- task breakdown
- architecture overview
- versioning and GitHub archive guide
- contribution guide
- GitHub issue and pull request templates

### Notes

- this release is planning-first and does not include functional writing automation yet
