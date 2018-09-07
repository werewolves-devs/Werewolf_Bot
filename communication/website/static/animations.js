function showPart(number) {
    var show_table = [
        document.getElementById("part1"),
        document.getElementById("part2"),
        document.getElementById("part3")
    ]

    show_table[0].style.display = "none";
    show_table[1].style.display = "none";
    show_table[2].style.display = "none";
    show_table[number-1].style.display = "block";
}

function unPack() {
    showPart(2);
    setTimeout(function(){showPart(3)}, 15000);
}