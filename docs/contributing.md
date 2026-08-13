# Contributing

First of all, thank you for your interest in Puppeteer! We'd love to accept your patches and contributions!

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License Agreement (CLA). You (or your employer) retain the copyright to your contribution; this simply gives us permission to use and redistribute your contributions as part of the project. Head over to <https://cla.developers.google.com/> to see your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one (even if it was for a different project), you probably don't need to do it again.

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/puppeteer/puppeteer
   cd puppeteer
   ```

   Or open directly with GitHub Codespaces:

   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=90796663&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json)

2. Install dependencies:

   ```bash
   npm install
   # Or to download Firefox by default:
   PUPPETEER_BROWSER=firefox npm install
   ```

3. Build all packages:

   ```bash
   npm run build
   ```

4. Run all tests:

   ```bash
   npm test
   ```

## Building a Single Package

To build a single package within the monorepo:

```bash
npm run build --workspace <package> # e.g., puppeteer
```

This will build all dependent packages automatically thanks to [wireit](https://github.com/google/wireit), which behaves similarly to GNU Make.

### Watch Mode

To continuously build a package on file changes:

```bash
npm run build --watch --workspace <package> # e.g., puppeteer
```

> **Note:** Only specify a single package to watch. `wireit` will automatically rebuild dependent workspaces as needed.

## Removing Stale Artifacts

Generated artifacts (such as `packages/puppeteer-core/src/types.ts`) can occasionally become stale. To clean build artifacts, run:

```bash
npm run clean
# Or specify a workspace:
npm run clean --workspace <package>
```

## Comprehensive Testing

In addition to `npm test`, several specific test scripts are available:

- `test-install` - Verifies proper installation and basic functionality of `puppeteer` and `puppeteer-core`.
- `test-types` - Tests TypeScript definitions using [`tsd`](https://github.com/SamVerschueren/tsd).
- `test:chrome:**` - Runs tests on Chrome.
- `test:firefox:**` - Runs tests on Firefox.
- `unit` - Runs fast unit tests without browser instances.

Default execution via `npm test` runs `test:{chrome,firefox}:headless`.

Puppeteer uses a custom test runner on top of Mocha that consults [TestExpectations.json](https://github.com/puppeteer/puppeteer/blob/main/test/TestExpectations.json). See details in [`tools/mocha-runner`](https://github.com/puppeteer/puppeteer/tree/main/tools/mocha-runner).

### Unit Tests

Unit tests execute without launching a full browser instance and leverage the native Node.js test runner:

```bash
npm run unit
```

## Code Reviews

All submissions require code review via GitHub Pull Requests. Please review [GitHub Help](https://help.github.com/articles/about-pull-requests/) if you are unfamiliar with PR workflows.

## Code Style

Our code style is strictly enforced via [ESLint](https://eslint.org/) (`eslint.config.mjs`) and [Prettier](https://prettier.io) (`.prettierrc.cjs`).

Verify your code locally:

```bash
npm run lint
```

To automatically fix styling errors:

```bash
npm run format
```

## Project Structure

- `packages/`: Public source code for published packages.
- `test/`: Integration and end-to-end test suites.
- `test-d/`: TypeScript type definition tests (`tsd`).
- `tools/`: Build scripts, CI utilities, and test runner configurations.

## API Guidelines

When adding new API methods or events:

- Expose minimal information. When in doubt, defer public exposure.
- Prefer explicit methods over getters/setters (except for namespace roots like `page.keyboard`).
- Use lowercase string literals for event names and option values.
- Avoid utility/sugar APIs that can easily be implemented in user-land unless heavily requested.

## Commit Messages

Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) specification.

Breaking changes must include `BREAKING CHANGE:` in the footer:

```text
fix(page): fix page.pizza method

This patch fixes page.pizza so that it works with iframes.

Issues: #123, #234

BREAKING CHANGE: page.pizza now delivers pizza at home by default.
To deliver to a different location, use the "deliver" option:
  `page.pizza({deliver: 'work'})`.
```

## Writing Documentation & TSDoc

API documentation is generated automatically from TSDoc comments via `npm run docs`. **Do not edit files in `docs/api` manually.**

- Document all public methods using TSDoc comments (`@public` or `@internal`).
- Keep TSDoc lines under 90 characters.

### Local Documentation Site Setup

1. Install root dependencies without scripts: `npm i --ignore-scripts`
2. Generate API docs: `npm run docs`
3. Install website dependencies: `npm i --prefix website`
4. Start local site: `npm start --prefix website`

## For Project Maintainers

### Rolling New Chrome Versions

Chrome browser pins are updated automatically via a daily [GitHub Action](https://github.com/puppeteer/puppeteer/actions/workflows/update-browser-pins.yml).

To run manually:

```bash
node tools/update_browser_revision.mjs
```

### Releasing to npm

Releases are automated via [Release Please](https://github.com/googleapis/release-please). Merge the automated release Pull Request to publish packages to npm.
