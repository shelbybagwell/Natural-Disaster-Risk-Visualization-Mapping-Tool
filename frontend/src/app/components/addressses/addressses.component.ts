import { Component } from '@angular/core';

@Component({
  selector: 'app-addressses',
  standalone: false,
  templateUrl: './addressses.component.html',
  styleUrl: './addressses.component.scss'
})
export class AddresssesComponent {
/**
 * This component will be filled by the call, 
 * link should be generated to use params for street, city, state zip that can be passed into map page
 */
  addresses: { title: string, address: string, link: string}[] = [
    { 
      title: 'Home Address',
      address: '50 Main St, Salt Lake City, UT, 84103',
      link: '/map' 
    },
    {
      title: 'Work Address',
      address: '50 Main St, Salt Lake City, UT, 84103',
      link: '/map'
    }
  ];

}
