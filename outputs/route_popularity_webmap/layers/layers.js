var wms_layers = [];


        var lyr_DarkMatternolabels_0 = new ol.layer.Tile({
            'title': 'Dark Matter [no labels]',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' &middot; <a href="https://cartodb.com/basemaps/">Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.</a>',
                url: 'http://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png'
            })
        });
var format_network_stats_1 = new ol.format.GeoJSON();
var features_network_stats_1 = format_network_stats_1.readFeatures(json_network_stats_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_network_stats_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_network_stats_1.addFeatures(features_network_stats_1);
var lyr_network_stats_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_network_stats_1, 
                style: style_network_stats_1,
                interactive: true,
    title: 'network_stats<br />\
    <img src="styles/legend/network_stats_1_0.png" /> 1 - 2<br />\
    <img src="styles/legend/network_stats_1_1.png" /> 2 - 3<br />\
    <img src="styles/legend/network_stats_1_2.png" /> 3 - 5<br />\
    <img src="styles/legend/network_stats_1_3.png" /> 5 - 8<br />\
    <img src="styles/legend/network_stats_1_4.png" /> 8 - 12<br />\
    <img src="styles/legend/network_stats_1_5.png" /> 12 - 17<br />\
    <img src="styles/legend/network_stats_1_6.png" /> 17 - 23<br />\
    <img src="styles/legend/network_stats_1_7.png" /> 23 - 28<br />\
    <img src="styles/legend/network_stats_1_8.png" /> 28 - 36<br />\
    <img src="styles/legend/network_stats_1_9.png" /> 36 - 45<br />\
    <img src="styles/legend/network_stats_1_10.png" /> 45 - 55<br />\
    <img src="styles/legend/network_stats_1_11.png" /> 55 - 68<br />\
    <img src="styles/legend/network_stats_1_12.png" /> 68 - 80<br />\
    <img src="styles/legend/network_stats_1_13.png" /> 80 - 92,4<br />\
    <img src="styles/legend/network_stats_1_14.png" /> 92,4 - 111<br />\
    <img src="styles/legend/network_stats_1_15.png" /> 111 - 132<br />\
    <img src="styles/legend/network_stats_1_16.png" /> 132 - 152<br />\
    <img src="styles/legend/network_stats_1_17.png" /> 152 - 168<br />\
    <img src="styles/legend/network_stats_1_18.png" /> 168 - 192<br />\
    <img src="styles/legend/network_stats_1_19.png" /> 192 - 214<br />\
    <img src="styles/legend/network_stats_1_20.png" /> 214 - 239<br />\
    <img src="styles/legend/network_stats_1_21.png" /> 239 - 266<br />\
    <img src="styles/legend/network_stats_1_22.png" /> 266 - 300,2<br />\
    <img src="styles/legend/network_stats_1_23.png" /> 300,2 - 333<br />\
    <img src="styles/legend/network_stats_1_24.png" /> 333 - 369,3<br />\
    <img src="styles/legend/network_stats_1_25.png" /> 369,3 - 413,6<br />\
    <img src="styles/legend/network_stats_1_26.png" /> 413,6 - 458,3<br />\
    <img src="styles/legend/network_stats_1_27.png" /> 458,3 - 516,8<br />\
    <img src="styles/legend/network_stats_1_28.png" /> 516,8 - 562<br />\
    <img src="styles/legend/network_stats_1_29.png" /> 562 - 622<br />\
    <img src="styles/legend/network_stats_1_30.png" /> 622 - 679<br />\
    <img src="styles/legend/network_stats_1_31.png" /> 679 - 735<br />\
    <img src="styles/legend/network_stats_1_32.png" /> 735 - 816<br />\
    <img src="styles/legend/network_stats_1_33.png" /> 816 - 888<br />\
    <img src="styles/legend/network_stats_1_34.png" /> 888 - 974,5<br />\
    <img src="styles/legend/network_stats_1_35.png" /> 974,5 - 1071,1<br />\
    <img src="styles/legend/network_stats_1_36.png" /> 1071,1 - 1162<br />\
    <img src="styles/legend/network_stats_1_37.png" /> 1162 - 1253<br />\
    <img src="styles/legend/network_stats_1_38.png" /> 1253 - 1371<br />\
    <img src="styles/legend/network_stats_1_39.png" /> 1371 - 1504<br />\
    <img src="styles/legend/network_stats_1_40.png" /> 1504 - 1643<br />\
    <img src="styles/legend/network_stats_1_41.png" /> 1643 - 1814<br />\
    <img src="styles/legend/network_stats_1_42.png" /> 1814 - 1993,6<br />\
    <img src="styles/legend/network_stats_1_43.png" /> 1993,6 - 2119,3<br />\
    <img src="styles/legend/network_stats_1_44.png" /> 2119,3 - 2308,4<br />\
    <img src="styles/legend/network_stats_1_45.png" /> 2308,4 - 2506,1<br />\
    <img src="styles/legend/network_stats_1_46.png" /> 2506,1 - 2677,9<br />\
    <img src="styles/legend/network_stats_1_47.png" /> 2677,9 - 2882<br />\
    <img src="styles/legend/network_stats_1_48.png" /> 2882 - 3131<br />\
    <img src="styles/legend/network_stats_1_49.png" /> 3131 - 3350,5<br />\
    <img src="styles/legend/network_stats_1_50.png" /> 3350,5 - 3640,2<br />\
    <img src="styles/legend/network_stats_1_51.png" /> 3640,2 - 3957,6<br />\
    <img src="styles/legend/network_stats_1_52.png" /> 3957,6 - 4289<br />\
    <img src="styles/legend/network_stats_1_53.png" /> 4289 - 4699,9<br />\
    <img src="styles/legend/network_stats_1_54.png" /> 4699,9 - 5114<br />\
    <img src="styles/legend/network_stats_1_55.png" /> 5114 - 5560,7<br />\
    <img src="styles/legend/network_stats_1_56.png" /> 5560,7 - 6048,4<br />\
    <img src="styles/legend/network_stats_1_57.png" /> 6048,4 - 6621,7<br />\
    <img src="styles/legend/network_stats_1_58.png" /> 6621,7 - 7190,7<br />\
    <img src="styles/legend/network_stats_1_59.png" /> 7190,7 - 7814,6<br />\
    <img src="styles/legend/network_stats_1_60.png" /> 7814,6 - 8681,3<br />\
    <img src="styles/legend/network_stats_1_61.png" /> 8681,3 - 9393<br />\
    <img src="styles/legend/network_stats_1_62.png" /> 9393 - 10321,5<br />\
    <img src="styles/legend/network_stats_1_63.png" /> 10321,5 - 11111,6<br />\
    <img src="styles/legend/network_stats_1_64.png" /> 11111,6 - 12227,5<br />\
    <img src="styles/legend/network_stats_1_65.png" /> 12227,5 - 13257,7<br />\
    <img src="styles/legend/network_stats_1_66.png" /> 13257,7 - 14478,7<br />\
    <img src="styles/legend/network_stats_1_67.png" /> 14478,7 - 15704<br />\
    <img src="styles/legend/network_stats_1_68.png" /> 15704 - 17084,3<br />\
    <img src="styles/legend/network_stats_1_69.png" /> 17084,3 - 19038,9<br />\
    <img src="styles/legend/network_stats_1_70.png" /> 19038,9 - 21158,2<br />\
    <img src="styles/legend/network_stats_1_71.png" /> 21158,2 - 23083,6<br />\
    <img src="styles/legend/network_stats_1_72.png" /> 23083,6 - 25263,7<br />\
    <img src="styles/legend/network_stats_1_73.png" /> 25263,7 - 27493,9<br />\
    <img src="styles/legend/network_stats_1_74.png" /> 27493,9 - 30190<br />\
    <img src="styles/legend/network_stats_1_75.png" /> 30190 - 32693,9<br />\
    <img src="styles/legend/network_stats_1_76.png" /> 32693,9 - 35904,6<br />\
    <img src="styles/legend/network_stats_1_77.png" /> 35904,6 - 39943<br />\
    <img src="styles/legend/network_stats_1_78.png" /> 39943 - 44590,8<br />\
    <img src="styles/legend/network_stats_1_79.png" /> 44590,8 - 48828,2<br />\
    <img src="styles/legend/network_stats_1_80.png" /> 48828,2 - 54280<br />\
    <img src="styles/legend/network_stats_1_81.png" /> 54280 - 59883,6<br />\
    <img src="styles/legend/network_stats_1_82.png" /> 59883,6 - 65221<br />\
    <img src="styles/legend/network_stats_1_83.png" /> 65221 - 72043,2<br />\
    <img src="styles/legend/network_stats_1_84.png" /> 72043,2 - 81584,8<br />\
    <img src="styles/legend/network_stats_1_85.png" /> 81584,8 - 92375,7<br />\
    <img src="styles/legend/network_stats_1_86.png" /> 92375,7 - 101763,6<br />\
    <img src="styles/legend/network_stats_1_87.png" /> 101763,6 - 113852,7<br />\
    <img src="styles/legend/network_stats_1_88.png" /> 113852,7 - 128803,3<br />\
    <img src="styles/legend/network_stats_1_89.png" /> 128803,3 - 147656,5<br />\
    <img src="styles/legend/network_stats_1_90.png" /> 147656,5 - 170374,3<br />\
    <img src="styles/legend/network_stats_1_91.png" /> 170374,3 - 196573,2<br />\
    <img src="styles/legend/network_stats_1_92.png" /> 196573,2 - 236457,6<br />\
    <img src="styles/legend/network_stats_1_93.png" /> 236457,6 - 274444,8<br />\
    <img src="styles/legend/network_stats_1_94.png" /> 274444,8 - 318796,1<br />\
    <img src="styles/legend/network_stats_1_95.png" /> 318796,1 - 371581,2<br />\
    <img src="styles/legend/network_stats_1_96.png" /> 371581,2 - 444897,3<br />\
    <img src="styles/legend/network_stats_1_97.png" /> 444897,3 - 599263,2<br />\
    <img src="styles/legend/network_stats_1_98.png" /> 599263,2 - 820180,3<br />\
    <img src="styles/legend/network_stats_1_99.png" /> 820180,3 - 1623029<br />'
        });

lyr_DarkMatternolabels_0.setVisible(true);lyr_network_stats_1.setVisible(true);
var layersList = [lyr_DarkMatternolabels_0,lyr_network_stats_1];
lyr_network_stats_1.set('fieldAliases', {'fid': 'fid', 'route_coun': 'route_coun', 'popularity': 'popularity', });
lyr_network_stats_1.set('fieldImages', {'fid': '', 'route_coun': '', 'popularity': '', });
lyr_network_stats_1.set('fieldLabels', {'fid': 'no label', 'route_coun': 'no label', 'popularity': 'inline label', });
lyr_network_stats_1.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});