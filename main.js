function list_parties() {
	var client = new HttpClient();
	client.get('http://127.0.0.1:5000/get_parties', function(response) {
	    document.getElementById('parties').innerHTML = response
	});
}

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }
        anHttpRequest.open("GET", aUrl, true);            
        anHttpRequest.send(null);
    }
}