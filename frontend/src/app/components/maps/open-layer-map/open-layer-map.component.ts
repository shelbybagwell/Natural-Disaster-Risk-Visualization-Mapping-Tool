import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Input } from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import { fromLonLat, fromUserCoordinate } from 'ol/proj';
import OSM from 'ol/source/OSM';

@Component({
  selector: 'app-open-layer-map',
  standalone: false,
  templateUrl: './open-layer-map.component.html',
  styleUrl: './open-layer-map.component.scss'
})
export class OpenLayerMapComponent {
  @ViewChild('mapContainer') mapContainer!: ElementRef;
  @Input() centerPoint: number[] = [-119.4149, 36.7783];

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
}
