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
            return false;
        },

        supportedSourceCheckPriority: function () {
            return 0;
        },

        isPossiblySupportedSource: function (obj) {
            // Only process HTTP(S) URLs
            if (!/^https?:\/\//.test(obj.url)) {
                return false;
            }

            // Skip binary/non-page content types
            if (obj.contentType) {
                if (/^(image\/|application\/(pdf|zip|rar|exe|msi|octet-stream)|text\/(css|javascript))/.test(obj.contentType)) {
                    return false;
                }
                // Only proceed for HTML pages and unknown content types
                if (/^(video\/|audio\/)/.test(obj.contentType)) {
                    return false;
                }
            }

            // Skip extremely large files that are definitely not web pages
            if (obj.resourceSize !== -1 && obj.resourceSize > 50 * 1024 * 1024) {
                return false;
            }

            // Skip URLs that look like direct file downloads (have a known non-media extension)
            var urlPath = obj.url.split('?')[0].split('#')[0].toLowerCase();
            if (/\.(zip|exe|msi|dmg|pkg|deb|rpm|tar|gz|bz2|xz|7z|rar|cab|iso|img|apk|ipa|jar|war|ear|pdf|doc|docx|xls|xlsx|ppt|pptx|txt|csv|bin|dat|db|sqlite|log|cfg|ini|conf|sh|bat|ps1|dll|so|dylib|whl|egg|gem|nupkg|vsix)$/.test(urlPath)) {
                return false;
            }

            // Let yt-dlp try everything else - this covers all 1800+ supported sites
            return true;
        },

        overrideUrlPolicy: function (url) {
            return false;
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
