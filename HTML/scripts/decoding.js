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
 new link: https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html
 (working 17th January 2023)

*/

/**
 * Decodes the input of the textfield "output_area" to the (hopefully) original text.
 * Uses a naive algorithm ignoring the limited precision of number in the computer.
 * Loads the char data from the sessionStorage.
 */
decodeInput = function() {
    var input = Number(document.getElementById("output_area").value);
    totalChars = sessionStorage.getItem("totalChars");
    charMap = new Map(JSON.parse(sessionStorage.getItem("charMap")));
    let decodedInput = decode(input, totalChars, generateCharIntervals(totalChars, charMap));
    document.getElementById("input_area").value = decodedInput;
}

/**
 * Decodes the input to a text using the relative occurences of each char.
 * @param {number} input - input number between 0 and 1
 * @param {number} totalChars - total number of chars
 * @param {Map} charIntervals - Character interval map
 * @returns {number} decoded Message
 */
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

/**
 * Findes in which char interval the inputValue falls and returns the corresponding char.
 * @param {number} inputValue - input number between 0 and 1
 * @param {Map} charIntervals - Character interval map
 * @returns {string} decoded char (returns "Error" if an error occures)
 */
findChar = function(inputValue, charIntervals) {
    let lastChar = "Error"
    for ( let [key, value] of charIntervals) {
        if (inputValue < value[0]) {
            break;
        }
        lastChar = key;
    }
    return lastChar;
}

/**
 * Decodes the input of the textfield "output_area" to the (hopefully) original text.
 * Uses Mark Nelson's c++ algorithm modified to fit our needs and javascript.
 * Loads the char data from the sessionStorage.
 */
decodeInputPrecise = function() {
    var input = document.getElementById("output_area").value;
    totalChars = sessionStorage.getItem("totalChars");
    charMap = new Map(JSON.parse(sessionStorage.getItem("charMap")));
    let decodedInput = decodePrecice(input, totalChars, charMap);
    document.getElementById("input_area").value = decodedInput;
}

/**
 * Decodes the input from a binary number using the relative occurences of each char.
 * Uses Mark Nelson's c++ algorithm modified to fit our needs and javascript.
 * For a deeper insight into the how and why see his article:
 * https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html
 * @param {string} input - binary number
 * @param {number} totalChars - total number of chars
 * @param {Map} charMap - Character occurrence map
* @returns {string} output - decoded message
 */
decodePrecice = function(input, totalChars, charMap) {
    var output = "";
    var charIntervals = generateCharIntervalsPrecice(charMap);
    var uint32Bounds = new Uint32Array([0, 0xFFFFFFFF, 0]);
    // 0 = lowerBound, 1 = upperBound, 2 = value
    const uint32IfConstans = new Uint32Array([0x80000000 , 0x40000000, 0xC0000000]);
    // load the first 32 bit of the input string into the 32bit int array
    for (var i = 0 ; i < 32 ; i++) {
        uint32Bounds[2] <<= 1;
        uint32Bounds[2] += (input[0] >>> 0);
        input = input.substring(1);
    }
    for (var i = 0; i < totalChars; i++) {
        var intervalSize = uint32Bounds[1] - uint32Bounds[0] + 1;
        // if ((((uint32Bounds[2] - uint32Bounds[0] + 1) * totalChars -1) / intervalSize) > totalChars) {
        //     console.log("ERROR, value of char to high");
        // }
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


/**
 * Findes in which char interval the inputValue falls and returns the corresponding char.
 * @param {number} inputValue - input number between 0 and 1
 * @param {Map} charIntervals - Character interval map
 * @returns {string} decoded char (returns "Error" if an error occures)
 */
findCharPrecise = function(inputValue, charIntervals) {
    let lastChar = "Error";
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