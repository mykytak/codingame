/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

var boosts = 1;

// game loop
while (true) {
    var inputs = readline().split(' ');
    var x = parseInt(inputs[0]);
    var y = parseInt(inputs[1]);
    var ncX = parseInt(inputs[2]); // x position of the next check point
    var ncY = parseInt(inputs[3]); // y position of the next check point
    var ncDist = parseInt(inputs[4]); // distance to the next checkpoint
    var ncAngle = parseInt(inputs[5]); // angle between your pod orientation and the direction of the next checkpoint
    var inputs = readline().split(' ');
    var opponentX = parseInt(inputs[0]);
    var opponentY = parseInt(inputs[1]);

    // Write an action using print()
    // To debug: printErr('Debug messages...');
    
    var xt = ncX,
        yt = ncY,
        thrust = 100;

    var absAngle = Math.abs(ncAngle);

    thrust = ncDist > 1000 && (boosts-- > 0) ? 'BOOST'
           : (absAngle > 140 || ncDist < 500  ? 5
           : (absAngle > 110 || ncDist < 800  ? 25
           : (                  ncDist < 1200 ? 60
           : (absAngle > 80  || ncDist < 1500 ? 80
           :  100
           ))));

    // You have to output the target position
    // followed by the power (0 <= thrust <= 100)
    // i.e.: "x y thrust"
    print(xt + ' ' + yt + ' ' + thrust);
}
