const form = document.querySelector("#destination-form");
const destinationInput = document.querySelector("#destination");
const suggestions = document.querySelector("#destination-options");
const formStatus = document.querySelector("#form-status");
const routeLine = document.querySelector("#route-line");
const routePoints = document.querySelector("#route-points");

const start = "startpunkt";
const connections = [
    ["startpunkt", "knoten_1"],
    ["knoten_1", "ost_1"],
    ["ost_1", "ost_2"],
    ["knoten_1", "knoten_2"],
    ["knoten_2", "knoten_nord"],
    ["knoten_nord", "nord_1"],
    ["knoten_nord", "nord_2"],
    ["knoten_2", "knoten_3"],
    ["knoten_3", "knoten_4"],
    ["knoten_4", "nord_west_1"],
    ["knoten_4", "west_1"],
    ["knoten_4", "sued_west"],
    ["west_1", "west_2"],
];

const points = {
    startpunkt: [675, 400],
    knoten_1: [680, 318],
    knoten_2: [556, 314],
    knoten_3: [488, 354],
    knoten_4: [327, 349],
    knoten_nord: [624, 185],
    ost_1: [769, 330],
    ost_2: [880, 340],
    nord_1: [511, 185],
    nord_2: [777, 176],
    nord_west_1: [163, 82],
    west_1: [165, 349],
    west_2: [96, 348],
    sued_west: [255, 485],
};

const destinations = new Set([
    "ost_1",
    "ost_2",
    "nord_1",
    "nord_2",
    "nord_west_1",
    "west_1",
    "west_2",
    "sued_west",
]);

const destinationOptions = [...destinations];
let activeSuggestion = -1;

function closeSuggestions() {
    suggestions.classList.remove("is-open");
    destinationInput.setAttribute("aria-expanded", "false");
    activeSuggestion = -1;
}

function renderSuggestions(showAll = false) {
    const query = showAll ? "" : destinationInput.value.trim().toLowerCase();
    const matches = destinationOptions.filter((destination) => destination.includes(query));

    suggestions.replaceChildren();
    matches.forEach((destination, index) => {
        const suggestion = document.createElement("li");
        suggestion.className = "suggestion";
        suggestion.setAttribute("role", "option");
        suggestion.textContent = destination;
        suggestion.addEventListener("mousedown", (event) => {
            event.preventDefault();
            destinationInput.value = destination;
            closeSuggestions();
        });
        suggestion.dataset.index = index;
        suggestions.appendChild(suggestion);
    });

    activeSuggestion = -1;
    suggestions.classList.toggle("is-open", matches.length > 0);
    destinationInput.setAttribute("aria-expanded", String(matches.length > 0));
}

destinationInput.addEventListener("input", renderSuggestions);
destinationInput.addEventListener("focus", () => renderSuggestions(true));
destinationInput.addEventListener("click", () => renderSuggestions(true));
destinationInput.addEventListener("keydown", (event) => {
    const items = [...suggestions.querySelectorAll(".suggestion")];

    if (event.key === "Escape") {
        closeSuggestions();
        return;
    }

    if (!items.length || !suggestions.classList.contains("is-open")) {
        return;
    }

    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        activeSuggestion = (activeSuggestion + (event.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
        items.forEach((item, index) => item.classList.toggle("is-active", index === activeSuggestion));
        destinationInput.value = items[activeSuggestion].textContent;
    }

    if (event.key === "Enter" && activeSuggestion >= 0) {
        event.preventDefault();
        closeSuggestions();
    }
});

document.addEventListener("click", (event) => {
    if (!event.target.closest(".input-field")) {
        closeSuggestions();
    }
});

function findPath(goal) {
    const queue = [[start, [start]]];
    const visited = new Set([start]);

    while (queue.length > 0) {
        const [current, path] = queue.shift();

        if (current === goal) {
            return path;
        }

        for (const [from, to] of connections) {
            if (from === current && !visited.has(to)) {
                visited.add(to);
                queue.push([to, [...path, to]]);
            }
        }
    }

    return null;
}

function drawPath(path) {
    routeLine.setAttribute(
        "points",
        path.map((point) => points[point].join(",")).join(" ")
    );
    routeLine.classList.remove("route-visible");
    void routeLine.offsetWidth;
    routeLine.classList.add("route-visible");
    routePoints.replaceChildren();

    for (const [index, point] of path.entries()) {
        const marker = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        marker.setAttribute("cx", points[point][0]);
        marker.setAttribute("cy", points[point][1]);
        marker.setAttribute("r", index === 0 || index === path.length - 1 ? "9" : "5");
        marker.setAttribute("class", index === path.length - 1 ? "route-point destination-point" : "route-point");
        routePoints.appendChild(marker);
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const destination = destinationInput.value.trim().toLowerCase();

    if (!destinations.has(destination)) {
        routeLine.setAttribute("points", "");
        routeLine.classList.remove("route-visible");
        routePoints.replaceChildren();
        formStatus.textContent = "Bitte wähle ein bekanntes Ziel aus der Liste.";
        formStatus.setAttribute("data-error", "true");
        return;
    }

    const path = findPath(destination);

    if (!path) {
        formStatus.textContent = "Für dieses Ziel wurde kein Weg gefunden.";
        formStatus.setAttribute("data-error", "true");
        return;
    }

    drawPath(path);
    formStatus.removeAttribute("data-error");
    formStatus.textContent = `Weg zu „${destination}“ angezeigt.`;
});
