import { Component, inject } from '@angular/core';
import { Address } from '../../../interfaces/address';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-address-form',
  standalone: false,
  templateUrl: './address-form.component.html',
  styleUrl: './address-form.component.scss'
})
export class AddressFormComponent {
  addressForm!: FormGroup;
  fb = inject(FormBuilder);

  constructor() {
    this.addressForm = this.fb.group({
      streetAddress: ['', [Validators.required]],
      city: ['', []],
      state: ['', []],
      zip: ['', [Validators.required]]
    });
  }

  lookUp(entry: FormGroup){
    console.log(entry);
    alert("This will get coordinates and pass them to the map");
    //code to call API service
  }

  save(entry: Address){}

  cancel(){
    this.addressForm.reset();
  }
}
