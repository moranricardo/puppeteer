# Examples & Use Cases

## Official Examples

The [Puppeteer repository](https://github.com/puppeteer/puppeteer/tree/main/examples) includes official code samples maintained by the core team.

These examples cover common automation tasks such as:
- Generating PDFs and full-page screenshots.
- Intercepting and modifying network requests.
- Automating forms and user interactions using modern Locators (`page.locator()`).
- Executing direct Chrome DevTools Protocol (CDP) commands.

## Dedicated Example Suite

For a broader set of community-contributed code snippets, visit the dedicated [Puppeteer Examples Repository](https://github.com/puppeteer/examples).

This suite covers scenarios like event forwarding from the browser to Node.js, handling frames, custom query selectors, and managing browser contexts.

## Community Projects, Tools & Demos

Below is a curated list of third-party tools, frameworks, and guides built on top of Puppeteer.

### Rendering and Web Scraping

- **[Crawlee (formerly Apify SDK)](https://crawlee.dev/)**: Scalable web crawling and scraping library for Node.js. Automatically manages browser pools, proxies, request queues, and anti-blocking strategies with Puppeteer.
- **[Browserless](https://github.com/browserless/browserless)**: Headless Chrome/Firefox as a service, allowing remote execution of Puppeteer scripts in Docker or cloud environments.
- **[Puppetron](https://github.com/cheeaun/puppetron)**: Demo showing how to use Puppeteer to render dynamic pages into static HTML.
- **[Pupperender](https://github.com/LasaleFamine/pupperender)**: Express middleware that renders SPA pages using Puppeteer when requests originate from social media or search engine bots.
- **[Headless Chrome Crawler](https://github.com/yujiosaka/headless-chrome-crawler)**: Distributed crawler providing high-level APIs to manipulate headless browser sessions.
- **[Puppeteer on AWS Lambda](https://github.com/Sparticuz/chromium)**: Guidelines and binaries for executing Puppeteer and Chromium on serverless platforms like AWS Lambda.

### Testing and Utilities

- **[Jest Puppeteer](https://github.com/argos-ci/jest-puppeteer)**: Zero-configuration runner for executing tests with Jest and Puppeteer, including custom assertions.
- **[Puppetry](https://puppetry.app/)**: Desktop GUI application to build Puppeteer and Jest automated tests without writing code manually.
- **[Puppeteer to Istanbul Example](https://github.com/bcoe/puppeteer-to-istanbul-example)**: Demo showing how to convert Puppeteer code coverage into Istanbul/nyc reports.
- **[Puppeteer HAR Generator](https://github.com/Everettss/puppeteer-har)**: Utility to record network activity during Puppeteer sessions and export standard `.har` files.
- **[Puppeteer Loadtest](https://github.com/svenkatreddy/puppeteer-loadtest)**: CLI tool to perform load testing using Puppeteer scripts.
