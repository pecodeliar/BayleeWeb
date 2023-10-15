// https://medium.com/hypersphere-codes/detecting-system-theme-in-javascript-css-react-f6b961916d48
const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
const storageTheme = window.localStorage.getItem("theme");
if ((storageTheme === "auto" && darkThemeMq.matches === true) || storageTheme === "dark") {
    document.querySelector("body").classList.add("dark-theme");
};

function themeSwitch() {

    const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
    var theme = window.localStorage.getItem("theme");
    //console.log(theme);
    if ((theme === "auto" && darkThemeMq.matches === true) || theme === "dark") {
        document.querySelector("body").classList.toggle("dark-theme");
        window.localStorage.setItem("theme", "light");
    } else if ((theme === "auto" && darkThemeMq.matches === false) || theme === "light") {
        document.querySelector("body").classList.toggle("dark-theme");
        window.localStorage.setItem("theme", "dark");
    } else if (theme === null) {
        // For Mobile Devies
        document.querySelector("body").classList.toggle("dark-theme");
        window.localStorage.setItem("theme", "dark");
    };

}


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("pfp");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

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



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function toast(message, error=null) {
  /* https://www.w3schools.com/howto/howto_js_snackbar.asp */
  // Get the snackbar DIV
  var snackbar = document.getElementById("snackbar");
  snackbar.innerText = message;

  if (error !== null) {
      const alert = document.getElementById("alert");
      alert.style.display = "block";
      alert.innerText = error;
      console.log(error);
  }

  // Add the "show" class to DIV
  snackbar.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);
}

function authentication(action) {
  console.log(action);
  if (action === "Login") {

    const csrftoken = getCookie('csrftoken');

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch(`/api/login`, {
            method: 'POST',
            //credentials: "same-origin",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
              },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => {
            if (response.ok) return response.json();
            return response.json().then(response => {throw new Error(response.error)})
        })
        .then(data => {

                // https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage
                sessionStorage.setItem("token", data.token);
                window.location.href = "/";

        })
        .catch(error => {
            toast("Error. Reason stickied above.", error);
        });

  } else if (action === "Register") {

    const csrftoken = getCookie('csrftoken');

        const username = document.getElementById("username");
        const email = document.getElementById("email");
        //const access = document.getElementById("access");
        const password = document.getElementById("password");
        const confirmation = document.getElementById("confirmation");

        fetch(`/api/register`, {
            method: 'POST',
            //credentials: "same-origin",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
              },
            body: JSON.stringify({
                username: username.value,
                email: email.value,
                //access_code: access.value,
                password1: password.value,
                password2: confirmation.value,
            })
        })
        .then(response => {
            if (response.ok) return response.json();
            return response.json().then(response => {
                if (response.username !== undefined) {
                    username.style.backgroundColor = "var(--error)";
                    username.style.color = "var(--on-error)";
                    throw new Error("A user with this username already exists.");
                } else if (response.error !== undefined) {
                    password.style.backgroundColor = "var(--error)";
                    confirmation.style.backgroundColor = "var(--error)";
                    access.style.backgroundColor = "var(--error)";
                    password.style.color = "var(--on-error)";
                    confirmation.style.color = "var(--on-error)";
                    throw new Error(response.error);
                }  else if (response.email !== undefined) {
                    email.style.backgroundColor = "var(--error)";
                    email.style.color = "var(--on-error)";
                    throw new Error(response.email);
                } /*else if (response.access_code !== undefined) {
                    access.style.backgroundColor = "var(--error)";
                    access.style.color = "var(--on-error)";
                    throw new Error(response.access_code);
                }*/

            })
        })
        .then(data => {
                // https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage
                sessionStorage.setItem("token", data.token);
                window.location.href = "/";
        })
        .catch(error => {
            toast("Error. Reason stickied above.", error);
        });


  }



}

function listing(action, id=null) {

    /** Action should be either "create" or "edit".
     * If action is edit, id should be passed into the function as well.
     */

    const csrftoken = getCookie('csrftoken');

    const title = document.getElementById("id_title").value;
    const description = document.getElementById("id_description").value;
    const price = document.getElementById("id_price").value;
    const image = document.getElementById("id_image_link").value;

    let url = null;
    if (id === null) {
        url = "/api/listings/";
    } else {
        url = `/api/listings/${id}/`
    }

        fetch(url, {
            method: (action === "create") ? 'POST' : 'PATCH',
            //credentials: "same-origin",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
              },
            body: JSON.stringify({
                title: title,
                description: description,
                starting_price: price,
                image: image
            })
        })
        .then(response => {
            if (response.ok) return response.json();
            return response.json().then(response => {throw new Error(response.error)})
        })
        .then(data => {

          console.log(data)
          window.location.href = `/listing/${data.id}`;

        })
        .catch(error => {
            toast("Error. Reason stickied above.", error);
        });
}

function watch(action, listingId) {

    const csrftoken = getCookie('csrftoken');

    /** Action should be 'Add' or 'Remove' */
    return fetch(`/api/listings/${listingId}/watch`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            action: action
        })
    })
    .then(response => {
        if (response.ok) return response.json();
        return response.json().then(response => {throw new Error(response.error)})
    })
    .then(() => {

        const button = document.getElementById("list-wl-btn");

        if (action === "Add") {
            button.value = "Remove";
            button.innerText = "Remove From Watchlist";
        } else {
            button.value = "Add";
            button.innerText = "Add From Watchlist";
        }

    })
    .catch(error => {
        toast("Error. Reason stickied above.", error);
    });

}

function editProfile(userId) {

    const firstName = document.getElementById("id_first_name").value;
    const lastName = document.getElementById("id_last_name").value;
    const username = document.getElementById("id_username").value;
    const pfp = document.getElementById("id_profile_picture").value;
    const pfpCredit = document.getElementById("id_pfp_credit").value;
    const banner = document.getElementById("id_banner").value;
    const bannerCredit = document.getElementById("id_banner_credit").value;


    const csrftoken = getCookie('csrftoken');

    fetch(`/api/users/${userId}/`, {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            username: username,
            profile_picture: pfp,
            pfp_credit: pfpCredit,
            banner: banner,
            banner_credit: bannerCredit,
        })
    })
    .then(response => {
        if (response.ok) return response.json();
        return response.json().then(response => {throw new Error(response.error)})
    })
    .then(result => {

        console.log(result);
        window.location.href = `/profile/${userId}`;

    })
    .catch(error => {
        console.log(error);
    });
    
}

function placeBid(listingId) {

    const price = document.getElementById("id_bid").value;

    const csrftoken = getCookie('csrftoken');

    fetch(`/api/listings/${listingId}/bids/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            price: parseFloat(price)
        })
    })
    .then(response => {
        if (response.ok) return response.json();
        return response.json().then(response => {
            if (response.price !== undefined) {
                throw new Error(response.price);
            } else if (response.error !== undefined) {
                throw new Error(response.error);
            }  else if (response.non_field_errors !== undefined) {
                throw new Error(response.non_field_errors);
            }
        })
    })
    .then(() => {

        window.location.href = `/listing/${listingId}`;

    })
    .catch(error => {
        toast("Error. Reason stickied above.", error);
    });

}

function makeComment(listingId, username) {

    const text = document.getElementById("id_comment");

    const csrftoken = getCookie('csrftoken');

    fetch(`/api/listings/${listingId}/comments/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            text: text.value
        })
    })
    .then(response => {
        if (response.ok) return response.json();
        return response.json().then(response => {
            if (response.price !== undefined) {
                throw new Error(response.text);
            } else if (response.error !== undefined) {
                throw new Error(response.error);
            }  else if (response.non_field_errors !== undefined) {
                throw new Error(response.non_field_errors);
            }
        })
    })
    .then(result => {

        console.log(result);

        text.value = "";

        // Add comment element to page without reloading
        const container = document.getElementById("comments-row");

        const parent = document.createElement("div");
        parent.setAttribute("class", "comment-item");
        container.prepend(parent);
        
        const pfpCont = document.createElement("div");
        pfpCont.setAttribute("class", "users-comment-pfp");
        parent.append(pfpCont);

        const pfpLink = document.createElement("a");
        pfpLink.setAttribute("href", `/profile/${result.creator}`);
        pfpCont.append(pfpLink);

        const pfpImg = document.createElement("img");
        pfpImg.setAttribute("class", "comment-pfp");
        pfpImg.src = document.getElementById("make-cmnt-pfp").src;
        pfpLink.append(pfpImg);

        const textCont = document.createElement("div");
        textCont.setAttribute("class", "comment-details");
        parent.append(textCont);

        const creator = document.createElement("p");
        creator.setAttribute("id", "user-cmnt-name");
        creator.innerText = username;
        textCont.append(creator);

        const comment = document.createElement("p");
        comment.setAttribute("id", "user-cmnt-text");
        comment.innerText = result.text;
        textCont.append(comment);

        // Hide no comments text
        const noComments = document.getElementById("no-cmnts-text");
        if (noComments !== null) {
            noComments.style.display = "none";
        }

    })
    .catch(error => {
        toast("Error. Reason stickied above.", error);
    });

}