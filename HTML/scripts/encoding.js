/*
The MIT License (MIT)

Copyright (c) 2014 Mark Thomas Nelson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

 This code was written by Mario Navarro Krauß and Vito Schopper to illustrate
 and visualize the arithmetic coding algorithm used for Data Compression.
 The encoding and decoding scripts use parts of the algorithm descriped 
 by Mark Nelson' article:
 Data Compression With Arithmetic Coding
 published at: http://marknelson.us/2014/10/19/data-compression-with-arithmetic-coding

*/

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
    document.getElementById("output_area").value = "";
    createCharElement(charMap, totalChars);
    encodePrecice(input, totalChars, charMap);
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
            else if (uint32Bounds[0] >= (uint32IfConstans[1]) && uint32Bounds[1] < (uint32IfConstans[2])) {
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
    pending_bits++;
    if (uint32Bounds[0] < uint32IfConstans[1]) {
        output_bit_plus_pending(0, pending_bits);
    }
    else {
        output_bit_plus_pending(1, pending_bits);
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