/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

var boosts = 1;

// game loop
while (true) {
    var me = {},
        p  = {},
        bwn = {};
    
    var inputs = readline().split(' ');
    me.x = parseInt(inputs[0]);
    me.y = parseInt(inputs[1]);
    p.x = parseInt(inputs[2]); // x position of the next check point
    p.y = parseInt(inputs[3]); // y position of the next check point
    bwn.dist = parseInt(inputs[4]); // distance to the next checkpoint
    me.angle = parseInt(inputs[5]); // angle between your pod orientation and the direction of the next checkpoint
    
    var inputs = readline().split(' ');
    var opponentX = parseInt(inputs[0]);
    var opponentY = parseInt(inputs[1]);

    // Write an action using print()
    // To debug: printErr('Debug messages...');
    
    bwn.x = me.x - p.x;
    bwn.y = me.y - p.y;
    bwn.nx = bwn.x/bwn.dist;
    bwn.ny = bwn.y/bwn.dist;
    
    var len = (v) => Math.sqrt(v.x*v.x + v.y*v.y);
    
    p.len = len(p);
    p.nx = p.x/p.len;
    p.ny = p.y/p.len;
    
    //p.nx = p.tx * Math.cos(me.angle) - p.ty * Math.sin(me.angle);
    //p.ny = p.ty * Math.sin(me.angle) + p.ty * Math.cos(me.angle);
    
//rotated_point.x = point.x * cos(angle) - point.y * sin(angle);
//rotated_point.y = point.x * sin(angle) + point.y * cos(angle);
    
    p.mx = 1 || p.x > me.x ? 1 : -1;
    p.my = 1 || p.y > me.y ? 1 : -1;
    
    var angle = Math.acos(bwn.nx*p.nx + bwn.ny*p.ny);
    
    var dx = 400 * Math.cos(angle) - 400 * Math.sin(angle),
        dy = 400 * Math.sin(angle) + 400 * Math.cos(angle);
    
    printErr(dx*p.mx, dy*p.my, me.angle);
    
    var xt = p.x + p.mx * (dx ? dx : 0),
        yt = p.y + p.my * (dy ? dy : 0),
        thrust = 100;

    var absAngle = Math.abs(me.angle);

    thrust = bwn.dist > 1000 && (boosts-- > 0)  ? 'BOOST'
           : (absAngle > 140 || bwn.dist < 800  ? 5
           : (absAngle > 110 || bwn.dist < 1200 ? 25
           : (                  bwn.dist < 1500 ? 60
           : (absAngle > 80  || bwn.dist < 3000 ? 80
           :  100
           ))));

    // You have to output the target position
    // followed by the power (0 <= thrust <= 100)
    // i.e.: "x y thrust"
    print(parseInt(xt) + ' ' + parseInt(yt) + ' ' + thrust);
}
