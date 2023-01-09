encodeInput = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
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

encodeInputPrecise = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
    document.getElementById("output_area").value = "0b";
    createCharElement(charMap, totalChars);
    encodePrecice(input, totalChars, charMap);
    document.getElementById("output_area").innerHTML += "n";
}

encodePrecice = function(input, totalChars, charMap) {
    var charIntervals = generateCharIntervalsPrecice(charMap);
    var uint32Bounds = new Uint32Array([0, 0xFFFFFFFF]);
    const uint32IfConstans = new Uint32Array([0x80000000, 0x40000000, 0xC0000000]);
    var pending_bits = 0;
    for (var i = 0; i < input.length; i++) {
        var intervalSize = uint32Bounds[1] - uint32Bounds[0] + 1;
        uint32Bounds[1]  = uint32Bounds[0] + (intervalSize * charIntervals.get(input[i])[1]) / totalChars - 1;
        uint32Bounds[0] = uint32Bounds[0] + (intervalSize * charIntervals.get(input[i])[0]) / totalChars; 
        while (true) {
            if (uint32Bounds[1] < (uint32IfConstans[0])) {
                output_bit_plus_pending(0, pending_bits);
                pending_bits = 0;
                uint32Bounds[0] <<= 1;
                uint32Bounds[1] <<= 1;
                uint32Bounds[1] |= 1;
            } 
            else if (uint32Bounds[0] >= (uint32IfConstans[0])) {
                output_bit_plus_pending(1, pending_bits);
                pending_bits = 0;
                uint32Bounds[0] <<= 1;
                uint32Bounds[1] <<= 1;
                uint32Bounds[1] |= 1;
            } 
            else if (uint32Bounds[0] >= (uint32IfConstans[1]) && uint32Bounds[1] < (uint32IfConstans[0])) {
                pending_bits++;
                uint32Bounds[0] <<= 1;
                uint32Bounds[0] &= 0x7FFFFFFF;
                uint32Bounds[1] <<= 1;
                uint32Bounds[1] |= 0x80000001;
            }
            else { 
                break;
            }   
        } 
    }
}

output_bit_plus_pending = function(bit, pending_bits) {
    output_bit(bit);
    while (pending_bits--) {
        output_bit(!bit);
    }    
}

output_bit = function(bit) {
    document.getElementById("output_area").value += bit*1;
}

generateCharIntervalsPrecice = function(charMap) {
    var lowerBound = 0;
    for ( let [key, value] of charMap) {
        var upperBound = lowerBound + value;
        charMap.set(key, [lowerBound, upperBound]);
        lowerBound = upperBound;
    }
    return charMap;
}

decimalToBinary = function(decimal) {
    return (decimal >>> 0).toString(2);
}