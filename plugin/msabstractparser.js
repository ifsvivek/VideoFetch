var g_browsers = Object.create(null);

var msAbstractParser = (function () {
    function MsAbstractParser() {
    }

    MsAbstractParser.prototype = {

        parse: function (obj, customArgs) {
            console.log("parsing...");

            let args = [];
            let tmpCookies;
            let systemUserAgent;
            let systemBrowser;
            let allowWbCookies = true;

            try {
                systemUserAgent = qtJsSystem.defaultUserAgent;
                systemBrowser = qtJsSystem.defaultWebBrowser;
                allowWbCookies = App.pluginsAllowWbCookies;
            }
            catch (e) { }

            let proxyUrl = qtJsNetworkProxyMgr.proxyForUrl(obj.url).url();
            if (proxyUrl) {
                proxyUrl = proxyUrl.replace(/^https:\/\//i, 'http://'); // FDM bug workaround
                args.push("--proxy", proxyUrl);
            }

            args.push("-J", "--flat-playlist", "--no-warnings", "--compat-options", "no-youtube-unavailable-videos");

            if (allowWbCookies) {
                if (obj.cookies && obj.cookies.length) {
                    tmpCookies = qtJsTools.createTmpFile("request_" + obj.requestId + "_cookies");
                    if (tmpCookies && tmpCookies.writeText(cookiesToNetscapeText(obj.cookies)))
                        args.push("--cookies", tmpCookies.path);
                }
                else {
                    let browser = obj.browser || systemBrowser;
                    if (browser) {
                        if (!(browser in g_browsers)) {
                            return this.checkBrowser(obj.requestId, obj.interactive, browser)
                                .then(() => this.parse(obj, customArgs));
                        }
                        else if (g_browsers[browser]) {
                            args.push('--cookies-from-browser', browser);
                        }
                    }
                }
            }

            let userAgent = obj.userAgent || systemUserAgent;
            if (userAgent)
                args.push('--user-agent', userAgent);

            if (customArgs.length)
                args = args.concat(customArgs);

            args.push(obj.url);

            return launchPythonScript(obj.requestId, obj.interactive, "yt-dlp/yt_dlp/__main__.py", args)
                .then(function (obj) {
                    console.log("Python result: ", obj.output);

                    return new Promise(function (resolve, reject) {
                        var output = obj.output.trim();
                        if (!output || output[0] !== '{') {
                            var errorInfo = parseYtDlpError(output);
                            reject(errorInfo);
                        }
                        else {
                            try {
                                resolve(JSON.parse(output));
                            } catch (e) {
                                reject({
                                    error: "Failed to parse yt-dlp JSON output",
                                    isParseError: true
                                });
                            }
                        }
                    });
                });
        },

        isSupportedSource: function (url) {
            // Let yt-dlp decide what it can handle - don't hardcode domains
            return false; // Always use isPossiblySupportedSource for broader coverage
        },

        supportedSourceCheckPriority: function () {
            return 100; // Higher priority to ensure this plugin is tried for supported URLs
        },

        isPossiblySupportedSource: function (obj) {
            // Be very permissive - let yt-dlp decide what it can handle
            // Only exclude obvious non-video content and very basic checks
            
            // Skip binary files that are clearly not video pages
            if (obj.contentType) {
                if (/^(image\/|application\/(pdf|zip|rar|exe|msi|octet-stream)|text\/(css|javascript))/.test(obj.contentType)) {
                    return false;
                }
            }
            
            // Skip extremely large files that are definitely not web pages
            if (obj.resourceSize !== -1 && obj.resourceSize > 50 * 1024 * 1024) {
                return false;
            }
            
            // Only process HTTP(S) URLs
            if (!/^https?:\/\//.test(obj.url)) {
                return false;
            }
            
            // Let yt-dlp try everything else - this covers all 1800+ supported sites
            return true;
        },

        overrideUrlPolicy: function (url) {
            return true;
        },

        checkBrowser: function (requestId, interactive, browser) {
            console.log("Checking browser support (", browser, ")...");

            return launchPythonScript(requestId, interactive, "yt-dlp/yt_dlp/__main__.py", ['--cookies-from-browser', browser, 'e692ec362191442c960a761ac6b84878://test.test'])
                .then(function (obj) {
                    console.log("Python result: ", obj.output);

                    return new Promise(function (resolve, reject) {
                        var output = obj.output.trim();
                        if (!output) {
                            reject({
                                error: "Parse error",
                                isParseError: false
                            });
                        }
                        else {
                            let isSupported = /"e692ec362191442c960a761ac6b84878"/.test(output);

                            console.log(browser, " supported: ", isSupported);

                            g_browsers[browser] = isSupported;

                            resolve();
                        }
                    });
                });
        }
    };

    return new MsAbstractParser();
}());
