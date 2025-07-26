document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
});

async function checkAuthentication() {
  const loginButton = document.getElementById('login-button');
  const logoutButton = document.getElementById('logout-button');
  const token = getCookie('token');
  if (!token) {
    loginButton.style.display = 'block';
    logoutButton.style.display = 'none';
  } else {
    loginButton.style.display = 'none';
    logoutButton.style.display = 'block';
    // Fetch places data if the user is authenticated
    document.getElementById("connected").textContent=getCookie("user")
    fetchPlaces(token);
  }
}

async function logOut() {
  if (confirm("Are you sure to logout ?")) {
    suprCookie(['token', 'user']);
    window.location.href='index.html';
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

function suprCookie (names){
  names.forEach(name => {
    document.cookie = name+'=; Max-Age=-99999999;';
  });
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
  const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  });
  if (response.ok) {
    
    const data = await response.json();
    displayPlaces(data)
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function displayPlaces(places) {
  const placeCard = document.getElementById('places-list');
  places.forEach(place => {
    const article = document.createElement('article');
    const button = document.createElement('button');
    const title = document.createElement('h3');
    const price = document.createElement('p');
    article.dataset.price = `${place.price}`
    button.classList.add('details-button');
    button.classList.add('button');
    button.addEventListener('click', function(){
      document.cookie = `place=${place.id}; path=/`;
      window.location.href = 'place.html';
    });
    article.classList.add('place-card');
    title.classList.add('place-card-title');
    price.classList.add('place-card-price');
    button.appendChild(document.createTextNode('View Details'));
    title.appendChild(document.createTextNode(place.title));
    price.appendChild(document.createTextNode(`Price per night : ${place.price} $`));
    article.appendChild(title);
    article.appendChild(price);
    article.appendChild(button);
    placeCard.appendChild(article);
  });
}

async function goLogin() {
  window.location.href = 'login.html';
}

async function goIndex() {
  window.location.href = 'index.html';
}

document.getElementById('price-filter').addEventListener('change', (event) => {
  placeCard = document.getElementsByClassName('place-card')
  for (let i = 0; i < placeCard.length; i++) {
    if (Number(placeCard[i].dataset.price) >= Number(event.target.value)) {
      placeCard[i].style.display = 'none';
    }
    else {
      placeCard[i].style.display = 'flex';
    }
  }
});

function getPlaceId(test) {
  console.log(test)
}

