import { Component } from '@angular/core';
import { Address } from '../../../interfaces/address';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-address-form',
  standalone: false,
  templateUrl: './address-form.component.html',
  styleUrl: './address-form.component.scss'
})
export class AddressFormComponent {
  addressForm!: FormGroup;
  address!: Address;

  lookUp(entry: Address){
    console.log(entry);
    //code to call API service
  }

  cancel(){}
}
