import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Input, SimpleChanges } from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import { fromLonLat, fromUserCoordinate } from 'ol/proj';
import OSM from 'ol/source/OSM';
import { elementAt, from } from 'rxjs';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import Style from 'ol/style/Style';
import Icon from 'ol/style/Icon';

@Component({
  selector: 'app-open-layer-map',
  standalone: false,
  templateUrl: './open-layer-map.component.html',
  styleUrl: './open-layer-map.component.scss'
})
export class OpenLayerMapComponent {
  @ViewChild('mapContainer') mapContainer!: ElementRef;
  @Input() centerPoint: number[] = [-119.4149, 36.7783];
  @Input() mapData: any;

  map!: Map;

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.map = new Map({
      target: this.mapContainer.nativeElement,
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        center: fromLonLat(this.centerPoint),
        zoom: 8,
      }),
    });
  }

  ngOnChanges(changes: SimpleChanges){
    if(changes['mapData'] && this.mapData){
      if(this.mapData.currentLocation){
        this.map.getView().setCenter(fromLonLat(this.mapData.currentLocation));
        const marker = new Feature(new Point(fromLonLat(this.mapData.currentLocation)));

        marker.setStyle(new Style({
          image: new Icon({
            src: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
            scale: 0.05
          })
        }));

        const markerLayer = new VectorLayer({
          source: new VectorSource({
            features: [marker]
          })
        });

        this.map.addLayer(markerLayer);
      }
      if (this.mapData.fireData){
        let alerts = this.mapData.fireData.county_alerts[0]; // get most recent alert
        let potential_footprints = this.mapData.fireData.fire_data;
        
        potential_footprints.forEach((element: any) => {
          let confidenceString = element.description["Confidence[0-100%]"];
          const percentage = parseFloat(confidenceString);
          let confidence = percentage/100;
          element.description["Confidence[0-100%]"] = confidence;
        });
        let footprint = potential_footprints.reduce((prev : any, curr : any) => {
          return (curr.description["Confidence[0-100%]"] >= prev.description["Confidence[0-100%]"] ? curr : prev);
        });
        console.log(footprint.description.Latitude);
        console.log(footprint.description.Longitude);

        const fireMarker = new Feature(new Point(fromLonLat([footprint.description.Longitude, footprint.description.Latitude])));

        fireMarker.setStyle(new Style({
          image: new Icon({
            src: "https://cdn-icons-png.flaticon.com/512/1453/1453025.png",
            scale: 0.05
          })
        }));

        const fireMarkerLayer = new VectorLayer({
          source: new VectorSource({
            features: [fireMarker]
          })
        });

        this.map.addLayer(fireMarkerLayer);
        // This code below is if we want multiple footprints later
        // let kept_footprints: any[] = [];
        // potential_footprints.forEach((element: any) => {
        //   let confidenceString = element.description["Confidence[0-100%]"];
        //   const percentage = parseFloat(confidenceString);
        //   let confidence = percentage/100;
        //   if (confidence >= 0.5) {
        //     kept_footprints.push(element)
        //   }
        // });
      }
    }
  }
}
