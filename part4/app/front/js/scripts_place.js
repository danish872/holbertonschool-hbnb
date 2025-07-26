document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
});

function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review-button');
  const loginButton = document.getElementById('login-button');
  if (!token) {
    addReviewSection.style.display = 'none';
    loginButton.style.display = 'block';
  } else {
    addReviewSection.style.display = 'block';
    loginButton.style.display = 'none';
    document.getElementById("connected").textContent = getCookie("user")
    fetchPlaceDetails(token, getCookie('place'));
  }
}

async function logOut() {
  if (confirm("Are you sure to logout ?")) {
    suprCookie(['token', 'user']);
    window.location.href = 'index.html';
  }
}

function getCookie(name) {
  const cookies = {};
  document.cookie.split('; ').forEach(cookie => {
    const [key, value] = cookie.split('=');
    cookies[key] = value;
  });
  return cookies[name];
}

function suprCookie(names) {
  names.forEach(name => {
    document.cookie = name + '=; Max-Age=-99999999;';
  });
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails function
  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  });
  if (response.ok) {
    const data = await response.json();
    displayPlaceDetails(data);
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function displayPlaceDetails(place) {
  // Clear the current content of the place details section
  // Create elements to display the place details (name, description, price, amenities and reviews)
  // Append the created elements to the place details section
  document.getElementById('place-title').textContent = place.title;
  document.getElementById('place-description').textContent = place.description;
  document.getElementById('place-price').textContent = place.price;
  document.getElementById('place-owner').textContent = place.owner.first_name + ' ' + place.owner.last_name;
  place.amenities.forEach(element => {
    const amenitiesCard = document.createElement('article');
    amenitiesCard.classList.add('amenity-card');
    amenity = document.createElement('p');
    img = document.createElement('img');
    img.setAttribute('src', `./image/icon_${element.name}.png`);
    amenity.textContent = element.name;
    amenitiesCard.appendChild(img);
    amenitiesCard.appendChild(amenity);
    document.getElementById("amenities").appendChild(amenitiesCard);
  });
  if (place.amenities.length === 0) {
    document.getElementById("amenities").textContent = "No amenity found";
  }
  place.reviews.forEach(element => {
    const reviewsCard = document.createElement('article');
    reviewsCard.classList.add('review-card');
    reviewWriter = document.createElement('h4');
    const user = fetchUserDetails(element.user);
    user.then(function (result) {
      const userName = result.first_name + " " + result.last_name
      reviewWriter.textContent = userName;
      reviewRating = document.createElement('p');
      reviewRating.textContent = element.rating;
      reviewContet = document.createElement('p');
      reviewContet.textContent = element.text;
      reviewsCard.appendChild(reviewWriter);
      reviewsCard.appendChild(reviewRating);
      reviewsCard.appendChild(reviewContet);
      console.log(userName, getCookie('user'))
      if (userName === getCookie('user')) {
        document.getElementById("log-user-review").appendChild(reviewsCard);
      }
      else {
        document.getElementById("existing-review").appendChild(reviewsCard);
      }
    })
  });
  if (place.reviews.length === 0) {
    document.getElementById("existing-review").textContent = "No Review found";
  }
}

async function goLogin() {
  window.location.href = 'login.html';
}

async function goIndex() {
  window.location.href = 'index.html';
}

async function fetchUserDetails(userId) {
  // Make a GET request to fetch user details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayuserDetails function
  const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  });
  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Login failed: ' + response.statusText);
  }
}
function togglepopup() {
  let popup = document.querySelector(".popup-frame");
  popup.classList.toggle("open");
};

async function addReview() {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails function
  const placeId = getCookie('place');
  const token = getCookie('token');
  const text = document.getElementById("review-content").value;
  const rating = document.getElementById("rating").value;
  const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      "text": text,
      "rating": rating,
      "place_id": placeId
    })
  });
  if (response.ok) {
    window.location.reload();
    document.getElementById("review-content").value = '';
  } else {
    alert('post failed: ' + response.statusText);
  }
}

