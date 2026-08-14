

--- FILE: docs/browsers-api/browsers.browser.md ---

---
sidebar_label: Browser
---

# Browser enum

Supported browsers.

### Signature

```typescript
export declare enum Browser
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

CHROME

</td><td>

`"chrome"`

</td><td>

</td></tr>
<tr><td>

CHROMEDRIVER

</td><td>

`"chromedriver"`

</td><td>

</td></tr>
<tr><td>

CHROMEHEADLESSSHELL

</td><td>

`"chrome-headless-shell"`

</td><td>

</td></tr>
<tr><td>

CHROMIUM

</td><td>

`"chromium"`

</td><td>

</td></tr>
<tr><td>

FIREFOX

</td><td>

`"firefox"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserplatform.md ---

---
sidebar_label: BrowserPlatform
---

# BrowserPlatform enum

Platform names used to identify a OS platform x architecture combination in the way that is relevant for the browser download.

### Signature

```typescript
export declare enum BrowserPlatform
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

LINUX

</td><td>

`"linux"`

</td><td>

</td></tr>
<tr><td>

LINUX_ARM

</td><td>

`"linux_arm"`

</td><td>

</td></tr>
<tr><td>

MAC

</td><td>

`"mac"`

</td><td>

</td></tr>
<tr><td>

MAC_ARM

</td><td>

`"mac_arm"`

</td><td>

</td></tr>
<tr><td>

WIN32

</td><td>

`"win32"`

</td><td>

</td></tr>
<tr><td>

WIN64

</td><td>

`"win64"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserprovider.getdownloadurl.md ---

---
sidebar_label: BrowserProvider.getDownloadUrl
---

# BrowserProvider.getDownloadUrl() method

Get the download URL for the requested browser.

The buildId can be either an exact version (e.g., "131.0.6778.109") or an alias (e.g., "latest", "stable"). Custom providers should handle version resolution internally if they support aliases.

Returns null if the buildId cannot be resolved to a valid version. The URL is not validated - download will fail later if URL doesn't exist.

Can be synchronous for simple URL construction or asynchronous if version resolution/network requests are needed.

### Signature

```typescript
interface BrowserProvider {
  getDownloadUrl(options: DownloadOptions): Promise<URL | null> | URL | null;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

Download options (buildId may be alias or exact version)

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;URL \| null&gt; \| URL \| null

Download URL, or null if version cannot be resolved

## Example

```ts
// Synchronous example
getDownloadUrl(options) {
  const platform = mapPlatform(options.platform);
  return new URL(`https://releases.example.com/v${options.buildId}/${platform}.zip`);
}

// Asynchronous example with version mapping
async getDownloadUrl(options) {
  const electronVersion = await resolveElectronVersion(options.buildId);
  if (!electronVersion) return null;

  const platform = mapPlatform(options.platform);
  return new URL(`https://github.com/electron/electron/releases/download/v${electronVersion}/${platform}.zip`);
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.getexecutablepath.md ---

---
sidebar_label: BrowserProvider.getExecutablePath
---

# BrowserProvider.getExecutablePath() method

Get the relative path to the executable within the extracted archive.

### Signature

```typescript
interface BrowserProvider {
  getExecutablePath(options: {
    browser: Browser;
    buildId: string;
    platform: BrowserPlatform;
  }): Promise<string> | string;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

&#123; browser: [Browser](./browsers.browser.md); buildId: string; platform: [BrowserPlatform](./browsers.browserplatform.md); &#125;

</td><td>

Browser, buildId, and platform

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt; \| string

Relative path to the executable

## Example

```ts
// Electron uses simple structure
getExecutablePath() {
  return 'chromedriver/chromedriver';
}

// Custom provider with platform-specific paths
getExecutablePath(options) {
  return `binaries/${options.browser}-${options.platform}`;
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.getname.md ---

---
sidebar_label: BrowserProvider.getName
---

# BrowserProvider.getName() method

Get the name of this provider. Used for error messages and logging purposes.

### Signature

```typescript
interface BrowserProvider {
  getName(): string;
}
```

**Returns:**

string

The provider name (e.g., "DefaultProvider", "CustomProvider")

## Remarks

This method is used instead of `constructor.name` to avoid issues with minification in production builds.

## Example

```ts
getName() {
  return 'MyCustomProvider';
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.md ---

---
sidebar_label: BrowserProvider
---

# BrowserProvider interface

Interface for custom browser provider implementations. Allows users to implement alternative download sources for browsers.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By implementing this interface, you accept full responsibility for:

- Ensuring downloaded binaries are compatible with Puppeteer's expectations - Testing that browser launch and other features work with your binaries - Maintaining compatibility when Puppeteer or your download source changes - Version consistency across platforms if mixing sources

Puppeteer only tests and guarantees Chrome for Testing binaries.

### Signature

```typescript
export interface BrowserProvider
```

## Example

```typescript
class ElectronDownloader implements BrowserProvider {
  supports(options: DownloadOptions): boolean {
    return options.browser === Browser.CHROMEDRIVER;
  }

  getDownloadUrl(options: DownloadOptions): URL {
    const platform = mapToPlatform(options.platform);
    return new URL(
      `v${options.buildId}/chromedriver-v${options.buildId}-${platform}.zip`,
      'https://github.com/electron/electron/releases/download/',
    );
  }

  getExecutablePath(options): string {
    const ext = options.platform.includes('win') ? '.exe' : '';
    return `chromedriver/chromedriver${ext}`;
  }
}
```

## Methods

<table><thead><tr><th>

Method

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="getdownloadurl">[getDownloadUrl(options)](./browsers.browserprovider.getdownloadurl.md)</span>

</td><td>

Get the download URL for the requested browser.

The buildId can be either an exact version (e.g., "131.0.6778.109") or an alias (e.g., "latest", "stable"). Custom providers should handle version resolution internally if they support aliases.

Returns null if the buildId cannot be resolved to a valid version. The URL is not validated - download will fail later if URL doesn't exist.

Can be synchronous for simple URL construction or asynchronous if version resolution/network requests are needed.

</td></tr>
<tr><td>

<span id="getexecutablepath">[getExecutablePath(options)](./browsers.browserprovider.getexecutablepath.md)</span>

</td><td>

Get the relative path to the executable within the extracted archive.

</td></tr>
<tr><td>

<span id="getname">[getName()](./browsers.browserprovider.getname.md)</span>

</td><td>

Get the name of this provider. Used for error messages and logging purposes.

**Remarks:**

This method is used instead of `constructor.name` to avoid issues with minification in production builds.

</td></tr>
<tr><td>

<span id="supports">[supports(options)](./browsers.browserprovider.supports.md)</span>

</td><td>

Check if this provider supports the given browser/platform. Used for filtering before attempting downloads.

Can be synchronous for quick checks or asynchronous if version resolution/network requests are needed.

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserprovider.supports.md ---

---
sidebar_label: BrowserProvider.supports
---

# BrowserProvider.supports() method

Check if this provider supports the given browser/platform. Used for filtering before attempting downloads.

Can be synchronous for quick checks or asynchronous if version resolution/network requests are needed.

### Signature

```typescript
interface BrowserProvider {
  supports(options: DownloadOptions): Promise<boolean> | boolean;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

Download options to check

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;boolean&gt; \| boolean

True if this provider supports the browser/platform combination


--- FILE: docs/browsers-api/browsers.browsertag.md ---

---
sidebar_label: BrowserTag
---

# BrowserTag enum

Enum describing a release channel for a browser.

You can use this in combination with [resolveBuildId()](./browsers.resolvebuildid.md) to resolve a build ID based on a release channel.

### Signature

```typescript
export declare enum BrowserTag
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

BETA

</td><td>

`"beta"`

</td><td>

</td></tr>
<tr><td>

CANARY

</td><td>

`"canary"`

</td><td>

</td></tr>
<tr><td>

DEV

</td><td>

`"dev"`

</td><td>

</td></tr>
<tr><td>

DEVEDITION

</td><td>

`"devedition"`

</td><td>

</td></tr>
<tr><td>

ESR

</td><td>

`"esr"`

</td><td>

</td></tr>
<tr><td>

LATEST

</td><td>

`"latest"`

</td><td>

</td></tr>
<tr><td>

NIGHTLY

</td><td>

`"nightly"`

</td><td>

</td></tr>
<tr><td>

STABLE

</td><td>

`"stable"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.buildarchivefilename.md ---

---
sidebar_label: buildArchiveFilename
---

# buildArchiveFilename() function

Utility function to build a standard archive filename.

### Signature

```typescript
export declare function buildArchiveFilename(
  browser: Browser,
  platform: BrowserPlatform,
  buildId: string,
  extension?: string,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
<tr><td>

extension

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.candownload.md ---

---
sidebar_label: canDownload
---

# canDownload() function

### Signature

```typescript
export declare function canDownload(options: InstallOptions): Promise<boolean>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;boolean&gt;


--- FILE: docs/browsers-api/browsers.cdp_websocket_endpoint_regex.md ---

---
sidebar_label: CDP_WEBSOCKET_ENDPOINT_REGEX
---

# CDP_WEBSOCKET_ENDPOINT_REGEX variable

### Signature

```typescript
CDP_WEBSOCKET_ENDPOINT_REGEX: RegExp;
```


--- FILE: docs/browsers-api/browsers.chromereleasechannel.md ---

---
sidebar_label: ChromeReleaseChannel
---

# ChromeReleaseChannel enum

### Signature

```typescript
export declare enum ChromeReleaseChannel
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

BETA

</td><td>

`"beta"`

</td><td>

</td></tr>
<tr><td>

CANARY

</td><td>

`"canary"`

</td><td>

</td></tr>
<tr><td>

DEV

</td><td>

`"dev"`

</td><td>

</td></tr>
<tr><td>

STABLE

</td><td>

`"stable"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli._constructor_.md ---

---
sidebar_label: CLI.(constructor)
---

# CLI.(constructor)

Constructs a new instance of the `CLI` class

### Signature

```typescript
class CLI {
  constructor(
    opts?:
      | string
      | {
          cachePath?: string;
          scriptName?: string;
          version?: string;
          prefixCommand?: {
            cmd: string;
            description: string;
          };
          allowCachePathOverride?: boolean;
          pinnedBrowsers?: Partial<
            Record<
              Browser,
              {
                buildId: string;
                skipDownload: boolean;
              }
            >
          >;
        },
    rl?: readline.Interface,
  );
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

string \| &#123; cachePath?: string; scriptName?: string; version?: string; prefixCommand?: &#123; cmd: string; description: string; &#125;; allowCachePathOverride?: boolean; pinnedBrowsers?: Partial&lt;Record&lt;[Browser](./browsers.browser.md), &#123; buildId: string; skipDownload: boolean; &#125;&gt;&gt;; &#125;

</td><td>

_(Optional)_

</td></tr>
<tr><td>

rl

</td><td>

readline.Interface

</td><td>

_(Optional)_

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli.md ---

---
sidebar_label: CLI
---

# CLI class

### Signature

```typescript
export declare class CLI
```

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(opts, rl)](./browsers.cli._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `CLI` class

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="run">[run(argv)](./browsers.cli.run.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli.run.md ---

---
sidebar_label: CLI.run
---

# CLI.run() method

### Signature

```typescript
class CLI {
  run(argv: string[]): Promise<void>;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

argv

</td><td>

string\[\]

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.computeexecutablepath.md ---

---
sidebar_label: computeExecutablePath
---

# computeExecutablePath() function

### Signature

```typescript
export declare function computeExecutablePath(
  options: ComputeExecutablePathOptions,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[ComputeExecutablePathOptions](./browsers.options.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.computesystemexecutablepath.md ---

---
sidebar_label: computeSystemExecutablePath
---

# computeSystemExecutablePath() function

Returns a path to a system-wide Chrome installation given a release channel name by checking known installation locations (using [https://pptr.dev/browsers-api/browsers.computesystemexecutablepath](https://pptr.dev/browsers-api/browsers.computesystemexecutablepath)). If Chrome instance is not found at the expected path, an error is thrown.

### Signature

```typescript
export declare function computeSystemExecutablePath(
  options: SystemOptions,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[SystemOptions](./browsers.systemoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.createprofile.md ---

---
sidebar_label: createProfile
---

# createProfile() function

### Signature

```typescript
export declare function createProfile(
  browser: Browser,
  opts: ProfileOptions,
): Promise<void>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

opts

</td><td>

[ProfileOptions](./browsers.profileoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.defaultprovider._constructor_.md ---

---
sidebar_label: DefaultProvider.(constructor)
---

# DefaultProvider.(constructor)

Constructs a new instance of the `DefaultProvider` class

### Signature

```typescript
class DefaultProvider {
  constructor(baseUrl?: string);
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

baseUrl

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.defaultprovider.getdownloadurl.md ---

---
sidebar_label: DefaultProvider.getDownloadUrl
---

# DefaultProvider.getDownloadUrl() method

### Signature

```typescript
class DefaultProvider {
  getDownloadUrl(options: DownloadOptions): URL;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

URL


--- FILE: docs/browsers-api/browsers.defaultprovider.getexecutablepath.md ---

---
sidebar_label: DefaultProvider.getExecutablePath
---

# DefaultProvider.getExecutablePath() method

### Signature

```typescript
class DefaultProvider {
  getExecutablePath(options: {
    browser: Browser;
    buildId: string;
    platform: BrowserPlatform;
  }): string;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

&#123; browser: [Browser](./browsers.browser.md); buildId: string; platform: [BrowserPlatform](./browsers.browserplatform.md); &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.defaultprovider.getname.md ---

---
sidebar_label: DefaultProvider.getName
---

# DefaultProvider.getName() method

### Signature

```typescript
class DefaultProvider {
  getName(): string;
}
```

**Returns:**

string


--- FILE: docs/browsers-api/browsers.defaultprovider.md ---

---
sidebar_label: DefaultProvider
---

# DefaultProvider class

Default provider implementation that uses default sources. This is the standard provider used by Puppeteer.

### Signature

```typescript
export declare class DefaultProvider implements BrowserProvider
```

**Implements:** [BrowserProvider](./browsers.browserprovider.md)

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(baseUrl)](./browsers.defaultprovider._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `DefaultProvider` class

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="getdownloadurl">[getDownloadUrl(options)](./browsers.defaultprovider.getdownloadurl.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getexecutablepath">[getExecutablePath(options)](./browsers.defaultprovider.getexecutablepath.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getname">[getName()](./browsers.defaultprovider.getname.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="supports">[supports(\_options)](./browsers.defaultprovider.supports.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.defaultprovider.supports.md ---

---
sidebar_label: DefaultProvider.supports
---

# DefaultProvider.supports() method

### Signature

```typescript
class DefaultProvider {
  supports(_options: DownloadOptions): boolean;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

\_options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

boolean


--- FILE: docs/browsers-api/browsers.detectbrowserplatform.md ---

---
sidebar_label: detectBrowserPlatform
---

# detectBrowserPlatform() function

### Signature

```typescript
export declare function detectBrowserPlatform(): BrowserPlatform | undefined;
```

**Returns:**

[BrowserPlatform](./browsers.browserplatform.md) \| undefined


--- FILE: docs/browsers-api/browsers.downloadoptions.md ---

---
sidebar_label: DownloadOptions
---

# DownloadOptions interface

Options passed to a provider.

### Signature

```typescript
export interface DownloadOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.getdownloadurl.md ---

---
sidebar_label: getDownloadUrl
---

# getDownloadUrl() function

Retrieves a URL for downloading the binary archive of a given browser.

The archive is bound to the specific platform and build ID specified.

### Signature

```typescript
export declare function getDownloadUrl(
  browser: Browser,
  platform: BrowserPlatform,
  buildId: string,
  baseUrl?: string,
): URL;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
<tr><td>

baseUrl

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

URL


--- FILE: docs/browsers-api/browsers.getinstalledbrowsers.md ---

---
sidebar_label: getInstalledBrowsers
---

# getInstalledBrowsers() function

Returns metadata about browsers installed in the cache directory.

### Signature

```typescript
export declare function getInstalledBrowsers(
  options: GetInstalledBrowsersOptions,
): Promise<InstalledBrowser[]>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[GetInstalledBrowsersOptions](./browsers.getinstalledbrowsersoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;[InstalledBrowser](./browsers.installedbrowser.md)\[\]&gt;


--- FILE: docs/browsers-api/browsers.getinstalledbrowsersoptions.md ---

---
sidebar_label: GetInstalledBrowsersOptions
---

# GetInstalledBrowsersOptions interface

### Signature

```typescript
export interface GetInstalledBrowsersOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

The path to the root of the cache directory.

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.getversioncomparator.md ---

---
sidebar_label: getVersionComparator
---

# getVersionComparator() function

Returns a version comparator for the given browser that can be used to sort browser versions.

### Signature

```typescript
export declare function getVersionComparator(
  browser: Browser,
): (a: string, b: string) => number;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

(a: string, b: string) =&gt; number


--- FILE: docs/browsers-api/browsers.install.md ---

---
sidebar_label: install
---

# install() function

<h2 id="overload-1">install(): Promise&lt;InstalledBrowser&gt;</h2>

Downloads and unpacks the browser archive according to the [InstallOptions](./browsers.installoptions.md).

### Signature

```typescript
export declare function install(
  options: InstallOptions & {
    unpack?: true;
  },
): Promise<InstalledBrowser>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md) &amp; &#123; unpack?: true; &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;[InstalledBrowser](./browsers.installedbrowser.md)&gt;

a [InstalledBrowser](./browsers.installedbrowser.md) instance.

<h2 id="overload-2">install(): Promise&lt;string&gt;</h2>

Downloads the browser archive according to the [InstallOptions](./browsers.installoptions.md) without unpacking.

### Signature

```typescript
export declare function install(
  options: InstallOptions & {
    unpack: false;
  },
): Promise<string>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md) &amp; &#123; unpack: false; &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;

the absolute path to the archive.


--- FILE: docs/browsers-api/browsers.installedbrowser.md ---

---
sidebar_label: InstalledBrowser
---

# InstalledBrowser class

### Signature

```typescript
export declare class InstalledBrowser
```

## Remarks

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `InstalledBrowser` class.

## Properties

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

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

</td></tr>
<tr><td>

<span id="executablepath">executablePath</span>

</td><td>

`readonly`

</td><td>

string

</td><td>

</td></tr>
<tr><td>

<span id="path">path</span>

</td><td>

`readonly`

</td><td>

string

</td><td>

Path to the root of the installation folder. Use [computeExecutablePath()](./browsers.computeexecutablepath.md) to get the path to the executable binary.

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="readmetadata">[readMetadata()](./browsers.installedbrowser.readmetadata.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="writemetadata">[writeMetadata(metadata)](./browsers.installedbrowser.writemetadata.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.installedbrowser.readmetadata.md ---

---
sidebar_label: InstalledBrowser.readMetadata
---

# InstalledBrowser.readMetadata() method

### Signature

```typescript
class InstalledBrowser {
  readMetadata(): Metadata;
}
```

**Returns:**

[Metadata](./browsers.metadata.md)


--- FILE: docs/browsers-api/browsers.installedbrowser.writemetadata.md ---

---
sidebar_label: InstalledBrowser.writeMetadata
---

# InstalledBrowser.writeMetadata() method

### Signature

```typescript
class InstalledBrowser {
  writeMetadata(metadata: Metadata): void;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

metadata

</td><td>

[Metadata](./browsers.metadata.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

void


--- FILE: docs/browsers-api/browsers.installoptions.md ---

---
sidebar_label: InstallOptions
---

# InstallOptions interface

### Signature

```typescript
export interface InstallOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="baseurl">baseUrl</span>

</td><td>

`optional`

</td><td>

string

</td><td>

Determines the host that will be used for downloading.

</td><td>

Either

- https://storage.googleapis.com/chrome-for-testing-public or - https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central

</td></tr>
<tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to install.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

Determines which buildId to download. BuildId should uniquely identify binaries and they are used for caching.

</td><td>

</td></tr>
<tr><td>

<span id="buildidalias">buildIdAlias</span>

</td><td>

`optional`

</td><td>

string

</td><td>

An alias for the provided `buildId`. It will be used to maintain local metadata to support aliases in the `launch` command.

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

Determines the path to download browsers to.

</td><td>

</td></tr>
<tr><td>

<span id="downloadprogresscallback">downloadProgressCallback</span>

</td><td>

`optional`

</td><td>

'default' \| ((downloadedBytes: number, totalBytes: number) =&gt; void)

</td><td>

Provides information about the progress of the download. If set to 'default', the default callback implementing a progress bar will be used.

</td><td>

</td></tr>
<tr><td>

<span id="installdeps">installDeps</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to attempt to install system-level dependencies required for the browser.

Only supported for Chrome on Debian or Ubuntu. Requires system-level privileges to run `apt-get`.

</td><td>

`false`

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
<tr><td>

<span id="providers">providers</span>

</td><td>

`optional`

</td><td>

[BrowserProvider](./browsers.browserprovider.md)\[\]

</td><td>

Custom provider implementation for alternative download sources.

If not provided, uses the default provider. Multiple providers can be chained - they will be tried in order. The default provider is automatically added as the final fallback.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By using custom providers, you accept full responsibility for:

- **Version compatibility**: Different platforms may receive different binary versions - **Archive compatibility**: Binary structure must match Puppeteer's expectations - **Feature integration**: Browser launch and other Puppeteer features may not work - **Testing**: You must validate that downloaded binaries work with Puppeteer

**Puppeteer only tests and guarantees compatibility with default binaries.**

</td><td>

</td></tr>
<tr><td>

<span id="unpack">unpack</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to unpack and install browser archives.

</td><td>

`true`

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.launch.md ---

---
sidebar_label: launch
---

# launch() function

Launches a browser process according to [LaunchOptions](./browsers.launchoptions.md).

### Signature

```typescript
export declare function launch(opts: LaunchOptions): Process;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

[LaunchOptions](./browsers.launchoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

[Process](./browsers.process.md)


--- FILE: docs/browsers-api/browsers.launchoptions.md ---

---
sidebar_label: LaunchOptions
---

# LaunchOptions interface

### Signature

```typescript
export interface LaunchOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="args">args</span>

</td><td>

`optional`

</td><td>

string\[\]

</td><td>

Additional arguments to pass to the executable when launching.

</td><td>

</td></tr>
<tr><td>

<span id="detached">detached</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to spawn process in the [detached](https://nodejs.org/api/child_process.html#optionsdetached) mode.

</td><td>

`true` except on Windows.

</td></tr>
<tr><td>

<span id="dumpio">dumpio</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

If true, forwards the browser's process stdout and stderr to the Node's process stdout and stderr.

</td><td>

`false`.

</td></tr>
<tr><td>

<span id="env">env</span>

</td><td>

`optional`

</td><td>

Record&lt;string, string \| undefined&gt;

</td><td>

Environment variables to set for the browser process.

</td><td>

</td></tr>
<tr><td>

<span id="executablepath">executablePath</span>

</td><td>

</td><td>

string

</td><td>

Absolute path to the browser's executable.

</td><td>

</td></tr>
<tr><td>

<span id="handlesighup">handleSIGHUP</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGHUP in the Node process and tries to gracefully close the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="handlesigint">handleSIGINT</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGINT in the Node process and tries to kill the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="handlesigterm">handleSIGTERM</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGTERM in the Node process and tries to gracefully close the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="onexit">onExit</span>

</td><td>

`optional`

</td><td>

() =&gt; Promise&lt;void&gt;

</td><td>

A callback to run after the browser process exits or before the process will be closed via the [Process.close()](./browsers.process.close.md) call (including when handling signals). The callback is only run once.

</td><td>

</td></tr>
<tr><td>

<span id="pipe">pipe</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Configures stdio streams to open two additional streams for automation over those streams instead of WebSocket.

</td><td>

`false`.

</td></tr>
<tr><td>

<span id="signal">signal</span>

</td><td>

`optional`

</td><td>

AbortSignal

</td><td>

If provided, the process will be killed when the signal is aborted.

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.makeprogresscallback.md ---

---
sidebar_label: makeProgressCallback
---

# makeProgressCallback() function

### Signature

```typescript
export declare function makeProgressCallback(
  browser: Browser,
  buildId: string,
): (downloadedBytes: number, totalBytes: number) => void;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
</tbody></table>

**Returns:**

(downloadedBytes: number, totalBytes: number) =&gt; void


--- FILE: docs/browsers-api/browsers.metadata.md ---

---
sidebar_label: Metadata
---

# Metadata interface

### Signature

```typescript
export interface Metadata
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="aliases">aliases</span>

</td><td>

</td><td>

Record&lt;string, string&gt;

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="executablepaths">executablePaths</span>

</td><td>

`optional`

</td><td>

Record&lt;string, string&gt;

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.options.md ---

---
sidebar_label: Options
---

# Options interface

### Signature

```typescript
export interface ComputeExecutablePathOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to launch.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

Determines which buildId to download. BuildId should uniquely identify binaries and they are used for caching.

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string \| null

</td><td>

Root path to the storage directory.

Can be set to `null` if the executable path should be relative to the extracted download location. E.g. `./chrome-linux64/chrome`.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process._constructor_.md ---

---
sidebar_label: Process.(constructor)
---

# Process.(constructor)

Constructs a new instance of the `Process` class

### Signature

```typescript
class Process {
  constructor(opts: LaunchOptions);
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

[LaunchOptions](./browsers.launchoptions.md)

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process.close.md ---

---
sidebar_label: Process.close
---

# Process.close() method

### Signature

```typescript
class Process {
  close(): Promise<void>;
}
```

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.process.getrecentlogs.md ---

---
sidebar_label: Process.getRecentLogs
---

# Process.getRecentLogs() method

Get recent logs (stderr + stdout) emitted by the browser.

### Signature

```typescript
class Process {
  getRecentLogs(): string[];
}
```

**Returns:**

string\[\]


--- FILE: docs/browsers-api/browsers.process.hasclosed.md ---

---
sidebar_label: Process.hasClosed
---

# Process.hasClosed() method

### Signature

```typescript
class Process {
  hasClosed(): Promise<void>;
}
```

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.process.kill.md ---

---
sidebar_label: Process.kill
---

# Process.kill() method

### Signature

```typescript
class Process {
  kill(): void;
}
```

**Returns:**

void


--- FILE: docs/browsers-api/browsers.process.md ---

---
sidebar_label: Process
---

# Process class

### Signature

```typescript
export declare class Process
```

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(opts)](./browsers.process._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `Process` class

</td></tr>
</tbody></table>

## Properties

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

<span id="nodeprocess">nodeProcess</span>

</td><td>

`readonly`

</td><td>

childProcess.ChildProcess

</td><td>

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="close">[close()](./browsers.process.close.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getrecentlogs">[getRecentLogs()](./browsers.process.getrecentlogs.md)</span>

</td><td>

</td><td>

Get recent logs (stderr + stdout) emitted by the browser.

</td></tr>
<tr><td>

<span id="hasclosed">[hasClosed()](./browsers.process.hasclosed.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="kill">[kill()](./browsers.process.kill.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="waitforlineoutput">[waitForLineOutput(regex, timeout)](./browsers.process.waitforlineoutput.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process.waitforlineoutput.md ---

---
sidebar_label: Process.waitForLineOutput
---

# Process.waitForLineOutput() method

### Signature

```typescript
class Process {
  waitForLineOutput(regex: RegExp, timeout?: number): Promise<string>;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

regex

</td><td>

RegExp

</td><td>

</td></tr>
<tr><td>

timeout

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;


--- FILE: docs/browsers-api/browsers.profileoptions.md ---

---
sidebar_label: ProfileOptions
---

# ProfileOptions interface

### Signature

```typescript
export interface ProfileOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="path">path</span>

</td><td>

</td><td>

string

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="preferences">preferences</span>

</td><td>

</td><td>

Record&lt;string, unknown&gt;

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.resolvebuildid.md ---

---
sidebar_label: resolveBuildId
---

# resolveBuildId() function

### Signature

```typescript
export declare function resolveBuildId(
  browser: Browser,
  platform: BrowserPlatform,
  tag: string | BrowserTag,
): Promise<string>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

tag

</td><td>

string \| [BrowserTag](./browsers.browsertag.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;


--- FILE: docs/browsers-api/browsers.resolvedefaultuserdatadir.md ---

---
sidebar_label: resolveDefaultUserDataDir
---

# resolveDefaultUserDataDir() function

Returns the expected default user data dir for the given channel. It does not check if the dir actually exists.

### Signature

```typescript
export declare function resolveDefaultUserDataDir(
  browser: Browser,
  platform: BrowserPlatform,
  channel: ChromeReleaseChannel,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

channel

</td><td>

[ChromeReleaseChannel](./browsers.chromereleasechannel.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.systemoptions.md ---

---
sidebar_label: SystemOptions
---

# SystemOptions interface

### Signature

```typescript
export interface SystemOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to launch.

</td><td>

</td></tr>
<tr><td>

<span id="channel">channel</span>

</td><td>

</td><td>

[ChromeReleaseChannel](./browsers.chromereleasechannel.md)

</td><td>

Release channel to look for on the system.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.timeouterror.md ---

---
sidebar_label: TimeoutError
---

# TimeoutError class

### Signature

```typescript
export declare class TimeoutError extends Error
```

**Extends:** Error

## Remarks

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `TimeoutError` class.


--- FILE: docs/browsers-api/browsers.uninstall.md ---

---
sidebar_label: uninstall
---

# uninstall() function

### Signature

```typescript
export declare function uninstall(options: UninstallOptions): Promise<void>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[UninstallOptions](./browsers.uninstalloptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.uninstalloptions.md ---

---
sidebar_label: UninstallOptions
---

# UninstallOptions interface

### Signature

```typescript
export interface UninstallOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to uninstall.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

The browser build to uninstall

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

The path to the root of the cache directory.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines the platform for the browser binary.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.webdriver_bidi_websocket_endpoint_regex.md ---

---
sidebar_label: WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX
---

# WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX variable

### Signature

```typescript
WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX: RegExp;
```


--- FILE: docs/browsers-api/index.md ---

---
sidebar_label: API
---

# @puppeteer/browsers

Manage and launch browsers/drivers from a CLI or programmatically.

## System requirements

- A compatible Node version (see `engines` in `package.json`).
- For Firefox downloads:
  - Linux builds: `xz` and `bzip2` utilities are required to unpack `.tar.gz` and `.tar.bz2` archives.
  - MacOS builds: `hdiutil` is required to unpack `.dmg` archives.

## CLI

Use `npx` to run the CLI:

```bash
# This will install and run the @puppeteer/browsers package.
# If it is already installed in the current directory, the installed
# version will be used.
npx @puppeteer/browsers --help
```

Built-in per-command `help` will provide all documentation you need to use the CLI.

```bash
npx @puppeteer/browsers --help # help for all commands
npx @puppeteer/browsers install --help # help for the install command
npx @puppeteer/browsers launch --help # help for the launch command
npx @puppeteer/browsers clear --help # help for the clear command
npx @puppeteer/browsers list --help # help for the list command
```

You can specify the version of the `@puppeteer/browsers` when using
`npx`:

```bash
# Always install and use the latest version from the registry.
npx @puppeteer/browsers@latest --help
# Always use a specifc version.
npx @puppeteer/browsers@2.4.1 --help
# Always install the latest version and automatically confirm the installation.
npx --yes @puppeteer/browsers@latest --help
```

To clear all installed browsers, use the `clear` command:

```bash
npx @puppeteer/browsers clear
```

To list all installed browsers, use the `list` command:

```bash
npx @puppeteer/browsers list
```

Some example to give an idea of what the CLI looks like (use the `--help` command for more examples):

```sh
# Download the latest available Chrome for Testing binary corresponding to the Stable channel.
npx @puppeteer/browsers install chrome@stable

# Download a specific Chrome for Testing version.
npx @puppeteer/browsers install chrome@116.0.5793.0

# Download the latest Chrome for Testing version for the given milestone.
npx @puppeteer/browsers install chrome@117

# Download the latest available ChromeDriver version corresponding to the Canary channel.
npx @puppeteer/browsers install chromedriver@canary

# Download a specific ChromeDriver version.
npx @puppeteer/browsers install chromedriver@116.0.5793.0

# On Ubuntu/Debian and only for Chrome, install the browser and required system dependencies.
# If the browser version has already been installed, the command
# will still attempt to install system dependencies.
# Requires root privileges.
npx puppeteer browsers install chrome --install-deps
```

## Known limitations

1. Launching the system browsers is only possible for Chrome/Chromium.

## Custom Providers

You can implement custom browser providers to download from alternative sources like corporate mirrors, private repositories, or specialized browser builds.

```typescript
import {
  BrowserProvider,
  DownloadOptions,
  Browser,
  BrowserPlatform,
} from '@puppeteer/browsers';

class SimpleMirrorProvider implements BrowserProvider {
  constructor(private mirrorUrl: string) {}

  supports(options: DownloadOptions): boolean {
    return options.browser === Browser.CHROME;
  }

  getDownloadUrl(options: DownloadOptions): URL | null {
    const {buildId, platform} = options;
    const filenameMap = {
      [BrowserPlatform.LINUX]: 'chrome-linux64.zip',
      [BrowserPlatform.MAC]: 'chrome-mac-x64.zip',
      [BrowserPlatform.MAC_ARM]: 'chrome-mac-arm64.zip',
      [BrowserPlatform.WIN32]: 'chrome-win32.zip',
      [BrowserPlatform.WIN64]: 'chrome-win64.zip',
    };
    const filename = filenameMap[platform];
    if (!filename) return null;
    return new URL(`${this.mirrorUrl}/chrome/${buildId}/${filename}`);
  }

  getExecutablePath(options: DownloadOptions): string {
    const {platform} = options;
    if (
      platform === BrowserPlatform.MAC ||
      platform === BrowserPlatform.MAC_ARM
    ) {
      return 'chrome-mac/Chromium.app/Contents/MacOS/Chromium';
    } else if (platform === BrowserPlatform.LINUX) {
      return 'chrome-linux64/chrome';
    } else if (platform.includes('win')) {
      return 'chrome-win64/chrome.exe';
    }
    throw new Error(`Unsupported platform: ${platform}`);
  }
}
```

Use with the `install` API:

```typescript
import {install} from '@puppeteer/browsers';

const customProvider = new SimpleMirrorProvider('https://internal.company.com');

await install({
  browser: Browser.CHROME,
  buildId: '120.0.6099.109',
  platform: BrowserPlatform.LINUX,
  cacheDir: '/tmp/puppeteer-cache',
  providers: [customProvider],
});
```

Multiple providers can be chained - they're tried in order until one succeeds, with a default provider such as Chrome for Testing, as an automatic fallback.

:::caution
Custom providers are NOT officially supported by Puppeteer. You accept full responsibility for binary compatibility, testing, and maintenance.
:::

## API

The programmatic API allows installing and launching browsers from your code. See the `test` folder for examples on how to use the `install`, `canInstall`, `launch`, `computeExecutablePath`, `computeSystemExecutablePath` and other methods.

## Classes

<table><thead><tr><th>

Class

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="cli">[CLI](./browsers.cli.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="defaultprovider">[DefaultProvider](./browsers.defaultprovider.md)</span>

</td><td>

Default provider implementation that uses default sources. This is the standard provider used by Puppeteer.

</td></tr>
<tr><td>

<span id="installedbrowser">[InstalledBrowser](./browsers.installedbrowser.md)</span>

</td><td>

**Remarks:**

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `InstalledBrowser` class.

</td></tr>
<tr><td>

<span id="process">[Process](./browsers.process.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="timeouterror">[TimeoutError](./browsers.timeouterror.md)</span>

</td><td>

**Remarks:**

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `TimeoutError` class.

</td></tr>
</tbody></table>

## Enumerations

<table><thead><tr><th>

Enumeration

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="browser">[Browser](./browsers.browser.md)</span>

</td><td>

Supported browsers.

</td></tr>
<tr><td>

<span id="browserplatform">[BrowserPlatform](./browsers.browserplatform.md)</span>

</td><td>

Platform names used to identify a OS platform x architecture combination in the way that is relevant for the browser download.

</td></tr>
<tr><td>

<span id="browsertag">[BrowserTag](./browsers.browsertag.md)</span>

</td><td>

Enum describing a release channel for a browser.

You can use this in combination with [resolveBuildId()](./browsers.resolvebuildid.md) to resolve a build ID based on a release channel.

</td></tr>
<tr><td>

<span id="chromereleasechannel">[ChromeReleaseChannel](./browsers.chromereleasechannel.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Functions

<table><thead><tr><th>

Function

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="buildarchivefilename">[buildArchiveFilename(browser, platform, buildId, extension)](./browsers.buildarchivefilename.md)</span>

</td><td>

Utility function to build a standard archive filename.

</td></tr>
<tr><td>

<span id="candownload">[canDownload(options)](./browsers.candownload.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="computeexecutablepath">[computeExecutablePath(options)](./browsers.computeexecutablepath.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="computesystemexecutablepath">[computeSystemExecutablePath(options)](./browsers.computesystemexecutablepath.md)</span>

</td><td>

Returns a path to a system-wide Chrome installation given a release channel name by checking known installation locations (using [https://pptr.dev/browsers-api/browsers.computesystemexecutablepath](https://pptr.dev/browsers-api/browsers.computesystemexecutablepath)). If Chrome instance is not found at the expected path, an error is thrown.

</td></tr>
<tr><td>

<span id="createprofile">[createProfile(browser, opts)](./browsers.createprofile.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="detectbrowserplatform">[detectBrowserPlatform()](./browsers.detectbrowserplatform.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="getdownloadurl">[getDownloadUrl(browser, platform, buildId, baseUrl)](./browsers.getdownloadurl.md)</span>

</td><td>

Retrieves a URL for downloading the binary archive of a given browser.

The archive is bound to the specific platform and build ID specified.

</td></tr>
<tr><td>

<span id="getinstalledbrowsers">[getInstalledBrowsers(options)](./browsers.getinstalledbrowsers.md)</span>

</td><td>

Returns metadata about browsers installed in the cache directory.

</td></tr>
<tr><td>

<span id="getversioncomparator">[getVersionComparator(browser)](./browsers.getversioncomparator.md)</span>

</td><td>

Returns a version comparator for the given browser that can be used to sort browser versions.

</td></tr>
<tr><td>

<span id="install">[install(options)](./browsers.install.md)</span>

</td><td>

Downloads and unpacks the browser archive according to the [InstallOptions](./browsers.installoptions.md).

</td></tr>
<tr><td>

<span id="install">[install(options)](./browsers.install.md#overload-2)</span>

</td><td>

Downloads the browser archive according to the [InstallOptions](./browsers.installoptions.md) without unpacking.

</td></tr>
<tr><td>

<span id="launch">[launch(opts)](./browsers.launch.md)</span>

</td><td>

Launches a browser process according to [LaunchOptions](./browsers.launchoptions.md).

</td></tr>
<tr><td>

<span id="makeprogresscallback">[makeProgressCallback(browser, buildId)](./browsers.makeprogresscallback.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="resolvebuildid">[resolveBuildId(browser, platform, tag)](./browsers.resolvebuildid.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="resolvedefaultuserdatadir">[resolveDefaultUserDataDir(browser, platform, channel)](./browsers.resolvedefaultuserdatadir.md)</span>

</td><td>

Returns the expected default user data dir for the given channel. It does not check if the dir actually exists.

</td></tr>
<tr><td>

<span id="uninstall">[uninstall(options)](./browsers.uninstall.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Interfaces

<table><thead><tr><th>

Interface

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="browserprovider">[BrowserProvider](./browsers.browserprovider.md)</span>

</td><td>

Interface for custom browser provider implementations. Allows users to implement alternative download sources for browsers.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By implementing this interface, you accept full responsibility for:

- Ensuring downloaded binaries are compatible with Puppeteer's expectations - Testing that browser launch and other features work with your binaries - Maintaining compatibility when Puppeteer or your download source changes - Version consistency across platforms if mixing sources

Puppeteer only tests and guarantees Chrome for Testing binaries.

</td></tr>
<tr><td>

<span id="downloadoptions">[DownloadOptions](./browsers.downloadoptions.md)</span>

</td><td>

Options passed to a provider.

</td></tr>
<tr><td>

<span id="getinstalledbrowsersoptions">[GetInstalledBrowsersOptions](./browsers.getinstalledbrowsersoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="installoptions">[InstallOptions](./browsers.installoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="launchoptions">[LaunchOptions](./browsers.launchoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="metadata">[Metadata](./browsers.metadata.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="options">[Options](./browsers.options.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="profileoptions">[ProfileOptions](./browsers.profileoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="systemoptions">[SystemOptions](./browsers.systemoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="uninstalloptions">[UninstallOptions](./browsers.uninstalloptions.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Variables

<table><thead><tr><th>

Variable

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="cdp_websocket_endpoint_regex">[CDP_WEBSOCKET_ENDPOINT_REGEX](./browsers.cdp_websocket_endpoint_regex.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="webdriver_bidi_websocket_endpoint_regex">[WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX](./browsers.webdriver_bidi_websocket_endpoint_regex.md)</span>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browser.md ---

---
sidebar_label: Browser
---

# Browser enum

Supported browsers.

### Signature

```typescript
export declare enum Browser
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

CHROME

</td><td>

`"chrome"`

</td><td>

</td></tr>
<tr><td>

CHROMEDRIVER

</td><td>

`"chromedriver"`

</td><td>

</td></tr>
<tr><td>

CHROMEHEADLESSSHELL

</td><td>

`"chrome-headless-shell"`

</td><td>

</td></tr>
<tr><td>

CHROMIUM

</td><td>

`"chromium"`

</td><td>

</td></tr>
<tr><td>

FIREFOX

</td><td>

`"firefox"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserplatform.md ---

---
sidebar_label: BrowserPlatform
---

# BrowserPlatform enum

Platform names used to identify a OS platform x architecture combination in the way that is relevant for the browser download.

### Signature

```typescript
export declare enum BrowserPlatform
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

LINUX

</td><td>

`"linux"`

</td><td>

</td></tr>
<tr><td>

LINUX_ARM

</td><td>

`"linux_arm"`

</td><td>

</td></tr>
<tr><td>

MAC

</td><td>

`"mac"`

</td><td>

</td></tr>
<tr><td>

MAC_ARM

</td><td>

`"mac_arm"`

</td><td>

</td></tr>
<tr><td>

WIN32

</td><td>

`"win32"`

</td><td>

</td></tr>
<tr><td>

WIN64

</td><td>

`"win64"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserprovider.getdownloadurl.md ---

---
sidebar_label: BrowserProvider.getDownloadUrl
---

# BrowserProvider.getDownloadUrl() method

Get the download URL for the requested browser.

The buildId can be either an exact version (e.g., "131.0.6778.109") or an alias (e.g., "latest", "stable"). Custom providers should handle version resolution internally if they support aliases.

Returns null if the buildId cannot be resolved to a valid version. The URL is not validated - download will fail later if URL doesn't exist.

Can be synchronous for simple URL construction or asynchronous if version resolution/network requests are needed.

### Signature

```typescript
interface BrowserProvider {
  getDownloadUrl(options: DownloadOptions): Promise<URL | null> | URL | null;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

Download options (buildId may be alias or exact version)

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;URL \| null&gt; \| URL \| null

Download URL, or null if version cannot be resolved

## Example

```ts
// Synchronous example
getDownloadUrl(options) {
  const platform = mapPlatform(options.platform);
  return new URL(`https://releases.example.com/v${options.buildId}/${platform}.zip`);
}

// Asynchronous example with version mapping
async getDownloadUrl(options) {
  const electronVersion = await resolveElectronVersion(options.buildId);
  if (!electronVersion) return null;

  const platform = mapPlatform(options.platform);
  return new URL(`https://github.com/electron/electron/releases/download/v${electronVersion}/${platform}.zip`);
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.getexecutablepath.md ---

---
sidebar_label: BrowserProvider.getExecutablePath
---

# BrowserProvider.getExecutablePath() method

Get the relative path to the executable within the extracted archive.

### Signature

```typescript
interface BrowserProvider {
  getExecutablePath(options: {
    browser: Browser;
    buildId: string;
    platform: BrowserPlatform;
  }): Promise<string> | string;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

&#123; browser: [Browser](./browsers.browser.md); buildId: string; platform: [BrowserPlatform](./browsers.browserplatform.md); &#125;

</td><td>

Browser, buildId, and platform

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt; \| string

Relative path to the executable

## Example

```ts
// Electron uses simple structure
getExecutablePath() {
  return 'chromedriver/chromedriver';
}

// Custom provider with platform-specific paths
getExecutablePath(options) {
  return `binaries/${options.browser}-${options.platform}`;
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.getname.md ---

---
sidebar_label: BrowserProvider.getName
---

# BrowserProvider.getName() method

Get the name of this provider. Used for error messages and logging purposes.

### Signature

```typescript
interface BrowserProvider {
  getName(): string;
}
```

**Returns:**

string

The provider name (e.g., "DefaultProvider", "CustomProvider")

## Remarks

This method is used instead of `constructor.name` to avoid issues with minification in production builds.

## Example

```ts
getName() {
  return 'MyCustomProvider';
}
```


--- FILE: docs/browsers-api/browsers.browserprovider.md ---

---
sidebar_label: BrowserProvider
---

# BrowserProvider interface

Interface for custom browser provider implementations. Allows users to implement alternative download sources for browsers.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By implementing this interface, you accept full responsibility for:

- Ensuring downloaded binaries are compatible with Puppeteer's expectations - Testing that browser launch and other features work with your binaries - Maintaining compatibility when Puppeteer or your download source changes - Version consistency across platforms if mixing sources

Puppeteer only tests and guarantees Chrome for Testing binaries.

### Signature

```typescript
export interface BrowserProvider
```

## Example

```typescript
class ElectronDownloader implements BrowserProvider {
  supports(options: DownloadOptions): boolean {
    return options.browser === Browser.CHROMEDRIVER;
  }

  getDownloadUrl(options: DownloadOptions): URL {
    const platform = mapToPlatform(options.platform);
    return new URL(
      `v${options.buildId}/chromedriver-v${options.buildId}-${platform}.zip`,
      'https://github.com/electron/electron/releases/download/',
    );
  }

  getExecutablePath(options): string {
    const ext = options.platform.includes('win') ? '.exe' : '';
    return `chromedriver/chromedriver${ext}`;
  }
}
```

## Methods

<table><thead><tr><th>

Method

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="getdownloadurl">[getDownloadUrl(options)](./browsers.browserprovider.getdownloadurl.md)</span>

</td><td>

Get the download URL for the requested browser.

The buildId can be either an exact version (e.g., "131.0.6778.109") or an alias (e.g., "latest", "stable"). Custom providers should handle version resolution internally if they support aliases.

Returns null if the buildId cannot be resolved to a valid version. The URL is not validated - download will fail later if URL doesn't exist.

Can be synchronous for simple URL construction or asynchronous if version resolution/network requests are needed.

</td></tr>
<tr><td>

<span id="getexecutablepath">[getExecutablePath(options)](./browsers.browserprovider.getexecutablepath.md)</span>

</td><td>

Get the relative path to the executable within the extracted archive.

</td></tr>
<tr><td>

<span id="getname">[getName()](./browsers.browserprovider.getname.md)</span>

</td><td>

Get the name of this provider. Used for error messages and logging purposes.

**Remarks:**

This method is used instead of `constructor.name` to avoid issues with minification in production builds.

</td></tr>
<tr><td>

<span id="supports">[supports(options)](./browsers.browserprovider.supports.md)</span>

</td><td>

Check if this provider supports the given browser/platform. Used for filtering before attempting downloads.

Can be synchronous for quick checks or asynchronous if version resolution/network requests are needed.

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.browserprovider.supports.md ---

---
sidebar_label: BrowserProvider.supports
---

# BrowserProvider.supports() method

Check if this provider supports the given browser/platform. Used for filtering before attempting downloads.

Can be synchronous for quick checks or asynchronous if version resolution/network requests are needed.

### Signature

```typescript
interface BrowserProvider {
  supports(options: DownloadOptions): Promise<boolean> | boolean;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

Download options to check

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;boolean&gt; \| boolean

True if this provider supports the browser/platform combination


--- FILE: docs/browsers-api/browsers.browsertag.md ---

---
sidebar_label: BrowserTag
---

# BrowserTag enum

Enum describing a release channel for a browser.

You can use this in combination with [resolveBuildId()](./browsers.resolvebuildid.md) to resolve a build ID based on a release channel.

### Signature

```typescript
export declare enum BrowserTag
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

BETA

</td><td>

`"beta"`

</td><td>

</td></tr>
<tr><td>

CANARY

</td><td>

`"canary"`

</td><td>

</td></tr>
<tr><td>

DEV

</td><td>

`"dev"`

</td><td>

</td></tr>
<tr><td>

DEVEDITION

</td><td>

`"devedition"`

</td><td>

</td></tr>
<tr><td>

ESR

</td><td>

`"esr"`

</td><td>

</td></tr>
<tr><td>

LATEST

</td><td>

`"latest"`

</td><td>

</td></tr>
<tr><td>

NIGHTLY

</td><td>

`"nightly"`

</td><td>

</td></tr>
<tr><td>

STABLE

</td><td>

`"stable"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.buildarchivefilename.md ---

---
sidebar_label: buildArchiveFilename
---

# buildArchiveFilename() function

Utility function to build a standard archive filename.

### Signature

```typescript
export declare function buildArchiveFilename(
  browser: Browser,
  platform: BrowserPlatform,
  buildId: string,
  extension?: string,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
<tr><td>

extension

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.candownload.md ---

---
sidebar_label: canDownload
---

# canDownload() function

### Signature

```typescript
export declare function canDownload(options: InstallOptions): Promise<boolean>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;boolean&gt;


--- FILE: docs/browsers-api/browsers.cdp_websocket_endpoint_regex.md ---

---
sidebar_label: CDP_WEBSOCKET_ENDPOINT_REGEX
---

# CDP_WEBSOCKET_ENDPOINT_REGEX variable

### Signature

```typescript
CDP_WEBSOCKET_ENDPOINT_REGEX: RegExp;
```


--- FILE: docs/browsers-api/browsers.chromereleasechannel.md ---

---
sidebar_label: ChromeReleaseChannel
---

# ChromeReleaseChannel enum

### Signature

```typescript
export declare enum ChromeReleaseChannel
```

## Enumeration Members

<table><thead><tr><th>

Member

</th><th>

Value

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

BETA

</td><td>

`"beta"`

</td><td>

</td></tr>
<tr><td>

CANARY

</td><td>

`"canary"`

</td><td>

</td></tr>
<tr><td>

DEV

</td><td>

`"dev"`

</td><td>

</td></tr>
<tr><td>

STABLE

</td><td>

`"stable"`

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli._constructor_.md ---

---
sidebar_label: CLI.(constructor)
---

# CLI.(constructor)

Constructs a new instance of the `CLI` class

### Signature

```typescript
class CLI {
  constructor(
    opts?:
      | string
      | {
          cachePath?: string;
          scriptName?: string;
          version?: string;
          prefixCommand?: {
            cmd: string;
            description: string;
          };
          allowCachePathOverride?: boolean;
          pinnedBrowsers?: Partial<
            Record<
              Browser,
              {
                buildId: string;
                skipDownload: boolean;
              }
            >
          >;
        },
    rl?: readline.Interface,
  );
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

string \| &#123; cachePath?: string; scriptName?: string; version?: string; prefixCommand?: &#123; cmd: string; description: string; &#125;; allowCachePathOverride?: boolean; pinnedBrowsers?: Partial&lt;Record&lt;[Browser](./browsers.browser.md), &#123; buildId: string; skipDownload: boolean; &#125;&gt;&gt;; &#125;

</td><td>

_(Optional)_

</td></tr>
<tr><td>

rl

</td><td>

readline.Interface

</td><td>

_(Optional)_

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli.md ---

---
sidebar_label: CLI
---

# CLI class

### Signature

```typescript
export declare class CLI
```

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(opts, rl)](./browsers.cli._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `CLI` class

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="run">[run(argv)](./browsers.cli.run.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.cli.run.md ---

---
sidebar_label: CLI.run
---

# CLI.run() method

### Signature

```typescript
class CLI {
  run(argv: string[]): Promise<void>;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

argv

</td><td>

string\[\]

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.computeexecutablepath.md ---

---
sidebar_label: computeExecutablePath
---

# computeExecutablePath() function

### Signature

```typescript
export declare function computeExecutablePath(
  options: ComputeExecutablePathOptions,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[ComputeExecutablePathOptions](./browsers.options.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.computesystemexecutablepath.md ---

---
sidebar_label: computeSystemExecutablePath
---

# computeSystemExecutablePath() function

Returns a path to a system-wide Chrome installation given a release channel name by checking known installation locations (using [https://pptr.dev/browsers-api/browsers.computesystemexecutablepath](https://pptr.dev/browsers-api/browsers.computesystemexecutablepath)). If Chrome instance is not found at the expected path, an error is thrown.

### Signature

```typescript
export declare function computeSystemExecutablePath(
  options: SystemOptions,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[SystemOptions](./browsers.systemoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.createprofile.md ---

---
sidebar_label: createProfile
---

# createProfile() function

### Signature

```typescript
export declare function createProfile(
  browser: Browser,
  opts: ProfileOptions,
): Promise<void>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

opts

</td><td>

[ProfileOptions](./browsers.profileoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.defaultprovider._constructor_.md ---

---
sidebar_label: DefaultProvider.(constructor)
---

# DefaultProvider.(constructor)

Constructs a new instance of the `DefaultProvider` class

### Signature

```typescript
class DefaultProvider {
  constructor(baseUrl?: string);
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

baseUrl

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.defaultprovider.getdownloadurl.md ---

---
sidebar_label: DefaultProvider.getDownloadUrl
---

# DefaultProvider.getDownloadUrl() method

### Signature

```typescript
class DefaultProvider {
  getDownloadUrl(options: DownloadOptions): URL;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

URL


--- FILE: docs/browsers-api/browsers.defaultprovider.getexecutablepath.md ---

---
sidebar_label: DefaultProvider.getExecutablePath
---

# DefaultProvider.getExecutablePath() method

### Signature

```typescript
class DefaultProvider {
  getExecutablePath(options: {
    browser: Browser;
    buildId: string;
    platform: BrowserPlatform;
  }): string;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

&#123; browser: [Browser](./browsers.browser.md); buildId: string; platform: [BrowserPlatform](./browsers.browserplatform.md); &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.defaultprovider.getname.md ---

---
sidebar_label: DefaultProvider.getName
---

# DefaultProvider.getName() method

### Signature

```typescript
class DefaultProvider {
  getName(): string;
}
```

**Returns:**

string


--- FILE: docs/browsers-api/browsers.defaultprovider.md ---

---
sidebar_label: DefaultProvider
---

# DefaultProvider class

Default provider implementation that uses default sources. This is the standard provider used by Puppeteer.

### Signature

```typescript
export declare class DefaultProvider implements BrowserProvider
```

**Implements:** [BrowserProvider](./browsers.browserprovider.md)

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(baseUrl)](./browsers.defaultprovider._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `DefaultProvider` class

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="getdownloadurl">[getDownloadUrl(options)](./browsers.defaultprovider.getdownloadurl.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getexecutablepath">[getExecutablePath(options)](./browsers.defaultprovider.getexecutablepath.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getname">[getName()](./browsers.defaultprovider.getname.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="supports">[supports(\_options)](./browsers.defaultprovider.supports.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.defaultprovider.supports.md ---

---
sidebar_label: DefaultProvider.supports
---

# DefaultProvider.supports() method

### Signature

```typescript
class DefaultProvider {
  supports(_options: DownloadOptions): boolean;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

\_options

</td><td>

[DownloadOptions](./browsers.downloadoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

boolean


--- FILE: docs/browsers-api/browsers.detectbrowserplatform.md ---

---
sidebar_label: detectBrowserPlatform
---

# detectBrowserPlatform() function

### Signature

```typescript
export declare function detectBrowserPlatform(): BrowserPlatform | undefined;
```

**Returns:**

[BrowserPlatform](./browsers.browserplatform.md) \| undefined


--- FILE: docs/browsers-api/browsers.downloadoptions.md ---

---
sidebar_label: DownloadOptions
---

# DownloadOptions interface

Options passed to a provider.

### Signature

```typescript
export interface DownloadOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.getdownloadurl.md ---

---
sidebar_label: getDownloadUrl
---

# getDownloadUrl() function

Retrieves a URL for downloading the binary archive of a given browser.

The archive is bound to the specific platform and build ID specified.

### Signature

```typescript
export declare function getDownloadUrl(
  browser: Browser,
  platform: BrowserPlatform,
  buildId: string,
  baseUrl?: string,
): URL;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
<tr><td>

baseUrl

</td><td>

string

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

URL


--- FILE: docs/browsers-api/browsers.getinstalledbrowsers.md ---

---
sidebar_label: getInstalledBrowsers
---

# getInstalledBrowsers() function

Returns metadata about browsers installed in the cache directory.

### Signature

```typescript
export declare function getInstalledBrowsers(
  options: GetInstalledBrowsersOptions,
): Promise<InstalledBrowser[]>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[GetInstalledBrowsersOptions](./browsers.getinstalledbrowsersoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;[InstalledBrowser](./browsers.installedbrowser.md)\[\]&gt;


--- FILE: docs/browsers-api/browsers.getinstalledbrowsersoptions.md ---

---
sidebar_label: GetInstalledBrowsersOptions
---

# GetInstalledBrowsersOptions interface

### Signature

```typescript
export interface GetInstalledBrowsersOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

The path to the root of the cache directory.

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.getversioncomparator.md ---

---
sidebar_label: getVersionComparator
---

# getVersionComparator() function

Returns a version comparator for the given browser that can be used to sort browser versions.

### Signature

```typescript
export declare function getVersionComparator(
  browser: Browser,
): (a: string, b: string) => number;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

(a: string, b: string) =&gt; number


--- FILE: docs/browsers-api/browsers.install.md ---

---
sidebar_label: install
---

# install() function

<h2 id="overload-1">install(): Promise&lt;InstalledBrowser&gt;</h2>

Downloads and unpacks the browser archive according to the [InstallOptions](./browsers.installoptions.md).

### Signature

```typescript
export declare function install(
  options: InstallOptions & {
    unpack?: true;
  },
): Promise<InstalledBrowser>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md) &amp; &#123; unpack?: true; &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;[InstalledBrowser](./browsers.installedbrowser.md)&gt;

a [InstalledBrowser](./browsers.installedbrowser.md) instance.

<h2 id="overload-2">install(): Promise&lt;string&gt;</h2>

Downloads the browser archive according to the [InstallOptions](./browsers.installoptions.md) without unpacking.

### Signature

```typescript
export declare function install(
  options: InstallOptions & {
    unpack: false;
  },
): Promise<string>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[InstallOptions](./browsers.installoptions.md) &amp; &#123; unpack: false; &#125;

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;

the absolute path to the archive.


--- FILE: docs/browsers-api/browsers.installedbrowser.md ---

---
sidebar_label: InstalledBrowser
---

# InstalledBrowser class

### Signature

```typescript
export declare class InstalledBrowser
```

## Remarks

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `InstalledBrowser` class.

## Properties

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

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

</td></tr>
<tr><td>

<span id="executablepath">executablePath</span>

</td><td>

`readonly`

</td><td>

string

</td><td>

</td></tr>
<tr><td>

<span id="path">path</span>

</td><td>

`readonly`

</td><td>

string

</td><td>

Path to the root of the installation folder. Use [computeExecutablePath()](./browsers.computeexecutablepath.md) to get the path to the executable binary.

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="readmetadata">[readMetadata()](./browsers.installedbrowser.readmetadata.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="writemetadata">[writeMetadata(metadata)](./browsers.installedbrowser.writemetadata.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.installedbrowser.readmetadata.md ---

---
sidebar_label: InstalledBrowser.readMetadata
---

# InstalledBrowser.readMetadata() method

### Signature

```typescript
class InstalledBrowser {
  readMetadata(): Metadata;
}
```

**Returns:**

[Metadata](./browsers.metadata.md)


--- FILE: docs/browsers-api/browsers.installedbrowser.writemetadata.md ---

---
sidebar_label: InstalledBrowser.writeMetadata
---

# InstalledBrowser.writeMetadata() method

### Signature

```typescript
class InstalledBrowser {
  writeMetadata(metadata: Metadata): void;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

metadata

</td><td>

[Metadata](./browsers.metadata.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

void


--- FILE: docs/browsers-api/browsers.installoptions.md ---

---
sidebar_label: InstallOptions
---

# InstallOptions interface

### Signature

```typescript
export interface InstallOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="baseurl">baseUrl</span>

</td><td>

`optional`

</td><td>

string

</td><td>

Determines the host that will be used for downloading.

</td><td>

Either

- https://storage.googleapis.com/chrome-for-testing-public or - https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central

</td></tr>
<tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to install.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

Determines which buildId to download. BuildId should uniquely identify binaries and they are used for caching.

</td><td>

</td></tr>
<tr><td>

<span id="buildidalias">buildIdAlias</span>

</td><td>

`optional`

</td><td>

string

</td><td>

An alias for the provided `buildId`. It will be used to maintain local metadata to support aliases in the `launch` command.

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

Determines the path to download browsers to.

</td><td>

</td></tr>
<tr><td>

<span id="downloadprogresscallback">downloadProgressCallback</span>

</td><td>

`optional`

</td><td>

'default' \| ((downloadedBytes: number, totalBytes: number) =&gt; void)

</td><td>

Provides information about the progress of the download. If set to 'default', the default callback implementing a progress bar will be used.

</td><td>

</td></tr>
<tr><td>

<span id="installdeps">installDeps</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to attempt to install system-level dependencies required for the browser.

Only supported for Chrome on Debian or Ubuntu. Requires system-level privileges to run `apt-get`.

</td><td>

`false`

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
<tr><td>

<span id="providers">providers</span>

</td><td>

`optional`

</td><td>

[BrowserProvider](./browsers.browserprovider.md)\[\]

</td><td>

Custom provider implementation for alternative download sources.

If not provided, uses the default provider. Multiple providers can be chained - they will be tried in order. The default provider is automatically added as the final fallback.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By using custom providers, you accept full responsibility for:

- **Version compatibility**: Different platforms may receive different binary versions - **Archive compatibility**: Binary structure must match Puppeteer's expectations - **Feature integration**: Browser launch and other Puppeteer features may not work - **Testing**: You must validate that downloaded binaries work with Puppeteer

**Puppeteer only tests and guarantees compatibility with default binaries.**

</td><td>

</td></tr>
<tr><td>

<span id="unpack">unpack</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to unpack and install browser archives.

</td><td>

`true`

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.launch.md ---

---
sidebar_label: launch
---

# launch() function

Launches a browser process according to [LaunchOptions](./browsers.launchoptions.md).

### Signature

```typescript
export declare function launch(opts: LaunchOptions): Process;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

[LaunchOptions](./browsers.launchoptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

[Process](./browsers.process.md)


--- FILE: docs/browsers-api/browsers.launchoptions.md ---

---
sidebar_label: LaunchOptions
---

# LaunchOptions interface

### Signature

```typescript
export interface LaunchOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="args">args</span>

</td><td>

`optional`

</td><td>

string\[\]

</td><td>

Additional arguments to pass to the executable when launching.

</td><td>

</td></tr>
<tr><td>

<span id="detached">detached</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Whether to spawn process in the [detached](https://nodejs.org/api/child_process.html#optionsdetached) mode.

</td><td>

`true` except on Windows.

</td></tr>
<tr><td>

<span id="dumpio">dumpio</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

If true, forwards the browser's process stdout and stderr to the Node's process stdout and stderr.

</td><td>

`false`.

</td></tr>
<tr><td>

<span id="env">env</span>

</td><td>

`optional`

</td><td>

Record&lt;string, string \| undefined&gt;

</td><td>

Environment variables to set for the browser process.

</td><td>

</td></tr>
<tr><td>

<span id="executablepath">executablePath</span>

</td><td>

</td><td>

string

</td><td>

Absolute path to the browser's executable.

</td><td>

</td></tr>
<tr><td>

<span id="handlesighup">handleSIGHUP</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGHUP in the Node process and tries to gracefully close the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="handlesigint">handleSIGINT</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGINT in the Node process and tries to kill the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="handlesigterm">handleSIGTERM</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Handles SIGTERM in the Node process and tries to gracefully close the browser process.

</td><td>

`true`.

</td></tr>
<tr><td>

<span id="onexit">onExit</span>

</td><td>

`optional`

</td><td>

() =&gt; Promise&lt;void&gt;

</td><td>

A callback to run after the browser process exits or before the process will be closed via the [Process.close()](./browsers.process.close.md) call (including when handling signals). The callback is only run once.

</td><td>

</td></tr>
<tr><td>

<span id="pipe">pipe</span>

</td><td>

`optional`

</td><td>

boolean

</td><td>

Configures stdio streams to open two additional streams for automation over those streams instead of WebSocket.

</td><td>

`false`.

</td></tr>
<tr><td>

<span id="signal">signal</span>

</td><td>

`optional`

</td><td>

AbortSignal

</td><td>

If provided, the process will be killed when the signal is aborted.

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.makeprogresscallback.md ---

---
sidebar_label: makeProgressCallback
---

# makeProgressCallback() function

### Signature

```typescript
export declare function makeProgressCallback(
  browser: Browser,
  buildId: string,
): (downloadedBytes: number, totalBytes: number) => void;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

buildId

</td><td>

string

</td><td>

</td></tr>
</tbody></table>

**Returns:**

(downloadedBytes: number, totalBytes: number) =&gt; void


--- FILE: docs/browsers-api/browsers.metadata.md ---

---
sidebar_label: Metadata
---

# Metadata interface

### Signature

```typescript
export interface Metadata
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="aliases">aliases</span>

</td><td>

</td><td>

Record&lt;string, string&gt;

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="executablepaths">executablePaths</span>

</td><td>

`optional`

</td><td>

Record&lt;string, string&gt;

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.options.md ---

---
sidebar_label: Options
---

# Options interface

### Signature

```typescript
export interface ComputeExecutablePathOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to launch.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

Determines which buildId to download. BuildId should uniquely identify binaries and they are used for caching.

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string \| null

</td><td>

Root path to the storage directory.

Can be set to `null` if the executable path should be relative to the extracted download location. E.g. `./chrome-linux64/chrome`.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process._constructor_.md ---

---
sidebar_label: Process.(constructor)
---

# Process.(constructor)

Constructs a new instance of the `Process` class

### Signature

```typescript
class Process {
  constructor(opts: LaunchOptions);
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

opts

</td><td>

[LaunchOptions](./browsers.launchoptions.md)

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process.close.md ---

---
sidebar_label: Process.close
---

# Process.close() method

### Signature

```typescript
class Process {
  close(): Promise<void>;
}
```

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.process.getrecentlogs.md ---

---
sidebar_label: Process.getRecentLogs
---

# Process.getRecentLogs() method

Get recent logs (stderr + stdout) emitted by the browser.

### Signature

```typescript
class Process {
  getRecentLogs(): string[];
}
```

**Returns:**

string\[\]


--- FILE: docs/browsers-api/browsers.process.hasclosed.md ---

---
sidebar_label: Process.hasClosed
---

# Process.hasClosed() method

### Signature

```typescript
class Process {
  hasClosed(): Promise<void>;
}
```

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.process.kill.md ---

---
sidebar_label: Process.kill
---

# Process.kill() method

### Signature

```typescript
class Process {
  kill(): void;
}
```

**Returns:**

void


--- FILE: docs/browsers-api/browsers.process.md ---

---
sidebar_label: Process
---

# Process class

### Signature

```typescript
export declare class Process
```

## Constructors

<table><thead><tr><th>

Constructor

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="_constructor_">[(constructor)(opts)](./browsers.process._constructor_.md)</span>

</td><td>

</td><td>

Constructs a new instance of the `Process` class

</td></tr>
</tbody></table>

## Properties

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

<span id="nodeprocess">nodeProcess</span>

</td><td>

`readonly`

</td><td>

childProcess.ChildProcess

</td><td>

</td></tr>
</tbody></table>

## Methods

<table><thead><tr><th>

Method

</th><th>

Modifiers

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="close">[close()](./browsers.process.close.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="getrecentlogs">[getRecentLogs()](./browsers.process.getrecentlogs.md)</span>

</td><td>

</td><td>

Get recent logs (stderr + stdout) emitted by the browser.

</td></tr>
<tr><td>

<span id="hasclosed">[hasClosed()](./browsers.process.hasclosed.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="kill">[kill()](./browsers.process.kill.md)</span>

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="waitforlineoutput">[waitForLineOutput(regex, timeout)](./browsers.process.waitforlineoutput.md)</span>

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.process.waitforlineoutput.md ---

---
sidebar_label: Process.waitForLineOutput
---

# Process.waitForLineOutput() method

### Signature

```typescript
class Process {
  waitForLineOutput(regex: RegExp, timeout?: number): Promise<string>;
}
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

regex

</td><td>

RegExp

</td><td>

</td></tr>
<tr><td>

timeout

</td><td>

number

</td><td>

_(Optional)_

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;


--- FILE: docs/browsers-api/browsers.profileoptions.md ---

---
sidebar_label: ProfileOptions
---

# ProfileOptions interface

### Signature

```typescript
export interface ProfileOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="path">path</span>

</td><td>

</td><td>

string

</td><td>

</td><td>

</td></tr>
<tr><td>

<span id="preferences">preferences</span>

</td><td>

</td><td>

Record&lt;string, unknown&gt;

</td><td>

</td><td>

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.resolvebuildid.md ---

---
sidebar_label: resolveBuildId
---

# resolveBuildId() function

### Signature

```typescript
export declare function resolveBuildId(
  browser: Browser,
  platform: BrowserPlatform,
  tag: string | BrowserTag,
): Promise<string>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

tag

</td><td>

string \| [BrowserTag](./browsers.browsertag.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;string&gt;


--- FILE: docs/browsers-api/browsers.resolvedefaultuserdatadir.md ---

---
sidebar_label: resolveDefaultUserDataDir
---

# resolveDefaultUserDataDir() function

Returns the expected default user data dir for the given channel. It does not check if the dir actually exists.

### Signature

```typescript
export declare function resolveDefaultUserDataDir(
  browser: Browser,
  platform: BrowserPlatform,
  channel: ChromeReleaseChannel,
): string;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

browser

</td><td>

[Browser](./browsers.browser.md)

</td><td>

</td></tr>
<tr><td>

platform

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

</td></tr>
<tr><td>

channel

</td><td>

[ChromeReleaseChannel](./browsers.chromereleasechannel.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

string


--- FILE: docs/browsers-api/browsers.systemoptions.md ---

---
sidebar_label: SystemOptions
---

# SystemOptions interface

### Signature

```typescript
export interface SystemOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to launch.

</td><td>

</td></tr>
<tr><td>

<span id="channel">channel</span>

</td><td>

</td><td>

[ChromeReleaseChannel](./browsers.chromereleasechannel.md)

</td><td>

Release channel to look for on the system.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines which platform the browser will be suited for.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.timeouterror.md ---

---
sidebar_label: TimeoutError
---

# TimeoutError class

### Signature

```typescript
export declare class TimeoutError extends Error
```

**Extends:** Error

## Remarks

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `TimeoutError` class.


--- FILE: docs/browsers-api/browsers.uninstall.md ---

---
sidebar_label: uninstall
---

# uninstall() function

### Signature

```typescript
export declare function uninstall(options: UninstallOptions): Promise<void>;
```

## Parameters

<table><thead><tr><th>

Parameter

</th><th>

Type

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

options

</td><td>

[UninstallOptions](./browsers.uninstalloptions.md)

</td><td>

</td></tr>
</tbody></table>

**Returns:**

Promise&lt;void&gt;


--- FILE: docs/browsers-api/browsers.uninstalloptions.md ---

---
sidebar_label: UninstallOptions
---

# UninstallOptions interface

### Signature

```typescript
export interface UninstallOptions
```

## Properties

<table><thead><tr><th>

Property

</th><th>

Modifiers

</th><th>

Type

</th><th>

Description

</th><th>

Default

</th></tr></thead>
<tbody><tr><td>

<span id="browser">browser</span>

</td><td>

</td><td>

[Browser](./browsers.browser.md)

</td><td>

Determines which browser to uninstall.

</td><td>

</td></tr>
<tr><td>

<span id="buildid">buildId</span>

</td><td>

</td><td>

string

</td><td>

The browser build to uninstall

</td><td>

</td></tr>
<tr><td>

<span id="cachedir">cacheDir</span>

</td><td>

</td><td>

string

</td><td>

The path to the root of the cache directory.

</td><td>

</td></tr>
<tr><td>

<span id="platform">platform</span>

</td><td>

`optional`

</td><td>

[BrowserPlatform](./browsers.browserplatform.md)

</td><td>

Determines the platform for the browser binary.

</td><td>

**Auto-detected.**

</td></tr>
</tbody></table>


--- FILE: docs/browsers-api/browsers.webdriver_bidi_websocket_endpoint_regex.md ---

---
sidebar_label: WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX
---

# WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX variable

### Signature

```typescript
WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX: RegExp;
```


--- FILE: docs/browsers-api/index.md ---

---
sidebar_label: API
---

# @puppeteer/browsers

Manage and launch browsers/drivers from a CLI or programmatically.

## System requirements

- A compatible Node version (see `engines` in `package.json`).
- For Firefox downloads:
  - Linux builds: `xz` and `bzip2` utilities are required to unpack `.tar.gz` and `.tar.bz2` archives.
  - MacOS builds: `hdiutil` is required to unpack `.dmg` archives.

## CLI

Use `npx` to run the CLI:

```bash
# This will install and run the @puppeteer/browsers package.
# If it is already installed in the current directory, the installed
# version will be used.
npx @puppeteer/browsers --help
```

Built-in per-command `help` will provide all documentation you need to use the CLI.

```bash
npx @puppeteer/browsers --help # help for all commands
npx @puppeteer/browsers install --help # help for the install command
npx @puppeteer/browsers launch --help # help for the launch command
npx @puppeteer/browsers clear --help # help for the clear command
npx @puppeteer/browsers list --help # help for the list command
```

You can specify the version of the `@puppeteer/browsers` when using
`npx`:

```bash
# Always install and use the latest version from the registry.
npx @puppeteer/browsers@latest --help
# Always use a specifc version.
npx @puppeteer/browsers@2.4.1 --help
# Always install the latest version and automatically confirm the installation.
npx --yes @puppeteer/browsers@latest --help
```

To clear all installed browsers, use the `clear` command:

```bash
npx @puppeteer/browsers clear
```

To list all installed browsers, use the `list` command:

```bash
npx @puppeteer/browsers list
```

Some example to give an idea of what the CLI looks like (use the `--help` command for more examples):

```sh
# Download the latest available Chrome for Testing binary corresponding to the Stable channel.
npx @puppeteer/browsers install chrome@stable

# Download a specific Chrome for Testing version.
npx @puppeteer/browsers install chrome@116.0.5793.0

# Download the latest Chrome for Testing version for the given milestone.
npx @puppeteer/browsers install chrome@117

# Download the latest available ChromeDriver version corresponding to the Canary channel.
npx @puppeteer/browsers install chromedriver@canary

# Download a specific ChromeDriver version.
npx @puppeteer/browsers install chromedriver@116.0.5793.0

# On Ubuntu/Debian and only for Chrome, install the browser and required system dependencies.
# If the browser version has already been installed, the command
# will still attempt to install system dependencies.
# Requires root privileges.
npx puppeteer browsers install chrome --install-deps
```

## Known limitations

1. Launching the system browsers is only possible for Chrome/Chromium.

## Custom Providers

You can implement custom browser providers to download from alternative sources like corporate mirrors, private repositories, or specialized browser builds.

```typescript
import {
  BrowserProvider,
  DownloadOptions,
  Browser,
  BrowserPlatform,
} from '@puppeteer/browsers';

class SimpleMirrorProvider implements BrowserProvider {
  constructor(private mirrorUrl: string) {}

  supports(options: DownloadOptions): boolean {
    return options.browser === Browser.CHROME;
  }

  getDownloadUrl(options: DownloadOptions): URL | null {
    const {buildId, platform} = options;
    const filenameMap = {
      [BrowserPlatform.LINUX]: 'chrome-linux64.zip',
      [BrowserPlatform.MAC]: 'chrome-mac-x64.zip',
      [BrowserPlatform.MAC_ARM]: 'chrome-mac-arm64.zip',
      [BrowserPlatform.WIN32]: 'chrome-win32.zip',
      [BrowserPlatform.WIN64]: 'chrome-win64.zip',
    };
    const filename = filenameMap[platform];
    if (!filename) return null;
    return new URL(`${this.mirrorUrl}/chrome/${buildId}/${filename}`);
  }

  getExecutablePath(options: DownloadOptions): string {
    const {platform} = options;
    if (
      platform === BrowserPlatform.MAC ||
      platform === BrowserPlatform.MAC_ARM
    ) {
      return 'chrome-mac/Chromium.app/Contents/MacOS/Chromium';
    } else if (platform === BrowserPlatform.LINUX) {
      return 'chrome-linux64/chrome';
    } else if (platform.includes('win')) {
      return 'chrome-win64/chrome.exe';
    }
    throw new Error(`Unsupported platform: ${platform}`);
  }
}
```

Use with the `install` API:

```typescript
import {install} from '@puppeteer/browsers';

const customProvider = new SimpleMirrorProvider('https://internal.company.com');

await install({
  browser: Browser.CHROME,
  buildId: '120.0.6099.109',
  platform: BrowserPlatform.LINUX,
  cacheDir: '/tmp/puppeteer-cache',
  providers: [customProvider],
});
```

Multiple providers can be chained - they're tried in order until one succeeds, with a default provider such as Chrome for Testing, as an automatic fallback.

:::caution
Custom providers are NOT officially supported by Puppeteer. You accept full responsibility for binary compatibility, testing, and maintenance.
:::

## API

The programmatic API allows installing and launching browsers from your code. See the `test` folder for examples on how to use the `install`, `canInstall`, `launch`, `computeExecutablePath`, `computeSystemExecutablePath` and other methods.

## Classes

<table><thead><tr><th>

Class

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="cli">[CLI](./browsers.cli.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="defaultprovider">[DefaultProvider](./browsers.defaultprovider.md)</span>

</td><td>

Default provider implementation that uses default sources. This is the standard provider used by Puppeteer.

</td></tr>
<tr><td>

<span id="installedbrowser">[InstalledBrowser](./browsers.installedbrowser.md)</span>

</td><td>

**Remarks:**

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `InstalledBrowser` class.

</td></tr>
<tr><td>

<span id="process">[Process](./browsers.process.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="timeouterror">[TimeoutError](./browsers.timeouterror.md)</span>

</td><td>

**Remarks:**

The constructor for this class is marked as internal. Third-party code should not call the constructor directly or create subclasses that extend the `TimeoutError` class.

</td></tr>
</tbody></table>

## Enumerations

<table><thead><tr><th>

Enumeration

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="browser">[Browser](./browsers.browser.md)</span>

</td><td>

Supported browsers.

</td></tr>
<tr><td>

<span id="browserplatform">[BrowserPlatform](./browsers.browserplatform.md)</span>

</td><td>

Platform names used to identify a OS platform x architecture combination in the way that is relevant for the browser download.

</td></tr>
<tr><td>

<span id="browsertag">[BrowserTag](./browsers.browsertag.md)</span>

</td><td>

Enum describing a release channel for a browser.

You can use this in combination with [resolveBuildId()](./browsers.resolvebuildid.md) to resolve a build ID based on a release channel.

</td></tr>
<tr><td>

<span id="chromereleasechannel">[ChromeReleaseChannel](./browsers.chromereleasechannel.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Functions

<table><thead><tr><th>

Function

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="buildarchivefilename">[buildArchiveFilename(browser, platform, buildId, extension)](./browsers.buildarchivefilename.md)</span>

</td><td>

Utility function to build a standard archive filename.

</td></tr>
<tr><td>

<span id="candownload">[canDownload(options)](./browsers.candownload.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="computeexecutablepath">[computeExecutablePath(options)](./browsers.computeexecutablepath.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="computesystemexecutablepath">[computeSystemExecutablePath(options)](./browsers.computesystemexecutablepath.md)</span>

</td><td>

Returns a path to a system-wide Chrome installation given a release channel name by checking known installation locations (using [https://pptr.dev/browsers-api/browsers.computesystemexecutablepath](https://pptr.dev/browsers-api/browsers.computesystemexecutablepath)). If Chrome instance is not found at the expected path, an error is thrown.

</td></tr>
<tr><td>

<span id="createprofile">[createProfile(browser, opts)](./browsers.createprofile.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="detectbrowserplatform">[detectBrowserPlatform()](./browsers.detectbrowserplatform.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="getdownloadurl">[getDownloadUrl(browser, platform, buildId, baseUrl)](./browsers.getdownloadurl.md)</span>

</td><td>

Retrieves a URL for downloading the binary archive of a given browser.

The archive is bound to the specific platform and build ID specified.

</td></tr>
<tr><td>

<span id="getinstalledbrowsers">[getInstalledBrowsers(options)](./browsers.getinstalledbrowsers.md)</span>

</td><td>

Returns metadata about browsers installed in the cache directory.

</td></tr>
<tr><td>

<span id="getversioncomparator">[getVersionComparator(browser)](./browsers.getversioncomparator.md)</span>

</td><td>

Returns a version comparator for the given browser that can be used to sort browser versions.

</td></tr>
<tr><td>

<span id="install">[install(options)](./browsers.install.md)</span>

</td><td>

Downloads and unpacks the browser archive according to the [InstallOptions](./browsers.installoptions.md).

</td></tr>
<tr><td>

<span id="install">[install(options)](./browsers.install.md#overload-2)</span>

</td><td>

Downloads the browser archive according to the [InstallOptions](./browsers.installoptions.md) without unpacking.

</td></tr>
<tr><td>

<span id="launch">[launch(opts)](./browsers.launch.md)</span>

</td><td>

Launches a browser process according to [LaunchOptions](./browsers.launchoptions.md).

</td></tr>
<tr><td>

<span id="makeprogresscallback">[makeProgressCallback(browser, buildId)](./browsers.makeprogresscallback.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="resolvebuildid">[resolveBuildId(browser, platform, tag)](./browsers.resolvebuildid.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="resolvedefaultuserdatadir">[resolveDefaultUserDataDir(browser, platform, channel)](./browsers.resolvedefaultuserdatadir.md)</span>

</td><td>

Returns the expected default user data dir for the given channel. It does not check if the dir actually exists.

</td></tr>
<tr><td>

<span id="uninstall">[uninstall(options)](./browsers.uninstall.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Interfaces

<table><thead><tr><th>

Interface

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="browserprovider">[BrowserProvider](./browsers.browserprovider.md)</span>

</td><td>

Interface for custom browser provider implementations. Allows users to implement alternative download sources for browsers.

⚠️ **IMPORTANT**: Custom providers are NOT officially supported by Puppeteer.

By implementing this interface, you accept full responsibility for:

- Ensuring downloaded binaries are compatible with Puppeteer's expectations - Testing that browser launch and other features work with your binaries - Maintaining compatibility when Puppeteer or your download source changes - Version consistency across platforms if mixing sources

Puppeteer only tests and guarantees Chrome for Testing binaries.

</td></tr>
<tr><td>

<span id="downloadoptions">[DownloadOptions](./browsers.downloadoptions.md)</span>

</td><td>

Options passed to a provider.

</td></tr>
<tr><td>

<span id="getinstalledbrowsersoptions">[GetInstalledBrowsersOptions](./browsers.getinstalledbrowsersoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="installoptions">[InstallOptions](./browsers.installoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="launchoptions">[LaunchOptions](./browsers.launchoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="metadata">[Metadata](./browsers.metadata.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="options">[Options](./browsers.options.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="profileoptions">[ProfileOptions](./browsers.profileoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="systemoptions">[SystemOptions](./browsers.systemoptions.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="uninstalloptions">[UninstallOptions](./browsers.uninstalloptions.md)</span>

</td><td>

</td></tr>
</tbody></table>

## Variables

<table><thead><tr><th>

Variable

</th><th>

Description

</th></tr></thead>
<tbody><tr><td>

<span id="cdp_websocket_endpoint_regex">[CDP_WEBSOCKET_ENDPOINT_REGEX](./browsers.cdp_websocket_endpoint_regex.md)</span>

</td><td>

</td></tr>
<tr><td>

<span id="webdriver_bidi_websocket_endpoint_regex">[WEBDRIVER_BIDI_WEBSOCKET_ENDPOINT_REGEX](./browsers.webdriver_bidi_websocket_endpoint_regex.md)</span>

</td><td>

</td></tr>
</tbody></table>
