int: n_packages;
array[1..n_packages] of int: n_versions;

int: n_deps;
array[1..n_deps] of int: from_pkg;
array[1..n_deps] of int: from_ver;
array[1..n_deps] of int: to_pkg;
array[1..n_deps] of int: min_ver;
array[1..n_deps] of int: max_ver;

array[1..n_packages] of var 0..max(n_versions): selected;

constraint forall(i in 1..n_packages)(selected[i] <= n_versions[i]);
constraint selected[1] > 0;

constraint forall(d in 1..n_deps)(
    (selected[from_pkg[d]] = from_ver[d]) ->
        (selected[to_pkg[d]] >= min_ver[d] /\
         selected[to_pkg[d]] <= max_ver[d])
);

solve satisfy;

output [
    "Установленные версии (0 = не установлен):\n"
] ++ [
    "  пакет \(i): версия \(selected[i])\n"
    | i in 1..n_packages
];
