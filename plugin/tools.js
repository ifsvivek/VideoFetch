// Helper function to convert cookies to Netscape format
function cookiesToNetscapeText(cookies) {
    if (!cookies || !cookies.length) {
        return "";
    }
    
    let result = "# Netscape HTTP Cookie File\n";
    
    for (let cookie of cookies) {
        // Format: domain, domainSpecified, path, secure, expiration, name, value
        let domain = cookie.domain || "";
        let domainSpecified = domain.startsWith(".") ? "TRUE" : "FALSE";
        let path = "/";
        let secure = cookie.isSecure ? "TRUE" : "FALSE";
        let expiration = cookie.expirationDate ? Math.floor(cookie.expirationDate / 1000) : "0";
        let name = cookie.name || "";
        let value = cookie.value || "";
        
        result += `${domain}\t${domainSpecified}\t${path}\t${secure}\t${expiration}\t${name}\t${value}\n`;
    }
    
    return result;
}

// Enhanced error handling for yt-dlp output - pass through exact errors
function parseYtDlpError(output) {
    if (!output) {
        return { error: "No output from yt-dlp", isParseError: true };
    }
    
    // Look for ERROR lines and extract the exact message
    const errorLines = output.split('\n').filter(line => 
        line.includes('ERROR:') || line.includes('WARNING:')
    );
    
    if (errorLines.length > 0) {
        // Use the first error message, cleaned up
        let errorMsg = errorLines[0]
            .replace(/^ERROR:\s*/i, '')
            .replace(/^WARNING:\s*/i, '')
            .trim();
            
        // Common error types for better user experience
        if (/unsupported url/i.test(errorMsg)) {
            return { error: `Unsupported URL: ${errorMsg}`, isParseError: false };
        }
        if (/video unavailable/i.test(errorMsg)) {
            return { error: `Video unavailable: ${errorMsg}`, isParseError: false };
        }
        if (/private video/i.test(errorMsg)) {
            return { error: `Private video: ${errorMsg}`, isParseError: false };
        }
        if (/geo.?block/i.test(errorMsg) || /not available in your country/i.test(errorMsg)) {
            return { error: `Geo-blocked: ${errorMsg}`, isParseError: false };
        }
        if (/sign in/i.test(errorMsg) || /login/i.test(errorMsg)) {
            return { error: `Authentication required: ${errorMsg}`, isParseError: false };
        }
        
        // Return the exact error message from yt-dlp
        return { error: errorMsg, isParseError: true };
    }
    
    // If no ERROR line found, return generic message
    return { error: "Failed to extract video information", isParseError: true };
}

