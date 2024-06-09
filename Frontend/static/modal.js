// modal.js
document.addEventListener("DOMContentLoaded", function() {
    // Get the modal
    var modal = document.getElementById("myModal");

    // Display the modal if it should be shown
    var show_modal = document.getElementById("show_modal").value;
    if (show_modal === "True") {
        modal.style.display = "block";
    }

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

document.getElementById('login').addEventListener('click', function() {
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;
    if (user) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'student_name': user ,'student_password': password})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter the number of iterations');
    }
});

document.getElementById('create_student').addEventListener('click', function() {
    if (user) {
        fetch('/create_student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'type': 'Create Student', 'data': {'user': 'user' ,'password': 'password'}})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter the number of iterations');
    }
});

document.getElementById('login_simulate').addEventListener('click', function() {
    const user = document.getElementById('user').value;
    const password = document.getElementById('password').value;
    if (user) {
        fetch('/login_simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'student_name': user ,'student_password': password})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter the number of iterations');
    }
});


