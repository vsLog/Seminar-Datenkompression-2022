decodeInput = function() {
    var input = decodeFromBinary(String(document.getElementById("output_area").value));
    totalChars = sessionStorage.getItem("totalChars");
    charMap = new Map(JSON.parse(sessionStorage.getItem("charMap")));
    decodedInput = decode(input, totalChars, generateCharIntervals(totalChars, charMap));
    document.getElementById("input_area").value = decodedInput;
}

decodeFromBinary = function(input) {
	x = 0;
	decoded = input.slice(2)
	 for (var i = 1; i < decoded.length; i++) {
		 console.log(i, decoded[i])
		if (parseInt(decoded[i-1]) == 1) {
			x += 2**(-i)
		}
		console.log(x)
	}
	return x
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

decodeInputPrecise = function() {
    var input = document.getElementById("output_area").value;
    totalChars = sessionStorage.getItem("totalChars");
    charMap = new Map(JSON.parse(sessionStorage.getItem("charMap")));
    decodedInput = decodePrecice(input, totalChars, charMap);
    document.getElementById("input_area").value = decodedInput;
}

decodePrecice = function(input, totalChars, charMap) {
    var output = "";
    var charIntervals = generateCharIntervalsPrecice(charMap);
    var uint32Bounds = new Uint32Array([0, 0xFFFFFFFF, 0]);
    // 0 = lowerBound, 1 = upperBound, 2 = value
    const uint32IfConstans = new Uint32Array([0x80000000 , 0x40000000, 0xC0000000]);
    for (var i = 0 ; i < 32 ; i++) {
        uint32Bounds[2] <<= 1;
        uint32Bounds[2] += (input[0] >>> 0);
        input = input.substring(1);
    }
    for (var i = 0; i < totalChars; i++) {
        var intervalSize = uint32Bounds[1] - uint32Bounds[0] + 1;
        if ((((uint32Bounds[2] - uint32Bounds[0] + 1) * totalChars -1) / intervalSize) > totalChars) {
            console.log("ERROR, value of char to high");
        }
        var decodedChar = findCharPrecise((((uint32Bounds[2] - uint32Bounds[0] + 1) * totalChars - 1) / intervalSize), charIntervals);
        output = output.concat(decodedChar);
        uint32Bounds[1] = uint32Bounds[0] + (intervalSize * charIntervals.get(decodedChar)[1]) / totalChars - 1;
        uint32Bounds[0] = uint32Bounds[0] + (intervalSize * charIntervals.get(decodedChar)[0]) / totalChars; 
        while (true) {
            // Old not working Code:
            // if (uint32Bounds[0] >= uint32IfConstans[0] || uint32Bounds[1] < uint32IfConstans[0]) {
            //     uint32Bounds[0] <<= 1;
            //     uint32Bounds[1] <<= 1;
            //     uint32Bounds[1] |= 1;
            //     uint32Bounds[2] <<= 1;
            //     uint32Bounds[2] += (input[0] >>> 0);
            //     input = input.substring(1);
            //   } 
            // else if (uint32Bounds[0] >= uint32IfConstans[1] && uint32Bounds[1] < uint32IfConstans[2]) {
            //     uint32Bounds[0] <<= 1;
            //     uint32Bounds[0] &= 0x7FFFFFFF;
            //     uint32Bounds[1] <<= 1;
            //     uint32Bounds[1] |= 0x80000001;
            //     uint32Bounds[2] -= 0x4000000;
            //     uint32Bounds[2] <<= 1;
            //     uint32Bounds[2] += (input[0] >>> 0);
            //     input = input.substring(1);
            // } 
            // else { 
            //     break;
            // }
            if (uint32Bounds[1] < uint32IfConstans[0]) {
                // Do nothing
            }
            else if (uint32Bounds[0] >= uint32IfConstans[0]) {
                uint32Bounds[0] -= uint32IfConstans[0];
                uint32Bounds[1] -= uint32IfConstans[0];
                uint32Bounds[2] -= uint32IfConstans[0];
            } 
            else if (uint32Bounds[0] >= uint32IfConstans[1] && uint32Bounds[1] < uint32IfConstans[2]) {
                uint32Bounds[0] -= uint32IfConstans[1];
                uint32Bounds[1] -= uint32IfConstans[1];
                uint32Bounds[2] -= uint32IfConstans[1];
            } 
            else { 
                break;
            }
            uint32Bounds[0] <<= 1;
            uint32Bounds[1] <<= 1;
            uint32Bounds[1] |= 1;
            uint32Bounds[2] <<= 1;
            uint32Bounds[2] += (input[0] >>> 0);
            input = input.substring(1);         
        } 
    }
    return output;
}

findCharPrecise = function(inputValue, charIntervals) {
    lastChar = "Error";
    for ( let [key, value] of charIntervals) {
        if (inputValue < value[0]) {
            break;
        }
        lastChar = key;
    }
    if (lastChar == "Error") {
        console.log("Error findChar()");
    }
    return lastChar;
}