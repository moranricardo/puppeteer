# Puppeteer Architecture Overview

This diagram represents the structural hierarchy of objects and execution contexts within Puppeteer:

```mermaid
graph TD
    P[Puppeteer] <== DevTools Protocol ==> B[Browser]
    
    B --> BC1[BrowserContext 1]
    B --> BC2[BrowserContext]
    B --> BCN[BrowserContext N]
    
    subgraph BrowserContext_Workers [Shared & Service Workers]
        SW[Shared Workers]
        SEW[Service Workers]
    end
    
    BC2 --- BrowserContext_Workers
    BC2 --> P1[Page 1]
    BC2 --> P2[Page 2]
    BC2 --> PN[Page N]
    
    P1 --> W[Workers]
    P1 --> F1[Frame]
    P1 --> F2[Frame 2]
    P1 --> FN[Frame N]
    
    subgraph Extensions [Extensions]
        EC_Ext[Execution Contexts]
    end
    
    F1 --- Extensions
    F1 --> EC[ExecutionContext frame]
```

## Hierarchy Breakdown

- **Puppeteer**: Primary entry point using DevTools Protocol / BiDi to communicate with the browser instance.
- **Browser**: Represents the running browser process.
- **BrowserContext**: Isolated sessions (like Incognito windows) with independent cookies and cache.
- **Page**: Individual tabs or pages running inside a `BrowserContext`.
- **Frame**: Execution targets within a `Page` (main frame and `iframes`).
- **ExecutionContext**: JavaScript execution environments attached to frames or web workers.
