'use strict';
/* global Monogatari */

// 相容性處理 - 支援不同瀏覽器
var monogatari = null;
if (typeof Monogatari !== 'undefined') {
    monogatari = Monogatari.Monogatari || Monogatari.default || Monogatari;
}

if (monogatari) {
    monogatari.settings({
        "Name": "噬心毒戀",
        "Version": "1.0.0",
        "Label": "Start",
        "Slots": 10,
        "AutoSave": 0,
        "SaveLabel": "存檔",
        "AutoSaveLabel": "自動存檔",
        "SaveScreenshots": true,
        "ShowCredits": false,
        "TextSpeed": 30,
        "AutoPlaySpeed": 5,
        "MultiLanguage": false,
        "ShowMainScreen": true,
        "TypeAnimation": true,
        "NVL": false,
        "Preload": true,
        "AssetsPath": {
            "root": "assets",
            "characters": "characters",
            "scenes": "scenes"
        }
    });
}
