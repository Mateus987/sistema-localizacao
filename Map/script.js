var lat = 35.58;
var long = 104.61;

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

var map = L.map('map');

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


var marker = L.marker([lat, long]);

for(let i = 0; i <= 50; i++)
{
    // Busca na API, ela vai atualizar lat e long
    lat += 0.01;
    long += 0.01;

    // Remove o antigo, póe o novo, e volta a buscar na API
    marker.removeFrom(map);
    marker = L.marker([lat, long]);
    map.setView([lat, long], 13);
    marker.addTo(map);
}
