import { Component, EventEmitter, Input, Output, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { AddressFormComponent } from '../../shared/address-form/address-form.component';


@Component({
  selector: 'app-map-container',
  standalone: false,
  templateUrl: './map-container.component.html',
  styleUrl: './map-container.component.scss'
})
export class MapContainerComponent {
    mapData:any ={};
    
    handleAddressSelected(eventData: any){
      console.log('map data', eventData);
      this.mapData = eventData;
    }

}
