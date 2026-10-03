var {0,100,110}: foo;
var {0,100,200}: target;
var {0,100}: left;
var {0,100}: right;
var {0,100,200}: shared;

constraint foo >= 100;
constraint target = 200;

constraint (foo = 110) -> (left = 100 /\ right = 100);
constraint (left = 100) -> (shared >= 100);
constraint (right = 100) -> (shared < 200);
constraint (shared = 100) -> (target < 200);

solve satisfy;

output [
    "foo    = \(foo)\n",
    "target = \(target)\n",
    "left   = \(left)\n",
    "right  = \(right)\n",
    "shared = \(shared)\n"
];
