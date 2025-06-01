/* Parse playlists */

var msBatchVideoParser = (function () {
    function MsBatchVideoParser() {
    }

    MsBatchVideoParser.prototype = {
        parse: function (obj) {
            return msAbstractParser.parse(obj, []);
        },

        isSupportedSource: function (url) {
            return msAbstractParser.isSupportedSource(url);
        },

        supportedSourceCheckPriority: function () {
            return msAbstractParser.supportedSourceCheckPriority();
        },

        isPossiblySupportedSource: function (obj) {
            return msAbstractParser.isPossiblySupportedSource(obj);
        },

        overrideUrlPolicy: function (url) {
            return msAbstractParser.overrideUrlPolicy(url);
        }
    };

    return new MsBatchVideoParser();
}());
