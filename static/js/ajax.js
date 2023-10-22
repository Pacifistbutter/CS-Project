var searchInput = document.getElementById("searchInput");
searchInput.addEventListener('keyup', searchHandler);

function searchHandler() {
    // console.log('You have clicked the search handler');

    // Instantiate an xhr object
    const xhr = new XMLHttpRequest();
    var q = searchInput.value;
    // console.log(q);
    var API_KEY = window.API_KEY;
    // console.log(API_KEY);
    var url = `http://api.weatherapi.com/v1/search.json?key=${API_KEY}&q=${q}`
    // Open the object
    xhr.open('GET', url , true);


    // What to do when response is ready
    xhr.onload = function () {
        if(this.status === 200){
            let obj = JSON.parse(this.responseText);
            let suggestion = document.getElementById('suggestion');
            str = "";
            for (key in obj)
            {
                str += `<option value="${obj[key].name}">${obj[key].region}, ${obj[key].country} </option>`;
            }
            suggestion.innerHTML = str;
        }
        else{
            console.log("Some error occured")
        }
    }

    // send the request
    xhr.send();
    // console.log("We are done fetching employees!");
    
}