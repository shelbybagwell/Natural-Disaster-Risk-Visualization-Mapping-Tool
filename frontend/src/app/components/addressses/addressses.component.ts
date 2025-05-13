import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { jwtDecode } from 'jwt-decode';

interface JwtPayload {
  sub: string; 
  [key: string]: any;
}

interface ApiResponse {
  status: string;
  data: any;
}

@Component({
  selector: 'app-addressses',
  standalone: false,
  templateUrl: './addressses.component.html',
  styleUrl: './addressses.component.scss'
})

export class AddresssesComponent {

  userAddressUrl: string = 'http://localhost:5000/addresses/';
  errorMessage: string = '';

  addresses: { id: string, title: string, address: string, latitude: number, longitude: number, link: string}[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadUserAddressList();
  }

  loadUserAddressList(){
    const token = localStorage.getItem('access_token');

    if (!token) {
      this.errorMessage = 'User not logged in';
      return;
    }

    try {
      const decoded: JwtPayload = jwtDecode(token);
      const userId = decoded.sub;

      this.http.get<ApiResponse>(`${this.userAddressUrl}list/user/${userId}`).subscribe({
        next: (response) => {
          
          this.addresses = [];

          console.log(response.data);

          if (response.data){
            for (const addr of response.data){

              this.addresses.push({
                id: addr._id,
                title: addr.address_name, 
                address: addr.street_address + " " + addr.city + " " + addr.zip + ", " + addr.state,
                latitude: addr.latitude, 
                longitude: addr.longitude,
                link: '/map' //TO DO: Adjust URL to use address params on search
              });
            }
          }
        },
        error: (err) => {
          this.errorMessage = 'Failed to load user data';
        }
      });
    } catch (err) {
      this.errorMessage = 'An unexpected error has occurred';
      console.error(err);
    }
  }

  deleteUserAddress(event: Event){
    
    const button = event.target as HTMLButtonElement;
    const addressId = button.getAttribute('data-id');

    console.log("Deleting address",  addressId);

    if (!addressId) {
      console.error('Address ID not found');
      return;
    }

    try {
      this.http.delete(`${this.userAddressUrl}${addressId}`).subscribe({
        next: () => {
          // Refresh list
          this.loadUserAddressList();
        },
        error: (err) => {
          this.errorMessage = 'Failed to delete address';
        }
      });
    } catch (err) {
      this.errorMessage = 'An unexpected error has occurred';
      console.error(err);
    }
  }
}
