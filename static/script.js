// Scroll progress bar (top)
window.onscroll = function () {
    buttonFunction();
    myFunction();
};

function myFunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}

// Back to top button
var btn = document.getElementById("button");

function buttonFunction() {
    var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;

    if (scrollTop > 100 && scrollHeight - clientHeight - scrollTop > 50) {
        btn.classList.add('show');
    } else {
        btn.classList.remove('show');
    }
}

btn.addEventListener('click', function (e) {
    e.preventDefault();
    $('html, body').animate({
        scrollTop: 0
    }, 10);
});

window.addEventListener('scroll', buttonFunction);
