# Conventional Commits

> The following is copied from conventionalcommits.org:

## Overview

The commit contains the following structural elements, to communicate intent to the consumers of your library:

- `fix`: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in semantic versioning).
- `feat`: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in semantic versioning).
- BREAKING CHANGE: a commit that has the text `BREAKING CHANGE: ` at the beginning of its optional body or footer section introduces a breaking API change (correlating with `MAJOR` in semantic versioning). A breaking change can be part of commits of any type. e.g., a `fix:`, `feat:` & `chore:` types would all be valid, in addition to any other type.
- Others: commit types other than `fix:` and `feat:` are allowed, for example @commitlint/config-conventional (based on the the Angular convention) recommends `chore:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others. We also recommend improvement for commits that improve a current implementation without adding a new feature or fixing a bug. Notice these types are not mandated by the conventional commits specification, and have no implicit effect in semantic versioning (unless they include a BREAKING CHANGE, which is NOT recommended). A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., `feat(parser): add ability to parse arrays`.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

- Commits MUST be prefixed with a type, which consists of a noun, feat, fix, etc., followed by a colon and a space.
- The type feat MUST be used when a commit adds a new feature to your application or library.
- The type fix MUST be used when a commit represents a bug fix for your application.
- An optional scope MAY be provided after a type. A scope is a phrase describing a section of the codebase enclosed in parenthesis, e.g., fix(parser):
- A description MUST immediately follow the type/scope prefix. The description is a short description of the code changes, e.g., fix: array parsing issue when multiple spaces were contained in string.
- A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
- A footer MAY be provided one blank line after the body (or after the description if body is missing). The footer SHOULD contain additional issue references about the code changes (such as the issues it fixes, e.g.,Fixes #13).
- Breaking changes MUST be indicated at the very beginning of the footer or body section of a commit. A breaking change MUST consist of the uppercase text BREAKING CHANGE, followed by a colon and a space.
- A description MUST be provided after the BREAKING CHANGE: , describing what has changed about the API, e.g., BREAKING CHANGE: environment variables now take precedence over config files.
- The footer MUST only contain BREAKING CHANGE, external links, issue references, and other meta-information.
- Types other than feat and fix MAY be used in your commit messages.

## Example Commit Messages

Commit message with description and breaking change in body:
```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

Commit message with no body:
```
docs: correct spelling of CHANGELOG
```

Commit message with scope:
```
feat(lang): added polish language
```
Commit message for a fix using an (optional) issue number:
```
fix: minor typos in code

see the issue for details on the typos fixed

fixes issue #12
```
