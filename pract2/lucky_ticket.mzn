include "alldifferent.mzn";

array[1..6] of var 0..9: digits;

constraint alldifferent(digits);

constraint digits[1] + digits[2] + digits[3] = digits[4] + digits[5] + digits[6];

var 0..27: sum3 = digits[1] + digits[2] + digits[3];

solve minimize sum3;

output [
    "Билет: \(digits[1])\(digits[2])\(digits[3])\(digits[4])\(digits[5])\(digits[6])\n",
    "Сумма первых трёх: \(sum3)\n",
    "Сумма последних трёх: \(digits[4] + digits[5] + digits[6])\n"
];
