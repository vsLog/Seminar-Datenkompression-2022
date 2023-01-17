/**
 * Creates a Map corresponding to the input parameter.
 * The Map counts the occurrences of each char containend in the input.
 * @param {string} str - input String
 * @returns {Map} charMap - Character occurrence map
 */
countChars = function (str) {
    var charMap = new Map();
    // Counts each the occurrences of each char
    for (var i = 0; i < str.length; i++) {
        if (charMap.has(str[i])) {
            charMap.set(str[i], (charMap.get(str[i]) + 1))
        }
        else {
            charMap.set(str[i], 1)
        }
    }
    return charMap
}

/**
 * Creates a String corresponding to a Map created by "countChars".
 * @param {Map} occurenceMap - input String
 * @returns {string} output - Character occurrence map
 */
mapToString = function (occurenceMap) {
    var output = "";
    for ( let [key, value] of occurenceMap) {
        output = output.concat(`${key}  occurs  ${value} times\n`);
    }
    return output
}

/**
 * Reads the input in the textfield "input_area" and outputs the occurrences of each char.
 * Stores the data in the sessionStorage.
 */
readInput = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    document.getElementById("output_area").value = mapToString(charMap);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
    createCharElement(charMap, totalChars);
}

/**
 * Creates a progress-bar using bootstrap 3 containing the occurenceMap data.
 * @param {Map} occurenceMap - Character occurrence map
 * @param {number} totalChars - total number of chars
 */
createCharElement = function(occurenceMap, totalChars) {
    var parent = document.getElementById("progressParent");
    parent.innerHTML = ""; // clears current progress-bar
    for (const char of occurenceMap.keys()) {
        // create a div for each unique char and fill it with the corresponding data
        g = document.createElement('div');
        g.setAttribute("class", "progress-bar progress-bar");
        g.setAttribute("role", "progressbar");
        // div gets a width related to it's relative occurrence count
        var width = (occurenceMap.get(char) / totalChars)*100 + '%';
        // div gets a random color to better differentiate between different divs
        g.setAttribute("style", `width:${width}; background-color: ${getRandomColor()}`);
        // adds tooltip containing  relative occurrence probability of char
        g.setAttribute("data-toggle", "tooltip");
        g.setAttribute("data-container", "body");
        g.setAttribute("title", `p(${char})=${occurenceMap.get(char)} / ${totalChars}`);
        g.innerHTML = char;
        parent.appendChild(g);
    }
}

/**
 * Creates a random rgb color.
 * @returns {string} color - rgb color
 */
function getRandomColor() {
    var color = `rgb(${rand(256)}, ${rand(256)}, ${rand(256)})`
    return color;
  }

/**
 * Creates a random number for a rgb color.
 * @returns {number} rgb color value
 */
function rand(max = 256) {
    return Math.floor(Math.random()*max);
  }