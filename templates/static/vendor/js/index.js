var toggleStatus = 1;
var dropStatus = 1;
var dropDownStatus = 1;

function dropRight() {
    if (dropStatus == 1 && toggleStatus == 0) {
        document.getElementById("navbarDropleft").style.display = "block";
        dropStatus = 0;
    }
    else if (dropStatus == 0 && toggleStatus == 0) {
        document.getElementById("navbarDropleft").style.display = "none";
        dropStatus = 1;
    }
};

function toggleMenu() {
    if (toggleStatus == 1) {
        document.getElementById("menu").style.left = "0";
        document.getElementById("block-outside").style.display = "block";
        toggleStatus = 0;
    }
    else if (toggleStatus == 0) {
        document.getElementById("menu").style.left = "-500px";
        document.getElementById("block-outside").style.display = "none";
        document.getElementById("navbarDropleft").style.display = "none";
        dropStatus = 1;
        toggleStatus = 1;
    }
};

function dropDown() {
    if (dropDownStatus == 1) {
        document.getElementById("profileDropDown").style.display = "block"
        dropDownStatus = 0
    }

    else if (dropDownStatus == 0) {
        document.getElementById("profileDropDown").style.display = "none"
        dropDownStatus = 1
    }
}