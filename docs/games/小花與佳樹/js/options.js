'use strict';
/* global Monogatari */

// 正確取得 monogatari 實例
const { Monogatari: monogatari } = Monogatari;

monogatari.settings({
    "Name": "圖書館的幽靈：少女的校園反擊課",
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
