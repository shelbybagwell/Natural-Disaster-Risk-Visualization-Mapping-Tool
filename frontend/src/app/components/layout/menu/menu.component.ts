import { Component, ViewChild, inject } from '@angular/core';
import {MatMenuModule, MatMenuTrigger} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: false,
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss'
})
export class MenuComponent {
  @ViewChild(MatMenuTrigger) trigger!: MatMenuTrigger;

  router = inject(Router)

  openMenu() {
    this.trigger.openMenu();
  }

  viewMap(){
    this.router.navigateByUrl("/map");
  }

  viewSavedAddresses(){
    this.router.navigateByUrl("addresses")
  }

  logout(){

    //Clear access token
    localStorage.setItem('access_token', "");
    
    this.router.navigateByUrl('/')
  }
}
