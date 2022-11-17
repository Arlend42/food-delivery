let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        componentRestrictions: {'country': ['al']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    // console.log(address)
    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('lng=>', longitude);
            // var latitudeElem = document.querySelector('#id_latitude');
            // latitudeElem.innerText = latitude.toString();
            // var longitudeElem = document.querySelector('#id_longitude');
            // longitudeElem.innerText = longitude.toString();
            $("#id_latitude").val(latitude);
            $("#id_longitude").val(longitude);
            $("#id_address").val(address);
        }
    });
    // loop throw the address components and assign other addresdata 
    console.log(place.address_components);  
    for(var i=0; i<place.address_components.length; i++){
        for (var j=0; j<place.address_components[i].types.length; j++){
            if (place.address_components[i].types[j] == 'locality'){
                $("#id_city").val(place.address_components[i].long_name);
            }
            // zip code
            if (place.address_components[i].types[j] == 'postal_code'){
                $("#id_zip_code").val(place.address_components[i].long_name);
            }else{
                $('#id_zip_code').val('');
            }
        }
    }
}
