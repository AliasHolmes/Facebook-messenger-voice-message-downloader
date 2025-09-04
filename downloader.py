// ==UserScript==
// @name         Messenger E2EE Voice Downloader
// @namespace    https://example.com
// @version      1.0
// @description  Capture and download decrypted voice messages in Messenger encrypted chats
// @match        https://www.facebook.com/messages/*
// @match        https://www.messenger.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    // Patch URL.createObjectURL to intercept audio blobs
    const originalCreate = URL.createObjectURL;
    URL.createObjectURL = function(blob) {
        try {
            if (blob && blob.type && blob.type.startsWith("audio/")) {
                console.log("[E2EE Voice Downloader] Captured audio blob:", blob);
                saveBlob(blob);
            }
        } catch (err) {
            console.warn("[E2EE Voice Downloader] Error checking blob:", err);
        }
        return originalCreate.apply(this, arguments);
    };

    function saveBlob(blob) {
        const url = originalCreate(blob);
        const a = document.createElement('a');
        a.href = url;
        const ext = blob.type.includes("mpeg") ? "mp3" : "m4a";
        a.download = `voice-${Date.now()}.${ext}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }

    console.log("[E2EE Voice Downloader] Script loaded and watching for audio blobs...");
})();
