/**
 * Send your busters out into the fog to trap ghosts and bring them home!
 **/

var bustersPerPlayer = parseInt(readline()); // the amount of busters you control
var ghostCount = parseInt(readline()); // the amount of ghosts on the map
var myTeamId = parseInt(readline()); // if this is 0, your base is on the top left of the map, if it is one, on the bottom right

var debug = false;

var base = {
    x: myTeamId ? 16000 : 0,
    y: myTeamId ? 9000  : 0
};

function nearBase(buster) {
    let near = 1000;
    return myTeamId ? buster.x + near >= base.x && buster.y + near >= base.y
                    : buster.x <= near && buster.y <=near 
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function debug(obj) {
    printErr(JSON.stringify(obj));
}

function vLen(obj, f1, f2) {
    f1 = f1 || 'dx';
    f2 = f2 || 'dy';
    return Math.sqrt(obj[f1]*obj[f1] + obj[f2]*obj[f2]);
}

function clone(obj) {
    return JSON.parse( JSON.stringify(obj) );
}

function dist(obj1, obj2) {
    let nobj = clone(obj2);
    nobj.dx = obj2.x - obj1.x;
    nobj.dy = obj2.y - obj1.y;
    return nobj;
}

function Container(name)
{
    var items = [];

    this.debug = (obj) => {
                    printErr(name, JSON.stringify(obj));
                }

    this.find =
        (id) => {
            for(var i in items) {
                if (items[i].id == id) return items[i];
            }

            return null;
        };

    this.update =
        (id, obj) => {
            for(var i in items) {
                if (items[i].id != id) continue;

                for (var attr in obj) { items[i][attr] = obj[attr]; }
                return true;
            }

            items.push(obj);
            return false;
        };

    return {
      update: (id, obj) => { this.update(id, obj); }
    , get: (id)  => this.find(id) 
    , map: (callback) => { return items.map(callback); }
    , closest: (buster) => {
                    if (items.length == 0) return null;

                    let res = items
                                .map((obj) => dist(buster, obj))
                                .sort((a, b) => {
                                    let la = vLen(a), lb = vLen(b);

                                    if (a.type != -1) return la < lb ? -1 : 1;

                                    let inRange = Math.abs(la - lb) <= 1000;

                                    return inRange ? (a.state < b.state ? -1 : 1)
                                                   : (la < lb ? -1 : 1);
                                });

                    let obj = res.shift(),
                        len = vLen(obj);

                    if (len > 2500) return null; //too far

                    obj.inRange = len <= 1740;
                    obj.tooClose = len <= 900;

                    return obj;
                }
    , clear: () => { items = []; }
    , closestFight: (buster) => {
                    var fighters = [];

                    for(var i in items) {
                        if (items[i].id != buster.id && items[i].state == 3) {
                            fighters.push( items[i].target );
                        }
                    }

                    if (!fighters.length) return null;

                    return fighters
                             .map((obj) => dist(buster, obj))
                             .sort((a, b) => vLen(a) < vLen(b) ? -1 : 1)
                             .shift();
                }
    }
}

var data = {
      busters: new Container('busters')
    , ghosts:  new Container('ghosts')
    , enemies: new Container('enemies')
    }

var ticks = ghostCount < 8 + 7  ? 7
         : (ghostCount < 8 + 15 ? 10
                                : 12
            );

function input(callback) {

    data.ghosts.clear();
    data.enemies.clear();
    ticks++;

    var entities = parseInt(readline()); // the number of busters and ghosts visible to you
    for (var i = 0; i < entities; i++) {
        var inputs = readline().split(' ');

        let obj  = {};
        obj.id   = parseInt(inputs[0], 10); // buster id or ghost id
        obj.x    = parseInt(inputs[1], 10);
        obj.y    = parseInt(inputs[2], 10);
        obj.type = parseInt(inputs[3], 10); // the team id if it is a buster, -1 if it is a ghost.

        obj.state = parseInt(inputs[4], 10); // For busters: 0=idle, 1=carrying a ghost.
        obj.value = parseInt(inputs[5], 10); // For busters: Ghost id being carried.
                                             // For ghosts: number of busters attempting to trap this ghost.

        let container = obj.type == !myTeamId ? 'enemies'
                      :(obj.type == myTeamId  ? 'busters'
                      :                         'ghosts' );

        if (container == 'ghosts' && obj.state > ticks) { continue; }

        if (container == 'busters') {
            var saved = data['busters'].get(obj.id);
            obj.stun = saved && saved.stun ? saved.stun - 1 : 0;
            obj.move = saved && saved.move ? saved.move - 1 : 0;
        }

        data[container].update(obj.id, obj);
    }

    callback();
}

function output() {
    // var points = [ '8000 2000' 
    //              , '14000 2000'
    //              , '2000 4500'
    //              , '8000 4500'
    //              , '14000 4500'
    //              , '2000 7000'
    //              , '8000 7000'
    //              , myTeamId ? '0 0' : '14000 7000'
    //              ];

    var points = myTeamId
               ? [ '15000 1000'
                 , '1000 8000'
                 , '2500 3000'
                 , '5000 1500'
                 , '10000 6000'
                 ]
               : [ '15000 1000'
                 , '1000 8000'
                 , '13500 6000'
                 , '10000 4500'
                 , '5000 3000'
                 ];

    // var points = [ '16000 0'
    //              , '8000 3000'
    //              , '0 9000'
    //              , myTeamId ? '0 0' : '16000 9000'
    //              ];


    data.busters.map((buster) => {
        if (buster.state == 2) {
            debug && printErr(buster.id, 'stunned');
            buster.action = 'MOVE ' + buster.x + ' ' + buster.y;
            buster.move = 0;
            return buster; //if buster stanned, do nothing.
        }

        if (buster.state == 1) {
            debug && printErr(buster.id, 'carry');
            // let near = nearBase(buster);

            buster.action = nearBase(buster) ? 'RELEASE' : 'MOVE ' + base.x + ' ' + base.y;
            buster.move = 0;
            return buster;
        }

        return ((printRes) => {
                    let ins = {
                        enemy: data.enemies.closest(buster)
                    ,   ghost: data.ghosts.closest(buster)
                    };

                    return printRes(ins);
                })((inp) => {
                    let enemy = inp.enemy,
                        ghost = inp.ghost;

                    if (enemy) {
                        if (enemy.inRange && enemy.state != 2 && !buster.stun) {
                            debug && printErr(buster.id, 'shot');
                            buster.action = 'STUN ' + enemy.id;
                            buster.stun = 20;
                            buster.move = 0;
                            return buster;
                        }
                        
                        // if (!ghost && !buster.stun) {
                        //     printErr(buster.id, 'want stun', enemy.id);
                        //     buster.action = 'MOVE ' + enemy.x + ' ' + enemy.y;
                        //     return buster;
                        // }
                    }

                    if (ghost) {
                        debug && printErr(buster.id, 'ghost detected', ghost.id);

                        let closest = data.busters.closestFight(buster);
                        if (closest && vLen(closest) < 1600 && closest.value <= ghost.value) {
                            buster.action = 'MOVE ' + closest.x + ' ' + closest.y;
                        }

                        if      (ghost.inRange)  { buster.action = 'BUST ' + ghost.id; buster.target = ghost; }
                        else if (ghost.tooClose) buster.action = 'MOVE ' + (ghost.x - 200) + ' '+ ghost.y;
                        else                     buster.action = 'MOVE ' + ghost.x + ' ' + ghost.y;
                        buster.move = 0;
                        return buster;
                    }

                    if (buster.move && buster.point != buster.x + ' ' + buster.y) {
                        debug && printErr(buster.id, 'wandering to ', buster.point);
                        return buster;
                    }

                    debug && printErr(buster.id, 'just wandering around');

                    let closest = data.busters.closestFight(buster);

                    if (closest) {
                        buster.action = 'MOVE ' + closest.x + ' ' + closest.y;
                        buster.move = 3;
                        return buster;
                    }

                    let randI = getRandomInt(0, points.length - 1);
                    buster.action = 'MOVE ' + points[randI];
                    buster.point = points[randI];
                    buster.move = 7;

                    points.splice(randI, 1);

                    return buster;
                });
    }).sort((a, b) => a.id < b.id ? -1 : 1)
      .map((buster) => print(buster.action));

}

// game loop
while (true) {
    input(output);
}
