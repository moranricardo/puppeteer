---
sidebar_label: Browser
---

# Browser class

[Browser](./puppeteer.browser.md) represents a browser instance that is either:

- connected to via [Puppeteer.connect()](./puppeteer.puppeteer.connect.md)
- launched by [PuppeteerNode.launch()](./puppeteer.puppeteernode.launch.md)

[Browser](./puppeteer.browser.md) [emits](./puppeteer.eventemitter.emit.md) various events which are documented in the [BrowserEvent](./puppeteer.browserevent.md) enum.

### Signature

```typescript
export declare abstract class Browser extends EventEmitter<BrowserEvents>
```

**Extends:** [EventEmitter](./puppeteer.eventemitter.md)&lt;[BrowserEvents](./puppeteer.browserevents.md)&gt;

## Remarks

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `Browser` class.

## Example 1

Using a [Browser](./puppeteer.browser.md) to create a [Page](./puppeteer.page.md):

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

## Example 2

Disconnecting from and reconnecting to a [Browser](./puppeteer.browser.md):

```ts
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch();
// Store the endpoint to be able to reconnect to the browser.
const browserWSEndpoint = browser.wsEndpoint();
// Disconnect puppeteer from the browser.
await browser.disconnect();

// Use the endpoint to reestablish a connection
const browser2 = await puppeteer.connect({browserWSEndpoint});
// Close the browser.
await browser2.close();
```

Properties
<table><thead><tr><th>
Property
</th><th>
Modifiers
</th><th>
Type
</th><th>
Description
</th></tr></thead>
<tbody><tr><td>
<span id="connected">connected</span>
</td><td>
readonly
</td><td>
boolean
</td><td>
Whether Puppeteer is connected to this browser.
</td></tr>
<tr><td>
<span id="debuginfo">debugInfo</span>
</td><td>
readonly
</td><td>
DebugInfo
</td><td>
(Experimental) Get debug information from Puppeteer.
Remarks:
Currently, includes pending protocol calls. In the future, we might add more info.
</td></tr>
</tbody></table>

Methods
<table><thead><tr><th>
Method
</th><th>
Modifiers
</th><th>
Description
</th></tr></thead>
<tbody><tr><td>
<span id="addscreen">addScreen(params)</span>
</td><td>
</td><td>
Adds a new screen, returns the added screen information object.
Remarks:
Only supported in headless mode.
</td></tr>
<tr><td>
<span id="browsercontexts">browserContexts()</span>
</td><td>
</td><td>
Gets a list of open browser contexts.
In a newly-created browser, this will return a single instance of BrowserContext.
</td></tr>
<tr><td>
<span id="close">close()</span>
</td><td>
</td><td>
Closes this browser and all associated pages.
</td></tr>
<tr><td>
<span id="cookies">cookies()</span>
</td><td>
</td><td>
Returns all cookies in the default BrowserContext.
Remarks:
Shortcut for browser.defaultBrowserContext().cookies().
</td></tr>
<tr><td>
<span id="createbrowsercontext">createBrowserContext(options)</span>
</td><td>
</td><td>
Creates a new browser context.
This won't share cookies/cache with other browser contexts.
</td></tr>
<tr><td>
<span id="defaultbrowsercontext">defaultBrowserContext()</span>
</td><td>
</td><td>
Gets the default browser context.
Remarks:
The default browser context cannot be closed.
</td></tr>
<tr><td>
<span id="deletecookie">deleteCookie(cookies)</span>
</td><td>
</td><td>
Removes cookies from the default BrowserContext.
Remarks:
Shortcut for browser.defaultBrowserContext().deleteCookie().
</td></tr>
<tr><td>
<span id="deletematchingcookies">deleteMatchingCookies(filters)</span>
</td><td>
</td><td>
Deletes cookies matching the provided filters from the default BrowserContext.
Remarks:
Shortcut for browser.defaultBrowserContext().deleteMatchingCookies().
</td></tr>
<tr><td>
<span id="disconnect">disconnect()</span>
</td><td>
</td><td>
Disconnects Puppeteer from this browser, but leaves the process running.
</td></tr>
<tr><td>
<span id="getwindowbounds">getWindowBounds(windowId)</span>
</td><td>
</td><td>
Gets the specified window bounds.
</td></tr>
<tr><td>
<span id="installextension">installExtension(path)</span>
</td><td>
</td><td>
Installs an extension and returns the ID. In Chrome, this is only available if the browser was created using pipe: true and the --enable-unsafe-extension-debugging flag is set.
</td></tr>
<tr><td>
<span id="isconnected">isConnected()</span>
</td><td>
deprecated
</td><td>
Whether Puppeteer is connected to this browser.
Deprecated:
Use Browser.connected.
</td></tr>
<tr><td>
<span id="newpage">newPage(options)</span>
</td><td>
</td><td>
Creates a new page in the default browser context.
</td></tr>
<tr><td>
<span id="pages">pages(includeAll)</span>
</td><td>
</td><td>
Gets a list of all open pages inside this Browser.
If there are multiple browser contexts, this returns all pages in all browser contexts.
Remarks:
Non-visible pages, such as "background_page", will not be listed here. You can find them using Target.page().
</td></tr>
<tr><td>
<span id="process">process()</span>
</td><td>
</td><td>
Gets the associated ChildProcess.
</td></tr>
<tr><td>
<span id="removescreen">removeScreen(screenId)</span>
</td><td>
</td><td>
Removes a screen.
Remarks:
Only supported in headless mode. Fails if the primary screen id is specified.
</td></tr>
<tr><td>
<span id="screens">screens()</span>
</td><td>
</td><td>
Gets a list of screen information objects.
</td></tr>
<tr><td>
<span id="setcookie">setCookie(cookies)</span>
</td><td>
</td><td>
Sets cookies in the default BrowserContext.
Remarks:
Shortcut for browser.defaultBrowserContext().setCookie().
</td></tr>
<tr><td>
<span id="setpermission">setPermission(origin, permissions)</span>
</td><td>
</td><td>
Sets the permission for a specific origin in the default BrowserContext.
Remarks:
Shortcut for browser.defaultBrowserContext().setPermission().
</td></tr>
<tr><td>
<span id="setwindowbounds">setWindowBounds(windowId, windowBounds)</span>
</td><td>
</td><td>
Sets the specified window bounds.
</td></tr>
<tr><td>
<span id="target">target()</span>
</td><td>
</td><td>
Gets the target associated with the default browser context).
</td></tr>
<tr><td>
<span id="targets">targets()</span>
</td><td>
</td><td>
Gets all active targets.
In case of multiple browser contexts, this returns all targets in all browser contexts.
</td></tr>
<tr><td>
<span id="uninstallextension">uninstallExtension(id)</span>
</td><td>
</td><td>
Uninstalls an extension. In Chrome, this is only available if the browser was created using pipe: true and the --enable-unsafe-extension-debugging flag is set.
</td></tr>
<tr><td>
<span id="useragent">userAgent()</span>
</td><td>
</td><td>
Gets this browser's original user agent.
Pages can override the user agent with Page.setUserAgent().
</td></tr>
<tr><td>
<span id="version">version()</span>
</td><td>
</td><td>
Gets a string representing this browser's name and version.
For headless browser, this is similar to "HeadlessChrome/61.0.3153.0". For non-headless or new-headless, this is similar to "Chrome/61.0.3153.0". For Firefox, it is similar to "Firefox/116.0a1".
The format of Browser.version() might change with future releases of browsers.
</td></tr>
<tr><td>
<span id="waitfortarget">waitForTarget(predicate, options)</span>
</td><td>
</td><td>
Waits until a target matching the given predicate appears and returns it.
This will look all open browser contexts.
</td></tr>
<tr><td>
<span id="wsendpoint">wsEndpoint()</span>
</td><td>
</td><td>
Gets the WebSocket URL to connect to this browser.
This is usually used with Puppeteer.connect().
You can find the debugger URL (webSocketDebuggerUrl) from http://HOST:PORT/json/version.
See browser endpoint for more information.
Remarks:
The format is always ws://HOST:PORT/devtools/browser/<id>.
</td></tr>
</tbody></table>