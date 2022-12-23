import * as fs from 'fs';

let rows = fs.readFileSync("day13.txt", 'utf8').split("\n");

function* parseRowPairs(rows: string[]) {
    for (let i = 0; i < rows.length; i+=3) {
        console.log("Parsing:\n" + rows[i] + "\n" + rows[i + 1]);
        yield [JSON.parse(rows[i]), JSON.parse(rows[i + 1])];
    }
}

function* parseRow(rows: string[]) {
    for (let i = 0; i < rows.length; i+=3) {
        yield JSON.parse(rows[i])
        yield JSON.parse(rows[i + 1]);
    }
}

function comparePair(left, right) {
    console.log("\t " + typeof left + " " + typeof right );
    if (typeof left === 'number' && typeof right === 'number') {
        if (left === right) {
            return 0;
        } else if (left < right) {
            return -1;
        } else {
            return 1;
        }
    } else if (typeof left !== 'number' && typeof right !== 'number') {
        for (let i = 0; i < Math.min(left.length, right.length); i++) {
            let result = comparePair(left[i], right[i]);
            if (result !== 0) {
                return result;
            }
        }
        if (left.length < right.length) {
            return -1;
        } else if (left.length > right.length) {
            return 1;
        } else {
            return 0;
        }
    } else if (typeof left !== 'number' && typeof right === 'number') {
        return comparePair(left, [right]);
    } else if (typeof left === 'number' && typeof right !== 'number') {
        return comparePair([left], right);
    }
    throw new Error("Invalid types");
}

let result = 0;
let i = 1;
for(let pair of parseRowPairs(rows)) {
    let p1 = pair[0];
    let p2 = pair[1];

    if(comparePair(p1, p2) < 0) {
        result += i;
    }
    i++;
}
console.log("Part1: " + result);

let rowsJsonParsed = [...parseRow(rows)];
rowsJsonParsed.sort(comparePair)

var i1 = -1;
var i2 = -1;

for (let i = 0; i < rowsJsonParsed.length; i++) {
    if (i1 === -1 && comparePair(rowsJsonParsed[i], [[2]] ) > 0) {
        i1 = i + 1;
    } else if (i1 !== -1 && comparePair(rowsJsonParsed[i], [[6]] ) > 0) {
        i2 = i + 2;
        break;
    }
}

console.log("Part2: " + i1 + " " + i2 + " " + (i1 * i2));