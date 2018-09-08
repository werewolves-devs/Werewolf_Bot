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

function unPack(token) {
    console.log("Unpacking...")
    showPart(2);
    setTimeout(function(){showPart(3)}, 15000);
    $(document).ready(function() {
        $.getJSON("/api/v1/" + token + "/rewards",function(results){
            console.log("This is the first result!")
            console.log(results);
            console.log(token)
            document.getElementById("link_1").href = ("/unbox/" + token + "/" + results.option1.code);
            document.getElementById("link_2").href = ("/unbox/" + token + "/" + results.option2.code);
            document.getElementById("link_3").href = ("/unbox/" + token + "/" + results.option3.code);
            document.getElementById("desc_1").innerHTML = results.option1.description;
            document.getElementById("desc_2").innerHTML = results.option2.description;
            document.getElementById("desc_3").innerHTML = results.option3.description;
            document.getElementById("title_1").innerHTML = results.option1.name;
            document.getElementById("title_2").innerHTML = results.option2.name;
            document.getElementById("title_3").innerHTML = results.option3.name;
            showRarity(results.option1.code,"rarity_1");
            showRarity(results.option2.code,"rarity_2");
            showRarity(results.option3.code,"rarity_3");
            console.log("Changed successfully!")
        });
    })
}

function showRarity(rarity_value,element) {
    if (rarity_value > 4000000-1) {
        document.getElementById(element).style.color = "#808000";
        document.getElementById(element).innerHTML = "LEGENDARY";
        return;
    }
    if (rarity_value > 3000000-1) {
        document.getElementById(element).style.color = "#ff00ff";
        document.getElementById(element).innerHTML = "EPIC";
        return;
    }
    if (rarity_value > 2000000-1) {
        document.getElementById(element).style.color = "#0080ff";
        document.getElementById(element).innerHTML = "RARE";
        return;
    }
    document.getElementById(element).innerHTML = "COMMON";
}