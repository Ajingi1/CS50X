
//start drop doown menu function
function dropDown(){
    let nav = document.getElementById("drop-down-nav");
    // let icon = document.getElementById('drop-down-icon');
    if (nav.className == 'nav-bar') {
        nav.className += ' responsive';
    } else {
        nav.className = 'nav-bar';
    }
}
// end of drop down function 