

=== FILE: docs/guides/browser-management.md ===

# Browser management

Usually, you start working with Puppeteer by either [launching](https://pptr.dev/api/puppeteer.puppeteernode.launch) or [connecting](https://pptr.dev/api/puppeteer.puppeteernode.connect) to a browser.

## Launching a browser

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

const page = await browser.newPage();

// ...
```

## Closing a browser

To gracefully close the browser, you use the [`browser.close()`](https://pptr.dev/api/puppeteer.browser.close) method:

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

const page = await browser.newPage();

await browser.close();
```

## Browser contexts

If you need to isolate your automation tasks, use [BrowserContexts](https://pptr.dev/api/puppeteer.browser.createbrowsercontext). Cookies and local storage are not shared between browser contexts. Also, you can close all pages in the context by closing the context.

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

const context = await browser.createBrowserContext();

const page1 = await context.newPage();
const page2 = await context.newPage();

await context.close();
```

## Permissions

You can also configure permissions for a browser context:

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();
const context = browser.defaultBrowserContext();

await context.overridePermissions('https://html5demos.com', ['geolocation']);
```

## Connecting to a running browser

If you launched a browser outside of Puppeteer, you can connect to it using the [`connect`](https://pptr.dev/api/puppeteer.puppeteernode.connect) method. Usually, you can grab a WebSocket endpoint URL from the browser output:

```ts
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://127.0.0.1:9222/...',
});

const page = await browser.newPage();

browser.disconnect();
```

:::note

Unlike `browser.close()`, `browser.disconnect()` does not shut down the browser or close any pages.

:::


=== FILE: docs/guides/chrome-extensions.md ===

# Chrome Extensions

Puppeteer can be used for testing Chrome Extensions.

## Load extensions

### Using `LaunchOptions`

```ts
import puppeteer from 'puppeteer';
import path from 'path';

const pathToExtension = path.join(process.cwd(), 'my-extension');
const browser = await puppeteer.launch({
  pipe: true,
  enableExtensions: [pathToExtension],
});
```

### At runtime

```ts
import puppeteer from 'puppeteer';
import path from 'path';

const pathToExtension = path.join(process.cwd(), 'my-extension');
const browser = await puppeteer.launch({
  pipe: true,
  enableExtensions: true,
});

await browser.installExtension(pathToExtension);
```

## Background contexts

You can get a reference to the extension service worker or background page, which can be useful for evaluating code in the extension context or forcefully terminating the service worker.

### Service worker (MV3)

```ts
import puppeteer from 'puppeteer';
import path from 'path';

const pathToExtension = path.join(process.cwd(), 'my-extension');
const browser = await puppeteer.launch({
  pipe: true,
  enableExtensions: [pathToExtension],
});

const workerTarget = await browser.waitForTarget(
  // Assumes that there is only one service worker created by the extension and its URL ends with background.js.
  target =>
    target.type() === 'service_worker' &&
    target.url().endsWith('background.js'),
);

const worker = await workerTarget.worker();

// Test the service worker.

await browser.close();
```

### Background page (MV2)

The following is code for getting a handle to the
[background page](https://developer.chrome.com/extensions/background_pages) of
an extension whose source is located in `./my-extension`:

```ts
import puppeteer from 'puppeteer';
import path from 'path';

const pathToExtension = path.join(process.cwd(), 'my-extension');
const browser = await puppeteer.launch({
  pipe: true,
  enableExtensions: [pathToExtension],
});
const backgroundPageTarget = await browser.waitForTarget(
  target => target.type() === 'background_page',
);
const backgroundPage = await backgroundPageTarget.page();

// Test the background page as you would any other page.

await browser.close();
```

## Popup

Access the service worker [as above](#service-worker-mv3). Then:

```ts
await worker.evaluate('chrome.action.openPopup();');

const popupTarget = await browser.waitForTarget(
  // Assumes that there is only one page with the URL ending with popup.html
  // and that is the popup created by the extension.
  target => target.type() === 'page' && target.url().endsWith('popup.html'),
);

const popupPage = await popupTarget.asPage();

// Test the popup page as you would any other page.

await browser.close();
```

## Content scripts

Content scripts are injected as normal. Use `browser.newPage()` and `page.goto()` to navigate to a page where a content script will be injected.

It is not currently possible to evaluate code in the content script isolated world.

## Learn more

To learn more, see the documentation on [Chrome for Developers](https://developer.chrome.com/docs/extensions/how-to/test/end-to-end-testing).


=== FILE: docs/guides/configuration.md ===

# Configuration

By default, Puppeteer downloads and uses a specific version of Chrome so its
API is guaranteed to work out of the box. To use Puppeteer with a different
version of Chrome or Chromium, pass in the executable's path when creating a
`Browser` instance:

```ts
const browser = await puppeteer.launch({executablePath: '/path/to/Chrome'});
```

You can also use Puppeteer with Firefox. See
[status of cross-browser support](https://pptr.dev/faq#q-what-is-the-status-of-cross-browser-support) for
more information.

All defaults in Puppeteer can be customized in two ways:

1. [Configuration files](#configuration-files) (**recommended**)
2. [Environment variables](#environment-variables)

:::caution

Note that some options are only customizable through environment variables (such
as `HTTPS_PROXY`).

:::

:::caution

Puppeteer's configuration files and environment variables are ignored by `puppeteer-core`.

:::

## Configuration files

Configuration files are the **recommended** choice for configuring Puppeteer.
Puppeteer will look up the file tree for any of the following formats:

- `.puppeteerrc.cjs`,
- `.puppeteerrc.js`,
- `.puppeteerrc` (YAML/JSON),
- `.puppeteerrc.json`,
- `.puppeteerrc.yaml`,
- `puppeteer.config.js`, and
- `puppeteer.config.cjs`

See the [`Configuration`](../api/puppeteer.configuration) interface for possible
options.

### Changing download options

When the changes to the configuration include changes to download option,
you will need to re-run postinstall scripts for them to take effect.

This can most easily be done with running:

```bash npm2yarn
npx puppeteer browsers install
```

### Examples

#### Downloading multiple browsers

Starting with v23.0.0, Puppeteer allows downloading multiple browser
without the need to run multiple commands.

Update the Puppeteer configuration file:

```js title="project-directory/.puppeteerrc.cjs"
/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = {
  // Download Chrome (default `skipDownload: false`).
  chrome: {
    skipDownload: false,
  },
  // Download Firefox (default `skipDownload: true`).
  firefox: {
    skipDownload: false,
  },
};
```

Run CLI to download the new configuration:

```bash npm2yarn
npx puppeteer browsers install
```

#### Changing the default cache directory

Starting in v19.0.0, Puppeteer stores browsers in `~/.cache/puppeteer` to
globally cache browsers between installation. This can cause problems if
`puppeteer` is packed during some build step and moved to a fresh location. The
following configuration can solve this issue (reinstall `puppeteer` to take
effect):

```js title="project-directory/.puppeteerrc.cjs"
const {join} = require('path');

/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = {
  // Changes the cache location for Puppeteer.
  cacheDirectory: join(__dirname, '.cache', 'puppeteer'),
};
```

:::note

Notice this is only possible with CommonJS configuration files as information
about the ambient environment is needed (in this case, `__dirname`).

:::

## Environment variables

Along with configuration files, Puppeteer looks for certain
[environment variables](https://en.wikipedia.org/wiki/Environment_variable) for
customizing behavior. Environment variables will always override configuration
file options when applicable.

The following options are _environment-only_ options

- `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` - defines HTTP proxy settings that are
  used to download and run the browser.

All other options can be found in the documentation for the
[`Configuration`](../api/puppeteer.configuration) interface.


=== FILE: docs/guides/cookies.md ===

# Cookies

Puppeteer offers methods to get, set and delete cookies ahead of time by
manipulating browser storage directly. This is useful if you need to
store and restore specific cookies for your tests.

## Getting cookies

The following example demonstrates how to get cookies available in the
browser's default
[BrowserContext](https://pptr.dev/api/puppeteer.browsercontext).

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

const page = await browser.newPage();

await page.goto('https://example.com');

// In this example, we set a cookie using script evaluation.
// Cookies can be set by the page/server in various ways.
await page.evaluate(() => {
  document.cookie = 'myCookie = MyCookieValue';
});

console.log(await browser.cookies()); // print available cookies.
```

## Setting cookies

Puppeteer can also write cookies directly into the browser's storage:

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

// Sets two cookies for the localhost domain.
await browser.setCookie(
  {
    name: 'cookie1',
    value: '1',
    domain: 'localhost',
    path: '/',
    expires: -1,
    httpOnly: false,
    secure: false,
    sourceScheme: 'NonSecure',
  },
  {
    name: 'cookie2',
    value: '2',
    domain: 'localhost',
    path: '/',
    expires: -1,
    httpOnly: false,
    secure: false,
    sourceScheme: 'NonSecure',
  },
);

console.log(await browser.cookies()); // print available cookies.
```

## Deleting cookies

[Browser.deleteCookie()](https://pptr.dev/api/puppeteer.browser.deletecookie) method allows deleting cookies from storage.

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();

// Deletes two cookies for the localhost domain.
await browser.deleteCookie(
  {
    name: 'cookie1',
    value: '1',
    domain: 'localhost',
    path: '/',
    expires: -1,
    httpOnly: false,
    secure: false,
    sourceScheme: 'NonSecure',
  },
  {
    name: 'cookie2',
    value: '2',
    domain: 'localhost',
    path: '/',
    expires: -1,
    httpOnly: false,
    secure: false,
    sourceScheme: 'NonSecure',
  },
);

console.log(await browser.cookies()); // print available cookies.
```

In addition to the `Browser` methods operating on the default browser
context, the same methods are available on the
[`BrowserContext`](https://pptr.dev/api/puppeteer.browsercontext) class.


=== FILE: docs/guides/debugging.md ===

# Debugging

Debugging with Puppeteer can be an arduous task. There is no _single_ method for
debugging all possible issues since Puppeteer touches many distinct components
of a browser such as network requests and Web APIs. On a high note, Puppeteer
provides _several_ methods for debugging which hopefully do cover all possible
issues.

## Background

In general, there are two possible sources of an issue: Code running on Node.js
(which we call _server code_), and
[code running in the browser](../api/puppeteer.page.evaluate)
(which we call _client code_). There is also a third possible source being the
browser itself (which we call _internal code_ or _browser code_), but if you suspect this is the
source **after attempting the methods below**, we suggest
[searching existing issues](https://github.com/puppeteer/puppeteer/issues)
before
[filing an issue](https://github.com/puppeteer/puppeteer/issues/new/choose).

## Debugging methods for all situations

These methods can be used to debug any situation. These should be used as a
quick sanity check before diving into more complex methods.

### Turn off [`headless`](../api/puppeteer.launchoptions)

Sometimes it's useful to see what the browser is displaying. Instead of
launching in
[`headless`](../api/puppeteer.launchoptions) mode,
launch a full version of the browser with
[`headless`](../api/puppeteer.launchoptions) set to
`false`:

```ts
const browser = await puppeteer.launch({headless: false});
```

### Puppeteer "slow-mo"

The [`slowMo`](../api/puppeteer.connectoptions) option slows down
Puppeteer operations by a specified amount of milliseconds. It's another way to
help see what's going on.

```ts
const browser = await puppeteer.launch({
  headless: false,
  slowMo: 250, // slow down by 250ms
});
```

## Debugging methods for client code

### Capture `console.*` output

Since client code runs in the browser, doing `console.*` in client code will not
directly log to Node.js. However, you can [listen (page.on)](../api/puppeteer.page) for
the [`console`](../api/puppeteer.pageevents) event which returns a
payload with the logged text.

```ts
page.on('console', msg => console.log('PAGE LOG:', msg.text()));

await page.evaluate(() => console.log(`url is ${location.href}`));
```

### Use the debugger in the browser

1. Set [`devtools`](../api/puppeteer.launchoptions) to
   `true` when launching Puppeteer:

   ```ts
   const browser = await puppeteer.launch({devtools: true});
   ```

2. Add `debugger` inside any client code you want debugged. For example,

   ```ts
   await page.evaluate(() => {
     debugger;
   });
   ```

   The Browser will now stop in the location the `debugger` word is found in
   debug mode.

## Debugging methods for server code

### Use the debugger in Node.js (Chrome/Chromium-only)

Since server code intermingles with client code, this method of debugging is
closely tied with the browser. For example, you can step over
`await page.click()` in the server script and see the click happen in the
browser.

Note that you won't be able to run `await page.click()` in DevTools console due
to this
[Chromium bug](https://bugs.chromium.org/p/chromium/issues/detail?id=833928), so
if you want to try something out, you have to add it to your test file.

1. Set [`headless`](../api/puppeteer.launchoptions) to
   `false`.
2. Add `debugger` to any server code you want debugged. For example,

   ```ts
   debugger;
   await page.click('a[target=_blank]');
   ```

3. Run your server code with `--inspect-brk`. For example,

   ```bash
   node --inspect-brk path/to/script.js
   ```

4. In the opened Chrome/Chromium browser, open `chrome://inspect/#devices` and
   click `inspect`.
5. In the newly opened test browser, press `F8` to resume test execution.
6. Now your `debugger` statement will be hit and you can debug in the test
   browser.

### Log DevTools protocol traffic

If all else fails, it's possible there may be an issue between Puppeteer and the
DevTools protocol. You can debug this by setting the `DEBUG` environment
variable before running your script. This will log internal traffic via
[`debug`](https://github.com/visionmedia/debug) under the `puppeteer` namespace.

:::warning

The logs may include sensitive information.

:::

```bash
# Basic verbose logging
env DEBUG="puppeteer:*" node script.js

# Prevent truncating of long messages
env DEBUG="puppeteer:*" env DEBUG_MAX_STRING_LENGTH=null node script.js

# Protocol traffic can be rather noisy. This example filters out all Network domain messages
env DEBUG="puppeteer:*" env DEBUG_COLORS=true node script.js 2>&1 | grep -v '"Network'

# Filter out all protocol messages but keep all other logging
env DEBUG="puppeteer:*,-puppeteer:protocol:*" node script.js
```

### Log pending protocol calls

If you encounter issues with async Puppeteer calls not getting resolved, try logging
pending callbacks by using the [`debugInfo`](https://pptr.dev/api/puppeteer.browser/#properties) interface
to see what call is the cause:

```ts
console.log(browser.debugInfo.pendingProtocolErrors);
```

The getter returns a list of `Error` objects and the stacktraces of the error objects
indicate which code triggered a protocol call.

## Debugging methods for the browser code

### Print browser logs

If the browser unexpectedly crashes or does not launch properly, it could be useful
to inspect logs from the browser process by setting the launch attribute `dumpio` to `true`.

```ts
const browser = await puppeteer.launch({
  dumpio: true,
});
```

In this case, Puppeteer forwards browser logs to the Node process' stdio.


=== FILE: docs/guides/docker.md ===

# Docker

Puppeteer offers a Docker image that includes [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) along with the required
dependencies and a pre-installed Puppeteer version. The image is available via
the
[GitHub Container Registry](https://github.com/puppeteer/puppeteer/pkgs/container/puppeteer).
The latest image is tagged as `latest` and other tags match Puppeteer versions.
For example,

```bash
docker pull ghcr.io/puppeteer/puppeteer:latest # pulls the latest
docker pull ghcr.io/puppeteer/puppeteer:16.1.0 # pulls the image that contains Puppeteer v16.1.0
```

The image is meant for running the browser in sandbox mode and therefore,
running the image requires the `SYS_ADMIN` capability.

## Usage

To use the docker image directly, run:

```bash
docker run -i --init --cap-add=SYS_ADMIN --rm ghcr.io/puppeteer/puppeteer:latest node -e "$(cat path/to/script.js)"
```

where `path/to/script.js` is the path relative to your working directory. Note
the image requires the `SYS_ADMIN` capability since the browser runs in sandbox
mode.

If you need to build an image based on a different base image, you can use our
[`Dockerfile`](https://github.com/puppeteer/puppeteer/blob/main/docker/Dockerfile)
as the starting point.

:::caution

Make sure to specify a init process via the `--init` flag or a custom `ENTRYPOINT`
to make sure all processes started by Puppeteer are managed properly.

:::

## dbus

The image installs and configures dbus for Chrome. Usually you would not
need dbus in the headless mode but you might see warnings in the browser
console. You can start the dbus service before launching
your application:

```
sudo service dbus start
```

See https://docs.docker.com/config/containers/multi-service_container/
for instructions how to start multiple processes in a container.


=== FILE: docs/guides/files.md ===

# Files

Currently, Puppeteer does not offer a way to handle file downloads in a programmatic way.
For uploading files, you need to locate a file input element and call [`ElementHandle.uploadFile`](https://pptr.dev/api/puppeteer.elementhandle.uploadfile).

```ts
const fileElement = await page.waitForSelector('input[type=file]');
await fileElement.uploadFile(['./path-to-local-file']);
```


=== FILE: docs/guides/getting-started.md ===

# Getting started

Puppeteer will be familiar to people using other browser testing frameworks. You
[launch](https://pptr.dev/api/puppeteer.puppeteernode.launch)/[connect](https://pptr.dev/api/puppeteer.puppeteernode.connect)
a [browser](https://pptr.dev/api/puppeteer.browser),
[create](https://pptr.dev/api/puppeteer.browser.newpage) some
[pages](https://pptr.dev/api/puppeteer.page), and then manipulate them with
[Puppeteer's API](https://pptr.dev/api).

The following example searches [developer.chrome.com](https://developer.chrome.com/) for blog posts with text "automate beyond recorder", click on the first result and print the full title of the blog post.

```ts
import puppeteer from 'puppeteer';
// Or import puppeteer from 'puppeteer-core';

// Launch the browser and open a new blank page.
const browser = await puppeteer.launch();
const page = await browser.newPage();

// Navigate the page to a URL.
await page.goto('https://developer.chrome.com/');

// Set screen size.
await page.setViewport({width: 1080, height: 1024});

// Open the search menu using the keyboard.
await page.keyboard.press('/');

// Type into search box using accessible input name.
await page.locator('::-p-aria(Search)').fill('automate beyond recorder');

// Wait and click on first result.
await page.locator('.devsite-result-item-link').click();

// Locate the full title with a unique string.
const textSelector = await page
  .locator('::-p-text(Customize and automate)')
  .waitHandle();
const fullTitle = await textSelector?.evaluate(el => el.textContent);

// Print the full title.
console.log('The title of this blog post is "%s".', fullTitle);

await browser.close();
```

For more in-depth usage, check our [documentation](https://pptr.dev/docs)
and [examples](https://github.com/puppeteer/puppeteer/tree/main/examples).


=== FILE: docs/guides/headless-modes.md ===

# Headless mode

By default Puppeteer launches the browser in
[the Headless mode](https://developer.chrome.com/docs/chromium/new-headless/).

```ts
const browser = await puppeteer.launch();
// Equivalent to
const browser = await puppeteer.launch({headless: true});
```

Before v22, Puppeteer launched the [old Headless mode](https://developer.chrome.com/docs/chromium/new-headless/) by default.
The old headless mode is now known as
[`chrome-headless-shell`](https://developer.chrome.com/blog/chrome-headless-shell)
and ships as a separate binary. `chrome-headless-shell` does not match the
behavior of the regular Chrome completely but it is currently more performant
for automation tasks where the complete Chrome feature set is not needed. If the performance
is more important for your use case, switch to `chrome-headless-shell` as following:

```ts
const browser = await puppeteer.launch({headless: 'shell'});
```

To launch a "headful" version of Chrome, set the
[`headless`](https://pptr.dev/api/puppeteer.launchoptions) to `false`
option when launching a browser:

```ts
const browser = await puppeteer.launch({headless: false});
```


=== FILE: docs/guides/installation.md ===

# Installation

To use Puppeteer in your project, run:

```bash npm2yarn
npm i puppeteer
```

When you install Puppeteer, it automatically downloads a recent version of
[Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing/) (~170MB macOS, ~282MB Linux, ~280MB Windows) and a `chrome-headless-shell` binary (starting with Puppeteer v21.6.0) that is [guaranteed to
work](https://pptr.dev/faq#q-why-doesnt-puppeteer-vxxx-work-with-a-certain-version-of-chrome-or-firefox)
with Puppeteer. The browser is downloaded to the `$HOME/.cache/puppeteer` folder
by default (starting with Puppeteer v19.0.0). See [configuration](https://pptr.dev/api/puppeteer.configuration) for configuration options and environmental variables to control the download behavior.

For every release since v1.7.0 we publish two packages:

- [`puppeteer`](https://www.npmjs.com/package/puppeteer)
- [`puppeteer-core`](https://www.npmjs.com/package/puppeteer-core)

`puppeteer` is a _product_ for browser automation. When installed, it downloads
a version of Chrome, which it then drives using `puppeteer-core`. Being an
end-user product, `puppeteer` automates several workflows using reasonable
defaults [that can be customized](https://pptr.dev/guides/configuration).

`puppeteer-core` is a _library_ to help drive anything that supports DevTools
protocol. Being a library, `puppeteer-core` is fully driven through its
programmatic interface implying no defaults are assumed and `puppeteer-core`
will not download Chrome when installed.

You should use `puppeteer-core` if you are
[connecting to a remote browser](https://pptr.dev/api/puppeteer.puppeteer.connect)
or [managing browsers yourself](https://pptr.dev/browsers-api).
If you are managing browsers yourself, you will need to call
[`puppeteer.launch`](https://pptr.dev/api/puppeteer.puppeteernode.launch) with
an explicit
[`executablePath`](https://pptr.dev/api/puppeteer.launchoptions)
(or [`channel`](https://pptr.dev/api/puppeteer.launchoptions) if it's
installed in a standard location).

When using `puppeteer-core`, remember to change the import:

```ts
import puppeteer from 'puppeteer-core';
```


=== FILE: docs/guides/javascript-execution.md ===

# JavaScript execution

Puppeteer allows evaluating JavaScript functions in the context of the page
driven by Puppeteer:

```ts
// Import puppeteer
import puppeteer from 'puppeteer';

(async () => {
  // Launch the browser
  const browser = await puppeteer.launch();

  // Create a page
  const page = await browser.newPage();

  // Go to your site
  await page.goto('YOUR_SITE');

  // Evaluate JavaScript
  const three = await page.evaluate(() => {
    return 1 + 2;
  });

  console.log(three);

  // Close browser.
  await browser.close();
})();
```

:::caution

Although the function is defined in your script context, it actually gets
converted to a string by Puppeteer, sent to the target page and evaluated there.
It means that the function cannot access scope variables or call other functions
defined in your Puppeteer script, and you need to define the entire function
logic within the function body.

:::

Alternatively, you can provide a function body as a string:

```ts
// Evaluate JavaScript
const three = await page.evaluate(`
    1 + 2
`);
```

:::caution

The example above produces the equivalent results but it also illustrates that
the types and global variables available to the evaluated function cannot be
known. Especially, in TypeScript you should be careful to make sure that objects
referenced by the evaluated function are correct.

:::

## Return types

The functions you evaluate can return values. If the returned value is of a
primitive type, it gets automatically converted by Puppeteer to a primitive type
in the script context like in the previous example.

If the script returns an object, Puppeteer serializes it to a JSON and
reconstructs it on the script side. This process might not always yield correct
results, for example, when you return a DOM node:

```ts
const body = await page.evaluate(() => {
  return document.body;
});
console.log(body); // {}, unexpected!
```

To work with the returned objects, Puppeteer offers a way to return objects by reference:

```ts
const body = await page.evaluateHandle(() => {
  return document.body;
});
console.log(body instanceof ElementHandle); // true
```

The returned object is either a `JSHandle` or a `ElementHandle`. `ElementHandle`
extends `JSHandle` and it is only created for DOM elements.

See the [API documentation](https://pptr.dev/api) for more details about what methods are available for handles.

## Returning promises

If you return a Promise from an evaluate call, the promise will be automatically
awaited. For example,

```ts
await page.evaluate(() => {
  // wait for 100ms.
  return new Promise(resolve => setTimeout(resolve, 100));
});
// Execution continues here once the Promise created in the page context resolves.
```

## Passing arguments to the evaluate function

You can provide arguments to your function:

```ts
const three = await page.evaluate(
  (a, b) => {
    return a + b; // 1 + 2
  },
  1,
  2,
);
```

The arguments can be primitive values or `JSHandle`s.

:::note

Page, JSHandle and ElementHandle offer several different helpers to evaluate
JavaScript but they all follow the basic principles outlined in this guide.

:::


=== FILE: docs/guides/links.md ===

# Links

- [API Documentation](https://pptr.dev/api)
- [Guides](https://pptr.dev/category/guides)
- [Examples](https://github.com/puppeteer/puppeteer/tree/main/examples)
- [Community list of Puppeteer resources](https://github.com/transitive-bullshit/awesome-puppeteer)


=== FILE: docs/guides/network-interception.md ===

# Request Interception

Once request interception is enabled, every request will stall unless it's
continued, responded or aborted.

An example of a naïve request interceptor that aborts all image requests:

```ts
import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', interceptedRequest => {
    if (interceptedRequest.isInterceptResolutionHandled()) return;
    if (
      interceptedRequest.url().endsWith('.png') ||
      interceptedRequest.url().endsWith('.jpg')
    )
      interceptedRequest.abort();
    else interceptedRequest.continue();
  });
  await page.goto('https://example.com');
  await browser.close();
})();
```

## Multiple Intercept Handlers and Asynchronous Resolutions

By default Puppeteer will raise a `Request is already handled!` exception if
`request.abort`, `request.continue`, or `request.respond` are called after any
of them have already been called.

Always assume that an unknown handler may have already called
`abort/continue/respond`. Even if your handler is the only one you registered,
3rd party packages may register their own handlers. It is therefore important to
always check the resolution status using
[request.isInterceptResolutionHandled](../api/puppeteer.httprequest.isinterceptresolutionhandled)
before calling `abort/continue/respond`.

Importantly, the intercept resolution may get handled by another listener while
your handler is awaiting an asynchronous operation. Therefore, the return value
of `request.isInterceptResolutionHandled` is only safe in a synchronous code
block. Always execute `request.isInterceptResolutionHandled` and
`abort/continue/respond` **synchronously** together.

This example demonstrates two synchronous handlers working together:

```ts
/*
This first handler will succeed in calling request.continue because the request interception has never been resolved.
*/
page.on('request', interceptedRequest => {
  if (interceptedRequest.isInterceptResolutionHandled()) return;
  interceptedRequest.continue();
});

/*
This second handler will return before calling request.abort because request.continue was already
called by the first handler.
*/
page.on('request', interceptedRequest => {
  if (interceptedRequest.isInterceptResolutionHandled()) return;
  interceptedRequest.abort();
});
```

This example demonstrates asynchronous handlers working together:

```ts
/*
This first handler will succeed in calling request.continue because the request interception has never been resolved.
*/
page.on('request', interceptedRequest => {
  // The interception has not been handled yet. Control will pass through this guard.
  if (interceptedRequest.isInterceptResolutionHandled()) return;

  // It is not strictly necessary to return a promise, but doing so will allow Puppeteer to await this handler.
  return new Promise(resolve => {
    // Continue after 500ms
    setTimeout(() => {
      // Inside, check synchronously to verify that the intercept wasn't handled already.
      // It might have been handled during the 500ms while the other handler awaited an async op of its own.
      if (interceptedRequest.isInterceptResolutionHandled()) {
        resolve();
        return;
      }
      interceptedRequest.continue();
      resolve();
    }, 500);
  });
});
page.on('request', async interceptedRequest => {
  // The interception has not been handled yet. Control will pass through this guard.
  if (interceptedRequest.isInterceptResolutionHandled()) return;

  await someLongAsyncOperation();
  // The interception *MIGHT* have been handled by the first handler, we can't be sure.
  // Therefore, we must check again before calling continue() or we risk Puppeteer raising an exception.
  if (interceptedRequest.isInterceptResolutionHandled()) return;
  interceptedRequest.continue();
});
```

For finer-grained introspection (see Cooperative Intercept Mode below), you may
also call
[request.interceptResolutionState](../api/puppeteer.httprequest.interceptresolutionstate)
synchronously before using `abort/continue/respond`.

Here is the example above rewritten using `request.interceptResolutionState`

```ts
/*
This first handler will succeed in calling request.continue because the request interception has never been resolved.
*/
page.on('request', interceptedRequest => {
  // The interception has not been handled yet. Control will pass through this guard.
  const {action} = interceptedRequest.interceptResolutionState();
  if (action === InterceptResolutionAction.AlreadyHandled) return;

  // It is not strictly necessary to return a promise, but doing so will allow Puppeteer to await this handler.
  return new Promise(resolve => {
    // Continue after 500ms
    setTimeout(() => {
      // Inside, check synchronously to verify that the intercept wasn't handled already.
      // It might have been handled during the 500ms while the other handler awaited an async op of its own.
      const {action} = interceptedRequest.interceptResolutionState();
      if (action === InterceptResolutionAction.AlreadyHandled) {
        resolve();
        return;
      }
      interceptedRequest.continue();
      resolve();
    }, 500);
  });
});
page.on('request', async interceptedRequest => {
  // The interception has not been handled yet. Control will pass through this guard.
  if (
    interceptedRequest.interceptResolutionState().action ===
    InterceptResolutionAction.AlreadyHandled
  )
    return;

  await someLongAsyncOperation();
  // The interception *MIGHT* have been handled by the first handler, we can't be sure.
  // Therefore, we must check again before calling continue() or we risk Puppeteer raising an exception.
  if (
    interceptedRequest.interceptResolutionState().action ===
    InterceptResolutionAction.AlreadyHandled
  )
    return;
  interceptedRequest.continue();
});
```

## Cooperative Intercept Mode

`request.abort`, `request.continue`, and `request.respond` can accept an
optional `priority` to work in Cooperative Intercept Mode. When all handlers are
using Cooperative Intercept Mode, Puppeteer guarantees that all intercept
handlers will run and be awaited in order of registration. The interception is
resolved to the highest-priority resolution. Here are the rules of Cooperative
Intercept Mode:

- All resolutions must supply a numeric `priority` argument to
  `abort/continue/respond`.
- If any resolution does not supply a numeric `priority`, Legacy Mode is active
  and Cooperative Intercept Mode is inactive.
- Async handlers finish before intercept resolution is finalized.
- The highest priority interception resolution "wins", i.e. the interception is
  ultimately aborted/responded/continued according to which resolution was given
  the highest priority.
- In the event of a tie, `abort` > `respond` > `continue`.

For standardization, when specifying a Cooperative Intercept Mode priority use
`0` or `DEFAULT_INTERCEPT_RESOLUTION_PRIORITY` (exported from `HTTPRequest`)
unless you have a clear reason to use a higher priority. This gracefully prefers
`respond` over `continue` and `abort` over `respond` and allows other handlers
to work cooperatively. If you do intentionally want to use a different priority,
higher priorities win over lower priorities. Negative priorities are allowed.
For example, `continue({}, 4)` would win over `continue({}, -2)`.

To preserve backward compatibility, any handler resolving the intercept without
specifying `priority` (Legacy Mode) causes immediate resolution. For Cooperative
Intercept Mode to work, all resolutions must use a `priority`. In practice, this
means you must still test for `request.isInterceptResolutionHandled` because a
handler beyond your control may have called `abort/continue/respond` without a
priority (Legacy Mode).

In this example, Legacy Mode prevails and the request is aborted immediately
because at least one handler omits `priority` when resolving the intercept:

```ts
// Final outcome: immediate abort()
page.setRequestInterception(true);
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Legacy Mode: interception is aborted immediately.
  request.abort('failed');
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;
  // Control will never reach this point because the request was already aborted in Legacy Mode

  // Cooperative Intercept Mode: votes for continue at priority 0.
  request.continue({}, 0);
});
```

In this example, Legacy Mode prevails and the request is continued because at
least one handler does not specify a `priority`:

```ts
// Final outcome: immediate continue()
page.setRequestInterception(true);
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to abort at priority 0.
  request.abort('failed', 0);
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Control reaches this point because the request was cooperatively aborted which postpones resolution.

  // { action: InterceptResolutionAction.Abort, priority: 0 }, because abort @ 0 is the current winning resolution
  console.log(request.interceptResolutionState());

  // Legacy Mode: intercept continues immediately.
  request.continue({});
});
page.on('request', request => {
  // { action: InterceptResolutionAction.AlreadyHandled }, because continue in Legacy Mode was called
  console.log(request.interceptResolutionState());
});
```

In this example, Cooperative Intercept Mode is active because all handlers
specify a `priority`. `continue()` wins because it has a higher priority than
`abort()`.

```ts
// Final outcome: cooperative continue() @ 5
page.setRequestInterception(true);
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to abort at priority 10
  request.abort('failed', 0);
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to continue at priority 5
  request.continue(request.continueRequestOverrides(), 5);
});
page.on('request', request => {
  // { action: InterceptResolutionAction.Continue, priority: 5 }, because continue @ 5 > abort @ 0
  console.log(request.interceptResolutionState());
});
```

In this example, Cooperative Intercept Mode is active because all handlers
specify `priority`. `respond()` wins because its priority ties with
`continue()`, but `respond()` beats `continue()`.

```ts
// Final outcome: cooperative respond() @ 15
page.setRequestInterception(true);
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to abort at priority 10
  request.abort('failed', 10);
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to continue at priority 15
  request.continue(request.continueRequestOverrides(), 15);
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to respond at priority 15
  request.respond(request.responseForRequest(), 15);
});
page.on('request', request => {
  if (request.isInterceptResolutionHandled()) return;

  // Cooperative Intercept Mode: votes to respond at priority 12
  request.respond(request.responseForRequest(), 12);
});
page.on('request', request => {
  // { action: InterceptResolutionAction.Respond, priority: 15 }, because respond @ 15 > continue @ 15 > respond @ 12 > abort @ 10
  console.log(request.interceptResolutionState());
});
```

## Cooperative Request Continuation

Puppeteer requires `request.continue()` to be called explicitly or the request
will hang. Even if your handler means to take no special action, or 'opt out',
`request.continue()` must still be called.

With the introduction of Cooperative Intercept Mode, two use cases arise for
cooperative request continuations: Unopinionated and Opinionated.

The first case (common) is that your handler means to opt out of doing anything
special the request. It has no opinion on further action and simply intends to
continue by default and/or defer to other handlers that might have an opinion.
But in case there are no other handlers, we must call `request.continue()` to
ensure that the request doesn't hang.

We call this an **Unopinionated continuation** because the intent is to continue
the request if nobody else has a better idea. Use
`request.continue({...}, DEFAULT_INTERCEPT_RESOLUTION_PRIORITY)` (or `0`) for
this type of continuation.

The second case (uncommon) is that your handler actually does have an opinion
and means to force continuation by overriding a lower-priority `abort()` or
`respond()` issued elsewhere. We call this an **Opinionated continuation**. In
these rare cases where you mean to specify an overriding continuation priority,
use a custom priority.

To summarize, reason through whether your use of `request.continue` is just
meant to be default/bypass behavior vs falling within the intended use case of
your handler. Consider using a custom priority for in-scope use cases, and a
default priority otherwise. Be aware that your handler may have both Opinionated
and Unopinionated cases.

## Upgrading to Cooperative Intercept Mode for package maintainers

If you are package maintainer and your package uses intercept handlers, you can
update your intercept handlers to use Cooperative Intercept Mode. Suppose you
have the following existing handler:

```ts
page.on('request', interceptedRequest => {
  if (request.isInterceptResolutionHandled()) return;
  if (
    interceptedRequest.url().endsWith('.png') ||
    interceptedRequest.url().endsWith('.jpg')
  )
    interceptedRequest.abort();
  else interceptedRequest.continue();
});
```

To use Cooperative Intercept Mode, upgrade `continue()` and `abort()`:

```ts
page.on('request', interceptedRequest => {
  if (request.isInterceptResolutionHandled()) return;
  if (
    interceptedRequest.url().endsWith('.png') ||
    interceptedRequest.url().endsWith('.jpg')
  )
    interceptedRequest.abort('failed', 0);
  else
    interceptedRequest.continue(
      interceptedRequest.continueRequestOverrides(),
      0,
    );
});
```

With those simple upgrades, your handler now uses Cooperative Intercept Mode
instead.

However, we recommend a slightly more robust solution because the above
introduces several subtle issues:

1. **Backward compatibility.** If any handler still uses a Legacy Mode
   resolution (ie, does not specify a priority), that handler will resolve the
   interception immediately even if your handler runs first. This could cause
   disconcerting behavior for your users because suddenly your handler is not
   resolving the interception and a different handler is taking priority when
   all the user did was upgrade your package.
2. **Hard-coded priority.** Your package user has no ability to specify the
   default resolution priority for your handlers. This can become important when
   the user wishes to manipulate the priorities based on use case. For example,
   one user might want your package to take a high priority while another user
   might want it to take a low priority.

To resolve both of these issues, our recommended approach is to export a
`setInterceptResolutionConfig()` from your package. The user can then call
`setInterceptResolutionConfig()` to explicitly activate Cooperative Intercept
Mode in your package so they aren't surprised by changes in how the interception
is resolved. They can also optionally specify a custom priority using
`setInterceptResolutionConfig(priority)` that works for their use case:

```ts
// Defaults to undefined which preserves Legacy Mode behavior
let _priority = undefined;

// Export a module configuration function
export const setInterceptResolutionConfig = (priority = 0) =>
  (_priority = priority);

/**
 * Note that this handler uses `DEFAULT_INTERCEPT_RESOLUTION_PRIORITY` to "pass" on this request. It is important to use
 * the default priority when your handler has no opinion on the request and the intent is to continue() by default.
 */
page.on('request', interceptedRequest => {
  if (request.isInterceptResolutionHandled()) return;
  if (
    interceptedRequest.url().endsWith('.png') ||
    interceptedRequest.url().endsWith('.jpg')
  )
    interceptedRequest.abort('failed', _priority);
  else
    interceptedRequest.continue(
      interceptedRequest.continueRequestOverrides(),
      DEFAULT_INTERCEPT_RESOLUTION_PRIORITY, // Unopinionated continuation
    );
});
```

If your package calls for more fine-grained control over resolution priorities,
use a config pattern like this:

```ts
interface InterceptResolutionConfig {
  abortPriority?: number;
  continuePriority?: number;
}

// This approach supports multiple priorities based on situational
// differences. You could, for example, create a config that
// allowed separate priorities for PNG vs JPG.
const DEFAULT_CONFIG: InterceptResolutionConfig = {
  abortPriority: undefined, // Default to Legacy Mode
  continuePriority: undefined, // Default to Legacy Mode
};

// Defaults to undefined which preserves Legacy Mode behavior
let _config: Partial<InterceptResolutionConfig> = {};

export const setInterceptResolutionConfig = (
  config: InterceptResolutionConfig,
) => (_config = {...DEFAULT_CONFIG, ...config});

page.on('request', interceptedRequest => {
  if (request.isInterceptResolutionHandled()) return;
  if (
    interceptedRequest.url().endsWith('.png') ||
    interceptedRequest.url().endsWith('.jpg')
  ) {
    interceptedRequest.abort('failed', _config.abortPriority);
  } else {
    // Here we use a custom-configured priority to allow for Opinionated
    // continuation.
    // We would only want to allow this if we had a very clear reason why
    // some use cases required Opinionated continuation.
    interceptedRequest.continue(
      interceptedRequest.continueRequestOverrides(),
      _config.continuePriority, // Why would we ever want priority!==0 here?
    );
  }
});
```

The above solutions ensure backward compatibility while also allowing the user
to adjust the importance of your package in the resolution chain when
Cooperative Intercept Mode is being used. Your package continues to work as
expected until the user has fully upgraded their code and all third party
packages to use Cooperative Intercept Mode. If any handler or package still uses
Legacy Mode, your package can still operate in Legacy Mode too.


=== FILE: docs/guides/network-logging.md ===

# Network logging

By default, Puppeteer listens for all network requests and responses and emits network events on the page.

```ts
const page = await browser.newPage();
page.on('request', request => {
  console.log(request.url());
});

page.on('response', response => {
  console.log(response.url());
});
```


=== FILE: docs/guides/ng-schematics.md ===

# Puppeteer Angular Schematic

Adds Puppeteer-based e2e tests to your Angular project.

## Getting started

Run the command below in an Angular CLI app directory and follow the prompts.

> Note this will add the schematic as a dependency to your project.

```bash
ng add @puppeteer/ng-schematics
```

Or you can use the same command followed by the [options](#options) below.

Currently, this schematic supports the following test runners:

- [**Jasmine**](https://jasmine.github.io/)
- [**Jest**](https://jestjs.io/)
- [**Mocha**](https://mochajs.org/)
- [**Node Test Runner**](https://nodejs.org/api/test.html)

With the schematics installed you can run E2E tests:

```bash
ng e2e
```

### Options

When adding schematics to your project you can to provide following options:

| Option          | Description                                            | Value                                      | Required |
| --------------- | ------------------------------------------------------ | ------------------------------------------ | -------- |
| `--test-runner` | The testing framework to install along side Puppeteer. | `"jasmine"`, `"jest"`, `"mocha"`, `"node"` | `true`   |

## Creating a single test file

Puppeteer Angular Schematic exposes a method to create a single test file.

```bash
ng generate @puppeteer/ng-schematics:e2e "<TestName>"
```

### Running test server and dev server at the same time

By default the E2E test will run the app on the same port as `ng start`.
To avoid this you can specify the port in the `angular.json`
Update either `e2e` or `puppeteer` (depending on the initial setup) to:

```json
{
  "e2e": {
    "builder": "@puppeteer/ng-schematics:puppeteer",
    "options": {
      "commands": [...],
      "devServerTarget": "sandbox:serve",
      "testRunner": "<TestRunner>",
      "port": 8080
    },
    ...
}
```

Now update the E2E test file `utils.ts` baseUrl to:

```ts
const baseUrl = 'http://localhost:8080';
```

## Contributing

Check out our [contributing guide](https://pptr.dev/contributing) to get an overview of what you need to develop in the Puppeteer repo.

### Sandbox smoke tests

To make integration easier smoke test can be run with a single command, that will create a fresh install of Angular (single application and a multi application projects). Then it will install the schematics inside them and run the initial e2e tests:

```bash
node tools/smoke.mjs
```

### Unit Testing

The schematics utilize `@angular-devkit/schematics/testing` for verifying correct file creation and `package.json` updates. To execute the test suit:

```bash npm2yarn
npm run test
```

## Migrating from Protractor

### Entry point

Puppeteer has its own [`browser`](https://pptr.dev/api/puppeteer.browser) that exposes the browser process.
A more close comparison for Protractor's `browser` would be Puppeteer's [`page`](https://pptr.dev/api/puppeteer.page).

```ts
// Testing framework specific imports

import {setupBrowserHooks, getBrowserState} from './utils';

describe('<Test Name>', function () {
  setupBrowserHooks();
  it('is running', async function () {
    const {page} = getBrowserState();
    // Query elements
    await page
      .locator('my-component')
      // Click on the element once found
      .click();
  });
});
```

### Getting element properties

You can easily get any property of the element.

```ts
// Testing framework specific imports

import {setupBrowserHooks, getBrowserState} from './utils';

describe('<Test Name>', function () {
  setupBrowserHooks();
  it('is running', async function () {
    const {page} = getBrowserState();
    // Query elements
    const elementText = await page
      .locator('.my-component')
      .map(button => button.innerText)
      // Wait for element to show up
      .wait();

    // Assert via assertion library
  });
});
```

### Query Selectors

Puppeteer supports multiple types of selectors, namely, the CSS, ARIA, text, XPath and pierce selectors.
The following table shows Puppeteer's equivalents to [Protractor By](https://www.protractortest.org/#/api?view=ProtractorBy).

> For improved reliability and reduced flakiness try our
> **Experimental** [Locators API](https://pptr.dev/guides/page-interactions#locators)

| By                | Protractor code                               | Puppeteer querySelector                                      |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------ |
| CSS (Single)      | `$(by.css('<CSS>'))`                          | `page.$('<CSS>')`                                            |
| CSS (Multiple)    | `$$(by.css('<CSS>'))`                         | `page.$$('<CSS>')`                                           |
| Id                | `$(by.id('<ID>'))`                            | `page.$('#<ID>')`                                            |
| CssContainingText | `$(by.cssContainingText('<CSS>', '<TEXT>'))`  | `page.$('<CSS> ::-p-text(<TEXT>)')` `                        |
| DeepCss           | `$(by.deepCss('<CSS>'))`                      | `page.$(':scope >>> <CSS>')`                                 |
| XPath             | `$(by.xpath('<XPATH>'))`                      | `page.$('::-p-xpath(<XPATH>)')`                              |
| JS                | `$(by.js('document.querySelector("<CSS>")'))` | `page.evaluateHandle(() => document.querySelector('<CSS>'))` |

> For advanced use cases such as Protractor's `by.addLocator` you can check Puppeteer's [Custom selectors](https://pptr.dev/guides/query-selectors#custom-selectors).

### Actions Selectors

Puppeteer allows you to all necessary actions to allow test your application.

```ts
// Click on the element.
element(locator).click();
// Puppeteer equivalent
await page.locator(locator).click();

// Send keys to the element (usually an input).
element(locator).sendKeys('my text');
// Puppeteer equivalent
await page.locator(locator).fill('my text');

// Clear the text in an element (usually an input).
element(locator).clear();
// Puppeteer equivalent
await page.locator(locator).fill('');

// Get the value of an attribute, for example, get the value of an input.
element(locator).getAttribute('value');
// Puppeteer equivalent
const element = await page.locator(locator).waitHandle();
const value = await element.getProperty('value');
```

### Example

Sample Protractor test:

```ts
describe('Protractor Demo', function () {
  it('should add one and two', function () {
    browser.get('https://juliemr.github.io/protractor-demo/');
    element(by.model('first')).sendKeys(1);
    element(by.model('second')).sendKeys(2);

    element(by.id('gobutton')).click();

    expect(element(by.binding('latest')).getText()).toEqual('3');
  });
});
```

Sample Puppeteer migration:

```ts
import {setupBrowserHooks, getBrowserState} from './utils';

describe('Puppeteer Demo', function () {
  setupBrowserHooks();
  it('should add one and two', function () {
    const {page} = getBrowserState();
    await page.goto('https://juliemr.github.io/protractor-demo/');

    await page.locator('.form-inline > input:nth-child(1)').fill('1');
    await page.locator('.form-inline > input:nth-child(2)').fill('2');
    await page.locator('#gobutton').fill('2');

    const result = await page
      .locator('.table tbody td:last-of-type')
      .map(header => header.innerText)
      .wait();

    expect(result).toEqual('3');
  });
});
```


=== FILE: docs/guides/page-interactions.md ===

# Page interactions

Puppeteer allows interacting with elements on the page through mouse, touch
events and keyboard input. Usually you first query a DOM element using a [CSS
selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors) and
then invoke an action on the selected element. All of Puppeteer APIs that accept
a selector, accept a [CSS
selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors) by
default. Additionally, Puppeteer offers [custom selector syntax](#selectors) that allows
finding elements using XPath, Text, Accessibility attributes and accessing
Shadow DOM without the need to execute JavaScript.

If you want to emit mouse or
keyboard events without selecting an element first, use the
[`page.mouse`](https://pptr.dev/api/puppeteer.mouse),
[`page.keyboard`](https://pptr.dev/api/puppeteer.keyboard) and
[`page.touchscreen`](https://pptr.dev/api/puppeteer.touchscreen) APIs. The rest
of this guide, gives an overview on how to select DOM elements and invoke
actions on them.

## Locators

Locators is the recommended way to select an element and interact with it.
Locators encapsulate the information on how to select an element and they allow
Puppeteer to automatically wait for the element to be present in the DOM and to
be in the right state for the action. You always instantiate a locator using the
[`page.locator()`](https://pptr.dev/api/puppeteer.page.locator) or
[`frame.locator()`](https://pptr.dev/api/puppeteer.frame.locator) function. If
the locator API doesn't offer a functionality you need, you can still use lower
level APIs such as
[`page.waitForSelector()`](https://pptr.dev/api/puppeteer.page.waitforselector)
or [`ElementHandle`](https://pptr.dev/api/puppeteer.elementhandle).

### Clicking an element using locators

```ts
// 'button' is a CSS selector.
await page.locator('button').click();
```

The locator automatically checks the following before clicking:

- Ensures the element is in the viewport.
- Waits for the element to become
  [visible](https://pptr.dev/api/puppeteer.elementhandle.isvisible) or hidden.
- Waits for the element to become enabled.
- Waits for the element to have a stable bounding box over two consecutive
  animation frames.

### Filling out an input

```ts
// 'input' is a CSS selector.
await page.locator('input').fill('value');
```

Automatically detects the input type and choose an appropriate way to fill it
out with the provided value. For example, it will fill out `<select>` elements as
well as `<input>` elements.

The locator automatically checks the following before typing into the input:

- Ensures the element is in the viewport.
- Waits for the element to become
  [visible](https://pptr.dev/api/puppeteer.elementhandle.isvisible) or hidden.
- Waits for the element to become enabled.
- Waits for the element to have a stable bounding box over two consecutive
  animation frames.

#### Hover over an element

```ts
await page.locator('div').hover();
```

The locator automatically checks the following before hovering:

- Ensures the element is in the viewport.
- Waits for the element to become
  [visible](https://pptr.dev/api/puppeteer.elementhandle.isvisible) or hidden.
- Waits for the element to have a stable bounding box over two consecutive
  animation frames.

#### Scroll an element

The [`.scroll()`] functions uses mouse wheel events to scroll an element.

```ts
// Scroll the div element by 10px horizontally
// and by 20 px vertically.
await page.locator('div').scroll({
  scrollLeft: 10,
  scrollTop: 20,
});
```

The locator automatically checks the following before scrolling:

- Ensures the element is in the viewport.
- Waits for the element to become
  [visible](https://pptr.dev/api/puppeteer.elementhandle.isvisible) or hidden.
- Waits for the element to have a stable bounding box over two consecutive
  animation frames.

### Waiting for element to be visible

Sometimes you only need to wait for the element to be visible.

```ts
// '.loading' is a CSS selector.
await page.locator('.loading').wait();
```

The locator automatically checks the following before returning:

- Waits for the element to become
  [visible](https://pptr.dev/api/puppeteer.elementhandle.isvisible) or hidden.

### Waiting for a function

Sometimes it is useful to wait for an arbitrary condition expressed as a
JavaScript function. In this case, locator can be defined using a function
instead of a selector. The following example waits until at least 3 paragraphs
are present on the page, then extracts their text. You can also call locator
functions such as `.click()` or `.fill()` instead of mapping elements to text.

```ts
const paragraphs = await page
  .locator(() => {
    const paragraphs = document.querySelectorAll('p');

    if (paragraphs.length >= 3) {
      return [...paragraphs].map(p => p.textContent);
    }
  })
  .wait();
```

### Applying filters on locators

The following example shows how to add extra conditions to the locator expressed
as a JavaScript function. The button element will only be clicked if its
`textContent` is 'My button'.

```ts
await page
  .locator('button')
  .filter(button => button.textContent === 'My button')
  .click();
```

Since `.filter()`'s callback is executed in browser context, it doesn't have access to variables from the Node scope. You can build a string function to inject a variable:

```ts
const buttonName = 'My button';
await page
  .locator('button')
  .filter(`button => button.textContent === ${JSON.stringify(buttonName)}`)
  .click();
```

### Returning values from a locator

The [`map`](https://pptr.dev/api/puppeteer.locator.map) function allows mapping
an element to a JavaScript value. In this case, calling `wait()` will return the
deserialized JavaScript value.

```ts
const enabled = await page
  .locator('button')
  .map(button => !button.disabled)
  .wait();
```

### Returning ElementHandles from a locator

The [`waitHandle`](https://pptr.dev/api/puppeteer.locator.waithandle) function
allows returning the
[ElementHandle](https://pptr.dev/api/puppeteer.elementhandle). It might be
useful if there is no corresponding locator API for the action you need.

```ts
const buttonHandle = await page.locator('button').waitHandle();
await buttonHandle.click();
```

### Configuring locators

Locators can be configured to tune configure the preconditions and other options:

```ts
// Clicks on a button without waiting for any preconditions.
await page
  .locator('button')
  .setEnsureElementIsInTheViewport(false)
  .setVisibility(null)
  .setWaitForEnabled(false)
  .setWaitForStableBoundingBox(false)
  .click();
```

### Locator timeouts

By default, locators inherit the timeout setting from the page. But it is
possible to set the timeout on the per-locator basis. A
[TimeoutError](https://pptr.dev/api/puppeteer.timeouterror) will be thrown if
the element is not found or the preconditions are not met within the specified
time period.

```ts
// Time out after 3 sec.
await page.locator('button').setTimeout(3000).click();
```

### Getting locator events

Currently, locators support [a single
event](https://pptr.dev/api/puppeteer.locatorevents) that notifies you when the
locator is about to perform the action indicating that pre-conditions have been
met:

```ts
let willClick = false;
await page
  .locator('button')
  .on(LocatorEvent.Action, () => {
    willClick = true;
  })
  .click();
```

This event can be used for logging/debugging or other purposes. The event might
fire multiple times if the locator retries the action.

## waitForSelector

[`waitForSelector`](https://pptr.dev/api/puppeteer.page.waitforselector) is a
lower-level API compared to locators that allows waiting for an element to be
available in DOM. It does not automatically retry the action if it fails and
requires manually disposing the resulting ElementHandle to prevent memory leaks.
The method exists on the Page, Frame and ElementHandle instances.

```ts
// Import puppeteer
import puppeteer from 'puppeteer';

// Launch the browser.
const browser = await puppeteer.launch();

// Create a page.
const page = await browser.newPage();

// Go to your site.
await page.goto('YOUR_SITE');

// Query for an element handle.
const element = await page.waitForSelector('div > .class-name');

// Do something with element...
await element.click(); // Just an example.

// Dispose of handle.
await element.dispose();

// Close browser.
await browser.close();
```

Some page level APIs such as `page.click(selector)`, `page.type(selector)`,
`page.hover(selector)` are implemented using `waitForSelector` for
backwards-compatibility reasons.

## Querying without waiting

Sometimes you know that the elements are already on the page. In that case,
Puppeteer offers multiple ways to find an element or multiple elements matching a
selector. These methods exist on Page, Frame and ElementHandle instances.

- [`page.$()`](https://pptr.dev/api/puppeteer.page._) returns a single element
  matching a selector.
- [`page.$$()`](https://pptr.dev/api/puppeteer.page.__) returns all elements matching a selector.
- [`page.$eval()`](https://pptr.dev/api/puppeteer.page._eval) returns the result
  of running a JavaScript function on the first element matching a selector.
- [`page.$$eval()`](https://pptr.dev/api/puppeteer.page.__eval) returns the
  result of running a JavaScript function on each element matching a selector.

## Selectors

Puppeteer accepts [CSS
selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors) in
every API that accepts a selector. Additionally, you can opt-in into using
additional selector syntax to do more than CSS selectors offer.

### Non-CSS selectors

Puppeteer extends the CSS syntax with custom
[pseudo-elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements)
that define how to select an element using a non-CSS selector. The Puppeteer
supported pseudo-elements are prefixed with a `-p` vendor prefix.

#### XPath selectors (`-p-xpath`)

XPath selectors will use the browser's native [`Document.evaluate`](https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate) to query for elements.

```ts
// Runs the `//h2` as the XPath expression.
const element = await page.waitForSelector('::-p-xpath(//h2)');
```

#### Text selectors (`-p-text`)

Text selectors will select "minimal" elements containing the given text, even
within (open) shadow roots. Here, "minimum" means the deepest elements that
contain a given text, but not their parents (which technically will also contain
the given text).

```ts
// Click a button inside a div element that has Checkout as the inner text.
await page.locator('div ::-p-text(Checkout)').click();
// You need to escape CSS selector syntax such '(', ')' if it is part of the your search text ('Checkout (2 items)').
await page.locator(':scope >>> ::-p-text(Checkout \\(2 items\\))').click();
// or use quotes escaping any quotes that are part of the search text ('He said: "Hello"').
await page.locator(':scope >>> ::-p-text("He said: \\"Hello\\"")').click();
```

#### ARIA selectors (`-p-aria`)

ARIA selectors can be used to find elements using the computed accessible name
and role. These labels are computed using the browsers internal representation
of the accessibility tree. That means that ARIA relationships such as labeledby
are resolved before the query is run. The ARIA selectors are useful if you do
not want to depend on any particular DOM structure or DOM attributes.

```ts
await page.locator('::-p-aria(Submit)').click();
await page.locator('::-p-aria([name="Click me"][role="button"])').click();
```

#### Pierce selector (`pierce/`)

Pierce selector is a selector that returns all elements matching the provided CSS selector in
all shadow roots in the document. We recommend using [deep
combinators](#querying-elements-in-shadow-dom) instead because they offer more
flexibility in combining difference selectors. `pierce/` is only available in
the [prefixed notation](#prefixed-selector-syntax).

```ts
await page.locator('pierce/div').click();
// Same query as the pierce/ one using deep combinators.
await page.locator('& >>> div').click();
```

### Querying elements in Shadow DOM

CSS selectors do not allow descending into Shadow DOM, therefore, Puppeteer adds
two combinators to the CSS selector syntax that allow searching inside [shadow
DOM](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM).

#### The `>>>` combinator

The `>>>` is called the _deep descendent_ combinator. It is analogous to the
CSS's descendent combinator (denoted with a single space character <code>&nbsp;</code>, for
example, `div button`) and it selects matching elements under the parent element
at any depth. For example, `my-custom-element >>> button` would select all
button elements that are available inside shadow DOM of the `my-custom-element`
(the shadow host).

:::note

Deep combinators only work on the first "depth" of CSS selectors and open shadow
roots; for example, `:is(div > > a)` will not work.

:::

#### The `>>>>` combinator

The `>>>>` is called the _deep child_ combinator. It is analogous to the CSS's
child combinator (denoted with `>`, for example, `div > button`) and it selects
matching elements under the parent element's immediate shadow root, if the
element has one. For example,
`my-custom-element >>>> button` would select all button elements that are available
inside the immediate shadow root of the `my-custom-element` (the shadow host).

### Custom selectors

You can also add your own pseudo element using
[Puppeteer.registerCustomQueryHandler](../api/puppeteer.puppeteer.registercustomqueryhandler.md).
This is useful for creating custom selectors based on framework objects or your application.

For example, you can write all your selectors using the `react-component` pseudo-element
and implement a custom logic how to resolve the provided ID.

```ts
Puppeteer.registerCustomQueryHandler('react-component', {
  queryOne: (elementOrDocument, selector) => {
    // Dummy example just delegates to querySelector but you can find your
    // React component because this callback runs in the page context.
    return elementOrDocument.querySelector(`[id="${CSS.escape(selector)}"]`);
  },
  queryAll: (elementOrDocument, selector) => {
    // Dummy example just delegates to querySelector but you can find your
    // React component because this callback runs in the page context.
    return elementOrDocument.querySelectorAll(`[id="${CSS.escape(selector)}"]`);
  },
});
```

In your application you can now write selectors as following.

```ts
await page.locator('::-p-react-component(MyComponent)').click();
// OR used in conjunction with other selectors.
await page.locator('.side-bar ::-p-react-component(MyComponent)').click();
```

Another example shows how you can define a custom query handler for locating vue
components:

:::caution

Be careful when relying on internal APIs of libraries or frameworks. They can change at any time.

:::

```ts
Puppeteer.registerCustomQueryHandler('vue', {
  queryOne: (element, name) => {
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_ELEMENT);
    do {
      const currentNode = walker.currentNode;
      if (
        currentNode.__vnode?.ctx?.type?.name.toLowerCase() ===
        name.toLocaleLowerCase()
      ) {
        return currentNode;
      }
    } while (walker.nextNode());

    return null;
  },
});
```

Search for a given view component as following:

```ts
const element = await page.$('::-p-vue(MyComponent)');
```

### Prefixed selector syntax

:::caution

While we maintain prefixed selectors, the recommended way is to use the selector syntax documented above.

:::

The following legacy syntax (`${nonCssSelectorName}/${nonCssSelector}`) allows
running a single non-CSS selector at a time is also supported. Note that this
syntax does not allow combining multiple selectors.

```ts
// Same as ::-p-text("My text").
await page.locator('text/My text').click();
// Same as ::-p-xpath(//h2).
await page.locator('xpath///h2').click();
// Same as ::-p-aria(My label).
await page.locator('aria/My label').click();

await page.locator('pierce/div').click();
```


=== FILE: docs/guides/pdf-generation.md ===

# PDF generation

For printing PDFs use [`Page.pdf()`](https://pptr.dev/api/puppeteer.page.pdf).

```ts
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com', {
  waitUntil: 'networkidle2',
});
// Saves the PDF to hn.pdf.
await page.pdf({
  path: 'hn.pdf',
});

await browser.close();
```

By default, the [`Page.pdf()`](https://pptr.dev/api/puppeteer.page.pdf) waits for fonts to be loaded.


=== FILE: docs/guides/running-puppeteer-in-extensions.md ===

# Running Puppeteer in Chrome extensions

:::caution

Chrome extensions environment is significantly different from the usual Node.JS environment, therefore, the support for running Puppeteer in chrome.debugger
is currently experimental. Please submit issues https://github.com/puppeteer/puppeteer/issues/new/choose if you encounted bugs.

:::

Chrome Extensions allow accessing Chrome DevTools Protocol via [`chrome.debugger`](https://developer.chrome.com/docs/extensions/reference/api/debugger).
[`chrome.debugger`](https://developer.chrome.com/docs/extensions/reference/api/debugger) provides a restricted access to CDP and allows attaching to one
page at a time. Therefore, Puppeteer requires a different transport to be used and Puppeteer's view is limited to a single page. It means you can
interact with a single page and its frames and workers but cannot create new pages using Puppeteer. To create a new page you need to use the
[`chrome.tabs`](https://developer.chrome.com/docs/extensions/reference/api/tabs) API and establish a new Puppeteer connection.

## How to run Puppeteer in Chrome extensions

:::note

See https://github.com/puppeteer/puppeteer/tree/main/examples/puppeteer-in-extension for a complete example.

:::

To run Puppeteer in an extension, first you need to produce a browser-compatible build using a bundler such as rollup or webpack:

1. When importing Puppeteer use the browser-specific entrypoint from puppeteer-core `puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js'`:

```ts
import {
  connect,
  ExtensionTransport,
} from 'puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js';

// Create a tab or find a tab to attach to.
const tab = await chrome.tabs.create({
  url,
});
// Connect Puppeteer using the ExtensionTransport.connectTab.
const browser = await connect({
  transport: await ExtensionTransport.connectTab(tab.id),
});
// You will have a single page on the browser object, which corresponds
// to the tab you connected the transport to.
const [page] = await browser.pages();
// Perform the usual operations with Puppeteer page.
console.log(await page.evaluate('document.title'));
browser.disconnect();
```

2. Build your extension using a bundler. For example, the following configuration can be used with rollup:

```js
import {nodeResolve} from '@rollup/plugin-node-resolve';

export default {
  input: 'main.mjs',
  output: {
    format: 'esm',
    dir: 'out',
  },
  // If you do not need to use WebDriver BiDi protocol,
  // exclude chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js to minimize the bundle size.
  external: ['chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js'],
  plugins: [
    nodeResolve({
      // Indicate that we target a browser environment.
      browser: true,
      // Exclude any dependencies except for puppeteer-core.
      // `npm install puppeteer-core` # To install puppeteer-core if needed.
      resolveOnly: ['puppeteer-core'],
    }),
  ],
};
```


=== FILE: docs/guides/running-puppeteer-in-the-browser.md ===

# Running Puppeteer in the browser

Puppeteer is a powerful tool for automating browsers, but did you know its API can also run within a browser itself? This enables you to leverage Puppeteer's capabilities for tasks that don't require Node.js specific features.

:::note

Note that while the Puppeteer API can run from a client webpage, the automation actions are sent to a separate browser with an open debugging port.

:::

## Supported Features

While running in the browser, Puppeteer offers a variety of functionalities including:

1. WebSocket Connections: Establish connections to existing browser instances using WebSockets. Launching or downloading browsers directly is not supported as it relies on Node.js APIs.
2. Script Evaluation: Execute JavaScript code within the remote browser context.
3. Document Manipulation: Generate PDFs and screenshots of the remote browser page.
4. Page Management: Create, close, and navigate between different web pages in the remote browser.
5. Cookie Handling: Inspect, modify, and manage cookies within the remote browser.
6. Network Control: Monitor and intercept network requests made by the remote browser.

## How to run Puppeteer in the browser

:::note

See https://github.com/puppeteer/puppeteer/tree/main/examples/puppeteer-in-browser for a complete example.

:::

To run Puppeteer in the browser, first you need to produce a browser-compatible build using a bundler such as rollup or webpack:

1. When importing Puppeteer use the browser-specific entrypoint from puppeteer-core `puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js'`:

```ts
import puppeteer from 'puppeteer-core/lib/esm/puppeteer/puppeteer-core-browser.js';

const browser = await puppeteer.connect({
  browserWSEndpoint: wsUrl,
});

alert('Browser has ' + (await browser.pages()).length + ' pages');

browser.disconnect();
```

2. Build your app using a bundler. For example, the following configuration can be used with rollup:

```js
import {nodeResolve} from '@rollup/plugin-node-resolve';

export default {
  input: 'main.mjs',
  output: {
    format: 'esm',
    dir: 'out',
  },
  // If you do not need to use WebDriver BiDi protocol,
  // exclude chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js to minimize the bundle size.
  external: ['chromium-bidi/lib/cjs/bidiMapper/BidiMapper.js'],
  plugins: [
    nodeResolve({
      // Indicate that we target a browser environment.
      browser: true,
      // Exclude any dependencies except for puppeteer-core.
      // `npm install puppeteer-core` # To install puppeteer-core if needed.
      resolveOnly: ['puppeteer-core'],
    }),
  ],
};
```

:::note

Do not forget to include a valid browser WebSocket endpoint when connecting to a remote browser instance.

:::

3. Include the produced bundle into a web page.


=== FILE: docs/guides/screen-configuration.md ===

# Screen configuration

Use [`--screen-info`](https://chromium.googlesource.com/chromium/src/+/main/components/headless/screen_info/README.md) command line switch to configure headless screen.

The following script configures Chrome to run in a dual-screen configuration. The primary 800x600 screen is configured in a landscape orientation, and the secondary 600x800 screen, positioned directly to the right of the primary screen, is in a portrait orientation.

```ts
import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    args: ['--screen-info={800x600 label=1st}{600x800 label=2nd}'],
  });

  const screens = await browser.screens();
  const screenInfos = screens.map(
    s =>
      `Screen [${s.id}]` +
      ` ${s.left},${s.top} ${s.width}x${s.height}` +
      ` label='${s.label}'` +
      ` isPrimary=${s.isPrimary}` +
      ` isExtended=${s.isExtended}` +
      ` isInternal=${s.isInternal}` +
      ` colorDepth=${s.colorDepth}` +
      ` devicePixelRatio=${s.devicePixelRatio}` +
      ` avail=${s.availLeft},${s.availTop} ${s.availWidth}x${s.availHeight}` +
      ` orientation.type=${s.orientation.type}` +
      ` orientation.angle=${s.orientation.angle}`,
  );

  console.log(
    `Number of screens: ${screens.length}\n` + screenInfos.join('\n'),
  );

  await browser.close();
})();
```

Output:

```
Number of screens: 2
Screen [1] 0,0 800x600 label='1st' isPrimary=true isExtended=true isInternal=false colorDepth=24 devicePixelRatio=1 avail=0,0 800x600 orientation.type=landscapePrimary orientation.angle=0
Screen [2] 800,0 600x800 label='2nd' isPrimary=false isExtended=true isInternal=false colorDepth=24 devicePixelRatio=1 avail=800,0 600x800 orientation.type=portraitPrimary orientation.angle=0
```

With no `--screen-info` switch, the headless screen has one 800x600 screen unless the `--window-size` switch is specified, in which case the headless screen is as large as the requested window size.

:::caution

The `--screen-info` switch is only available in headless mode. Headful Chrome always uses physical platform screens.

:::

## Dynamic headless screen configuration

Use Puppeteer's [`Browser.addScreen`](https://pptr.dev/next/api/puppeteer.browser.addscreen) and [`Browser.removeScreen`](https://pptr.dev/next/api/puppeteer.browser.removescreen) methods to add and remove screens while Chrome browser is running. Use [`Browser.screens`](https://pptr.dev/next/api/puppeteer.browser.screens) method to retrieve the current screen configuration.

The following script adds and removes a secondary screen while logging the screen configuration at each step.

```ts
import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    args: ['--screen-info={800x600 label=1st}'],
  });

  function getScreenInfo(s) {
    return (
      `Screen [${s.id}]` +
      ` ${s.left},${s.top} ${s.width}x${s.height}` +
      ` label='${s.label}'` +
      ` isPrimary=${s.isPrimary}` +
      ` isExtended=${s.isExtended}`
    );
  }

  async function logScreenConfig(text) {
    if (text !== undefined) {
      console.log(text);
    }
    const screens = await browser.screens();
    const screenInfos = screens.map(s => getScreenInfo(s));

    console.log(
      `Number of screens: ${screens.length}\n` + screenInfos.join('\n'),
    );
  }

  await logScreenConfig('---- Initial:');

  // Add a screen.
  const addedScreenInfo = await browser.addScreen({
    left: 800,
    top: 0,
    width: 800,
    height: 600,
    label: '2nd',
  });

  console.log('Added screen: ' + getScreenInfo(addedScreenInfo));
  await logScreenConfig('---- With the screen added:');

  // Remove the added screen.
  await browser.removeScreen(addedScreenInfo.id);
  await logScreenConfig('---- With added screen removed:');

  await browser.close();
})();
```

Output:

```
---- Initial:
Number of screens: 1
Screen [1] 0,0 800x600 label='1st' isPrimary=true isExtended=false
Added screen: Screen [2] 800,0 800x600 label='2nd' isPrimary=false isExtended=true
---- With the screen added:
Number of screens: 2
Screen [1] 0,0 800x600 label='1st' isPrimary=true isExtended=true
Screen [2] 800,0 800x600 label='2nd' isPrimary=false isExtended=true
---- With added screen removed:
Number of screens: 1
Screen [1] 0,0 800x600 label='1st' isPrimary=true isExtended=false
```

:::caution

The `Browser.addScreen` and `Browser.removeScreen` methods are only available in headless mode. The `Browser.screens` method is available in both headful and headless modes.

:::


=== FILE: docs/guides/screenshots.md ===

# Screenshots

For capturing screenshots use [`Page.screenshot()`](https://pptr.dev/api/puppeteer.page.screenshot).

```ts
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com', {
  waitUntil: 'networkidle2',
});
await page.screenshot({
  path: 'hn.png',
});

await browser.close();
```

You can also capture a screenshot of a specific element using [`ElementHandle.screenshot()`](https://pptr.dev/api/puppeteer.elementhandle.screenshot):

```ts
const fileElement = await page.waitForSelector('div');
await fileElement.screenshot({
  path: 'div.png',
});
```

By default, [`ElementHandle.screenshot()`](https://pptr.dev/api/puppeteer.elementhandle.screenshot) tries to scroll the element into view
if it is hidden.


=== FILE: docs/guides/system-requirements.md ===

# System requirements

- Node 18+. Puppeteer follows the latest
  [maintenance LTS](https://github.com/nodejs/Release#release-schedule) version of
  Node

- TypeScript 4.7.4+ (If used with TypeScript).
  - Target ES2022 or later if you [type check node_modules](https://www.typescriptlang.org/tsconfig/#skipLibCheck).

- Chrome for Testing browser system requirements:
  - [Windows](https://support.google.com/chrome/a/answer/7100626?hl=en#:~:text=the%20specified%20criteria.-,Windows,-To%20use%20Chrome), x64 architecture
  - [MacOS](https://support.google.com/chrome/a/answer/7100626?hl=en#:~:text=Not%20yet%20scheduled-,Mac,-To%20use%20Chrome), x64 and arm64 architectures
  - [Debian/Ubuntu Linux](https://support.google.com/chrome/a/answer/7100626?hl=en#:~:text=10.15%20or%20later-,Linux,-To%20use%20Chrome), with x64 architecture
    - Required system packages https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/linux/debian/dist_package_versions.json
  - [openSUSE/Fedora Linux](https://support.google.com/chrome/a/answer/7100626?hl=en#:~:text=10.15%20or%20later-,Linux,-To%20use%20Chrome), with x64 architecture
    - Required system packages https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/linux/rpm/dist_package_provides.json

- Firefox browser system requirements:
  - https://www.mozilla.org/en-US/firefox/system-requirements/
  - The `xz` or `bzip2` utilities are required to unpack Firefox versions for Linux.


=== FILE: docs/guides/what-is-puppeteer.md ===

# What is Puppeteer?

Puppeteer is a JavaScript library which provides a high-level API to
control Chrome or Firefox over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) or
[WebDriver BiDi](https://pptr.dev/webdriver-bidi). Puppeteer runs in the
headless (no visible UI) by default but can be configured to run in a
visible ("headful") browser.

# Features

Most things that you can do manually in the browser can be done using Puppeteer!
Here are a few examples to get you started:

- Automate form submission, UI testing, keyboard input, etc.
- Create an automated testing environment using the latest JavaScript and
  browser features.
- Capture a
  [timeline trace](https://developer.chrome.com/docs/devtools/performance/reference)
  of your site to help diagnose performance issues.
- [Test Chrome Extensions](https://pptr.dev/guides/chrome-extensions).
- Generate screenshots and PDFs of pages.
- Crawl a SPA (Single-Page Application) and generate pre-rendered content (i.e.
  "SSR" (Server-Side Rendering)).


=== FILE: docs/guides/window-management.md ===

# Window management

Use Puppeteer's [`Browser.getWindowBounds`](https://pptr.dev/api/puppeteer.browser.getwindowbounds) and[`Browser.setWindowBounds`](https://pptr.dev/api/puppeteer.browser.setwindowbounds) methods to manage browser window position and state.

The following script opens a window at the default position on a primary 800x600 screen, then moves that window to a newly created screen and maximizes it there. After that it restores the window to its normal state.

```ts
import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    args: ['--screen-info={800x600}'],
  });

  async function logWindowBounds() {
    const bounds = await browser.getWindowBounds(windowId);
    console.log(
      `${bounds.left},${bounds.top}` +
        ` ${bounds.width}x${bounds.height}` +
        ` ${bounds.windowState}`,
    );
  }

  // Create new page.
  const page = await browser.newPage({type: 'window'});
  const windowId = await page.windowId();
  await logWindowBounds();

  // Add a screen to the right of the primary screen.
  const screenInfo = await browser.addScreen({
    left: 800,
    top: 0,
    width: 1600,
    height: 1200,
  });

  // Move the window to the newly created secondary screen.
  await browser.setWindowBounds(windowId, {
    left: screenInfo.left + 50,
    top: screenInfo.top + 50,
    width: screenInfo.width - 100,
    height: screenInfo.height - 100,
  });
  await logWindowBounds();

  // Maximize the window.
  await browser.setWindowBounds(windowId, {windowState: 'maximized'});
  await logWindowBounds();

  // Restore the window.
  await browser.setWindowBounds(windowId, {windowState: 'normal'});
  await logWindowBounds();

  await browser.close();
})();
```

Output:

```
20,20 780x580 normal
850,50 1500x1100 normal
800,0 1600x1200 maximized
850,50 1500x1100 normal
```

## Sizing page content

Use Puppeteer's [`Page.resize`](https://pptr.dev/api/puppeteer.page.resize) method to adjust the browser window size so that the content has the specified size.

Example:

```ts
import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    args: ['--screen-info={800x600}'],
  });

  const page = (await browser.pages())[0];

  // Default viewport restricts window to 800x600, so remove it.
  await page.setViewport(null);

  // Inner window size is updated asynchronously, so wait for
  // the window size change to get reported before logging it.
  const resized = page.evaluate(() => {
    return new Promise(resolve => {
      window.onresize = resolve;
    });
  });

  await page.resize({contentWidth: 600, contentHeight: 400});
  await resized;

  const result = await page.evaluate(() => {
    return (
      `Inner size: ${window.innerWidth}x${window.innerHeight}\n` +
      `Outer size: ${window.outerWidth}x${window.outerHeight}`
    );
  });

  console.log(result);

  await browser.close();
})();
```

Output:

```
Inner size: 600x400
Outer size: 600x487
```

## Fullscreen element

The following example demonstrates how to request full-screen mode for an element on click.

```ts
import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    args: ['--screen-info={1600x1200}'],
  });

  const page = (await browser.pages())[0];
  await page.setContent(`
    <div id="click-box" style="width: 10px; height: 10px;"/>
  `);

  await page.evaluate(() => {
    const element = document.getElementById('click-box');
    element.addEventListener('click', () => {
      element.requestFullscreen();
    });
  });

  await page.click('#click-box');

  const windowId = await page.windowId();
  const bounds = await browser.getWindowBounds(windowId);
  console.log(
    `${bounds.left},${bounds.top}` +
      ` ${bounds.width}x${bounds.height}` +
      ` ${bounds.windowState}`,
  );

  await browser.close();
})();
```

Output:

```
0,0 1600x1200 fullscreen
```
