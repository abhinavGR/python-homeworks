import webview

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Neo Maps</title>

<link
    href="https://unpkg.com/maplibre-gl@5.7.1/dist/maplibre-gl.css"
    rel="stylesheet"
/>

<script src="https://unpkg.com/maplibre-gl@5.7.1/dist/maplibre-gl.js"></script>

<style>
* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "Segoe UI",
        sans-serif;
    background: #f5f7fa;
}

#map {
    position: absolute;
    inset: 0;
}

/* -------------------------------------------------------
   FUTURISTIC TOP SEARCH
------------------------------------------------------- */

.search-panel {
    position: absolute;
    top: 22px;
    left: 24px;
    width: 430px;
    z-index: 20;
}

.search-box {
    height: 62px;
    display: flex;
    align-items: center;

    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.95);

    border-radius: 20px;

    box-shadow:
        0 15px 45px rgba(30, 50, 80, 0.16),
        0 2px 8px rgba(30, 50, 80, 0.08);

    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);

    transition: 0.25s ease;
}

.search-box:focus-within {
    border-color: rgba(50, 130, 255, 0.55);

    box-shadow:
        0 18px 55px rgba(30, 50, 80, 0.20),
        0 0 0 4px rgba(50, 130, 255, 0.08);
}

.logo {
    width: 40px;
    height: 40px;
    margin-left: 11px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 13px;

    color: white;
    font-size: 20px;
    font-weight: 800;

    background:
        linear-gradient(
            135deg,
            #1e8cff,
            #6a5cff
        );

    box-shadow:
        0 5px 16px rgba(50, 100, 255, 0.35);
}

#search {
    flex: 1;
    height: 100%;

    border: 0;
    outline: 0;

    padding: 0 15px;

    background: transparent;

    font-size: 16px;
    color: #182235;
}

#search::placeholder {
    color: #8b96a8;
}

.search-button {
    width: 45px;
    height: 45px;

    margin-right: 8px;

    border: 0;
    border-radius: 14px;

    background: #f1f5fa;

    color: #416080;

    font-size: 25px;

    cursor: pointer;

    transition: 0.2s;
}

.search-button:hover {
    background: #e6edf7;
    transform: scale(1.04);
}

/* -------------------------------------------------------
   SEARCH SUGGESTIONS
------------------------------------------------------- */

.suggestions {
    margin-top: 9px;

    overflow: hidden;

    border-radius: 18px;

    background: rgba(255, 255, 255, 0.95);

    box-shadow:
        0 20px 55px rgba(30, 50, 80, 0.18);

    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);

    display: none;
}

.suggestion {
    display: flex;
    align-items: center;

    padding: 13px 16px;

    cursor: pointer;

    border-bottom: 1px solid #edf1f5;

    transition: 0.15s;
}

.suggestion:last-child {
    border-bottom: 0;
}

.suggestion:hover,
.suggestion.active {
    background: #f2f7ff;
}

.suggestion-icon {
    width: 38px;
    height: 38px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-right: 12px;

    border-radius: 12px;

    background: #eef4fc;

    color: #4385d9;

    font-size: 17px;
}

.suggestion-text {
    min-width: 0;
}

.suggestion-name {
    font-weight: 650;
    color: #1b2638;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.suggestion-address {
    margin-top: 3px;

    font-size: 12px;
    color: #8995a7;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* -------------------------------------------------------
   FUTURISTIC SIDE CONTROL PANEL
------------------------------------------------------- */

.control-panel {
    position: absolute;

    right: 23px;
    top: 23px;

    z-index: 10;

    display: flex;
    flex-direction: column;
    gap: 9px;
}

.control {
    width: 50px;
    height: 50px;

    border: 1px solid rgba(255,255,255,0.9);

    border-radius: 16px;

    background: rgba(255,255,255,0.90);

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    box-shadow:
        0 10px 30px rgba(30,50,80,0.13);

    color: #35465e;

    font-size: 21px;

    cursor: pointer;

    transition:
        transform 0.18s,
        box-shadow 0.18s,
        background 0.18s;
}

.control:hover {
    transform: translateY(-2px);

    background: white;

    box-shadow:
        0 15px 35px rgba(30,50,80,0.20);
}

.control:active {
    transform: scale(0.94);
}

/* -------------------------------------------------------
   MAP STATUS PANEL
------------------------------------------------------- */

.status-panel {
    position: absolute;

    left: 24px;
    bottom: 23px;

    z-index: 10;

    padding: 13px 17px;

    border-radius: 16px;

    background: rgba(255,255,255,0.90);

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    box-shadow:
        0 12px 35px rgba(30,50,80,0.14);

    color: #516176;

    font-size: 12px;

    display: flex;
    align-items: center;
    gap: 9px;
}

.status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #27c889;

    box-shadow:
        0 0 0 4px rgba(39,200,137,0.12),
        0 0 12px rgba(39,200,137,0.45);
}

/* -------------------------------------------------------
   LOCATION MARKER
------------------------------------------------------- */

.neo-marker {
    width: 25px;
    height: 25px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            white 0 25%,
            #278cff 27% 100%
        );

    border: 3px solid white;

    box-shadow:
        0 4px 14px rgba(30,100,255,0.40);

    position: relative;
}

.neo-marker::before {
    content: "";

    position: absolute;

    left: 50%;
    top: 50%;

    width: 45px;
    height: 45px;

    transform: translate(-50%, -50%);

    border-radius: 50%;

    border: 2px solid rgba(39,140,255,0.30);

    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% {
        transform: translate(-50%, -50%) scale(.55);
        opacity: 1;
    }

    100% {
        transform: translate(-50%, -50%) scale(1.35);
        opacity: 0;
    }
}

/* -------------------------------------------------------
   MAPLIBRE ATTRIBUTION
------------------------------------------------------- */

.maplibregl-ctrl-attrib {
    border-radius: 12px 0 0 0 !important;
    background: rgba(255,255,255,.82) !important;
    backdrop-filter: blur(10px);
}
</style>
</head>

<body>

<div id="map"></div>

<!-- SEARCH -->
<div class="search-panel">

    <div class="search-box">

        <div class="logo">N</div>

        <input
            id="search"
            autocomplete="off"
            placeholder="Search places, roads, cities..."
        >

        <button
            class="search-button"
            onclick="searchPlace()"
        >⌕</button>

    </div>

    <div
        id="suggestions"
        class="suggestions"
    ></div>

</div>

<!-- CONTROLS -->
<div class="control-panel">

    <button
        class="control"
        onclick="zoomIn()"
        title="Zoom in"
    >+</button>

    <button
        class="control"
        onclick="zoomOut()"
        title="Zoom out"
    >−</button>

    <button
        class="control"
        onclick="goHome()"
        title="Home"
    >⌂</button>

    <button
        class="control"
        onclick="locateMe()"
        title="My location"
    >◎</button>

</div>

<!-- STATUS -->
<div class="status-panel">

    <span class="status-dot"></span>

    <span id="status">
        NEO MAPS • LIVE VECTOR MAP
    </span>

</div>

<script>

/* =======================================================
   MAP
======================================================= */

const HOME = [-96.7970, 32.7767];

let map;
let searchMarker = null;

let roadNameSource = null;
let transportationSource = null;

const searchInput =
    document.getElementById("search");

const suggestionsBox =
    document.getElementById("suggestions");

let searchResults = [];
let activeSuggestion = -1;
let searchTimer = null;


/* =======================================================
   MAP INITIALIZATION
======================================================= */

map = new maplibregl.Map({

    container: "map",

    style:
        "https://tiles.openfreemap.org/styles/liberty",

    center: HOME,

    zoom: 11.5,

    pitch: 0,

    bearing: 0,

    attributionControl: true,

    dragRotate: true,

    touchZoomRotate: true,

    maxZoom: 20,

    minZoom: 2

});


map.addControl(
    new maplibregl.NavigationControl({
        showCompass: false,
        showZoom: false
    }),
    "bottom-right"
);


/* =======================================================
   FIND SOURCE
======================================================= */

function findSourceForLayer(layerName) {

    const layers =
        map.getStyle().layers || [];

    for (const layer of layers) {

        if (
            layer["source-layer"] === layerName &&
            layer.source
        ) {
            return layer.source;
        }

    }

    return null;
}


/* =======================================================
   HIDE OLD ROAD LABELS / SHIELDS
======================================================= */

function hideExistingRoadNameLayers() {

    const layers =
        map.getStyle().layers || [];

    for (const layer of layers) {

        const sourceLayer =
            layer["source-layer"];

        if (
            sourceLayer === "transportation_name"
        ) {

            try {

                map.setLayoutProperty(
                    layer.id,
                    "visibility",
                    "none"
                );

            } catch (e) {}

        }

    }

}


/* =======================================================
   HIDE OLD SHIELDS
======================================================= */

function hideExistingShieldLayers() {

    const layers =
        map.getStyle().layers || [];

    for (const layer of layers) {

        const id =
            layer.id.toLowerCase();

        if (
            id.includes("shield") ||
            id.includes("road_shield")
        ) {

            try {

                map.setLayoutProperty(
                    layer.id,
                    "visibility",
                    "none"
                );

            } catch (e) {}

        }

    }

}


/* =======================================================
   MAKE ROADS CLEAN / LIGHT
======================================================= */

function makeRoadsLight() {

    const layers =
        map.getStyle().layers || [];

    for (const layer of layers) {

        if (
            layer.type !== "line" ||
            !layer["source-layer"]
        ) {
            continue;
        }

        const sourceLayer =
            layer["source-layer"];

        if (
            sourceLayer !== "transportation"
        ) {
            continue;
        }

        try {

            map.setPaintProperty(
                layer.id,
                "line-color",
                "#ffffff"
            );

        } catch (e) {}

        try {

            map.setPaintProperty(
                layer.id,
                "line-opacity",
                0.98
            );

        } catch (e) {}

    }

}


/* =======================================================
   SVG SHIELDS
======================================================= */

function interstateSvg() {

    return `
    <svg xmlns="http://www.w3.org/2000/svg"
         width="64"
         height="42"
         viewBox="0 0 64 42">

        <path
            d="M7 4
               Q32 0 57 4
               L54 38
               Q32 42 10 38
               Z"
            fill="#1855a5"
            stroke="#ffffff"
            stroke-width="3"/>

        <path
            d="M11 5
               Q32 2 53 5
               L51 14
               Q32 12 13 14
               Z"
            fill="#d72828"/>

        <text
            x="32"
            y="12"
            text-anchor="middle"
            font-size="7"
            font-family="Arial"
            font-weight="bold"
            fill="white">
            INTERSTATE
        </text>
    </svg>`;
}


function usSvg() {

    return `
    <svg xmlns="http://www.w3.org/2000/svg"
         width="58"
         height="42"
         viewBox="0 0 58 42">

        <path
            d="M5 6
               Q29 0 53 6
               L49 37
               Q29 42 9 37
               Z"
            fill="#ffffff"
            stroke="#222"
            stroke-width="2"/>

        <text
            x="29"
            y="17"
            text-anchor="middle"
            font-size="7"
            font-family="Arial"
            font-weight="bold">
            U.S.
        </text>

    </svg>`;
}


function texasSvg() {

    return `
    <svg xmlns="http://www.w3.org/2000/svg"
         width="54"
         height="42"
         viewBox="0 0 54 42">

        <path
            d="M27 2
               L31 9
               L40 7
               L38 16
               L48 21
               L39 26
               L40 36
               L29 33
               L22 40
               L18 31
               L7 32
               L12 23
               L5 16
               L15 14
               L17 5
               L25 10
               Z"
            fill="#ffffff"
            stroke="#666"
            stroke-width="2"/>

    </svg>`;
}


function genericSvg() {

    return `
    <svg xmlns="http://www.w3.org/2000/svg"
         width="58"
         height="38"
         viewBox="0 0 58 38">

        <rect
            x="2"
            y="2"
            width="54"
            height="34"
            rx="17"
            fill="#ffffff"
            stroke="#65758a"
            stroke-width="2"/>

    </svg>`;
}


/* =======================================================
   ADD SVG IMAGE
======================================================= */

function addSvgImage(name, svg) {

    return new Promise((resolve) => {

        const image =
            new Image();

        image.onload = () => {

            if (!map.hasImage(name)) {

                map.addImage(
                    name,
                    image
                );

            }

            resolve();

        };

        image.src =
            "data:image/svg+xml;charset=utf-8," +
            encodeURIComponent(svg);

    });

}


/* =======================================================
   ROAD NAMES
======================================================= */

function addCurrentRoadNames() {

    if (!roadNameSource) {
        return;
    }

    if (
        map.getLayer("neo-current-road-names")
    ) {
        map.removeLayer(
            "neo-current-road-names"
        );
    }

    map.addLayer({

        id: "neo-current-road-names",

        type: "symbol",

        source: roadNameSource,

        "source-layer":
            "transportation_name",

        minzoom: 10,

        filter: [
            "all",

            ["has", "name"],

            [
                "!=",
                ["get", "name"],
                ""
            ]
        ],

        layout: {

            "text-field":
                ["get", "name"],

            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                10,
                10,
                15,
                13,
                18,
                15
            ],

            "text-font": [
                "Noto Sans Regular"
            ],

            "text-letter-spacing":
                0.02,

            "symbol-placement":
                "line",

            "text-max-angle":
                30,

            "text-padding":
                30

        },

        paint: {

            "text-color":
                "#526173",

            "text-halo-color":
                "rgba(255,255,255,0.96)",

            "text-halo-width":
                2.2,

            "text-halo-blur":
                0.25

        }

    });

}


/* =======================================================
   HIGHWAY SHIELDS
======================================================= */

function addHighwayShields() {

    if (!roadNameSource) {
        return;
    }

    if (
        map.getLayer("neo-highway-shields")
    ) {
        map.removeLayer(
            "neo-highway-shields"
        );
    }

    map.addLayer({

        id: "neo-highway-shields",

        type: "symbol",

        source: roadNameSource,

        "source-layer":
            "transportation_name",

        minzoom: 7,

        filter: [
            "all",

            ["has", "ref"],

            [
                "!=",
                ["get", "ref"],
                ""
            ]
        ],

        layout: {

            "symbol-placement":
                "line",

            "symbol-spacing":
                650,

            "icon-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                0.42,
                12,
                0.52,
                17,
                0.60
            ],

            "icon-image": [
                "match",

                ["get", "network"],

                "us-interstate",
                "neo-interstate",

                "us-highway",
                "neo-us",

                "us-state",
                "neo-texas",

                "neo-generic"
            ],

            "text-field":
                ["to-string", ["get", "ref"]],

            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                8,
                12,
                10,
                17,
                12
            ],

            "text-font": [
                "Noto Sans Bold"
            ],

            "text-offset": [
                0,
                0
            ],

            "text-allow-overlap":
                false,

            "icon-allow-overlap":
                false

        },

        paint: {

            "text-color":
                "#1b2638",

            "text-halo-color":
                "#ffffff",

            "text-halo-width":
                1

        }

    });

}


/* =======================================================
   TOLL LABEL
======================================================= */

function addTollLabels() {

    if (!transportationSource) {
        return;
    }

    if (
        map.getLayer("neo-toll")
    ) {
        map.removeLayer(
            "neo-toll"
        );
    }

    map.addLayer({

        id: "neo-toll",

        type: "symbol",

        source:
            transportationSource,

        "source-layer":
            "transportation",

        minzoom: 10,

        filter: [
            "any",

            [
                "==",
                ["get", "toll"],
                "yes"
            ],

            [
                "==",
                ["get", "toll"],
                true
            ],

            [
                "==",
                ["get", "toll"],
                1
            ]

        ],

        layout: {

            "symbol-placement":
                "line",

            "symbol-spacing":
                1000,

            "text-field":
                "TOLL",

            "text-size":
                8,

            "text-font": [
                "Noto Sans Bold"
            ],

            "text-padding":
                20

        },

        paint: {

            "text-color":
                "#ffffff",

            "text-halo-color":
                "#596879",

            "text-halo-width":
                4

        }

    });

}


/* =======================================================
   SEARCH
======================================================= */

async function fetchSearchResults(query) {

    const url =
        "https://nominatim.openstreetmap.org/search" +
        "?format=jsonv2" +
        "&addressdetails=1" +
        "&limit=7" +
        "&countrycodes=us" +
        "&accept-language=en" +
        "&q=" +
        encodeURIComponent(query);

    const response =
        await fetch(url);

    if (!response.ok) {
        throw new Error(
            "Search request failed"
        );
    }

    return await response.json();
}


/* =======================================================
   SEARCH RESULT NAME
======================================================= */

function resultName(place) {

    if (
        place.name &&
        place.name.trim()
    ) {
        return place.name;
    }

    if (
        place.address &&
        place.address.road
    ) {
        return place.address.road;
    }

    return place.display_name
        .split(",")[0];

}


/* =======================================================
   ADDRESS
======================================================= */

function resultAddress(place) {

    const a =
        place.address || {};

    const parts = [];

    if (a.house_number)
        parts.push(a.house_number);

    if (a.road)
        parts.push(a.road);

    const city =
        a.city ||
        a.town ||
        a.village ||
        a.hamlet;

    if (city)
        parts.push(city);

    if (a.state)
        parts.push(a.state);

    if (a.postcode)
        parts.push(a.postcode);

    return parts.join(", ");

}


/* =======================================================
   ICON
======================================================= */

function resultIcon(place) {

    const type =
        (
            place.type ||
            ""
        ).toLowerCase();

    const cls =
        (
            place.class ||
            ""
        ).toLowerCase();

    if (
        type.includes("restaurant") ||
        type.includes("cafe") ||
        cls === "amenity"
    ) {
        return "●";
    }

    if (
        type.includes("hotel") ||
        type.includes("motel")
    ) {
        return "◆";
    }

    if (
        type.includes("motorway") ||
        type.includes("highway") ||
        type.includes("road")
    ) {
        return "━";
    }

    if (
        type.includes("city") ||
        type.includes("town") ||
        type.includes("village")
    ) {
        return "◇";
    }

    return "⌖";

}


/* =======================================================
   SHOW SUGGESTIONS
======================================================= */

function showSuggestions(results) {

    searchResults =
        results || [];

    activeSuggestion = -1;

    suggestionsBox.innerHTML = "";

    if (!searchResults.length) {

        suggestionsBox.style.display =
            "none";

        return;

    }

    searchResults.forEach(
        (place, index) => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "suggestion";

            item.innerHTML = `

                <div class="suggestion-icon">
                    ${resultIcon(place)}
                </div>

                <div class="suggestion-text">

                    <div class="suggestion-name">
                        ${escapeHtml(
                            resultName(place)
                        )}
                    </div>

                    <div class="suggestion-address">
                        ${escapeHtml(
                            resultAddress(place)
                        )}
                    </div>

                </div>
            `;

            item.onclick = () => {

                selectSearchResult(
                    index
                );

            };

            suggestionsBox.appendChild(
                item
            );

        }
    );

    suggestionsBox.style.display =
        "block";

}


/* =======================================================
   HTML ESCAPE
======================================================= */

function escapeHtml(value) {

    return String(value || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


/* =======================================================
   SELECT RESULT
======================================================= */

function selectSearchResult(index) {

    const place =
        searchResults[index];

    if (!place) {
        return;
    }

    const lon =
        parseFloat(place.lon);

    const lat =
        parseFloat(place.lat);

    let zoom = 16;

    const type =
        (
            place.type ||
            ""
        ).toLowerCase();

    if (
        type === "city" ||
        type === "town"
    ) {
        zoom = 12;
    }

    if (
        type === "state" ||
        type === "country"
    ) {
        zoom = 7;
    }

    map.flyTo({

        center: [
            lon,
            lat
        ],

        zoom: zoom,

        speed: 1.25,

        curve: 1.25,

        essential: true

    });

    if (searchMarker) {

        searchMarker.remove();

    }

    const markerElement =
        document.createElement(
            "div"
        );

    markerElement.className =
        "neo-marker";

    searchMarker =
        new maplibregl.Marker({
            element: markerElement
        })
        .setLngLat([
            lon,
            lat
        ])
        .addTo(map);

    searchInput.value =
        resultName(place);

    hideSuggestions();

    setStatus(
        "LOCATION • " +
        resultName(place)
    );

}


/* =======================================================
   SEARCH BUTTON
======================================================= */

async function searchPlace() {

    const query =
        searchInput.value.trim();

    if (query.length < 2) {
        return;
    }

    try {

        setStatus(
            "SEARCHING • " +
            query
        );

        const results =
            await fetchSearchResults(
                query
            );

        showSuggestions(results);

        if (results.length) {

            selectSearchResult(0);

        } else {

            setStatus(
                "NO RESULTS • " +
                query
            );

        }

    } catch (error) {

        console.error(error);

        setStatus(
            "SEARCH UNAVAILABLE"
        );

    }

}


/* =======================================================
   LIVE SEARCH
======================================================= */

searchInput.addEventListener(
    "input",
    () => {

        clearTimeout(
            searchTimer
        );

        const query =
            searchInput.value.trim();

        if (query.length < 2) {

            hideSuggestions();

            return;

        }

        searchTimer =
            setTimeout(
                async () => {

                    try {

                        const results =
                            await fetchSearchResults(
                                query
                            );

                        showSuggestions(
                            results
                        );

                    } catch (error) {

                        console.error(
                            error
                        );

                    }

                },
                350
            );

    }
);


/* =======================================================
   KEYBOARD SEARCH
======================================================= */

searchInput.addEventListener(
    "keydown",
    (event) => {

        const items =
            suggestionsBox.querySelectorAll(
                ".suggestion"
            );

        if (
            event.key ===
            "ArrowDown"
        ) {

            event.preventDefault();

            activeSuggestion =
                Math.min(
                    activeSuggestion + 1,
                    items.length - 1
                );

            updateActiveSuggestion(
                items
            );

        }

        else if (
            event.key ===
            "ArrowUp"
        ) {

            event.preventDefault();

            activeSuggestion =
                Math.max(
                    activeSuggestion - 1,
                    0
                );

            updateActiveSuggestion(
                items
            );

        }

        else if (
            event.key ===
            "Enter"
        ) {

            event.preventDefault();

            if (
                activeSuggestion >= 0
            ) {

                selectSearchResult(
                    activeSuggestion
                );

            } else {

                searchPlace();

            }

        }

        else if (
            event.key ===
            "Escape"
        ) {

            hideSuggestions();

        }

    }
);


/* =======================================================
   ACTIVE SUGGESTION
======================================================= */

function updateActiveSuggestion(
    items
) {

    items.forEach(
        (item, index) => {

            item.classList.toggle(
                "active",
                index ===
                activeSuggestion
            );

        }
    );

}


/* =======================================================
   HIDE SUGGESTIONS
======================================================= */

function hideSuggestions() {

    suggestionsBox.style.display =
        "none";

    activeSuggestion = -1;

}


/* =======================================================
   OUTSIDE CLICK
======================================================= */

document.addEventListener(
    "click",
    (event) => {

        if (
            !event.target.closest(
                ".search-panel"
            )
        ) {

            hideSuggestions();

        }

    }
);


/* =======================================================
   CONTROLS
======================================================= */

function zoomIn() {

    map.easeTo({

        zoom:
            Math.min(
                map.getZoom() + 1,
                20
            ),

        duration: 400

    });

}


function zoomOut() {

    map.easeTo({

        zoom:
            Math.max(
                map.getZoom() - 1,
                2
            ),

        duration: 400

    });

}


function goHome() {

    map.flyTo({

        center: HOME,

        zoom: 11.5,

        pitch: 0,

        bearing: 0,

        speed: 1.2,

        essential: true

    });

    setStatus(
        "NEO MAPS • DALLAS AREA"
    );

}


function locateMe() {

    if (
        !navigator.geolocation
    ) {

        setStatus(
            "LOCATION NOT AVAILABLE"
        );

        return;

    }

    setStatus(
        "LOCATING..."
    );

    navigator.geolocation.getCurrentPosition(

        (position) => {

            const lon =
                position.coords.longitude;

            const lat =
                position.coords.latitude;

            map.flyTo({

                center: [
                    lon,
                    lat
                ],

                zoom: 15,

                speed: 1.2,

                essential: true

            });

            if (searchMarker) {
                searchMarker.remove();
            }

            const element =
                document.createElement(
                    "div"
                );

            element.className =
                "neo-marker";

            searchMarker =
                new maplibregl.Marker({
                    element: element
                })
                .setLngLat([
                    lon,
                    lat
                ])
                .addTo(map);

            setStatus(
                "LOCATION • CURRENT POSITION"
            );

        },

        () => {

            setStatus(
                "LOCATION PERMISSION DENIED"
            );

        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 30000
        }

    );

}


/* =======================================================
   STATUS
======================================================= */

function setStatus(text) {

    document.getElementById(
        "status"
    ).textContent = text;

}


/* =======================================================
   MAP LOAD
======================================================= */

map.on(
    "load",
    async () => {

        setStatus(
            "NEO MAPS • LOADING VECTOR DATA"
        );

        roadNameSource =
            findSourceForLayer(
                "transportation_name"
            );

        transportationSource =
            findSourceForLayer(
                "transportation"
            );

        hideExistingRoadNameLayers();

        hideExistingShieldLayers();

        makeRoadsLight();

        addCurrentRoadNames();

        await addSvgImage(
            "neo-interstate",
            interstateSvg()
        );

        await addSvgImage(
            "neo-us",
            usSvg()
        );

        await addSvgImage(
            "neo-texas",
            texasSvg()
        );

        await addSvgImage(
            "neo-generic",
            genericSvg()
        );

        addHighwayShields();

        addTollLabels();

        setStatus(
            "NEO MAPS • LIVE VECTOR MAP"
        );

    }
);


/* =======================================================
   SMOOTH MAP EFFECTS
======================================================= */

map.on(
    "zoomstart",
    () => {

        document.body.style.cursor =
            "grabbing";

    }
);

map.on(
    "zoomend",
    () => {

        document.body.style.cursor =
            "default";

    }
);

</script>

</body>
</html>
"""


if __name__ == "__main__":

    webview.create_window(
        "Abhinav Maps",
        html=HTML,
        width=1500,
        height=900,
        min_size=(1000, 650),
        background_color="#f5f7fa"
    )

    webview.start(
        debug=False
    )