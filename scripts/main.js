//####################################################################################
//############### CHARGEMENT ET AFFICHAGE DES COUCHES CARTO ##########################
//####################################################################################

// Appel du fond de carte
mapboxgl.accessToken = 'pk.eyJ1IjoibGVwbGFuc3R1ZGlvIiwiYSI6ImNsdWNnMTRpNDEzeXoyanFuOGdxbm1kOXIifQ.bGLWHO7ce0M37dJCnJ0s3w';
const bounds = [[-10, 36], [15, 56]];
const map = new mapboxgl.Map({
    container: 'map',
    // style: 'mapbox://styles/leplanstudio/cm3h6y91h008b01sf3hbc10qh',
    style: 'mapbox://styles/leplanstudio/cmipzcx7k00ng01sbenbha21p',
    center: [2, 46.8],
    zoom: 5.1,
    minZoom: 5,
    maxZoom: 12,
    maxBounds: bounds,
});

// #######################################################################################
// ########### CHARGEMENT DES PICTOS sites de production et de stockage ##################

// Début de la balise des couches
map.on('load', () => {

    // ############# COUCHE demog-climat  ##################################################
    map.addSource('demog-climat', {
        type: 'geojson',
        data: 'DATA/points1km_projDemog_Climat.geojson'
    });

    // Couche de test : 
    map.addLayer({
        'id': 'heatwave',
        'type': 'circle',
        'source': 'demog-climat',
        'layout': {},
        'paint': {
            'circle-opacity': 0,
            // 'circle-color': ['match', ['get', 'n_heatwave_min20_max35'],
            //      '1', '#E4E8F7',
            //      '2', '#ADBBE8',
            //      '3', '#778DD8',
            //      '#d0003e'],
            'circle-color': [
                        'interpolate',
                    ['exponential', 1.75],
                    ['get','n_heatwave_min20_max35'],
                    1,
                    '#006bd7',
                    5,
                    '#00a2c7',
                    10,
                    '#eeea00',
                    15,
                    '#ee9f00',
                    20,
                    '#ee4b00',
                    25,
                    '#e10000',
                    30,
                    '#730000'
                    ],           
            'circle-radius': ['/', ['sqrt', ['/', ['get', 'S1_pop65p_2070'], 3.14]], 5]
        }
    });

    map.addLayer({
        'id': 'tropical-night',
        'type': 'circle',
        'source': 'demog-climat',
        'layout': {},
        'paint': {
            'circle-opacity': 0,
            // 'circle-color': ['match', ['get', 'n_heatwave_min20_max35'],
            //      '1', '#E4E8F7',
            //      '2', '#ADBBE8',
            //      '3', '#778DD8',
            //      '#d0003e'],
            'circle-color': [
                        'interpolate',
                    ['exponential', 1.75], // Set the interpolation type
                    ['get','n_tropical_nights_min20'],
                    1,
                    '#006bd7',
                    5,
                    '#00a2c7',
                    10,
                    '#eeea00',
                    15,
                    '#ee9f00',
                    20,
                    '#ee4b00',
                    25,
                    '#e10000',
                    30,
                    '#730000'
                    ],           
            'circle-radius': ['/', ['sqrt', ['/', ['get', 'S1_pop65p_2070'], 3.14]], 5]
        }
    });



    // Fin de la balise des couches 
});

// ##########################################################################################
// ########## Affichage des couches au clic sur la liste #################################
// ##########################################################################################

// ########## Affichage heatwave ################################################
document.getElementById('lien_heatwave').addEventListener('click', () => {
    const circleOpacity = map.getPaintProperty('heatwave', 'circle-opacity');
    if (circleOpacity === 0) {
        map.setPaintProperty('heatwave', 'circle-opacity', 0.8); this.className = '';
        document.getElementById("oeil_heatwave").innerHTML = '<i class="far fa-thin fa-eye" style="color:#D38D31; font-weight: 800;"></i>';
    } else {
        this.className = 'active'; map.setPaintProperty('heatwave', 'circle-opacity', 0);
        document.getElementById("oeil_heatwave").innerHTML = '<i class="far fa-thin fa-eye-slash"></i>';
    };
});


// ########## Affichage tropical night ################################################
document.getElementById('lien_tropical-night').addEventListener('click', () => {
    const circleOpacity = map.getPaintProperty('tropical-night', 'circle-opacity');
    if (circleOpacity === 0) {
        map.setPaintProperty('tropical-night', 'circle-opacity', 0.8); this.className = '';
        document.getElementById("oeil_tropical-night").innerHTML = '<i class="far fa-thin fa-eye" style="color:#D38D31; font-weight: 800;"></i>';
    } else {
        this.className = 'active'; map.setPaintProperty('tropical-night', 'circle-opacity', 0);
        document.getElementById("oeil_tropical-night").innerHTML = '<i class="far fa-thin fa-eye-slash"></i>';
    };
});
