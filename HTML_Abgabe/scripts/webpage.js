countChars = function (str) {
    var charMap = new Map();

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

mapToString = function (occurenceMap) {
    var output = "";
    for ( let [key, value] of occurenceMap) {
        output = output.concat(`${key}  occurs  ${value} times\n`);
    }
    return output
}

readInput = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    document.getElementById("output_area").value = mapToString(charMap);
    createCharElemnt(charMap, totalChars);
}

createCharElemnt = function(occurenceMap, totalChars) {
    var parent = document.getElementById("progressParent");
    parent.innerHTML = "";
    for (const char of occurenceMap.keys()) {
        g = document.createElement('div');
        g.setAttribute("class", "progress-bar progress-bar");
        g.setAttribute("role", "progressbar");
        var width = (occurenceMap.get(char) / totalChars)*100 + '%';
        g.setAttribute("style", `width:${width}; background-color: ${getRandomColor()}`);
        g.setAttribute("data-toggle", "tooltip");
        g.setAttribute("data-container", "body");
        g.setAttribute("title", `p(${char})=${occurenceMap.get(char)} / ${totalChars}`);
        g.innerHTML = char;
        parent.appendChild(g);
    }
    console.log(parent);
}

function getRandomColor() {
    var color = `rgb(${rand(256)}, ${rand(256)}, ${rand(256)})`
    return color;
  }

function rand(max = 256) {
    return Math.floor(Math.random()*max);
  }