const fs = require('fs');

const moves = fs.readFileSync(process.argv[2], 'utf8').split("\n");

function TailVisitedSet() {
    this.data = new Set();

    this.add = function([first, second]) {
      this.data.add(`${first},${second}`);
    };
}

const tailVisited = new TailVisitedSet();

var nPts = 10;
var nPtsm1 = nPts-1;
let pts = []

for (var i = 0; i < nPts; i++) {
    pts.push([0,0]);
}
tailVisited.add([0, 0]);

function logState() {
    let nY = Math.max(...pts.map(pt => pt[1]))+1;
    let nX = Math.max(...pts.map(pt => pt[0]))+1;

    for(var j = nY-1; j >= 0; j--) {
        var line = "";
        for(var i = 0; i < nX; i++) {
            let ptI = pts.findIndex(pt => pt[0] == i && pt[1] == j);
            //console.log(`ptI: ${ptI} ${i} ${j} ${pts}`);
            if (ptI >= 0) {
                let pt = pts[ptI];
                if (pt == pts[0]) {
                    line += "H";
                } else if(pt == pts[nPtsm1]) {
                    line += "T";
                } else {
                    line += ptI;
                }
            } else {
                line += ".";
            }
        }
        console.log(line);
    }
}

const moveDebug = false;
function resolveMove(head, tail) {
    let hX = head[0];
    let hY = head[1];
    let tX = tail[0];
    let tY = tail[1];
    let dX = hX-tX;
    let dY = hY-tY;
    let absDx = Math.abs(dX);
    let absDy = Math.abs(dY);
    let sumAbs = absDx + absDy;
    if (moveDebug) console.log(`dX: ${dX}, dY: ${dY}`);
    if (sumAbs <= 1) {
        if (moveDebug) console.log("directly adjacent");
    } else if (absDx == 1 && absDy == 1) {
        if (moveDebug) console.log("catty-corner adjacent");
    } else if (sumAbs == 2 || sumAbs == 3 || sumAbs == 4) {

        if(dX > 0) {
            if (moveDebug) console.log("move tail right");
            tX++;
        } else if(dX < 0) {
            if (moveDebug) console.log("move tail left");
            tX--;
        }

        if (dY < 0) {
            if (moveDebug) console.log("move tail down");
            tY--;
        } else if (dY > 0) {
            if (moveDebug) console.log("move tail up");
            tY++;
        }
    } else {
        console.log(`ERROR: sumAbs: ${sumAbs}, dX: ${dX}, dY: ${dY}`);
        process.exit(1);
    }

    return [tX, tY];
}

function resolveAllMoves() {
    for(var k = 0; k < nPtsm1; k++) {
        let kp1 = k+1;
        pts[kp1] = resolveMove(pts[k], pts[kp1]);

        if(kp1 == nPtsm1) {
            tailVisited.add(pts[nPtsm1]);
        }
    }
    logState();
}

var j = 0;
logState();
moves.forEach(function(move){
    console.log(`Starting: '${move}' ${j}`);
    var moveSplit = move.split(" ")
    var direction = moveSplit[0];
    var distance = parseInt(moveSplit[1]);
    for (var i = 0; i < distance; i++) {
        console.log(`Move Part: ${i}`);
        if (direction == "R") {
            pts[0][0]++;
        } else if (direction == "L") {
            pts[0][0]--;
        } else if (direction == "U") {
            pts[0][1]++;
        } else if (direction == "D") {
            pts[0][1]--;
        } else {
            console.log("ERROR: Unknown move type");
            process.exit(1);
        }
        resolveAllMoves();
    }
    j++;
})
console.log(tailVisited.data.size);