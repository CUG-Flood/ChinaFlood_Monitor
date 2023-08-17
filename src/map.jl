using JSServe
import JSServe.TailwindDashboard as D
using RCall

function get_st()
  R"""
  tidymet::st_met2481
  """ |> rcopy
end

st = get_st()

App() do
  js = ES6Module("https://esm.sh/v111/leaflet@1.9.3/es2022/leaflet.js")
  css = Asset("https://unpkg.com/leaflet@1.9.3/dist/leaflet.css")
  map_div = DOM.div(id="map"; style="height: 800px; width: 100%")

  textfield = D.TextField("StationName"; name="StationName")
  # JSServe.onjs(session, eval_button.value,
  #     js"""function (click){
  #     const js_src = $(editor.onchange).value;
  #     const result = new Function("return " + (js_src))()
  #     let dom;
  #     if (typeof result === 'object' && result.nodeName) {
  #         dom = result
  #     } else {
  #         const span = document.createElement("span")
  #         span.innerText = result;
  #         dom = span
  #     }
  #     JSServe.update_or_replace($(output), dom, false);
  #     return
  # }""")
  
  return DOM.div(
    css, map_div,
    textfield,
    
    js"""
    $(js).then(L=> {
        // 创建地图容器
        var map = L.map('map').setView([34, 55], 3);
        
        // 添加地图图层（OpenStreetMap）
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // 添加气象站标记
        var weatherStations = [
          { name: "站点1", location: [15, 70] },
          { name: "站点2", location: [55, 140] },
        ];

        weatherStations.forEach(function (station) {
          var marker = L.marker(station.location).addTo(map);
            //.bindPopup(station.name)
            //.openPopup();
          
          marker.on('click', function() {
            var text = document.getElementsByName("StationName")[0]
            text.value = station.name;
            // console.log(station.name);
            // displayStationInfo(station.name);
          });
        });
    })
    """
  )
end
