'use strict'

// fetch for homepage
let message = document.getElementById('intro');

const homepageUrl = 'https://diary10.herokuapp.com/api/v2/home';
fetch(`${homepageUrl}`)

    .then((response)=>{
        response.json().then((data) => {
        const Welcome = Object.values(data.Message.Message[0])

        const FetchedMessage =  `<h2 class="intro">${Welcome}</h2>`

        message.innerHTML = FetchedMessage
        
        })})
        .catch(err => console.log(err));