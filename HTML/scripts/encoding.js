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
 by Mark Nelson's article:
 Data Compression With Arithmetic Coding
 published at: http://marknelson.us/2014/10/19/data-compression-with-arithmetic-coding
 new link: https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html
 (working 17th January 2023)

*/


/**
 * Encodes the input of the textfield "input_area" to a number between 0 and 1.
 * Uses a naive algorithm ignoring the limited precision of number in the computer.
 * Stores the data in the sessionStorage.
 */
encodeInput = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
    createCharElement(charMap, totalChars);
    let encodedInput = encode(input, totalChars, charMap);
    document.getElementById("output_area").value = encodedInput;
}

/**
 * Encodes the input to a number between 0 and 1 using the relative occurences of each char.
 * @param {string} input - input String
 * @param {number} totalChars - total number of chars
 * @param {Map} charMap - Character occurrence map
 * @returns {number} encoded Message - number between 0 and 1
 */
encode = function(input, totalChars, charMap) {
    // calculate the intervals each char gets between 0 and 1
    var charIntervals = generateCharIntervals(totalChars, charMap);
    var upperBound = 1.0;
    var lowerBound = 0.0;
    // resize the interval in which the output will be contained to fit the charMap
    // if for example the letter 'a' has the intervall 0.25 to 0.75 then each time
    // 'a' comes up in the input the upper and lower Bound of the output will be 
    // recalculated so that it only contains the middle 50% between the old Bounds
    // [0, 1) becomes [0.25, 0.75) or [0.2, 0.6) becomes [0.3, 0.5)
    for (var i = 0; i < input.length; i++) {
        var intervalSize = upperBound - lowerBound;
        upperBound = lowerBound + intervalSize * charIntervals.get(input[i])[1];
        lowerBound = lowerBound + intervalSize * charIntervals.get(input[i])[0]; 
    }
    return (lowerBound + (upperBound-lowerBound)/2);
}

/**
 * Calculate the intervals each char has between 0 and 1 if their size corresponds
 * to their relative occurence probability.
 * @param {number} totalChars - total number of chars
 * @param {Map} charMap - Character occurrence map
 * @returns {Map} charMap - each char has its own [lowerBound, upperBound] interval
 */
generateCharIntervals = function(totalChars, charMap) {
    var lowerBound = 0.0;
    // starting from 0 the interval from 0 to 1 is split between the chars
    for ( let [key, value] of charMap) {
        var upperBound = (lowerBound + (value/totalChars));
        charMap.set(key, [lowerBound, upperBound]);
        lowerBound = upperBound;
    }
    return charMap;
}

/**
 * Encodes the input of the textfield "input_area" to a number between 0 and 1.
 * Uses Mark Nelson's c++ algorithm modified to fit our needs and javascript.
 * Stores the data in the sessionStorage.
 */
encodeInputPrecise = function() {
    var input = document.getElementById("input_area").value;
    var totalChars = input.length;
    var charMap = countChars(input);
    sessionStorage.setItem("totalChars", totalChars);
    sessionStorage.setItem("charMap", JSON.stringify(Array.from(charMap.entries())));
    document.getElementById("output_area").value = "";
    createCharElement(charMap, totalChars);
    let output = encodePrecice(input, totalChars, charMap);
    // Bootstrap 3.4.1 css leads to crashes when trying to copy large strings composed of only 0 and 1 (around 1 million chars)
    // Works in Bootstrap 4.6.2 css and 5.2.3 css
    document.getElementById("output_area").value = output;
    document.getElementById("inputSize").innerHTML =    "Eingabe Zeichen Länge ".concat(input.length);
    document.getElementById("inputBit").innerHTML =     "Eingabe Bit     Länge ".concat(input.length*8);
    document.getElementById("outputSize").innerHTML =   "Ausgabe Zeichen Länge ".concat(output.length);
    document.getElementById("outputBit").innerHTML =    "Ausgabe Bit     Länge".concat(output.length);
    document.getElementById("savedBit").innerHTML =     "Prozentualer Unterschied ".concat(Math.round((output.length-input.length*8)/(input.length*8)*100)).concat("%");
}

/**
 * Encodes the input to a binary number using the relative occurences of each char.
 * Uses Mark Nelson's c++ algorithm modified to fit our needs and javascript.
 * For a deeper insight into the how and why see his article:
 * https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html
 * @param {string} input - input String
 * @param {number} totalChars - total number of chars
 * @param {Map} charMap - Character occurrence map
 * @returns {number} output - binary number
 */
encodePrecice = function(input, totalChars, charMap) {
    /**
     * Output the pending bits.
     * Uses Mark Nelson's c++ algorithm modified to fit our needs and javascript.
     * For a deeper insight into the how and why see his article:
     * https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html
     * @param {boolean} bit - output bit
     * @param {number} pending_bits - number of pending bits
     */
    output_bit_plus_pending = function(bit, pending_bits) {
        output_bit(bit);
        while (pending_bits--) {
            output_bit(!bit);
        }    
    }

    /**
     * Output the bit to the "output_area".
     * @param {boolean} bit - output bit
     */
    output_bit = function(bit) {
        //document.getElementById("output_area").value += bit*1; // leads to heavy workload on larger inputs
        output = output.concat(bit*1);
    }

    let output = "";
    var charIntervals = generateCharIntervalsPrecice(charMap);
    // creates Arrays containing 32Bit numbers to recreate c++ int
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

    return output;
}

/**
 * Calculate the bounds of each char to be used by "encodePrecice".
 * @param {Map} charMap - Character occurrence map
 * @returns {Map} charMap - each char has its own [lowerBound, upperBound]
 */
generateCharIntervalsPrecice = function(charMap) {
    var lowerBound = 0;
    for ( let [key, value] of charMap) {
        var upperBound = lowerBound + value;
        charMap.set(key, [lowerBound, upperBound]);
        lowerBound = upperBound;
    }
    return charMap;
}

/**
 * Converts a decimal to a binary number. Return is a string!
 * @param {number} decimal - decimal number
 * @returns {string} binary number as string
 */
decimalToBinary = function(decimal) {
    return (decimal >>> 0).toString(2);
}