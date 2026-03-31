const demoUser = {
    username: "admin",
    password: "1234"
};

function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    if(user === demoUser.username && pass === demoUser.password) {
        alert("Login successful");
        window.location.href = "student.html";
    } else {
        alert("User not found");
    }
}