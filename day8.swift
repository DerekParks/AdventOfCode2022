import CoreData

let input = try String(contentsOfFile: "day8_test.txt", encoding: .utf8)

let inputArr: [[Int]] = input.split(whereSeparator: \.isNewline).map { line in
    return line.map { $0.wholeNumberValue! }
}

let nI = inputArr.count
let nJ = inputArr[0].count

var visible = 2 * (nI + nJ) - 4

print(inputArr)
print(nI, nJ)

var visibleArr = Array(repeating: Array(repeating: false, count: nJ), count: nI)

for ij in 0...(nI-1) {
    visibleArr[ij][0] = true
    visibleArr[ij][nJ-1] = true
    visibleArr[0][ij] = true
    visibleArr[nI-1][ij] = true
}

func update(i:Int, j: Int, maxPrev:Int) -> Int {
    if !visibleArr[i][j] && inputArr[i][j] > maxPrev {
        visibleArr[i][j] = true
        visible += 1
    }
    return max(maxPrev, inputArr[i][j])
}

for i in 1...(nI-2) {
    var maxPrev = inputArr[i][0]
    for j in 1...(nJ-2) {
        maxPrev = update(i:i, j:j, maxPrev:maxPrev)
    }

    maxPrev = inputArr[i][nJ-1]
    for j in (1...(nJ-1)).reversed() {
        maxPrev = update(i:i, j:j, maxPrev:maxPrev)
    }
}

for j in 1...(nJ-2) {
    var maxPrev = inputArr[0][j]
    for i in 1...(nI-2) {
        maxPrev = update(i:i, j:j, maxPrev:maxPrev)
    }

    maxPrev = inputArr[nI-1][j]
    for i in (1...(nI-2)).reversed() {
        maxPrev = update(i:i, j:j, maxPrev:maxPrev)
    }
}

print("part 1: \(visible)")

func visibleCount(i:Int, j: Int) -> Int {
    let thisTree = inputArr[i][j]
    var result = 1
    var count = 0
    for j in (j+1...(nJ-1)) {
        count += 1
        if inputArr[i][j] >= thisTree {
            break
        }
    }
    result *= count
    count = 0
    for j in (0...(j-1)).reversed() {
        count += 1
        if inputArr[i][j] >= thisTree {
            break
        }
    }
    result *= count
    count = 0
    for i in (0...(i-1)).reversed() {
        count += 1
        if inputArr[i][j] >= thisTree {
            break
        }
    }
    result *= count
    count = 0
    for i in (i+1...(nI-1)) {
        count += 1
        if inputArr[i][j] >= thisTree {
            break
        }
    }
    result *= count
    return result
}


let maxFound2 = (1..<(nI-1)).map { i in (1..<(nJ-1)).map { j in visibleCount(i:i, j:j) }.max()! }.max()!
print("part 2: \(maxFound2)")