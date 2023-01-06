decodeInput = function() {
    var input = Number(document.getElementById("output_area").value);
    totalChars = sessionStorage.getItem("totalChars");
    charMap = new Map(JSON.parse(sessionStorage.getItem("charMap")));
    decodedInput = decode(input, totalChars, generateCharIntervals(totalChars, charMap));
    document.getElementById("input_area").value = decodedInput;
}

decode = function(input, totalChars, charIntervals) {
    var output = "";
    var upperBound = 1.0;
    var lowerBound = 0.0;
    for (var i = 0; i < totalChars; i++) {
        var intervalSize = upperBound - lowerBound;
        var decodedChar = findChar(((input - lowerBound) / intervalSize), charIntervals);
        output = output.concat(decodedChar);
        upperBound = lowerBound + intervalSize * charIntervals.get(decodedChar)[1];
        lowerBound = lowerBound + intervalSize * charIntervals.get(decodedChar)[0]; 
    }
    return output;
}

findChar = function(inputValue, charIntervals) {
    lastChar = "Error"
    for ( let [key, value] of charIntervals) {
        if (inputValue < value[0]) {
            break;
        }
        lastChar = key;
    }
    return lastChar;
}

