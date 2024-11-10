/**
 *  Scripts for all pages
 */

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

// Footer year
const y = new Date();
let year = y.getFullYear();
document.getElementById("year-footer").innerHTML = `Copyright &copy; ${year} DuoLegal. All Rights Reserved`;

// JavaScript to toggle lawyer-specific fields
function toggleLawyerFields() {
    var lawyerCheckbox = document.getElementById("lawyer-checkbox");
    var lawyerFields = document.getElementById("lawyer-fields");

    // Select the lawyer-specific input fields
    var licenseIdField = document.getElementById("license_id");
    var lawSchoolField = document.getElementById("law_school");
    var lawFirmField = document.getElementById("law_firm");

    if (lawyerCheckbox.checked) {
        lawyerFields.style.display = "block";
        let height = 0;
        const maxHeight = lawyerFields.scrollHeight;

        // Animate the expansion
        const expandInterval = setInterval(function() {
            if (height < maxHeight) {
                height += 5;
                lawyerFields.style.height = height + "px";
                lawyerFields.style.opacity = height / maxHeight;
            } else {
                clearInterval(expandInterval);
                lawyerFields.style.height = "auto";
            }
        }, 10);

        // Add 'required' attribute to each lawyer-specific field
        licenseIdField.setAttribute("required", "true");
        lawSchoolField.setAttribute("required", "true");
        lawFirmField.setAttribute("required", "true");

    } else {
        let height = lawyerFields.scrollHeight;

        const collapseInterval = setInterval(function() {
            if (height > 0) {
                height -= 5;
                lawyerFields.style.height = height + "px";
                lawyerFields.style.opacity = (height / lawyerFields.scrollHeight) / 10;
            } else {
                clearInterval(collapseInterval);
                lawyerFields.style.height = "0";
                lawyerFields.style.display = "none";
            }
        }, 10);

        // Remove 'required' attribute from each lawyer-specific field
        licenseIdField.removeAttribute("required");
        lawSchoolField.removeAttribute("required");
        lawFirmField.removeAttribute("required");
    }
}
