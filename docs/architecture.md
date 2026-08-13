# Puppeteer Architecture Overview

This document describes the structural hierarchy of objects, execution contexts, and communication protocols within Puppeteer.

## Object Hierarchy Diagram

```mermaid
graph TD
    P[Puppeteer] <== CDP / WebDriver BiDi ==> B[Browser]
    
    B --> BC1[BrowserContext 1]
    B --> BC2[BrowserContext 2]
    B --> BCN[BrowserContext N]
    
    BC2 --> P1[Page 1]
    BC2 --> P2[Page 2]
    BC2 --> PN[Page N]
    
    BC2 -.-> SW[Service / Shared Workers]
    
    P1 --> W[Web Workers]
    P1 --> F1[Main Frame]
    P1 --> F2[iframe 1]
    P1 --> FN[iframe N]
    
    F1 --> EC1[Main ExecutionContext]
    F1 -.-> EC_Ext[Extension ExecutionContexts]
```

## Hierarchy Breakdown

- **Puppeteer**: Primary entry point. Communicates with the browser instance over Chrome DevTools Protocol (CDP) or WebDriver BiDi.
- **Browser**: Represents the running browser process (Chrome, Chromium, or Firefox).
- **BrowserContext**: Isolated browser sessions (similar to Incognito windows) with independent cookies, cache, and storage.
- **Page**: Individual browser tabs or pages running within a `BrowserContext`.
- **Frame**: Structural targets within a `Page`, representing the main document or embedded `iframes`.
- **ExecutionContext**: Isolated JavaScript execution environments where scripts run (frames, web workers, or browser extension scripts).
