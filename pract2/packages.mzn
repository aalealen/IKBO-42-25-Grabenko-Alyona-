var {100,110,120,130,140,150}: menu;
var {180,200,210,220,230}: dropdown;
var {100,200}: icons;

constraint icons = 100;

constraint (menu >= 110) -> (dropdown >= 200);
constraint (menu = 100)  -> (dropdown = 180);

constraint (dropdown >= 200) -> (icons = 200);

solve satisfy;

output [
    "menu     = \(menu div 100).\((menu mod 100) div 10).\(menu mod 10)\n",
    "dropdown = \(dropdown div 100).\((dropdown mod 100) div 10).\(dropdown mod 10)\n",
    "icons    = \(icons div 100).\((icons mod 100) div 10).\(icons mod 10)\n"
];
