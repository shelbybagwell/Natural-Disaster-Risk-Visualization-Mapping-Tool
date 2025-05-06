import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Input, SimpleChanges, ViewContainerRef, ComponentRef } from '@angular/core';
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
import Overlay from 'ol/Overlay';
import { MapPopupComponent } from '../../../map-popup/map-popup.component';
import { Polygon } from 'ol/geom';
import Stroke from 'ol/style/Stroke';

@Component({
  selector: 'app-open-layer-map',
  standalone: false,
  templateUrl: './open-layer-map.component.html',
  styleUrl: './open-layer-map.component.scss'
})
export class OpenLayerMapComponent {
  @ViewChild('mapContainer') mapContainer!: ElementRef;
  @ViewChild('popupContainer', {read: ViewContainerRef}) popupContainer!: ViewContainerRef;
  @Input() centerPoint: number[] = [-119.4149, 36.7783];
  @Input() mapData: any;

  map!: Map;
  popupOverlay!: Overlay;
  popupComponentRef!: ComponentRef<MapPopupComponent> | null;

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
    this.popupOverlay = new Overlay({
      element: document.getElementById('popup')!,
      autoPan: {
        animation: {
          duration: 250,
        },
      },
    });
    this.map.addOverlay(this.popupOverlay);

    this.map.on('singleclick', (event) => {
      const features = this.map.getFeaturesAtPixel(event.pixel);
      if (features && features.length > 0) {
        const feature = features[0];
        const coords = (feature.getGeometry() as Point).getCoordinates();
        const data = feature.get('data');

        if (data) {
          this.popupContainer.clear();

          const popupRef = this.popupContainer.createComponent(MapPopupComponent);
          popupRef.instance.data = data;
          popupRef.instance.close.subscribe(() => {
            this.popupOverlay.setPosition(undefined);
            this.popupContainer.clear();
          });

          this.popupComponentRef = popupRef;
          const popupEl = popupRef.location.nativeElement;
          document.getElementById('popup')!.appendChild(popupEl);

          this.popupOverlay.setPosition(coords);
        }
        else {
          this.popupOverlay.setPosition(undefined);
          this.popupContainer.clear();
        }
      }
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
        
        // const coordinates = [
        //   [
        //     fromLonLat(footprint.Polygon[0].slice(0,2)),
        //     fromLonLat(footprint.Polygon[1].slice(0,2)),
        //     fromLonLat(footprint.Polygon[2].slice(0,2)),
        //     fromLonLat(footprint.Polygon[3].slice(0,2)),
        //     fromLonLat(footprint.Polygon[4].slice(0,2))
        //   ]
        // ];
        // const polygon = new Polygon(coordinates);
        // const polyFeature = new Feature(polygon);
        // polyFeature.setStyle(new Style({
        //   stroke: new Stroke({
        //     color: 'red',
        //     width: 2,
        //   })
        // }));
        // const polyVectorLayer = new VectorLayer({
        //   source: new VectorSource({
        //     features: [polyFeature]
        //   })
        // });
        // this.map.addLayer(polyVectorLayer);

        // const fireMarker = new Feature(new Point(fromLonLat([footprint.description.Longitude, footprint.description.Latitude])));
        // fireMarker.setStyle(new Style({
        //   image: new Icon({
        //     src: "https://cdn-icons-png.flaticon.com/512/1453/1453025.png",
        //     scale: 0.05
        //   })
        // }));
        // fireMarker.set('data', footprint.description);
        // const fireMarkerLayer = new VectorLayer({
        //   source: new VectorSource({
        //     features: [fireMarker]
        //   })
        // });
        // this.map.addLayer(fireMarkerLayer);

        let kept_footprints: any[] = [];
        potential_footprints.forEach((element: any) => {
          if (element.description["Confidence[0-100%]"] >= 0.5) {
            kept_footprints.push(element)
          }
        });

        const features = kept_footprints.map(fp => {
          const fireMarker = new Feature(new Point(fromLonLat([fp.description.Longitude, fp.description.Latitude])));
          fireMarker.setStyle(new Style({
            image: new Icon({
              src: "https://cdn-icons-png.flaticon.com/512/1453/1453025.png",
              scale: 0.05
            })
          }));
          fireMarker.set('data', footprint.description);
          return fireMarker;
        });
        const footprintLayer = new VectorLayer({
          source: new VectorSource({
            features: features
          })
        });

        this.map.addLayer(footprintLayer);

        const polygons = kept_footprints.map(fp => {
          const coordinates = [
              [
                fromLonLat(fp.Polygon[0].slice(0,2)),
                fromLonLat(fp.Polygon[1].slice(0,2)),
                fromLonLat(fp.Polygon[2].slice(0,2)),
                fromLonLat(fp.Polygon[3].slice(0,2)),
                fromLonLat(fp.Polygon[4].slice(0,2))
              ]
            ];
            const polygon = new Polygon(coordinates);
            const polyFeature = new Feature(polygon);
            polyFeature.setStyle(new Style({
              stroke: new Stroke({
                color: 'red',
                width: 2
              })
            }));
            return polyFeature;
        });
        const polygonLayer = new VectorLayer({
          source: new VectorSource({
            features: polygons
          })
        });

        this.map.addLayer(polygonLayer);
      }
    }
  }
}
