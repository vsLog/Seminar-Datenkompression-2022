encodeInput = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
    document.getElementById("output_area").value = mapToString(charMap);
    createCharElement(charMap, totalChars);
    encodedInput = encode(input, totalChars, charMap);
    document.getElementById("output_area").value = encodedInput;
}

encode = function(input, totalChars, charMap) {
    var charIntervals = generateCharIntervals(totalChars, charMap);
    var upperBound = 1.0;
    var lowerBound = 0.0;
    for (var i = 0; i < input.length; i++) {
        var intervalSize = upperBound - lowerBound;
        upperBound = lowerBound + intervalSize * charIntervals.get(input[i])[1];
        lowerBound = lowerBound + intervalSize * charIntervals.get(input[i])[0]; 
    }
    return (lowerBound + (upperBound-lowerBound)/2);
}

generateCharIntervals = function(totalChars, charMap) {
    var lowerBound = 0.0;
    for ( let [key, value] of charMap) {
        var upperBound = (lowerBound + (value/totalChars));
        charMap.set(key, [lowerBound, upperBound]);
        lowerBound = upperBound;
    }
    return charMap;
}