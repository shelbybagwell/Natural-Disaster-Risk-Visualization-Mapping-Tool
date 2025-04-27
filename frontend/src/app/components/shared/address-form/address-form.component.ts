import { Component, inject, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Address } from '../../../interfaces/address';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { add, format } from 'ol/coordinate';
// import { ApiService } from '../../../services/api.service';

const GEO_URL = 'https://nominatim.openstreetmap.org/search';
const POLYGON_URL = 'http://localhost:5001/addresses/search';

@Component({
  selector: 'app-address-form',
  standalone: false,
  templateUrl: './address-form.component.html',
  styleUrl: './address-form.component.scss'
})
export class AddressFormComponent {
  addressForm!: FormGroup;
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  @Output() addressSelected = new EventEmitter<any>();

  constructor() {
    this.addressForm = this.fb.group({
      streetAddress: ['', [Validators.required]],
      addressLine2: ['', []],
      city: ['', [Validators.required]],
      state: ['', [Validators.required]],
      zip: ['', [Validators.required]]
    });
  }

  lookUp(entry: FormGroup){
    let geoCodeData: any;
    let polygonData;
    if (this.addressForm.invalid) {
      alert("Please fill in all required fields.");
      return;
    } else{
      let address = this.buildAddress(entry);
      // creating the big promise for both geocode and polygon data
      Promise.all([
        this.getGeocode(address),
        // ADD PYHON CALL HERE FOR POLYGON DATA
        this.getPolygon(address)
      ]).then(([rtnGeoData ]) => {
        geoCodeData = rtnGeoData;
      }).then(() => {
        this.addressSelected.emit({
          currentLocation: geoCodeData,
          fireData: null
        })
      }).catch((error) => {
        console.error('Error fetching data:', error);
      });
    }
  }

  // builds address object for callouts
  buildAddress(formGroup: FormGroup){
    const address = {
      street_address: formGroup.get('streetAddress')?.value,
      address_line2: formGroup.get('addressLine2')?.value,
      city: formGroup.get('city')?.value,
      state: formGroup.get('state')?.value,
      zip: formGroup.get('zip')?.value
    };
    return address
  }

  // gets geocode 
  async getGeocode(address: any){
    let params = new HttpParams({fromObject: {
        ...address,
        format: 'json',
        limit: '1'
    }});

    return new Promise((resolve, reject) => {
      this.http.get<any[]>(GEO_URL, { params }).subscribe({
        next: (data) => {
          if (data.length > 0) {
            resolve([data[0].lon, data[0].lat]);
          } else {
            reject('No results found');
          }
        },
        error: (error) => reject(error)
      });
    });
  }

  //add the python call to return polygon data and modal info
  async getPolygon(address: any) {
    console.log(address);

    return new Promise((resolve, reject) => {
      this.http.post<any[]>(POLYGON_URL, address).subscribe({
        next: (data) => {
          if (data.length > 0) {
            console.log("Got fire data yay");
          } else {
            reject('No results found');
          }
        },
        error: (error) => reject(error)
      });
    });
  }

  save(entry: Address){}

  cancel(){
    this.addressForm.reset();
  }
}
